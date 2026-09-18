#!/usr/bin/env python3
"""Genere le tableau de bord de suivi de la collecte call center (MDS JOB 002/26).

S'il n'y a encore aucune soumission sur le projet, le tableau de bord est rempli
avec un jeu de DEMONSTRATION genere localement et signale comme tel en clair.

Le bareme n'est pas redefini ici : il est lu dans form_structure.json (cle
`notation`), ecrite par build_form.py. Le score affiche est donc calcule avec la
meme table que celle des expressions XPath du formulaire.

Usage :
    python build_dashboard.py [--uid <uid Kobo>] [--demo]
"""
import argparse
import html
import json
import random
import zlib

from collections import Counter
from datetime import date, datetime, timedelta
from pathlib import Path

import theme
import traductions

BASE = Path(__file__).resolve().parent
SORTIE = BASE / "suivi_collecte.html"
UID_DEFAUT = "aMrWStmZLSCTA4yuaBZhxF"

STRUCTURE = json.loads((BASE / "form_structure.json").read_text(encoding="utf-8"))
LIBELLES = {l["name"]: l["label"] for l in STRUCTURE["survey"]}
NOTATION = STRUCTURE["notation"]
# {question : bareme}, dans l'ordre du questionnaire.
BAREME_DE = {n: t for s in NOTATION.values() for n, t in s["questions"]}
SECTION_DE = {n: cle for cle, s in NOTATION.items() for n, _ in s["questions"]}
TITRE_SECTION = {cle: s["titre"] for cle, s in NOTATION.items()}

# Le questionnaire de septembre 2026 ne liste plus que deux operateurs :
# Camtel, present dans la version precedente, en a disparu.
RESEAUX = ["Orange", "MTN"]
# Kobo exporte le code (orange, mtn) ou le libelle selon le mode d'export ;
# les majuscules sont celles ecrites par le formulaire.
OPERATEURS = {"orange": "Orange", "mtn": "MTN"}
OPERATEURS.update({l: l for l in RESEAUX})
OPERATEURS.update({l.upper(): l for l in RESEAUX})
COULEUR_OP = {"Orange": "var(--op-orange)", "MTN": "var(--op-mtn)"}

TRANCHES = {"1": "07h - 12h", "2": "12h - 18h", "3": "18h - 22h"}

# L'echelle des 22 criteres. Elle est ordinale ET porteuse d'un jugement de
# conformite : la rampe vert / ambre / rouge la dit, le N/A reste neutre parce
# qu'il ne vaut pas zero -- il sort du calcul.
NOTES = ["100", "50", "0", "na"]
LIBELLE_NOTE = {"100": "100 — totalement conforme",
                "50": "50 — partiellement conforme",
                "0": "0 — non conforme",
                "na": "N/A — non applicable"}
COULEUR_NOTE = {"100": "var(--st-good)", "50": "var(--st-warn)",
                "0": "var(--st-crit)", "na": "var(--muted)"}

# Les 25 scenarios, relus dans form_structure.json plutot que recopies : le
# libelle du questionnaire porte « code · famille · scenario », les trois
# colonnes de l'annexe MDS.
SCENARIOS = {}
for _c in STRUCTURE["choices"]:
    if _c["list_name"] == "scenario":
        _p = [x.strip() for x in _c["label"].split("·")]
        SCENARIOS[_c["name"]] = (_p[1], _p[2]) if len(_p) == 3 else ("", _p[-1])


def couleur_score(v):
    """Meme seuils que la pastille des dernieres soumissions."""
    if v is None:
        return "var(--muted)"
    return ("var(--st-good)" if v >= 80 else
            "var(--st-warn)" if v >= 60 else "var(--st-crit)")


# Les cas d'alerte critique, hors score : les cinq cas nommes du questionnaire
# et les six propres a la section A (accessibilite & serveur vocal, cochables
# sur ses seuls criteres). Libelles courts : ceux du questionnaire font trois
# lignes, illisibles en etiquette de graphique.
ALERTES = {"confidentialite": "Confidentialité",
           "info_erronee": "Information erronée",
           "irrespect": "Propos irrespectueux",
           "promesse": "Promesse non maîtrisée",
           "abandon": "Abandon non justifié",
           "accueil_incoherent": "Accueil incohérent",
           "menus_errones": "Menus erronés",
           "langue_indisponible": "Choix de langue",
           "boucle_ivr": "Boucle IVR",
           "coupure_redirection": "Coupure avant mise en relation",
           "attente_non_signalee": "Attente non signalée"}


# =====================================================================
# ACCES AUX DONNEES
# =====================================================================
# build_form.py renomme les questions a l'export : le tableau de bord interroge
# les champs sous leur nom interne et retrouve seul le nom porte par la base.
NOMS_BD = STRUCTURE.get("noms_bd", {})


def valeur(soumission, nom):
    """Kobo prefixe les champs du nom de leur groupe : on cherche le suffixe."""
    for candidat in (nom, NOMS_BD.get(nom)):
        if candidat is None:
            continue
        if candidat in soumission:
            return soumission[candidat]
        for cle, val in soumission.items():
            if cle.rsplit("/", 1)[-1] == candidat:
                return val
    return None


def charger_reelles(uid):
    import kobo
    k = kobo.Kobo(*kobo.charger_env())
    return k.donnees(uid)


def points(soumission, question):
    """(points obtenus, points en jeu) pour une question, ou None si hors score.

    Reproduit exactement la regle du formulaire : une question sans reponse
    (masquee par un `relevant`) ou repondue par une modalite non notee sort du
    numerateur comme du denominateur.
    """
    v = valeur(soumission, question)
    if v in (None, ""):
        return None
    p = (BAREME_DE.get(question) or {}).get(str(v))
    if p is None:
        return None
    return float(p), 100.0


def score(soumission, questions):
    num = den = 0.0
    for q in questions:
        r = points(soumission, q)
        if r:
            num += r[0]
            den += r[1]
    return (100 * num / den) if den else None


TOUTES_NOTEES = [n for s in NOTATION.values() for n, _ in s["questions"]]

# Une alerte critique se coche desormais sur le critere note 0 qui la revele ;
# `alertes`, la question de la page dediee, ne porte plus que les cas etrangers
# a un 0. Le tableau de bord lit les deux et n'en fait qu'un pour l'appel.
CHAMPS_ALERTE = ["alertes"] + [f"{n}_alerte" for n in TOUTES_NOTEES]

# Tous les champs d'alerte ne proposent pas la meme liste de cas : la section A
# a la sienne. La correspondance est relue dans le formulaire plutot que
# supposee ici -- le jeu de demonstration n'invente donc pas une alerte de
# serveur vocal sur un critere de conseiller, ni l'inverse.
LISTE_DE_CHAMP = {r["name"]: r["type"].split()[1] for r in STRUCTURE["survey"]
                  if r["type"].startswith("select_multiple")
                  and r["name"] in set(CHAMPS_ALERTE)}
CAS_DE_LISTE = {}
for _c in STRUCTURE["choices"]:
    if _c["list_name"] in set(LISTE_DE_CHAMP.values()) and _c["name"] in ALERTES:
        CAS_DE_LISTE.setdefault(_c["list_name"], []).append(_c["name"])


def cas_possibles(champ):
    """Les cas d'alerte que ce champ propose reellement, « aucune » exclue."""
    return CAS_DE_LISTE.get(LISTE_DE_CHAMP.get(champ, ""), [])


def alertes_de(soumission):
    """Les cas d'alerte critique de cet appel, d'ou qu'ils aient ete coches.

    Dedoublonne : le meme cas signale sur deux criteres reste une alerte pour
    l'appel. « Aucune alerte critique » n'en est pas une, elle est ecartee comme
    tout code inconnu.
    """
    codes = set()
    for champ in CHAMPS_ALERTE:
        codes |= {c for c in str(valeur(soumission, champ) or "").split()
                  if c in ALERTES}
    return codes


def generer_demo(n=124):
    """Jeu de demonstration : sert uniquement a montrer le tableau de bord vide."""
    rng = random.Random(2026)
    enqueteurs = ["A. Mbarga", "S. Fotso", "J. Ndam", "C. Ekani", "L. Tchoumi",
                  "R. Njoya"]
    # Qualite moyenne propre a chaque operateur.
    base = {"orange": 0.76, "mtn": 0.68}
    debut = date(2026, 9, 15)

    lignes = []
    for i in range(n):
        op = rng.choices(["orange", "mtn"], weights=[52, 48])[0]
        jour = debut + timedelta(days=min(int(rng.triangular(0, 15, 9)), 15))
        p = base[op]
        heure = rng.randint(8, 21)
        attente = max(1, int(rng.lognormvariate(3.0, 0.9)))
        secondes = max(45, int(rng.gauss(430, 190)))
        s = {
            "_id": 800000 + i,
            "_submission_time": f"{jour}T{rng.randint(8, 21):02d}:"
                                f"{rng.randint(0, 59):02d}:00",
            "date_evaluation": str(jour),
            "type_interview": "live",
            "reseau": op,
            "nom_enqueteur": rng.choice(enqueteurs),
            "identification_conseiller": f"Conseiller {rng.randint(1, 40)}",
            "scenario_joue": "S%02d" % rng.randint(1, 25),
            # La tranche n'est plus tiree au sort : elle se deduit de l'heure de
            # debut, comme le fait le `calculation` du formulaire.
            "heure_debut": f"{heure:02d}:{rng.randint(0, 59):02d}:00",
            "tranche_horaire": "1" if heure < 12 else "2" if heure < 18 else "3",
            "langue_enqueteur": rng.choices(["fr", "en"], weights=[8, 2])[0],
            "attente_conseiller": attente,
            "duree_appel": secondes,
            "temps_total": round(secondes / 60),
            "nb_transferts": rng.choices([0, 1, 2], weights=[70, 24, 6])[0],
        }
        s["nb_attentes"] = rng.choices([0, 1, 2, 3], weights=[46, 34, 14, 6])[0]
        if s["nb_attentes"]:
            s["duree_attentes"] = max(5, int(rng.lognormvariate(3.4, 0.8)))
        # Escalade et renvoi : deux appels sur dix environ.
        s["escalade"] = "1" if rng.random() < 0.22 else "2"
        s["renvoi_canal"] = "1" if rng.random() < 0.16 else "2"

        # Criteres masques par leur `relevant` : ils sont simplement absents,
        # comme le serait la reponse dans un export Kobo.
        masques = set()
        if s["escalade"] != "1" and s["renvoi_canal"] != "1":
            masques.add("Q15")
        if not (s["nb_attentes"] or s["nb_transferts"]
                or s["renvoi_canal"] == "1"):
            masques.add("Q18")

        for q in TOUTES_NOTEES:
            if q in masques:
                continue
            # Difficulte propre au critere, stable d'un appel a l'autre.
            biais = 0.72 + 0.55 * ((zlib.crc32(q.encode()) % 100) / 100.0)
            tirage = rng.random()
            seuil = min(0.96, p * biais + 0.08)
            if tirage < 0.04:                        # non observe
                s[q] = "na"
            elif tirage < seuil:
                s[q] = "100"
            elif tirage < seuil + (1 - seuil) * 0.62:
                s[q] = "50"
            else:
                s[q] = "0"
        # Le client doit rappeler d'autant plus souvent que l'appel a mal tourne.
        moyen = score(s, TOUTES_NOTEES) or 0
        s["Q25"] = "1" if rng.random() < max(0.03, 0.85 - moyen / 100) else "2"
        # Alertes critiques : rares, et cochees la ou elles se revelent -- sur
        # le critere note 0. Tout 0 n'est pas une alerte, loin de la. Le
        # reliquat de la page dediee (un cas observe hors d'un critere note 0)
        # est plus rare encore, mais pas impossible sur un appel bien note :
        # c'est tout l'interet de suivre les alertes a part.
        for q in TOUTES_NOTEES:
            if s.get(q) != "0":
                continue
            vues = [c for c in cas_possibles(f"{q}_alerte")
                    if rng.random() < 0.03]
            s[f"{q}_alerte"] = " ".join(vues) if vues else "aucune"
        autres = [c for c in cas_possibles("alertes")
                  if rng.random() < 0.002 + 0.006 * (1 - moyen / 100)]
        s["alertes"] = " ".join(autres) if autres else "aucune"
        lignes.append(s)
    return lignes


# =====================================================================
# AGREGATS
# =====================================================================
def moyenne(valeurs):
    valeurs = [v for v in valeurs if v is not None]
    return sum(valeurs) / len(valeurs) if valeurs else 0


def nombre(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def agreger(lignes):
    a = {"total": len(lignes)}
    a["enqueteurs"] = len({valeur(s, "nom_enqueteur") for s in lignes
                           if valeur(s, "nom_enqueteur")})
    a["conseillers"] = len({valeur(s, "identification_conseiller") for s in lignes
                            if valeur(s, "identification_conseiller")})

    # -- volume par jour
    par_jour = Counter()
    for s in lignes:
        d = valeur(s, "date_evaluation") or (s.get("_submission_time") or "")[:10]
        if d:
            par_jour[str(d)[:10]] += 1
    if par_jour:
        d0, d1 = min(par_jour), max(par_jour)
        jours, cur = [], datetime.strptime(d0, "%Y-%m-%d").date()
        fin = datetime.strptime(d1, "%Y-%m-%d").date()
        while cur <= fin:
            jours.append((str(cur), par_jour.get(str(cur), 0)))
            cur += timedelta(days=1)
        a["par_jour"] = jours
    else:
        a["par_jour"] = []

    a["par_operateur"] = Counter(OPERATEURS.get(valeur(s, "reseau"), "Non renseigné")
                                 for s in lignes)
    a["par_tranche"] = Counter(TRANCHES.get(str(valeur(s, "tranche_horaire")),
                                            "Non renseignée") for s in lignes)
    a["par_enqueteur"] = Counter(valeur(s, "nom_enqueteur") or "Non renseigné"
                                 for s in lignes)

    # -- scores : global, par section, par section x operateur
    a["score_global"] = moyenne([score(s, TOUTES_NOTEES) for s in lignes])
    a["score_section"] = {
        cle: moyenne([score(s, [n for n, _ in NOTATION[cle]["questions"]])
                      for s in lignes])
        for cle in NOTATION}
    a["score_section_op"] = {
        TITRE_SECTION[cle]: {
            op: (moyenne(v) if v else None)
            for op in RESEAUX
            for v in [[score(s, [n for n, _ in NOTATION[cle]["questions"]])
                       for s in lignes
                       if OPERATEURS.get(valeur(s, "reseau")) == op]]}
        for cle in NOTATION}
    a["score_operateur"] = {
        op: moyenne([score(s, TOUTES_NOTEES) for s in lignes
                     if OPERATEURS.get(valeur(s, "reseau")) == op])
        for op in RESEAUX}

    # -- reussite par question : moyenne des points obtenus, sur 100
    par_q = {}
    for q in TOUTES_NOTEES:
        obtenus = [points(s, q) for s in lignes]
        obtenus = [o for o in obtenus if o]
        if obtenus:
            par_q[q] = (100 * sum(o[0] for o in obtenus) / sum(o[1] for o in obtenus),
                        len(obtenus))
    a["par_question"] = sorted(((q, v, n) for q, (v, n) in par_q.items()),
                               key=lambda x: x[1])

    # -- repartition des notes, par section et toutes sections confondues
    a["notes"] = {}
    for cle in NOTATION:
        c = Counter()
        for s in lignes:
            for q, _ in NOTATION[cle]["questions"]:
                v = valeur(s, q)
                if v not in (None, ""):
                    c[str(v)] += 1
        a["notes"][cle] = {k: c.get(k, 0) for k in NOTES}
    a["notes_total"] = {k: sum(a["notes"][cle][k] for cle in NOTATION)
                        for k in NOTES}
    a["n_zeros"] = a["notes_total"]["0"]

    # -- durees et taux cles
    a["attente_moy"] = moyenne([nombre(valeur(s, "attente_conseiller"))
                                for s in lignes])
    a["attente_med"] = mediane([nombre(valeur(s, "attente_conseiller"))
                                for s in lignes])
    # La duree cumulee des mises en attente n'est saisie que s'il y en a eu :
    # la moyenne porte sur les seuls appels concernes, pas sur les zeros absents.
    a["hold_moy"] = moyenne([nombre(valeur(s, "duree_attentes"))
                             for s in lignes if valeur(s, "duree_attentes")])
    a["duree_moy"] = moyenne([nombre(valeur(s, "temps_total")) for s in lignes])
    a["transferts_moy"] = moyenne([nombre(valeur(s, "nb_transferts"))
                                   for s in lignes])

    # Q13 : resolution des le premier contact, ou meilleure solution accessible
    # effectivement mise en oeuvre. Seul un 100 compte comme FCR.
    reponses_q13 = [str(valeur(s, "Q13")) for s in lignes
                    if valeur(s, "Q13") not in (None, "", "na")]
    a["resolution_1er"] = (100 * reponses_q13.count("100") / len(reponses_q13)
                           if reponses_q13 else 0)
    a["n_escalade"] = sum(1 for s in lignes if str(valeur(s, "escalade")) == "1")
    a["n_renvoi"] = sum(1 for s in lignes
                        if str(valeur(s, "renvoi_canal")) == "1")
    a["n_rappel"] = sum(1 for s in lignes if str(valeur(s, "Q25")) == "1")

    # -- alertes critiques. Kobo exporte un select_multiple comme une liste de
    # codes separes par des espaces ; « aucune » n'est pas une alerte. Les 22
    # criteres notes et la page dediee sont relus ensemble par alertes_de().
    a["alertes"] = Counter()
    a["n_appels_alerte"] = 0
    for s in lignes:
        codes = alertes_de(s)
        if codes:
            a["n_appels_alerte"] += 1
        for c in codes:
            a["alertes"][c] += 1
    a["n_alertes"] = sum(a["alertes"].values())

    # -- score par scenario. Un scenario sans appel n'apparait pas : une barre
    # a zero se lirait comme un mauvais score, pas comme une absence.
    a["par_scenario"] = {}
    for code in SCENARIOS:
        appels = [s for s in lignes if str(valeur(s, "scenario_joue")) == code]
        if not appels:
            continue
        par_op = {}
        for op in RESEAUX:
            v = [score(s, TOUTES_NOTEES) for s in appels
                 if OPERATEURS.get(valeur(s, "reseau")) == op]
            v = [x for x in v if x is not None]
            par_op[op] = (sum(v) / len(v)) if v else None
        a["par_scenario"][code] = {
            "n": len(appels),
            "score": moyenne([score(s, TOUTES_NOTEES) for s in appels]),
            "ops": par_op}

    a["recentes"] = sorted(lignes, key=lambda s: s.get("_submission_time") or "",
                           reverse=True)[:12]
    a["score_de"] = {s.get("_id"): score(s, TOUTES_NOTEES) for s in lignes}
    return a


def mediane(valeurs):
    v = sorted(x for x in valeurs if x is not None)
    if not v:
        return 0
    m = len(v) // 2
    return v[m] if len(v) % 2 else (v[m - 1] + v[m]) / 2


# =====================================================================
# SVG — primitives reprises telles quelles du JOB 001/26
# =====================================================================
def ech(t):
    return html.escape(str(t), quote=True)


# --- bilingue : chaque texte porte sa version anglaise en data-en, le bouton
# de la barre d'outils bascule toute la page sans rechargement. Meme mecanique
# que guide_enqueteur.html, meme source (traductions.py).
def T(fr):
    """Version anglaise d'un libelle ; le francais a defaut de traduction."""
    return traductions.en(str(fr))


# Textes ecrits en dur dans ce fichier et destines a basculer. On les enregistre
# pour verifier a chaque generation qu'ils ont tous une traduction : le
# dictionnaire etant indexe sur le francais, une virgule deplacee ici ferait
# retomber en() sur le francais sans le moindre bruit.
TEXTES_VUS = set()


def att(fr, en=None, cle="data-en", controle=True):
    """Attribut data-en, vide quand les deux langues coincident.

    `controle=False` pour les valeurs issues des donnees (noms d'enqueteurs,
    marques, codes de question) : elles n'ont pas a etre traduites.
    """
    if controle:
        TEXTES_VUS.add(str(fr))
    en = T(fr) if en is None else en
    return "" if str(en) == str(fr) else f' {cle}="{html.escape(str(en), quote=True)}"'


def sp(fr, balise="span"):
    """Fragment bilingue : le francais visible, l'anglais en data-en.

    `balise` peut porter ses attributs ('th class="num"') : la balise fermante
    ne reprend que le nom.
    """
    return f"<{balise}{att(fr)}>{ech(fr)}</{balise.split()[0]}>"


def bi_html(fr, en):
    """Meme chose pour deux fragments HTML deja construits."""
    return "" if fr == en else f' data-en="{html.escape(en, quote=True)}"'


def tip(fr, en):
    """Infobulle bilingue : data-tip porte le francais, data-tip-en l'anglais."""
    return (f'data-tip="{html.escape(fr, quote=True)}"'
            + ("" if fr == en
               else f' data-tip-en="{html.escape(en, quote=True)}"'))


def courbe(jours, w=740, h=210):
    """Aire + ligne : progression quotidienne de la collecte."""
    if not jours:
        return sp("Aucune visite enregistrée.", 'p class="vide"')
    gl, gr, gt, gb = 46, 18, 16, 34
    vmax = max(max(v for _, v in jours), 1)
    pas = max(1, -(-vmax // 4))
    haut = pas * 4
    n = len(jours)
    px = lambda i: gl + (i * (w - gl - gr) / max(n - 1, 1))
    py = lambda v: gt + (h - gt - gb) * (1 - v / haut)

    pts = [(px(i), py(v)) for i, (_, v) in enumerate(jours)]
    ligne = " ".join(f"{'M' if i == 0 else 'L'}{x:.1f},{y:.1f}"
                     for i, (x, y) in enumerate(pts))
    aire = ligne + f" L{pts[-1][0]:.1f},{py(0):.1f} L{pts[0][0]:.1f},{py(0):.1f} Z"

    o = [f'<svg viewBox="0 0 {w} {h}" class="chart" role="img" '
         f'aria-label="Visites collectées par jour">']
    for k in range(5):
        v = pas * k
        y = py(v)
        o.append(f'<line x1="{gl}" y1="{y:.1f}" x2="{w-gr}" y2="{y:.1f}" class="grid"/>')
        o.append(f'<text x="{gl-9}" y="{y+4:.1f}" class="ax ax-r">{v}</text>')
    o.append(f'<path d="{aire}" fill="var(--vol-fill)"/>')
    o.append(f'<path d="{ligne}" fill="none" stroke="var(--vol)" stroke-width="2" '
             f'stroke-linejoin="round" stroke-linecap="round"/>')

    etiquettes = {0, n - 1, n // 2} if n > 3 else set(range(n))
    for i, (j, v) in enumerate(jours):
        x, y = pts[i]
        dernier = i == n - 1
        o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{5 if dernier else 4}" '
                 f'fill="var(--vol)" stroke="var(--card)" stroke-width="2" '
                 f'class="pt" '
                 + tip(f'{fr_date(j)} — {v} appel{"s" if v > 1 else ""}',
                       f'{fr_date(j)} — {v} call{"s" if v > 1 else ""}') + '/>')
        if i in etiquettes:
            o.append(f'<text x="{x:.1f}" y="{h-12}" class="ax ax-c">{fr_jour(j)}</text>')
    xd, yd = pts[-1]
    o.append(f'<text x="{xd-6:.1f}" y="{yd-13:.1f}" class="val val-end">'
             f'{jours[-1][1]}</text>')
    o.append("</svg>")
    return "".join(o)


def barres_h(items, couleur="var(--vol)", w=740, hauteur_barre=30, unite="",
             largeur_lib=132, badges=None):
    """Barres horizontales : items = [(libelle, valeur), ...]."""
    if not items:
        return sp("Aucune donnée.", 'p class="vide"')
    gd = 62 if not badges else 108
    h = len(items) * hauteur_barre + 10
    vmax = max(v for _, v in items) or 1
    piste = w - largeur_lib - gd
    o = [f'<svg viewBox="0 0 {w} {h}" class="chart" role="img">']
    for i, (lib, v) in enumerate(items):
        y = i * hauteur_barre + 5
        bw = max(2, piste * v / vmax)
        c = couleur(lib, v) if callable(couleur) else couleur
        o.append(f'<text x="0" y="{y+hauteur_barre/2+4:.0f}" class="ax ax-l"'
                 f'{att(lib, controle=False)}>{ech(lib)}</text>')
        o.append(f'<rect x="{largeur_lib}" y="{y+5:.0f}" width="{bw:.1f}" '
                 f'height="{hauteur_barre-14}" rx="4" fill="{c}" class="bar" '
                 + tip(f"{lib} — {fmt(v)}{unite}",
                       f"{T(lib)} — {fmt(v)}{unite}") + '/>')
        o.append(f'<text x="{largeur_lib+bw+9:.1f}" y="{y+hauteur_barre/2+4:.0f}" '
                 f'class="val">{fmt(v)}{unite}</text>')
        if badges:
            lab, cls = badges(v)
            o.append(f'<text x="{w-4}" y="{y+hauteur_barre/2+4:.0f}" '
                     f'class="val badge {cls}" text-anchor="end"'
                     f'{att(lab)}>{ech(lab)}</text>')
    o.append("</svg>")
    return "".join(o)


def barres_groupees(sections, ops, couleurs, w=740, h=250):
    """Barres verticales groupees : conformite par section et par operateur."""
    gl, gr, gt, gb = 44, 12, 22, 46
    pl = w - gl - gr
    ph = h - gt - gb
    lg = pl / len(sections)
    bw = min(30, (lg - 22) / len(ops))
    o = [f'<svg viewBox="0 0 {w} {h}" class="chart" role="img" '
         f'aria-label="Taux de conformité par section et par opérateur">']
    for k in range(5):
        v = k * 25
        y = gt + ph * (1 - v / 100)
        o.append(f'<line x1="{gl}" y1="{y:.1f}" x2="{w-gr}" y2="{y:.1f}" class="grid"/>')
        o.append(f'<text x="{gl-9}" y="{y+4:.1f}" class="ax ax-r">{v}%</text>')
    for i, sec in enumerate(sections):
        cx = gl + lg * i + lg / 2
        for j, op in enumerate(ops):
            v = sections[sec].get(op)
            if v is None:
                continue
            x = cx - (len(ops) * bw + (len(ops) - 1) * 2) / 2 + j * (bw + 2)
            bh = max(2, ph * v / 100)
            o.append(f'<rect x="{x:.1f}" y="{gt+ph-bh:.1f}" width="{bw:.1f}" '
                     f'height="{bh:.1f}" rx="4" fill="{couleurs[op]}" class="bar" '
                     + tip(f"{sec} · {op} — {v:.0f} / 100",
                           f"{T(sec)} · {op} — {v:.0f} / 100") + '/>')
            o.append(f'<text x="{x+bw/2:.1f}" y="{gt+ph-bh-6:.1f}" class="val val-s" '
                     f'text-anchor="middle">{v:.0f}</text>')
        o.append(f'<text x="{cx:.1f}" y="{h-24}" class="ax ax-c"'
                 f'{att(sec)}>{ech(sec)}</text>')
    o.append(f'<line x1="{gl}" y1="{gt+ph}" x2="{w-gr}" y2="{gt+ph}" class="axis"/>')
    o.append("</svg>")
    return "".join(o)


def fmt(v):
    return f"{v:.0f}" if isinstance(v, float) and abs(v - round(v)) < 0.05 else (
        f"{v:.1f}" if isinstance(v, float) else str(v))


MOIS = ["janv.", "févr.", "mars", "avr.", "mai", "juin", "juil.", "août",
        "sept.", "oct.", "nov.", "déc."]


def fr_date(j):
    d = datetime.strptime(j, "%Y-%m-%d").date()
    return f"{d.day} {MOIS[d.month-1]}"


def fr_jour(j):
    d = datetime.strptime(j, "%Y-%m-%d").date()
    return f"{d.day}/{d.month:02d}"



CSS_DASH = """
.wrap { max-width:1240px; margin:0 auto; padding:22px 26px 70px;
        display:flex; flex-direction:column; gap:20px; }

/* --- barre d'outils : bascule de langue --- */
.barre { position:sticky; top:0; z-index:14; background:var(--card);
         border-bottom:1px solid var(--rule); padding:9px 26px; }
.barre-in { max-width:1240px; margin:0 auto; display:flex; align-items:center;
            justify-content:space-between; gap:16px; flex-wrap:wrap; }
.barre-note { font-size:12px; color:var(--muted); }
.btn { font-family:"IBM Plex Sans",sans-serif; font-size:12px; font-weight:600;
       padding:6px 13px; border-radius:3px; border:1px solid var(--rule);
       background:var(--card); color:var(--ink-2); cursor:pointer;
       white-space:nowrap; }
.btn:hover { border-color:var(--accent); color:var(--accent); }
.btn-lang { font-family:"IBM Plex Mono",monospace; letter-spacing:.06em; }
.btn-lang[aria-pressed="true"] { border-color:var(--mds-amber);
                                 color:var(--amber-ink);
                                 background:var(--amber-soft); }

.alerte { background:var(--amber-soft); border:1px solid var(--mds-amber);
          border-radius:4px; padding:14px 18px; display:flex; flex-wrap:wrap;
          align-items:baseline; gap:12px; }
.alerte-tag { font-family:"IBM Plex Mono",monospace; font-size:10px; font-weight:700;
              letter-spacing:.13em; text-transform:uppercase; color:#3B2703;
              background:var(--mds-amber); padding:4px 9px; border-radius:2px;
              white-space:nowrap; }
.alerte p { margin:0; font-size:13px; color:var(--ink-2); flex:1 1 340px; }
.alerte code { font-family:"IBM Plex Mono",monospace; font-size:12px;
               background:var(--card); padding:1px 5px; border-radius:2px; }

.kpis { display:grid; grid-template-columns:repeat(auto-fit,minmax(180px,1fr)); gap:1px;
        background:var(--rule); border:1px solid var(--rule); border-radius:4px;
        overflow:hidden; }
.kpi { background:var(--card); padding:15px 18px 16px; display:flex; flex-direction:column;
       gap:2px; border-top:3px solid transparent; }
.kpi:first-child { border-top-color:var(--mds-amber); }
.kpi-lab { font-size:11px; font-weight:600; letter-spacing:.09em; text-transform:uppercase;
           color:var(--muted); }
.kpi-val { font-family:Archivo,sans-serif; font-size:30px; font-weight:700;
           line-height:1.15; letter-spacing:-.02em; color:var(--accent); }
.kpi-sub { font-size:12px; color:var(--muted); }

.grille { display:grid; grid-template-columns:repeat(auto-fit,minmax(400px,1fr));
         gap:20px; align-items:start; }
@media (max-width:720px) { .grille { grid-template-columns:1fr; } }
.panneau { background:var(--card); border:1px solid var(--rule); border-radius:4px;
           padding:18px 20px 16px; display:flex; flex-direction:column; gap:12px; }
.panneau > header { display:flex; justify-content:space-between; align-items:baseline;
                    gap:12px; flex-wrap:wrap; }
.panneau h2 { font-family:Archivo,sans-serif; font-size:14px; font-weight:700;
              letter-spacing:.02em; margin:0; display:flex; align-items:center; gap:9px; }
.panneau h2::before { content:""; width:14px; height:3px; background:var(--mds-amber);
                      border-radius:2px; flex:none; }
.panneau .sous { font-size:12px; color:var(--muted); margin:0; }
.large { grid-column:1/-1; }
.chart-box { overflow-x:auto; }
.chart { width:100%; height:auto; display:block; min-width:340px; }

.grid { stroke:var(--grid); stroke-width:1; }
.axis { stroke:var(--axis); stroke-width:1; }
.ax { fill:var(--muted); font-size:11px; font-family:"IBM Plex Sans",sans-serif;
      font-variant-numeric:tabular-nums; }
.ax-r { text-anchor:end; } .ax-c { text-anchor:middle; } .ax-l { text-anchor:start; }
.val { fill:var(--ink-2); font-size:11.5px; font-weight:600;
       font-family:"IBM Plex Mono",monospace; font-variant-numeric:tabular-nums; }
.val-s { font-size:10px; fill:var(--muted); }
.val-end { fill:var(--vol); font-size:13px; text-anchor:end; }
.badge { font-size:9.5px; letter-spacing:.08em; text-transform:uppercase; }
.b-crit { fill:var(--st-crit); } .b-ser { fill:var(--st-ser); } .b-warn { fill:var(--muted); }
.bar, .pt { transition:opacity .12s; }
.bar:hover, .pt:hover { opacity:.78; cursor:default; }

.legende { display:flex; flex-wrap:wrap; gap:6px 16px; font-size:12px; color:var(--ink-2); }
.lg { display:inline-flex; align-items:center; gap:6px; }
.lg i { width:10px; height:10px; border-radius:2px; display:inline-block; flex:none; }

.pastille { width:8px; height:8px; border-radius:50%; display:inline-block;
            margin-right:7px; vertical-align:baseline; }
details { border-top:1px solid var(--rule-soft); padding-top:10px; }
summary { font-size:12px; color:var(--accent); cursor:pointer; font-weight:600; }
details[open] summary { margin-bottom:10px; }
.vide { color:var(--muted); font-size:13px; font-style:italic; margin:0; }

#tip { position:fixed; z-index:20; background:var(--band); color:var(--band-ink);
       font-size:12px; padding:6px 10px; border-radius:3px; pointer-events:none;
       opacity:0; transition:opacity .1s; white-space:nowrap;
       font-family:"IBM Plex Sans",sans-serif; box-shadow:0 4px 14px rgba(0,0,0,.24);
       border-left:2px solid var(--mds-amber); }
#tip.on { opacity:1; }
footer { font-size:12px; color:var(--muted); border-top:1px solid var(--rule);
         padding-top:14px; }
"""


def barre_empilee(compte, ordre, libelles, couleurs, w=740, h=54):
    """Repartition ordinale : `compte` = {code: effectif}, dans l'ordre donne."""
    total = sum(compte.values())
    if not total:
        return sp("Aucune réponse.", 'p class="vide"')
    o = [f'<svg viewBox="0 0 {w} {h}" class="chart" role="img" '
         f'aria-label="Répartition des appréciations">']
    x = 0.0
    for k in ordre:
        v = compte.get(k, 0)
        if not v:
            continue
        seg = (w - 8) * v / total
        pct = 100 * v / total
        o.append(f'<rect x="{x:.1f}" y="0" width="{max(seg-2,1):.1f}" height="26" '
                 f'rx="4" fill="{couleurs[k]}" class="bar" '
                 + tip(f"{libelles[k]} — {v} réponses ({pct:.0f} %)",
                       f"{T(libelles[k])} — {v} answers ({pct:.0f} %)") + '/>')
        # Etiquette posee sous la barre : lisible quelle que soit la marche.
        if seg > 42:
            o.append(f'<text x="{x+seg/2:.1f}" y="45" class="val val-s" '
                     f'text-anchor="middle">{pct:.0f} %</text>')
        x += seg
    o.append("</svg>")
    return "".join(o)


# =====================================================================
# PAGE
# =====================================================================
def rendre(a, demo, uid):
    coul = COULEUR_OP

    bandeau_demo = ""
    if demo:
        demo_fr = ('<p>Le projet ne compte encore <strong>aucune soumission '
                   'réelle</strong>. Les chiffres ci-dessous sont un jeu fictif '
                   'généré localement, destiné à montrer le rendu du tableau de '
                   'bord. Relancer <code>python build_dashboard.py</code> après '
                   'les premières collectes pour basculer sur les données '
                   'réelles.</p>')
        demo_en = ('<p>The project has <strong>no real submission</strong> yet. '
                   'The figures below are a fictional set generated locally, '
                   'meant to show how the dashboard looks. Run <code>python '
                   'build_dashboard.py</code> again after the first collections '
                   'to switch to the real data.</p>')
        bandeau_demo = (
            '<div class="alerte">'
            + sp("Données de démonstration", 'span class="alerte-tag"')
            + f'<div{bi_html(demo_fr, demo_en)}>{demo_fr}</div></div>')

    # Les sous-titres portent des nombres : leurs deux versions sont montees ici.
    def sous(fr, en):
        return f'<p class="sous"{bi_html(fr, en)}>{fr}</p>'

    kpis = [
        ("Appels collectés", fmt(a["total"]),
         f'{a["enqueteurs"]} enquêteurs · {a["conseillers"]} conseillers',
         f'{a["enqueteurs"]} auditors · {a["conseillers"]} advisers'),
        ("Score total moyen", f'{a["score_global"]:.0f} / 100',
         f'sur {len(TOUTES_NOTEES)} critères notés · {a["n_zeros"]} notes de 0',
         f'across {len(TOUTES_NOTEES)} scored criteria · {a["n_zeros"]} zero '
         f'marks'),
        ("Résolution / FCR", f'{a["resolution_1er"]:.0f} %',
         f'{a["n_escalade"]} escalades · {a["n_renvoi"]} renvois · '
         f'{a["n_rappel"]} rappels à prévoir',
         f'{a["n_escalade"]} escalations · {a["n_renvoi"]} referrals · '
         f'{a["n_rappel"]} call-backs expected'),
        ("Attente avant conseiller", f'{a["attente_moy"]:.0f} s',
         f'médiane {a["attente_med"]:.0f} s · mise en attente '
         f'{a["hold_moy"]:.0f} s',
         f'median {a["attente_med"]:.0f} s · on hold {a["hold_moy"]:.0f} s'),
        ("Durée moyenne d'appel", f'{a["duree_moy"]:.0f} min',
         f'{a["transferts_moy"]:.1f} transfert par appel',
         f'{a["transferts_moy"]:.1f} transfer per call'),
        ("Alertes critiques", fmt(a["n_appels_alerte"]),
         f'{a["n_alertes"]} cas signalés · hors score',
         f'{a["n_alertes"]} cases reported · outside the score'),
    ]
    def tuile(lab, v, sfr, sen):
        return ('<div class="kpi">'
                + sp(lab, 'span class="kpi-lab"')
                + f'<span class="kpi-val">{ech(v)}</span>'
                + f'<span class="kpi-sub"{bi_html(ech(sfr), ech(sen))}>'
                + f'{ech(sfr)}</span></div>')

    tuiles = "".join(tuile(*k) for k in kpis)

    # -- questions les plus defaillantes : points perdus sur 100
    def badge(reussite):
        perdu = 100 - reussite
        if perdu >= 40:
            return "Critique", "b-crit"
        if perdu >= 25:
            return "Sérieux", "b-ser"
        return "À surveiller", "b-warn"

    def coul_perte(_lib, perdu):
        return ("var(--st-crit)" if perdu >= 40 else
                "var(--st-ser)" if perdu >= 25 else "var(--st-warn)")

    top = a["par_question"][:8]
    graph_faibles = barres_h([(q, round(100 - v)) for q, v, _ in top],
                             couleur=coul_perte, unite=" %", largeur_lib=64,
                             badges=lambda perdu: badge(100 - perdu))
    lignes_faibles = "".join(
        f'<tr><td class="mono">{ech(q)}</td>'
        f'<td class="mono">{ech(SECTION_DE.get(q, ""))}</td>'
        f'<td{att(LIBELLES.get(q, ""), controle=False)}>'
        f'{ech(LIBELLES.get(q, ""))}</td>'
        f'<td class="num">{v:.0f} / 100</td><td class="num">{n}</td></tr>'
        for q, v, n in top)

    # -- volumes
    graph_op = barres_h([(o, a["par_operateur"].get(o, 0)) for o in RESEAUX],
                        couleur=lambda l, _v: coul.get(l, "var(--vol)"),
                        largeur_lib=112)
    graph_tranche = barres_h([(t, a["par_tranche"].get(t, 0))
                              for t in TRANCHES.values()], largeur_lib=112)
    enq_tri = sorted(a["par_enqueteur"].items(), key=lambda x: -x[1])[:8]
    graph_enq = barres_h(enq_tri, largeur_lib=112)

    # -- scores
    graph_scores = barres_groupees(a["score_section_op"], RESEAUX, coul)
    graph_score_op = barres_h(
        [(o, a["score_operateur"].get(o) or 0) for o in RESEAUX],
        couleur=lambda l, _v: coul.get(l, "var(--vol)"), unite=" / 100",
        largeur_lib=112)
    graph_notes = barre_empilee(a["notes_total"], NOTES, LIBELLE_NOTE,
                                COULEUR_NOTE)
    # Scenarios du moins bien traite au mieux traite : c'est la tete de liste
    # qui interesse. L'etiquette porte le code et l'intitule, la famille et le
    # detail par operateur sont dans le tableau depliant.
    sc_tri = sorted(a["par_scenario"].items(), key=lambda x: x[1]["score"])
    def etiq_sc(code):
        lib = f'{code} · {SCENARIOS[code][1]}'
        return lib if len(lib) <= 38 else lib[:37].rstrip() + '…'

    graph_scenarios = barres_h(
        [(etiq_sc(c), round(d["score"])) for c, d in sc_tri],
        couleur=lambda _l, v: couleur_score(v), unite=" / 100",
        hauteur_barre=26, largeur_lib=248)
    lignes_scenarios = "".join(
        f'<tr><td class="mono">{ech(c)}</td>'
        f'<td{att(SCENARIOS[c][0], controle=False)}>{ech(SCENARIOS[c][0])}</td>'
        f'<td{att(SCENARIOS[c][1], controle=False)}>{ech(SCENARIOS[c][1])}</td>'
        f'<td class="num">{d["n"]}</td>'
        f'<td class="num">{d["score"]:.0f}</td>'
        + "".join(f'<td class="num">'
                  f'{"—" if d["ops"][o] is None else format(d["ops"][o], ".0f")}'
                  f'</td>' for o in RESEAUX)
        + '</tr>' for c, d in sc_tri)

    # Une alerte critique n'a pas de degre : toutes les barres sont rouges,
    # seule leur longueur distingue les cas.
    graph_alertes = barres_h(
        sorted(((ALERTES[c], a["alertes"].get(c, 0)) for c in ALERTES),
               key=lambda x: -x[1]),
        couleur=lambda _l, _v: "var(--st-crit)", largeur_lib=150)

    lignes_sections = "".join(
        f'<tr><td class="mono">{ech(cle)}</td>'
        f'<td{att(TITRE_SECTION[cle])}>{ech(TITRE_SECTION[cle])}</td>'
        f'<td class="num">{a["score_section"][cle]:.0f} / 100</td>'
        f'<td class="num">{len(NOTATION[cle]["questions"])}</td></tr>'
        for cle in NOTATION)

    lignes_notes = "".join(
        f'<tr><td class="mono">{ech(cle)}</td>'
        f'<td{att(TITRE_SECTION[cle])}>{ech(TITRE_SECTION[cle])}</td>'
        + "".join(f'<td class="num">{a["notes"][cle][k]}</td>' for k in NOTES)
        + "</tr>" for cle in NOTATION)

    legende_op = "".join(
        f'<span class="lg"><i style="background:{coul[o]}"></i>{ech(o)}</span>'
        for o in RESEAUX)
    legende_notes = "".join(
        f'<span class="lg"><i style="background:{COULEUR_NOTE[k]}"></i>'
        f'{sp(LIBELLE_NOTE[k])}</span>' for k in NOTES)

    def pastille_score(v):
        if v is None:
            return "—"
        c = ("var(--st-good)" if v >= 80 else "var(--st-warn)" if v >= 60
             else "var(--st-crit)")
        return f'<span class="pastille" style="background:{c}"></span>{v:.0f}'

    rec = "".join(
        f'<tr><td class="mono">{ech((s.get("_submission_time") or "")[:10])}</td>'
        f'<td>{ech(valeur(s, "nom_enqueteur") or "—")}</td>'
        f'<td><span class="pastille" style="background:'
        f'{coul.get(OPERATEURS.get(valeur(s, "reseau")), "var(--muted)")}"></span>'
        f'{ech(OPERATEURS.get(valeur(s, "reseau"), "—"))}</td>'
        f'<td class="mono">{ech(valeur(s, "scenario_joue") or "—")}</td>'
        f'<td class="num">{ech(valeur(s, "attente_conseiller") or "—")}</td>'
        f'<td class="num">{ech(valeur(s, "temps_total") or "—")}</td>'
        f'<td class="num">{pastille_score(a["score_de"].get(s.get("_id")))}</td></tr>'
        for s in a["recentes"])

    maj = datetime.now().strftime("%d/%m/%Y à %H:%M")
    periode = (f'{fr_date(a["par_jour"][0][0])} – {fr_date(a["par_jour"][-1][0])}'
               if a["par_jour"] else "—")

    entete = ("<title>Suivi Ghost Check Call Center</title>" + theme.POLICES
              + "<style>" + theme.TOKENS + theme.BASE_CSS + CSS_DASH + "</style>"
              + theme.bandeau(
                  sp("Suivi de la collecte"),
                  sp("Audit des call center Orange · MTN — Cameroun"),
                  [(sp("Période"), periode),
                   (sp("Projet Kobo"), uid or sp("non déployé")),
                   (sp("Mise à jour"), maj)])
              + BARRE_OUTILS)

    return entete + TEMPLATE.format(
        bandeau_demo=bandeau_demo, tuiles=tuiles, courbe=courbe(a["par_jour"]),
        graph_op=graph_op, graph_tranche=graph_tranche, graph_enq=graph_enq,
        graph_scores=graph_scores, graph_score_op=graph_score_op,
        graph_notes=graph_notes, graph_alertes=graph_alertes,
        graph_scenarios=graph_scenarios, lignes_scenarios=lignes_scenarios,
        graph_faibles=graph_faibles,
        lignes_faibles=lignes_faibles, lignes_sections=lignes_sections,
        lignes_notes=lignes_notes, legende_op=legende_op,
        legende_notes=legende_notes, recentes=rec,
        t_progression=sp("Progression quotidienne", "h2"),
        s_progression=sous(
            f'Appels enregistrés par date d\'évaluation · {a["total"]} au total '
            f'sur {len(a["par_jour"])} jours',
            f'Calls recorded by assessment date · {a["total"]} in total over '
            f'{len(a["par_jour"])} days'),
        t_scores=sp("Score par section et par opérateur", "h2"),
        s_scores=sp("Moyenne des points obtenus sur les points en jeu, en %. "
                    "Un critère noté N/A, ou masqué parce que la situation ne "
                    "s'est pas produite, sort du calcul au lieu de compter "
                    "zéro.", 'p class="sous"'),
        d_sections=sp("Afficher le score moyen de chaque section", "summary"),
        t_faibles=sp("Critères les plus défaillants", "h2"),
        s_faibles=sous(
            f'Part des points perdus sur chaque critère, 8 premiers sur '
            f'{len(TOUTES_NOTEES)} notés',
            f'Share of points lost on each criterion, first 8 out of '
            f'{len(TOUTES_NOTEES)} scored'),
        d_chiffre=sp("Afficher le détail chiffré", "summary"),
        t_op=sp("Appels par opérateur", "h2"),
        t_score_op=sp("Score total par opérateur", "h2"),
        s_score_op=sp("Toutes sections confondues", 'p class="sous"'),
        t_scenarios=sp("Score par scénario", "h2"),
        s_scenarios=sous(
            f'{len(a["par_scenario"])} scénario(s) joué(s) sur les '
            f'{len(SCENARIOS)} de l\'annexe, du moins bien traité au mieux '
            f'traité',
            f'{len(a["par_scenario"])} scenario(s) played out of the '
            f'{len(SCENARIOS)} in the annex, from the worst handled to the '
            f'best'),
        d_scenarios=sp("Afficher le détail par scénario", "summary"),
        th_famille=sp("Famille", "th"),
        t_alertes=sp("Alertes critiques", "h2"),
        s_alertes=sous(
            f'{a["n_appels_alerte"]} appel(s) sur {a["total"]} portent au moins '
            f'une alerte · elles n\'entrent pas dans le score',
            f'{a["n_appels_alerte"]} call(s) out of {a["total"]} carry at least '
            f'one alert · they do not enter the score'),
        t_notes=sp("Répartition des notes", "h2"),
        s_notes=sp("Toutes réponses des 22 critères scorés, N/A compris",
                   'p class="sous"'),
        d_notes=sp("Afficher le détail par section", "summary"),
        t_tranche=sp("Appels par tranche horaire", "h2"),
        t_enq=sp("Appels par enquêteur", "h2"),
        t_recentes=sp("Dernières soumissions", "h2"),
        th_section=sp("Section", "th"), th_intitule=sp("Intitulé", "th"),
        th_score_moyen=sp("Score moyen", 'th class="num"'),
        th_notees=sp("Critères notés", 'th class="num"'),
        th_code=sp("Code", "th"), th_question=sp("Critère", "th"),
        th_appels=sp("Appels", 'th class="num"'),
        th_date=sp("Date", "th"), th_enq=sp("Enquêteur", "th"),
        th_reseau=sp("Opérateur", "th"), th_scenario=sp("Scénario", "th"),
        th_attente=sp("Attente (s)", 'th class="num"'),
        th_duree=sp("Durée (min)", 'th class="num"'),
        th_score=sp("Score", 'th class="num"'),
        pied=PIED, i18n=I18N_JSON)


# Barre d'outils : le bouton de bascule FR / EN, colle sous le bandeau.
BARRE_OUTILS = (
    '<div class="barre"><div class="barre-in">'
    + sp("Tableau de bord bilingue — le choix de langue est conservé dans ce "
         "navigateur.", 'span class="barre-note"')
    + '<button type="button" class="btn btn-lang" id="langue" '
      'aria-pressed="false">English</button>'
    + '</div></div>')

PIED_FR = ("Tableau de bord régénéré par <code>build_dashboard.py</code> depuis "
           "l'API KoboToolbox. Le barème est lu dans "
           "<code>form_structure.json</code> : c'est celui qu'appliquent les "
           "calculs du formulaire, il n'est pas redéfini ici. Les données "
           "factuelles — attente, durée, mises en attente, transferts, renvoi "
           "— ne sont pas notées : elles sont décrites à part, comme les "
           "alertes critiques. Les scénarios restent à fournir par MDS.")
PIED_EN = ("Dashboard regenerated by <code>build_dashboard.py</code> from the "
           "KoboToolbox API. The scale is read from "
           "<code>form_structure.json</code>: it is the one applied by the "
           "form's own calculations, it is not redefined here. The factual "
           "data — waiting time, length, holds, transfers, referral — are not "
           "scored: they are described separately, as are the critical alerts. "
           "The scenarios are still to be supplied by MDS.")
PIED = f'<footer{bi_html(PIED_FR, PIED_EN)}>{PIED_FR}</footer>'


TEMPLATE = """
<div class="wrap">
  {bandeau_demo}

  <div class="kpis">{tuiles}</div>

  <section class="panneau large">
    <header>{t_progression}{s_progression}</header>
    <div class="chart-box">{courbe}</div>
  </section>

  <section class="panneau large">
    <header>{t_scores}{s_scores}</header>
    <div class="legende">{legende_op}</div>
    <div class="chart-box">{graph_scores}</div>
    <details>
      {d_sections}
      <table>
        <thead><tr>{th_section}{th_intitule}{th_score_moyen}{th_notees}</tr></thead>
        <tbody>{lignes_sections}</tbody>
      </table>
    </details>
  </section>

  <section class="panneau large">
    <header>{t_faibles}{s_faibles}</header>
    <div class="chart-box">{graph_faibles}</div>
    <details>
      {d_chiffre}
      <table>
        <thead><tr>{th_code}{th_section}{th_question}{th_score_moyen}{th_appels}</tr></thead>
        <tbody>{lignes_faibles}</tbody>
      </table>
    </details>
  </section>

  <div class="grille">
    <section class="panneau">
      <header>{t_op}</header>
      <div class="chart-box">{graph_op}</div>
    </section>

    <section class="panneau">
      <header>{t_score_op}{s_score_op}</header>
      <div class="chart-box">{graph_score_op}</div>
    </section>
  </div>

  <section class="panneau large">
    <header>{t_scenarios}{s_scenarios}</header>
    <div class="chart-box">{graph_scenarios}</div>
    <details>
      {d_scenarios}
      <table>
        <thead><tr>{th_code}{th_famille}{th_scenario}{th_appels}{th_score_moyen}<th class="num">Orange</th><th class="num">MTN</th></tr></thead>
        <tbody>{lignes_scenarios}</tbody>
      </table>
    </details>
  </section>

  <section class="panneau large">
    <header>{t_alertes}{s_alertes}</header>
    <div class="chart-box">{graph_alertes}</div>
  </section>

  <section class="panneau large">
    <header>{t_notes}{s_notes}</header>
    <div class="chart-box">{graph_notes}</div>
    <div class="legende">{legende_notes}</div>
    <details>
      {d_notes}
      <table>
        <thead><tr>{th_section}{th_intitule}<th class="num">100</th><th class="num">50</th><th class="num">0</th><th class="num">N/A</th></tr></thead>
        <tbody>{lignes_notes}</tbody>
      </table>
    </details>
  </section>

  <div class="grille">
    <section class="panneau">
      <header>{t_tranche}</header>
      <div class="chart-box">{graph_tranche}</div>
    </section>

    <section class="panneau">
      <header>{t_enq}</header>
      <div class="chart-box">{graph_enq}</div>
    </section>
  </div>

  <section class="panneau large">
    <header>{t_recentes}</header>
    <table>
      <thead><tr>{th_date}{th_enq}{th_reseau}{th_scenario}{th_attente}{th_duree}{th_score}</tr></thead>
      <tbody>{recentes}</tbody>
    </table>
  </section>

  {pied}
</div>

<div id="tip" role="status"></div>
<script>
const I18N = {i18n};
const tip = document.getElementById('tip');
document.addEventListener('mouseover', e => {{
  const c = e.target.closest('[data-tip]');
  if (!c) return;
  tip.textContent = c.getAttribute('data-tip');
  tip.classList.add('on');
}});
document.addEventListener('mousemove', e => {{
  if (!tip.classList.contains('on')) return;
  const m = 14, r = tip.getBoundingClientRect();
  tip.style.left = Math.min(e.clientX + m, innerWidth - r.width - 8) + 'px';
  tip.style.top = Math.max(e.clientY - r.height - m, 8) + 'px';
}});
document.addEventListener('mouseout', e => {{
  if (e.target.closest('[data-tip]')) tip.classList.remove('on');
}});

// --- bascule FR / EN : chaque texte porte sa version anglaise en data-en,
// chaque infobulle la sienne en data-tip-en. Meme mecanique que le guide.
// Messages fabriques par le navigateur : meme source que le reste
// (traductions.JS_TEXTES), aucune chaine en dur ici.
function t(cle) {{ return I18N[cle][LANG === 'en' ? 1 : 0]; }}

const CLE_LANGUE = 'mds_call_center_002_26:dashboard_langue';
let LANG = 'fr';
try {{ if (localStorage.getItem(CLE_LANGUE) === 'en') LANG = 'en'; }} catch (e) {{}}

// innerHTML n'est pas fiable sur les noeuds SVG : on y ecrit du texte brut.
function poser(el, contenu) {{
  if (el.ownerSVGElement) el.textContent = contenu.replace(/<[^>]+>/g, '');
  else el.innerHTML = contenu;
}}

function appliquerLangue(l) {{
  LANG = (l === 'en') ? 'en' : 'fr';
  document.documentElement.lang = LANG;
  document.querySelectorAll('[data-en]').forEach(el => {{
    if (el.dataset.fr === undefined) {{
      el.dataset.fr = el.ownerSVGElement ? el.textContent : el.innerHTML;
    }}
    poser(el, LANG === 'en' ? el.dataset.en : el.dataset.fr);
  }});
  document.querySelectorAll('[data-tip-en]').forEach(el => {{
    if (el.dataset.tipFr === undefined) {{
      el.dataset.tipFr = el.getAttribute('data-tip');
    }}
    el.setAttribute('data-tip', LANG === 'en' ? el.dataset.tipEn : el.dataset.tipFr);
  }});
  const b = document.getElementById('langue');
  b.textContent = t('bouton_langue');
  b.title = t('titre_langue_dash');
  b.setAttribute('aria-pressed', LANG === 'en' ? 'true' : 'false');
  try {{ localStorage.setItem(CLE_LANGUE, LANG); }} catch (e) {{}}
}}

document.getElementById('langue').addEventListener('click', () => {{
  appliquerLangue(LANG === 'en' ? 'fr' : 'en');
}});

appliquerLangue(LANG);
</script>
"""


# Seules les cles utilisees par cette page.
I18N_JSON = json.dumps(
    {c: list(traductions.JS_TEXTES[c]) for c in ("bouton_langue", "titre_langue_dash")},
    ensure_ascii=False)


def controler_traductions():
    """Signale les textes de cette page qui n'ont pas de version anglaise.

    Meme garde-fou que build_form.py : le dictionnaire etant indexe sur le
    libelle francais exact, une retouche du francais ici sans report dans
    traductions.py ferait retomber la bascule sur le francais, en silence.
    """
    manquantes = sorted(t for t in TEXTES_VUS if not traductions.couverte(t))
    if manquantes:
        print(f"  ATTENTION : {len(manquantes)} texte(s) sans traduction anglaise :")
        for m in manquantes:
            print(f"    - {m[:90]}")
    return manquantes


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--uid", default=UID_DEFAUT,
                   help="uid du projet Kobo (vide tant qu'il n'est pas déployé)")
    p.add_argument("--demo", action="store_true",
                   help="forcer le jeu de démonstration")
    args = p.parse_args()

    lignes, demo = [], args.demo
    if not args.demo and args.uid:
        try:
            lignes = charger_reelles(args.uid)
        except Exception as exc:              # API injoignable, token absent...
            print(f"Lecture Kobo impossible ({exc}) — bascule sur la démonstration.")
    if not lignes:
        demo = True
        lignes = generer_demo()

    SORTIE.write_text(rendre(agreger(lignes), demo, args.uid), encoding="utf-8")
    controler_traductions()
    print(f"OK : {SORTIE.name} — {len(lignes)} soumissions"
          + (" (DEMONSTRATION)" if demo else " (donnees reelles)"))
    print(f"  {len(TEXTES_VUS)} textes bilingues contrôlés")


if __name__ == "__main__":
    main()
