#!/usr/bin/env python3
"""Genere le questionnaire interactif de l'enqueteur (MDS JOB 002/26).

Meme moteur que le JOB 001/26 (audit des agences), pilote par
form_structure.json : une etape par section, et le bouton Suivant reste bloque
tant que toutes les questions obligatoires visibles de l'etape courante ne sont
pas renseignees. Les questions conditionnelles apparaissent comme dans
KoboCollect et le brouillon est conserve dans le navigateur de l'enqueteur.

UNE ETAPE MAL REMPLIE SE DIT AU CHANGEMENT DE PAGE. Le controle ne porte pas
seulement sur ce qui manque : les `constraint` du formulaire -- date dans le
futur, duree hors bornes, heure de fin anterieure a l'heure de debut -- sont
rejouees ici. La faute est surlignee des la saisie, puis nommee et bloquante au
moment de passer a l'etape suivante, au lieu d'etre decouverte a la fin, quand
tout est a relire.

Specifique au call center : la page **rejoue le bareme** du questionnaire. Le
score de chaque section et le score total sont recalcules a chaque reponse
sans jamais etre montres a l'enqueteur,
exactement comme le formulaire Kobo les calcule -- l'enqueteur voit sa note
avant meme de saisir dans KoboCollect.

La page est bilingue : chaque texte porte sa version anglaise dans un attribut
`data-en` (traductions.py) et le bouton FR / EN bascule toute la page sans
rechargement, comme le selecteur de langue de KoboCollect.

Sortie : guide_enqueteur.html
"""
import html
import json
import re
from pathlib import Path

import theme
import traductions

BASE = Path(__file__).resolve().parent
STRUCTURE = json.loads((BASE / "form_structure.json").read_text(encoding="utf-8"))
SORTIE = BASE / "guide_enqueteur.html"

SURVEY = STRUCTURE["survey"]
CHOICES = STRUCTURE["choices"]

LIEN_COLLECTE = "https://ee.kobotoolbox.org/52lAclB6"
SERVEUR = "https://kf.kobotoolbox.org"
COMPTE = "mds_cmr"

# Les calculs ne sont pas saisis par l'enqueteur : ils sont retires de la page.
IGNORES = {"calculate"}

# Les consignes citent des champs calcules (${temps_total}, ${operateur_nom}...).
# On rejoue leur calcul dans le navigateur plutot que d'afficher l'expression.
RE_IF = re.compile(r"if\(\s*\$\{(\w+)\}\s*=\s*'([^']*)'\s*,\s*'([^']*)'\s*,")
RE_SORTIE = re.compile(r"\$\{(\w+)\}")
RE_INSTANCE = re.compile(
    r"instance\('(\w+)'\)/root/item\[\s*name\s*=\s*\$\{(\w+)\}\s*\]/(\w+)")
# Deux formes de choice_filter : « colonne=${champ} » et, quand une modalite
# se rattache a plusieurs reponses, « selected(colonne, ${champ}) ».
RE_FILTRE = re.compile(r"(\w+)\s*=\s*\$\{(\w+)\}")
RE_FILTRE_SEL = re.compile(r"selected\(\s*(\w+)\s*,\s*\$\{(\w+)\}\s*\)")


def filtres_de(expression):
    """Couples (colonne, champ filtrant) lus dans un choice_filter."""
    return RE_FILTRE_SEL.findall(expression) + RE_FILTRE.findall(expression)

SAISIES = {"text": ("textarea", ""), "integer": ("input", "number"),
           "date": ("input", "date"), "time": ("input", "time")}
INFOS = {
    "audio": "Enregistrement joint dans KoboCollect au moment de l'appel.",
}
TYPES = {"text": "Texte libre", "integer": "Nombre", "date": "Date",
         "time": "Heure", "audio": "Enregistrement"}

LISTE_DE = {l["name"]: l["type"].split()[1]
            for l in SURVEY if l["type"].startswith("select")}
ETIQUETTES = {(c["list_name"], c["name"]): c["label"] for c in CHOICES}

# Champs deduits : leur calcul est rejoue a l'identique dans le navigateur.
#   {"t": "table",  "liste":.., "champ":.., "col":..}  -> lecture du referentiel
#   {"t": "chaine", "c": [[champ, {code: valeur}], ...]} -> if() imbriques
#   {"t": "special"} -> jour de la semaine et temps passe, calcules en JS
# Le bareme est lu dans form_structure.json : le navigateur applique la meme
# table que les calculs XPath du formulaire, il n'y a pas deux sources.
NOTATION = STRUCTURE["notation"]

CALCULS = {}
TABLES = {}
# Calculs que le parseur de chaines de if() ne sait pas lire -- ils comparent
# une date ou une heure, pas le code d'une modalite : le navigateur les rejoue
# a la main dans `calcule()`.
SPECIAUX = {"jour_semaine", "tranche_horaire"}
for _cle in NOTATION:
    SPECIAUX.add(f"SCORE_{_cle}")
SPECIAUX.add("SCORE_TOTAL")
for _l in SURVEY:
    if _l.get("readonly") != "yes" and _l["type"] != "calculate":
        continue
    if _l["name"].startswith("SCORE_"):
        CALCULS[_l["name"]] = {"t": "score",
                               "cle": _l["name"].split("_", 1)[1]}
        continue
    if _l["name"] in SPECIAUX:
        CALCULS[_l["name"]] = {"t": "special"}
        continue
    m = RE_INSTANCE.search(_l["calculation"])
    if m:
        liste_nom, champ, col = m.groups()
        CALCULS[_l["name"]] = {"t": "table", "liste": liste_nom,
                               "champ": champ, "col": col}
        TABLES.setdefault(liste_nom, {})
        continue
    chaine = []
    for champ, cod, val in RE_IF.findall(_l["calculation"]):
        if not chaine or chaine[-1][0] != champ:
            chaine.append([champ, {}])
        chaine[-1][1][cod] = val
    if chaine:
        CALCULS[_l["name"]] = {"t": "chaine", "c": chaine}

# Referentiel embarque : uniquement les listes reellement interrogees.
for _c in CHOICES:
    if _c["list_name"] in TABLES:
        TABLES[_c["list_name"]][_c["name"]] = {
            k: v for k, v in _c.items()
            if k not in ("list_name", "name", "label") and v}

# Libelles des modalites des champs cites dans les consignes (${motif_visite}...).
CITES = {n for _l in SURVEY for n in RE_SORTIE.findall(_l["label"] or "")}
ETIQ_JS = {n: {c["name"]: c["label"] for c in CHOICES
               if c["list_name"] == LISTE_DE[n]}
           for n in CITES if n in LISTE_DE}
ETIQ_EN = {n: {c: traductions.en(l) for c, l in tab.items()}
           for n, tab in ETIQ_JS.items()}


def e(t):
    """Echappe, met en gras les **...**, rend les sauts de ligne et les ${calculs}."""
    t = html.escape(t or "")
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t, flags=re.S)
    t = RE_SORTIE.sub(
        lambda m: f'<span class="calc" data-calc="{m.group(1)}">—</span>', t)
    return t.replace("\n\n", "<br><br>").replace("\n", "<br>")


def T(fr):
    """Version anglaise d'un libelle ; le francais a defaut de traduction."""
    return traductions.en(fr)


def txt(t):
    return html.escape(t or "")


def bi(texte, rendu=None):
    """Attribut data-en : la page porte les deux langues, le bouton bascule."""
    rendu = rendu or e
    version_fr, version_en = rendu(texte), rendu(T(texte))
    if version_fr == version_en:
        return ""
    return f' data-en="{html.escape(version_en, quote=True)}"'


def bi_html(fr_html, en_html):
    """Meme chose pour deux fragments HTML deja construits."""
    if fr_html == en_html:
        return ""
    return f' data-en="{html.escape(en_html, quote=True)}"'


def sp(fr, balise="span"):
    """Fragment d'interface bilingue : le francais visible, l'anglais en data-en."""
    return f'<{balise}{bi(fr, txt)}>{txt(fr)}</{balise}>'


def modalites(type_):
    if not type_.startswith("select"):
        return []
    nom = type_.split()[1]
    return [(c["name"], c["label"]) for c in CHOICES if c["list_name"] == nom]


def libelle_type(type_):
    if type_.startswith("select_one"):
        return "Un seul choix"
    if type_.startswith("select_multiple"):
        return "Choix multiple"
    return TYPES.get(type_, type_)


RE_CODE = re.compile(r"^(Q\d+|S\d\d_\d)(?:_(alerte|com|txt))?$")

# Suffixes affiches sous le code : l'alerte critique et le commentaire d'un
# score de 0, comme le « pourquoi » de Q25, portent le numero de leur question,
# pas un code a eux.
SUFFIXE_CODE = {"alerte": " alerte", "com": " com", "txt": " txt"}


def code(nom):
    """Code court affiche dans la gouttiere : « Q15 », « Q15 com », « TOTAL »."""
    if nom.startswith("SCORE_"):
        return nom.split("_", 1)[1]
    m = RE_CODE.match(nom)
    if not m:
        return ""
    return m.group(1) + SUFFIXE_CODE.get(m.group(2), "")


# Noms lisibles pour les champs sans code Qxx, utilises dans les etiquettes
# "Posee si ...".
ALIAS = {"escalade": "Escalade", "renvoi": "Renvoi",
         "nb_attentes": "Mises en attente", "nb_transferts": "Transferts",
         "scenario_joue": "Scénario",
         "region": "Région administrative", "departement": "Département",
         "ville": "Ville"}


def court(nom):
    return ALIAS.get(nom) or code(nom) or nom.replace("_", " ")


def etiquette(nom, valeur):
    return ETIQUETTES.get((LISTE_DE.get(nom, ""), valeur), valeur)


# ---------------------------------------------------------------------
# Conditions d'affichage : traduction generique des expressions XLSForm
# ---------------------------------------------------------------------
RE_NSEL = re.compile(r"not\(\s*selected\(\s*\$\{(\w+)\}\s*,\s*'([^']*)'\s*\)\s*\)")
RE_SEL = re.compile(r"selected\(\s*\$\{(\w+)\}\s*,\s*'([^']*)'\s*\)")
RE_NE = re.compile(r"\$\{(\w+)\}\s*!=\s*'([^']*)'")
RE_EQ = re.compile(r"\$\{(\w+)\}\s*=\s*'([^']*)'")
# Comparaison numerique : « au moins une mise en attente », « au moins un
# transfert ». La valeur n'est pas entre quotes, elle ne peut pas etre confondue
# avec une modalite.
RE_GT = re.compile(r"\$\{(\w+)\}\s*>\s*(\d+)")


def conditions(expr):
    """Retourne (mode, [(champ, operateur, valeur)]) ; mode vaut "and" ou "or"."""
    if not expr:
        return "and", []
    mode = "or" if " or " in expr else "and"
    clauses = [(n, "nsel", v) for n, v in RE_NSEL.findall(expr)]
    reste = RE_NSEL.sub("", expr)
    clauses += [(n, "sel", v) for n, v in RE_SEL.findall(reste)]
    reste = RE_SEL.sub("", reste)
    clauses += [(n, "ne", v) for n, v in RE_NE.findall(reste)]
    reste = RE_NE.sub("", reste)
    clauses += [(n, "eq", v) for n, v in RE_EQ.findall(reste)]
    reste = RE_EQ.sub("", reste)
    clauses += [(n, "gt", v) for n, v in RE_GT.findall(reste)]
    return mode, clauses


# Conditions trop longues ou trop techniques a enumerer : libelle ecrit a la
# main.
LIBELLE_SPECIAL = {
    # Le renvoi enumere ses trois destinations : les lister dans le tag
    # donnerait une phrase de deux lignes la ou une seule dit la meme chose.
    "renvoi_precision": "Posée si un renvoi a été indiqué",
    "Q15": "Posée en cas d'escalade ou de renvoi",
}
# Un `required` porteur d'une expression : la question est facultative tant que
# la condition n'est pas remplie. Le libelle du tag s'ecrit a la main, comme
# celui des conditions d'affichage. Aucune question du questionnaire n'en porte
# plus ; la mecanique reste, elle ne coute rien et resservira.
LIBELLE_OBLIGATION = {}
# Les 25 blocs de la section I portent deja le libelle du scenario en titre :
# « Posee si Scenario = S07 · Digital · Application operateur inaccessible »
# le repeterait mot pour mot. Une phrase suffit.
LIBELLE_BLOC_SCENARIO = "Posée si c'est le scénario que vous avez joué"


def libelle_condition(mode, clauses, nom_question="", anglais=False):
    def tr(x):
        return T(x) if anglais else x

    if nom_question in LIBELLE_SPECIAL:
        return tr(LIBELLE_SPECIAL[nom_question])
    if nom_question.startswith("grp_s") and nom_question[5:].isdigit():
        return tr(LIBELLE_BLOC_SCENARIO)
    if not clauses:
        return ""
    parts = []
    for nom, op, val in clauses:
        signe = {"nsel": "≠", "ne": "≠", "gt": ">"}.get(op, "=")
        parts.append(f"{tr(court(nom))} {signe} {tr(etiquette(nom, val))}")
    joint = tr(" ou ") if mode == "or" else tr(" et ")
    return tr("Posée si ") + joint.join(parts)


def attr_condition(ligne):
    """Retourne (attribut data-req, etiquette « Posée si … » deja balisee)."""
    mode, cl = conditions(ligne.get("relevant", ""))
    if not cl:
        return "", ""
    data = html.escape(json.dumps({"m": mode, "c": [list(c) for c in cl]},
                                  ensure_ascii=False))
    nom = ligne.get("name", "")
    lib = libelle_condition(mode, cl, nom)
    lib_en = libelle_condition(mode, cl, nom, anglais=True)
    tag = (f'<span class="tag tag-cond"{bi_html(txt(lib), txt(lib_en))}>'
           f'{txt(lib)}</span>')
    return f' data-req="{data}"', tag


def attr_obligation(req, nom):
    """Retourne (attribut data-obl-si, libelle du tag) d'un `required` expression.

    `required` vaut « yes » pour la quasi-totalite des questions ; il peut aussi
    porter une EXPRESSION, et la question n'est alors obligatoire que lorsque
    celle-ci est vraie. Elle se lit avec le parseur des `relevant`, et le
    navigateur l'evalue de la meme facon.
    """
    if not req or req == "yes":
        return "", ""
    mode, cl = conditions(req)
    if not cl:
        return "", ""
    data = html.escape(json.dumps({"m": mode, "c": [list(c) for c in cl]},
                                  ensure_ascii=False))
    return f' data-obl-si="{data}"', LIBELLE_OBLIGATION.get(
        nom, "Obligatoire sous condition")


# Une reponse peut etre PRESENTE ET FAUSSE : le formulaire Kobo pose des
# `constraint` -- date dans le futur, duree hors bornes, heure de fin anterieure
# a l'heure de debut. La page les rejoue pour signaler la faute des la saisie
# puis au changement d'etape, et non au moment du report dans KoboCollect.
#
# Trois formes couvrent tout le questionnaire ; une quatrieme qui apparaitrait
# est SIGNALEE A LA GENERATION plutot que silencieusement ignoree -- sans quoi
# la page laisserait passer ce que Kobo refusera.
RE_BORNES = re.compile(r"^\.\s*>=\s*(-?\d+)\s+and\s+\.\s*<=\s*(-?\d+)$")
RE_APRES = re.compile(r"^decimal-time\(\.\)\s*>\s*decimal-time\(\$\{(\w+)\}\)$")
CONTRAINTES_INCONNUES = []


def attr_contrainte(ligne):
    """(attribut data-ctr, paragraphe du message, specification lue).

    La specification sert deux fois : au navigateur, qui rejoue la contrainte,
    et au rendu du champ, qui en tire les bornes de la saisie.
    """
    expr = " ".join((ligne.get("constraint") or "").split())
    if not expr:
        return "", "", None
    bornes, apres = RE_BORNES.match(expr), RE_APRES.match(expr)
    if expr == ". <= today()":
        spec = {"t": "pas_futur"}
    elif bornes:
        spec = {"t": "borne", "min": int(bornes.group(1)),
                "max": int(bornes.group(2))}
    elif apres:
        spec = {"t": "apres", "champ": apres.group(1)}
    else:
        CONTRAINTES_INCONNUES.append((ligne["name"], expr))
        return "", "", None
    msg = ligne.get("constraint_message") or "Réponse invalide."
    data = html.escape(json.dumps(spec, ensure_ascii=False), quote=True)
    return (f' data-ctr="{data}"',
            f'<p class="q-invalide-txt"{bi(msg, txt)}>{txt(msg)}</p>', spec)


# ---------------------------------------------------------------------
# Decoupage en etapes : un groupe de premier niveau = une etape
# ---------------------------------------------------------------------
sections, pile = [], []
for ligne in SURVEY:
    t = ligne["type"]
    if t in IGNORES:
        continue
    if t == "begin_group":
        pile.append(ligne)
        if len(pile) == 1:
            sections.append({"titre": ligne["label"], "id": ligne["name"], "blocs": []})
        else:
            sections[-1]["blocs"].append({"kind": "sous_debut", "ligne": ligne})
        continue
    if t == "end_group":
        pile.pop()
        if pile:
            sections[-1]["blocs"].append({"kind": "sous_fin"})
        continue
    cible = {"kind": "q", "ligne": ligne}
    if not pile:
        sections.append({"titre": None, "id": f"libre_{len(sections)}", "blocs": [cible]})
    else:
        sections[-1]["blocs"].append(cible)


def compte_questions(s):
    """Les champs deduits ne sont pas saisis : ils ne comptent pas."""
    return sum(1 for b in s["blocs"]
               if b["kind"] == "q" and b["ligne"]["type"] != "note"
               and b["ligne"].get("readonly") != "yes")


# ---------------------------------------------------------------------
# Rendu d'une question
# ---------------------------------------------------------------------
def rendre_question(ligne):
    t = ligne["type"]
    if t == "note":
        return (f'<div class="consigne-bloc"{bi(ligne["label"])}>'
                f'{e(ligne["label"])}</div>')

    nom = html.escape(ligne["name"])
    attr_req, tag_cond = attr_condition(ligne)
    attr_ctr, p_invalide, spec_ctr = attr_contrainte(ligne)
    auto = ligne.get("readonly") == "yes"
    req = "" if auto else ligne.get("required", "")
    attr_obl_si, tag_obl = attr_obligation(req, ligne["name"])
    obligatoire = bool(req)
    attr_obl = (' data-obl="1"' + attr_obl_si) if obligatoire else ""
    attr_auto = ' data-auto="1"' if auto else ""

    o = [f'<article class="q" id="q-{nom}" data-name="{nom}"'
         f'{attr_req}{attr_obl}{attr_auto}{attr_ctr}>']
    c = code(ligne["name"])
    o.append('<div class="q-gutter">'
             + (f'<span class="q-code">{html.escape(c)}</span>' if c else "")
             + '<span class="q-etat" aria-hidden="true"></span></div>')
    o.append('<div class="q-body">')
    o.append(f'<p class="q-label" id="lab-{nom}"{bi(ligne["label"])}>'
             f'{e(ligne["label"])}</p>')

    def tag(classe, texte):
        return f'<span class="{classe}"{bi(texte, txt)}>{txt(texte)}</span>'

    meta = [tag("tag tag-type", libelle_type(t))]
    if auto:
        meta.append(tag("tag tag-auto", "Déduit — non saisi"))
    elif tag_obl:
        meta.append(tag("tag tag-req", tag_obl))
    elif obligatoire:
        meta.append(tag("tag tag-req", "Obligatoire"))
    else:
        meta.append(tag("tag", "Facultatif"))
    if tag_cond:
        meta.append(tag_cond)
    o.append(f'<div class="q-meta">{"".join(meta)}</div>')

    if ligne.get("hint"):
        o.append(f'<p class="q-hint"{bi(ligne["hint"])}>{e(ligne["hint"])}</p>')

    mods = modalites(t)
    if auto:
        calc = f'<span class="calc" data-calc="{nom}">—</span>'
        o.append(f'<p class="q-auto"'
                 f'{bi_html("Valeur déduite : " + calc, T("Valeur déduite :") + " " + calc)}>'
                 f'Valeur déduite : {calc}</p>')
    elif mods:
        multi = "true" if t.startswith("select_multiple") else "false"
        # Cascade generique : region -> departement -> ville (page 2).
        filtres = filtres_de(ligne.get("choice_filter", "") or "")
        attr_f = ""
        if filtres:
            champs = json.dumps([c for _col, c in filtres], ensure_ascii=False)
            attr_f = f' data-filtre="{html.escape(champs, quote=True)}"'
        o.append(f'<div class="choix-liste" role="group" aria-labelledby="lab-{nom}" '
                 f'data-multi="{multi}"{attr_f}>')
        cols = {c["name"]: c for c in CHOICES
                if c["list_name"] == t.split()[1]} if filtres else {}
        for i, (val, label) in enumerate(mods, 1):
            fv = ""
            if filtres:
                attendus = json.dumps([cols[val].get(col, "") for col, _c in filtres],
                                      ensure_ascii=False)
                fv = f' data-f="{html.escape(attendus, quote=True)}"'
            o.append(f'<button type="button" class="choix" data-v="{html.escape(val)}"'
                     f'{fv} aria-pressed="false"><span class="choix-n">{i}</span>'
                     f'<span{bi(label, txt)}>{html.escape(label)}</span></button>')
        if filtres:
            noms = ", ".join(court(champ) for _col, champ in filtres)
            noms_en = ", ".join(T(court(champ)) for _col, champ in filtres)
            vide = "Choisissez d'abord : " + noms + "."
            vide_en = T("Choisissez d'abord : ") + noms_en + "."
            o.append(f'<p class="choix-vide"{bi_html(txt(vide), txt(vide_en))}>'
                     f'{txt(vide)}</p>')
        o.append("</div>")
    elif t in SAISIES:
        balise, mode = SAISIES[t]
        if balise == "textarea":
            o.append(f'<textarea class="saisie" rows="2" aria-labelledby="lab-{nom}" '
                     f'data-ph-en="{html.escape(T("Votre réponse…"), quote=True)}" '
                     f'placeholder="Votre réponse…"></textarea>')
        else:
            # Les bornes du champ sont celles de la contrainte, relues une seule
            # fois : le navigateur borne la saisie, et contrainteTenue() dit la
            # meme chose quand elle est contournee au clavier ou au collage.
            sup = ""
            if t == "integer" and spec_ctr and spec_ctr["t"] == "borne":
                sup = f' min="{spec_ctr["min"]}" max="{spec_ctr["max"]}"'
            o.append(f'<input class="saisie saisie-courte" type="{mode}"{sup} '
                     f'aria-labelledby="lab-{nom}">')
    elif t in INFOS:
        o.append(f'<p class="q-auto"{bi(INFOS[t], txt)}>{txt(INFOS[t])}</p>')

    manque = "Cette réponse est obligatoire pour continuer."
    o.append(f'<p class="q-manque-txt"{bi(manque, txt)}>{txt(manque)}</p>')
    o.append(p_invalide)
    o.append("</div></article>")
    return "".join(o)


# ---------------------------------------------------------------------
# Blocs d'ouverture, places dans la premiere etape
# ---------------------------------------------------------------------
INTRO_FR = """
<div class="setup">
  <div class="bloc">
    <h3>Connexion KoboCollect</h3>
    <dl class="kv">
      <dt>Serveur</dt><dd>""" + SERVEUR + """</dd>
      <dt>Compte</dt><dd>""" + COMPTE + """</dd>
      <dt>Lien web</dt><dd>""" + (
          f'<a href="{LIEN_COLLECTE}">{LIEN_COLLECTE}</a>' if LIEN_COLLECTE
          else "projet a deployer &mdash; <code>python kobo.py deploy</code>") + """</dd>
    </dl>
  </div>
  <div class="bloc">
    <h3>Avant de passer les appels</h3>
    <ol>
      <li>KoboCollect : <em>Param&egrave;tres &rarr; Param&egrave;tres du serveur</em>, saisir l'URL et les identifiants MDS.</li>
      <li><em>T&eacute;l&eacute;charger un formulaire vide</em> &rarr; cocher le questionnaire &rarr; T&eacute;l&eacute;charger.</li>
      <li>Pr&eacute;parer un <strong>chronom&egrave;tre</strong> : la page <em>Mesures</em> relève l'attente avant conseiller, la dur&eacute;e de l'appel et le temps cumul&eacute; des mises en attente.</li>
      <li>Pr&eacute;voir de quoi <strong>noter les mots exacts</strong> du conseiller : tout crit&egrave;re <em>non conforme</em> doit &ecirc;tre &eacute;tay&eacute; par une formulation entendue.</li>
      <li>Un seul sc&eacute;nario par appel ; renseigner le questionnaire <strong>imm&eacute;diatement apr&egrave;s avoir raccroch&eacute;</strong>.</li>
      <li>Envoyer les formulaires finalis&eacute;s d&egrave;s qu'une connexion est disponible.</li>
    </ol>
  </div>
</div>

<div class="bloc" style="margin-bottom:22px">
  <h3>Comment utiliser cette page</h3>
  <ol>
    <li><strong>Une &eacute;tape &agrave; la fois.</strong> Le bouton <em>Suivant</em> ne s'active
        qu'une fois toutes les questions obligatoires de l'&eacute;tape renseign&eacute;es, exactement
        comme dans KoboCollect.</li>
    <li><strong>Une erreur se signale tout de suite.</strong> Une r&eacute;ponse
        impossible &mdash; date &agrave; venir, dur&eacute;e hors bornes, heure de fin
        ant&eacute;rieure &agrave; l'heure de d&eacute;but &mdash; est
        <strong>surlign&eacute;e d&egrave;s la saisie</strong> et vous retient
        &agrave; l'&eacute;tape tant qu'elle n'est pas corrig&eacute;e. Rien n'attend la
        fin du questionnaire.</li>
    <li><strong>Cliquez directement sur les modalit&eacute;s</strong> pour r&eacute;pondre ; un second
        clic annule le choix.</li>
    <li><strong>Vous ne notez pas, vous qualifiez.</strong> Quatre r&eacute;ponses partout :
        totalement conforme, partiellement conforme, non conforme, non applicable.
        <strong>Aucun score ne s'affiche</strong> : ni pendant la saisie, ni &agrave; la fin.
        Le calcul se fait en arri&egrave;re-plan et ne se lit que dans la base MDS.
        Un <em>non applicable</em> <strong>sort du calcul</strong> au lieu de compter z&eacute;ro.</li>
    <li><strong>Un <em>non conforme</em> ouvre un commentaire obligatoire.</strong> Il
        n'appara&icirc;t que l&agrave; : c'est une situation exceptionnelle ou une alerte
        critique, elle doit &ecirc;tre &eacute;tay&eacute;e par un fait observ&eacute; ou la
        formulation exacte du conseiller.</li>
    <li>Les questions conditionnelles <strong>apparaissent d'elles-m&ecirc;mes</strong> :
        escalade, renvoi en agence, mise en attente et transferts ne sont demand&eacute;s
        que si l'&eacute;v&eacute;nement s'est produit. R&eacute;pondez d'abord aux
        <em>Mesures</em>.</li>
    <li>Vos r&eacute;ponses sont <strong>conserv&eacute;es dans ce navigateur</strong> : la page peut
        &ecirc;tre ferm&eacute;e et rouverte sans perte.</li>
    <li><strong>La saisie officielle reste celle de KoboCollect.</strong> Utilisez
        <em>Copier les r&eacute;ponses</em> pour reporter une saisie faite hors connexion.</li>
    <li>Ne jamais r&eacute;v&eacute;ler que vous &ecirc;tes enqu&ecirc;teur pendant l'appel.</li>
  </ol>
</div>
"""

INTRO_EN = """
<div class="setup">
  <div class="bloc">
    <h3>KoboCollect connection</h3>
    <dl class="kv">
      <dt>Server</dt><dd>""" + SERVEUR + """</dd>
      <dt>Account</dt><dd>""" + COMPTE + """</dd>
      <dt>Web link</dt><dd>""" + (
          f'<a href="{LIEN_COLLECTE}">{LIEN_COLLECTE}</a>' if LIEN_COLLECTE
          else "project not deployed yet &mdash; <code>python kobo.py deploy</code>") + """</dd>
    </dl>
  </div>
  <div class="bloc">
    <h3>Before making the calls</h3>
    <ol>
      <li>KoboCollect: <em>Settings &rarr; Server settings</em>, enter the URL and the MDS credentials.</li>
      <li><em>Download a blank form</em> &rarr; tick the questionnaire &rarr; Download.</li>
      <li>Get a <strong>stopwatch</strong> ready: the <em>Measurements</em> page records the wait before the adviser, the length of the call and the total time on hold.</li>
      <li>Have something ready to <strong>write down the exact words</strong> used by the adviser: every criterion marked <em>not compliant</em> must be backed up by wording you heard.</li>
      <li>One scenario per call; fill in the questionnaire <strong>immediately after hanging up</strong>.</li>
      <li>Send the finalised forms as soon as a connection is available.</li>
    </ol>
  </div>
</div>

<div class="bloc" style="margin-bottom:22px">
  <h3>How to use this page</h3>
  <ol>
    <li><strong>One step at a time.</strong> The <em>Next</em> button only becomes
        active once every required question on the step has been answered, exactly
        as in KoboCollect.</li>
    <li><strong>A mistake is flagged straight away.</strong> An impossible answer
        &mdash; a date still to come, a length outside its bounds, a finish time
        earlier than the start time &mdash; is <strong>highlighted as you type</strong>
        and keeps you on the step until it is corrected. Nothing waits for the end of
        the questionnaire.</li>
    <li><strong>Click straight on the answer options</strong> to answer; a second
        click cancels the choice.</li>
    <li><strong>You are not marking, you are qualifying.</strong> Four answers
        everywhere: fully compliant, partially compliant, not compliant, not applicable.
        <strong>No score is ever shown</strong>: neither while you fill the form in nor
        at the end. It is worked out in the background and can only be read in the MDS
        database. A <em>not applicable</em> <strong>drops out of the
        calculation</strong> instead of counting as zero.</li>
    <li><strong>A <em>not compliant</em> opens a mandatory comment.</strong> It appears
        nowhere else: it is an exceptional situation or a critical alert, and must be
        backed up by an observed fact or the exact wording used by the adviser.</li>
    <li>Conditional questions <strong>appear on their own</strong>: escalation, branch
        referral, holds and transfers are only asked if the event actually happened.
        Answer the <em>Measurements</em> page first.</li>
    <li>Your answers are <strong>kept in this browser</strong>: the page can be
        closed and reopened without any loss.</li>
    <li><strong>The official data entry remains KoboCollect.</strong> Use
        <em>Copy answers</em> to transfer an entry made offline.</li>
    <li>Never reveal that you are an auditor during the call.</li>
  </ol>
</div>
"""

# Le bloc d'ouverture bascule en entier avec le bouton de langue.
INTRO = f'<div{bi_html(INTRO_FR, INTRO_EN)}>{INTRO_FR}</div>'

# ---------------------------------------------------------------------
# Assemblage du corps
# ---------------------------------------------------------------------
corps, index = [], []
for n, s in enumerate(sections):
    titre = s["titre"] or "Questions"
    index.append(
        f'<li><a href="#{s["id"]}" data-etape="{n}">'
        f'<span class="idx-n0">{n + 1}</span>'
        f'<span class="idx-nom"{bi(titre, txt)}>{html.escape(titre)}</span>'
        f'<span class="idx-n"><b>0</b>/{compte_questions(s)}</span></a></li>')
    corps.append(f'<section class="section" id="{s["id"]}" data-etape="{n}" hidden>'
                 f'<h2{bi(titre, txt)}>{html.escape(titre)}</h2>')
    if n == 0:
        corps.append(INTRO)

    ouvert = False
    for b in s["blocs"]:
        if b["kind"] == "sous_debut":
            attr, tag_cond = attr_condition(b["ligne"])
            sous_titre = b["ligne"]["label"]
            corps.append(f'<div class="sous"{attr}><h3>'
                         f'<span{bi(sous_titre, txt)}>{html.escape(sous_titre)}</span>'
                         + tag_cond + "</h3>")
            ouvert = True
        elif b["kind"] == "sous_fin":
            if ouvert:
                corps.append("</div>")
                ouvert = False
        else:
            corps.append(rendre_question(b["ligne"]))
    if ouvert:
        corps.append("</div>")
    corps.append("</section>")

N_RECAP = len(sections)
index.append(f'<li><a href="#recap" data-etape="{N_RECAP}">'
             f'<span class="idx-n0">{N_RECAP + 1}</span>'
             f'<span class="idx-nom"{bi("Récapitulatif", txt)}>Récapitulatif</span>'
             f'<span class="idx-n">—</span></a></li>')

TOTAL = sum(compte_questions(s) for s in sections)

CSS = """
.wrap { max-width:1240px; margin:0 auto; padding:22px 26px 40px;
        display:grid; grid-template-columns:250px 1fr; gap:34px; align-items:start; }
@media (max-width:940px) { .wrap { grid-template-columns:1fr; gap:22px; } }

/* --- barre de progression --- */
.progres { position:sticky; top:0; z-index:12; background:var(--card);
           border-bottom:1px solid var(--rule); padding:10px 26px; }
.progres-in { max-width:1240px; margin:0 auto; display:flex; align-items:center;
              gap:16px; flex-wrap:wrap; }
.jauge { flex:1 1 200px; height:8px; background:var(--rule-soft); border-radius:99px;
         overflow:hidden; min-width:140px; }
.jauge span { display:block; height:100%; width:0;
              background:linear-gradient(90deg,var(--mds-navy),var(--mds-cyan));
              border-radius:99px; transition:width .25s ease; }
:root[data-theme="dark"] .jauge span,
:root:not([data-theme="light"]) .jauge span { background:linear-gradient(90deg,var(--mds-cyan),var(--mds-amber)); }
.compteur { font-family:"IBM Plex Mono",monospace; font-size:12.5px; font-weight:600;
            white-space:nowrap; font-variant-numeric:tabular-nums; }
.compteur b { color:var(--accent); font-size:15px; }
.cpt-note { display:block; font-family:"IBM Plex Sans",sans-serif;
            font-size:11px; font-weight:400; color:var(--muted);
            letter-spacing:0; max-width:44ch; }
.actions { display:flex; gap:8px; }
.btn { font-family:"IBM Plex Sans",sans-serif; font-size:12px; font-weight:600;
       padding:6px 13px; border-radius:3px; border:1px solid var(--rule);
       background:var(--card); color:var(--ink-2); cursor:pointer; white-space:nowrap; }
.btn:hover { border-color:var(--accent); color:var(--accent); }
.btn-1 { background:var(--accent); border-color:var(--accent); color:var(--accent-ink); }
.btn-1:hover { filter:brightness(1.12); color:var(--accent-ink); }
.btn:disabled { opacity:.45; cursor:not-allowed; }
.btn:disabled:hover { border-color:var(--rule); color:var(--ink-2); }
.btn-1:disabled:hover { border-color:var(--accent); color:var(--accent-ink); }
.btn.en-attente { background:var(--card); color:var(--amber-ink);
                  border-color:var(--mds-amber); }
.btn.en-attente:hover { background:var(--amber-soft); color:var(--amber-ink); }
.btn-lang { font-family:"IBM Plex Mono",monospace; letter-spacing:.06em; }
.btn-lang[aria-pressed="true"] { border-color:var(--mds-amber); color:var(--amber-ink);
                                 background:var(--amber-soft); }

/* --- sommaire / etapes --- */
.rail { position:sticky; top:60px; }
@media (max-width:940px) { .rail { position:static; } }
.rail h4 { font-family:"IBM Plex Mono",monospace; font-size:10.5px; font-weight:600;
           letter-spacing:.14em; text-transform:uppercase; color:var(--muted);
           margin:0 0 10px 2px; }
.rail ul { list-style:none; margin:0; padding:0; }
.rail a { display:grid; grid-template-columns:auto 1fr auto; align-items:baseline;
          gap:9px; padding:8px 11px; text-decoration:none; font-size:13px;
          line-height:1.35; border-left:2px solid var(--rule-soft); color:var(--ink-2); }
.rail a:hover { background:var(--accent-soft); color:var(--ink); }
.rail a.on { border-left-color:var(--mds-amber); color:var(--ink); font-weight:600;
             background:var(--accent-soft); }
.rail a.fini .idx-n { color:var(--st-good); }
.rail a.ko .idx-n { color:var(--st-crit); }
.rail a.verrou { opacity:.45; cursor:not-allowed; }
.rail a.verrou:hover { background:none; color:var(--ink-2); }
.idx-n0 { font-family:"IBM Plex Mono",monospace; font-size:10.5px; font-weight:600;
          color:var(--muted); background:var(--rule-soft); border-radius:2px;
          padding:1px 5px; }
.rail a.on .idx-n0, .rail a.fini .idx-n0 { background:var(--accent);
                                           color:var(--accent-ink); }
/* Une etape mal remplie se signale dans le sommaire, courante ou non : la
   regle passe apres celle de l'etape courante, a specificite egale. */
.rail a.ko .idx-n0 { background:var(--st-crit); color:#fff; }
.idx-n { font-family:"IBM Plex Mono",monospace; font-size:11px; color:var(--muted);
         font-variant-numeric:tabular-nums; white-space:nowrap; }
.idx-n b { color:var(--accent); }

/* --- cartes d'entete --- */
.setup { display:grid; grid-template-columns:repeat(auto-fit,minmax(290px,1fr));
         gap:16px; margin-bottom:22px; }
.bloc { background:var(--card); border:1px solid var(--rule); border-radius:4px;
        padding:18px 20px; }
.bloc h3 { font-family:Archivo,sans-serif; font-size:12px; font-weight:700;
           letter-spacing:.1em; text-transform:uppercase; color:var(--accent);
           margin:0 0 12px; display:flex; align-items:center; gap:8px; }
.bloc h3::before { content:""; width:14px; height:3px; background:var(--mds-amber);
                   border-radius:2px; flex:none; }
.kv { display:grid; grid-template-columns:auto 1fr; gap:6px 14px; font-size:13px; margin:0; }
.kv dt { color:var(--muted); font-size:11px; letter-spacing:.06em; text-transform:uppercase;
         font-weight:600; padding-top:2px; }
.kv dd { margin:0; font-family:"IBM Plex Mono",monospace; font-size:12.5px;
         word-break:break-all; }
.bloc ol { margin:0; padding-left:19px; font-size:13.5px; color:var(--ink-2); }
.bloc ol li { margin-bottom:5px; }
.bloc ol li::marker { color:var(--mds-amber); font-weight:700; }

/* --- sections / etapes --- */
.section { margin-bottom:8px; scroll-margin-top:64px; }
.section[hidden] { display:none; }
.section h2 { font-family:Archivo,sans-serif; font-weight:700; font-size:16px;
              margin:0 0 14px; padding-bottom:9px; border-bottom:2px solid var(--accent);
              text-transform:uppercase; letter-spacing:.02em; }
.consigne-bloc { background:var(--amber-soft); border-left:3px solid var(--mds-amber);
                 padding:13px 16px; font-size:13px; line-height:1.55; color:var(--ink-2);
                 margin-bottom:14px; border-radius:0 3px 3px 0; }
.consigne-bloc strong { color:var(--ink); }
.calc { font-family:"IBM Plex Mono",monospace; font-weight:600;
        color:var(--accent); background:var(--accent-soft);
        padding:1px 6px; border-radius:2px; }

/* --- question --- */
.q { display:grid; grid-template-columns:66px 1fr; gap:14px; padding:15px 0;
     border-bottom:1px solid var(--rule-soft); }
.q:last-child { border-bottom:none; }
.q[hidden] { display:none; }
.q-gutter { display:flex; flex-direction:column; align-items:flex-start; gap:6px; }
.q-code { font-family:"IBM Plex Mono",monospace; font-size:11.5px; font-weight:600;
          color:var(--accent); background:var(--accent-soft); padding:2px 6px;
          border-radius:2px; white-space:nowrap; }
.q-etat { width:9px; height:9px; border-radius:50%; background:var(--rule);
          margin-left:3px; flex:none; }
.q.ok .q-etat { background:var(--st-good); }
.q.manque { background:var(--amber-soft); border-radius:3px;
            box-shadow:inset 3px 0 0 var(--st-crit); padding-left:11px;
            margin-left:-11px; }
.q.manque .q-etat { background:var(--st-crit); }
.q-manque-txt { display:none; margin:9px 0 0; font-size:12px; font-weight:600;
                color:var(--st-crit); }
.q.manque .q-manque-txt { display:block; }
/* Reponse presente mais fausse : meme severite qu'une reponse absente. */
.q.invalide { background:var(--amber-soft); border-radius:3px;
              box-shadow:inset 3px 0 0 var(--st-crit); padding-left:11px;
              margin-left:-11px; }
.q.invalide .q-etat { background:var(--st-crit); }
.q-invalide-txt { display:none; margin:9px 0 0; font-size:12px; font-weight:600;
                  color:var(--st-crit); }
.q.invalide .q-invalide-txt { display:block; }
.q-label { margin:0 0 8px; font-size:14.5px; font-weight:500; line-height:1.5; max-width:68ch; }
.q-meta { display:flex; flex-wrap:wrap; gap:6px; margin-bottom:9px; }
.tag { font-family:"IBM Plex Mono",monospace; font-size:10px; font-weight:500;
       letter-spacing:.06em; text-transform:uppercase; padding:2px 7px; border-radius:2px;
       border:1px solid var(--rule); color:var(--muted); }
.tag-req { color:var(--amber-ink); border-color:var(--mds-amber); background:var(--amber-soft); }
.tag-cond { color:var(--accent); border-color:currentColor; background:var(--accent-soft); }
.tag-auto { color:var(--muted); border-style:dashed; }
.choix[hidden] { display:none; }
.choix-vide { margin:0; font-size:12.5px; color:var(--muted); font-style:italic; }
.choix-vide[hidden] { display:none; }
.q-hint { margin:0 0 10px; font-size:12.5px; line-height:1.5; color:var(--muted);
          font-style:italic; max-width:72ch; border-left:2px solid var(--rule);
          padding-left:11px; }
.q-auto { margin:0; font-size:12.5px; color:var(--muted); background:var(--accent-soft);
          padding:8px 12px; border-radius:3px; display:inline-block; }

/* --- modalites cliquables --- */
.choix-liste { display:flex; flex-wrap:wrap; gap:7px; }
.choix { display:inline-flex; align-items:center; gap:8px; text-align:left;
         font-family:"IBM Plex Sans",sans-serif; font-size:13px; line-height:1.35;
         padding:7px 13px 7px 8px; border:1px solid var(--rule); border-radius:3px;
         background:var(--card); color:var(--ink-2); cursor:pointer;
         transition:background .12s, border-color .12s, color .12s; max-width:100%; }
.choix:hover { border-color:var(--accent); background:var(--accent-soft); color:var(--ink); }
.choix-n { font-family:"IBM Plex Mono",monospace; font-size:10.5px; font-weight:600;
           color:var(--muted); background:var(--accent-soft); border-radius:2px;
           padding:1px 5px; flex:none; }
.choix[aria-pressed="true"] { background:var(--accent); border-color:var(--accent);
                              color:var(--accent-ink); font-weight:500; }
.choix[aria-pressed="true"] .choix-n { background:rgba(255,255,255,.22);
                                       color:var(--accent-ink); }
:root[data-theme="dark"] .choix[aria-pressed="true"] .choix-n,
:root:not([data-theme="light"]) .choix[aria-pressed="true"] .choix-n { background:rgba(0,0,0,.25); }

.saisie { font-family:"IBM Plex Sans",sans-serif; font-size:13.5px; color:var(--ink);
          background:var(--card); border:1px solid var(--rule); border-radius:3px;
          padding:8px 11px; width:100%; max-width:560px; resize:vertical; }
.saisie-courte { max-width:210px; font-family:"IBM Plex Mono",monospace; }
.saisie:focus { border-color:var(--accent); }
.saisie::placeholder { color:var(--muted); opacity:.7; }

.sous { border:1px solid var(--rule); border-radius:4px; padding:2px 18px 10px;
        margin:14px 0; background:var(--card); }
.sous[hidden] { display:none; }
.sous h3 { font-family:Archivo,sans-serif; font-size:12.5px; font-weight:700;
           letter-spacing:.06em; text-transform:uppercase; color:var(--ink-2);
           margin:15px 0 4px; display:flex; flex-wrap:wrap; align-items:center; gap:10px; }

/* --- navigation bas de page --- */
.nav-bas { position:sticky; bottom:0; z-index:11; display:flex; align-items:center;
           justify-content:space-between; gap:14px; flex-wrap:wrap;
           background:var(--card); border-top:1px solid var(--rule);
           padding:12px 0 14px; margin-top:18px; }
.nav-etape { font-family:"IBM Plex Mono",monospace; font-size:12px; color:var(--muted);
             font-variant-numeric:tabular-nums; }
.nav-etape b { color:var(--ink); }
.nav-bas .btn { font-size:13px; padding:9px 20px; }
.nav-alerte { flex:1 1 100%; order:3; font-size:12.5px; font-weight:600;
              color:var(--st-crit); margin:0; }
.nav-alerte:empty { display:none; }

/* --- recapitulatif --- */
.recap-vide { color:var(--muted); font-size:13px; font-style:italic; margin:0; }
#recap-table td:first-child { width:110px; }
.toast { position:fixed; left:50%; bottom:26px; transform:translateX(-50%);
         background:var(--band); color:var(--band-ink); font-size:13px; padding:10px 18px;
         border-radius:4px; box-shadow:0 6px 20px rgba(0,0,0,.24); opacity:0;
         pointer-events:none; transition:opacity .18s; z-index:30;
         border-left:3px solid var(--mds-amber); }
.toast.on { opacity:1; }
footer { border-top:1px solid var(--rule); margin-top:26px; padding-top:18px;
         font-size:12.5px; color:var(--muted); max-width:72ch; }
footer strong { color:var(--ink); }
"""

JS = """
const CLE = 'mds_call_center_002_26_v1';
const CLE_LANGUE = CLE + ':langue';
let LANG = 'fr';
try { if (localStorage.getItem(CLE_LANGUE) === 'en') LANG = 'en'; } catch (e) {}

// Messages ecrits par le navigateur ; {n} porte le nombre.
function t(cle, n) {
  const m = I18N[cle][LANG === 'en' ? 1 : 0];
  return n === undefined ? m : m.replace('{n}', n);
}
const ETAPES = [...document.querySelectorAll('.section[data-etape]')];
const DERNIERE = ETAPES.length - 1;
let R = {}, etape = 0, maxEtape = 0;

try {
  const brut = JSON.parse(localStorage.getItem(CLE) || '{}') || {};
  R = brut.reponses || {};
  etape = Math.min(brut.etape || 0, DERNIERE);
  maxEtape = Math.min(Math.max(brut.maxEtape || 0, etape), DERNIERE);
} catch (e) { R = {}; }

function sauver() {
  try {
    localStorage.setItem(CLE, JSON.stringify({ reponses: R, etape, maxEtape }));
  } catch (e) {}
}

function estVide(v) {
  return Array.isArray(v) ? v.length === 0 : (v === undefined || v === null || v === '');
}

// Reproduit les conditions du XLSForm. Elle sert deux fois : l'affichage
// (`relevant`) et l'obligation conditionnelle (`required` porteur d'une
// expression, voir le commentaire de la page 14 du formulaire).
function condVraie(brut) {
  let cond;
  try { cond = JSON.parse(brut); } catch (e) { return true; }
  const teste = ([n, op, v]) => {
    const val = R[n];
    if (op === 'eq') return val === v;
    if (op === 'sel') return Array.isArray(val) ? val.includes(v) : val === v;
    if (op === 'nsel') return !(Array.isArray(val) ? val.includes(v) : val === v);
    if (op === 'ne') return val !== undefined && val !== v;
    if (op === 'gt') return !estVide(val) && Number(val) > Number(v);
    return true;
  };
  return cond.m === 'or' ? cond.c.some(teste) : cond.c.every(teste);
}

function visible(el) {
  const brut = el.dataset.req;
  return !brut || condVraie(brut);
}

// Une question sans `data-obl-si` est obligatoire des qu'elle est visible ;
// avec, elle ne l'est que lorsque sa condition est vraie.
function obligatoire(q) {
  const brut = q.dataset.oblSi;
  return !brut || condVraie(brut);
}

// Une question masquee est VIDEE, comme le fait ODK des qu'un champ cesse
// d'etre pertinent. Sans cela, le commentaire d'un score de 0 pose sur une
// question elle-meme conditionnelle resterait affiche sur une reponse fantome,
// et cette reponse continuerait de peser dans le score.
function vider(q) {
  const n = q.dataset.name;
  if (R[n] === undefined) return false;
  delete R[n];
  q.querySelectorAll('.choix').forEach(b => b.setAttribute('aria-pressed', 'false'));
  q.querySelectorAll('.saisie').forEach(s => { s.value = ''; });
  q.classList.remove('ok', 'manque');
  return true;
}

function oublier(el) {
  let change = false;
  el.querySelectorAll('.q[data-name]').forEach(q => { change = vider(q) || change; });
  if (el.matches('.q[data-name]')) change = vider(el) || change;
  return change;
}

function majVisibilite() {
  // Masquer une question peut en masquer une autre : on repasse tant que la
  // visibilite bouge, avec une borne pour ne jamais boucler.
  let efface = false;
  for (let passe = 0; passe < 6; passe++) {
    let change = false;
    document.querySelectorAll('[data-req]').forEach(el => {
      const cache = !visible(el);
      el.hidden = cache;
      if (cache && oublier(el)) change = true;
    });
    if (!change) break;
    efface = true;
  }
  if (efface) sauver();
}

function manquantes(sec) {
  return [...sec.querySelectorAll('.q[data-name][data-obl]')].filter(q =>
    !q.hidden && !q.closest('.sous[hidden]') && obligatoire(q)
    && estVide(R[q.dataset.name]));
}

// « HH:MM » en minutes : la contrainte d'heure du formulaire compare deux
// decimal-time(), ce qui revient au meme sur une saisie <input type="time">.
function enMinutes(v) {
  const m = /^(\\d{1,2}):(\\d{2})/.exec(v || '');
  return m ? Number(m[1]) * 60 + Number(m[2]) : NaN;
}

// La `constraint` du formulaire, rejouee. Une reponse vide n'est jamais fausse
// -- c'est l'affaire de manquantes() -- et une contrainte qu'on ne saurait pas
// evaluer ne bloque personne : elle n'aurait pas ete emise (voir
// CONTRAINTES_INCONNUES, signalees a la generation).
function contrainteTenue(q) {
  const brut = q.dataset.ctr;
  if (!brut) return true;
  const v = R[q.dataset.name];
  if (estVide(v)) return true;
  const c = JSON.parse(brut);
  if (c.t === 'borne') {
    const n = Number(v);
    return !Number.isFinite(n) || (n >= c.min && n <= c.max);
  }
  if (c.t === 'pas_futur') {
    const d = new Date(v + 'T00:00'), j = new Date();
    j.setHours(0, 0, 0, 0);
    return isNaN(d.getTime()) || d <= j;
  }
  if (c.t === 'apres') {
    const a = enMinutes(R[c.champ]), b = enMinutes(v);
    return isNaN(a) || isNaN(b) || b > a;
  }
  return true;
}

function invalides(sec) {
  return [...sec.querySelectorAll('.q[data-name][data-ctr]')].filter(q =>
    !q.hidden && !q.closest('.sous[hidden]') && !contrainteTenue(q));
}

// Ce qui empeche de quitter l'etape, dans l'ordre de la page : ce qui manque et
// ce qui est faux, surlignes ensemble. Retourne le nombre de problemes.
// `avertir` distingue le depart bloque -- on le dit -- du simple retour en
// arriere, ou l'on se contente de marquer l'etape quittee.
function signalerEtape(sec, avertir) {
  const vides = manquantes(sec), faux = invalides(sec);
  vides.forEach(q => q.classList.add('manque'));
  faux.forEach(q => q.classList.add('invalide'));
  const tous = vides.concat(faux);
  if (!tous.length) return 0;
  if (avertir !== false) {
    tous.sort((a, b) => (a.compareDocumentPosition(b) &
                         Node.DOCUMENT_POSITION_FOLLOWING) ? -1 : 1);
    tous[0].scrollIntoView({ behavior: 'smooth', block: 'center' });
    toast(faux.length
      ? (faux.length > 1 ? t('corriger_n', faux.length) : t('corriger_1'))
      : t('manque', vides.length));
  }
  return tous.length;
}

function majEtat() {
  majVisibilite();
  majFiltres();

  let vus = 0, faits = 0;
  ETAPES.forEach(sec => {
    let sv = 0, sf = 0, sx = 0;
    sec.querySelectorAll('.q[data-name]').forEach(q => {
      if (q.dataset.auto) return;            // champ deduit : rien a saisir
      const cache = q.hidden || q.closest('.sous[hidden]');
      // Le surlignage d'une reponse fausse ne se merite pas : il apparait des
      // la saisie, sans attendre le changement de page.
      const juste = contrainteTenue(q);
      q.classList.toggle('invalide', !cache && !juste);
      if (!cache && !juste) sx++;      // une question masquee ne gene personne
      const ok = !estVide(R[q.dataset.name]) && juste;
      q.classList.toggle('ok', ok);
      if (ok) q.classList.remove('manque');
      if (cache) return;
      // Un champ facultatif tant que sa condition d'obligation n'est pas
      // remplie ne compte au denominateur que s'il a ete renseigne : sinon
      // l'etape n'atteindrait jamais « fini ».
      if (!ok && !obligatoire(q)) return;
      sv++; if (ok) sf++;
    });
    const a = document.querySelector('.rail a[data-etape="' + sec.dataset.etape + '"]');
    if (a) {
      a.querySelector('.idx-n').innerHTML = '<b>' + sf + '</b>/' + sv;
      a.classList.toggle('fini', sv > 0 && sf === sv);
      a.classList.toggle('ko', sx > 0);
    }
    vus += sv; faits += sf;
  });

  document.getElementById('faits').textContent = faits;
  document.getElementById('vus').textContent = vus;
  document.querySelector('.jauge span').style.width =
    (vus ? (100 * faits / vus) : 0) + '%';

  const restant = manquantes(ETAPES[etape]).length;
  const faux = invalides(ETAPES[etape]).length;
  const suiv = document.getElementById('suivant');
  suiv.classList.toggle('en-attente', restant + faux > 0);
  suiv.textContent = etape === DERNIERE ? t('terminer') :
    (etape === DERNIERE - 1 ? t('voir_recap') : t('suivant'));
  const dits = [];
  if (restant) dits.push(restant > 1 ? t('reste_n', restant) : t('reste_1'));
  if (faux) dits.push(faux > 1 ? t('corriger_n', faux) : t('corriger_1'));
  document.getElementById('nav-alerte').textContent = dits.join(' · ');
  majCalculs();
  majRecap();
}

function afficherEtape(i, defiler) {
  etape = Math.max(0, Math.min(i, DERNIERE));
  maxEtape = Math.max(maxEtape, etape);
  ETAPES.forEach(s => { s.hidden = Number(s.dataset.etape) !== etape; });
  document.querySelectorAll('.rail a').forEach(a => {
    const n = Number(a.dataset.etape);
    a.classList.toggle('on', n === etape);
    a.classList.toggle('verrou', n > maxEtape);
    a.setAttribute('aria-disabled', n > maxEtape ? 'true' : 'false');
  });
  document.getElementById('etape-n').textContent = etape + 1;
  document.getElementById('precedent').disabled = etape === 0;
  sauver(); majEtat();
  if (defiler !== false) window.scrollTo({ top: 0, behavior: 'smooth' });
}

// --- notation : le navigateur rejoue le bareme du formulaire.
// Une question masquee par un `relevant` ne compte ni au numerateur ni au
// denominateur, exactement comme le calcul XPath de build_form.py.
function masquee(nom) {
  const q = document.querySelector('.q[data-name="' + nom + '"]');
  return !q || q.hidden || !!q.closest('.sous[hidden]');
}

// [points obtenus, points en jeu] pour un critere, ou null s'il est hors
// score : masque par sa condition, sans reponse, ou note « Non applicable »
// (modalite sans points dans le bareme).
function pointsDe(nom, table) {
  if (masquee(nom)) return null;
  const v = R[nom];
  if (v === undefined || v === '') return null;
  const p = table ? table[v] : null;
  if (p === null || p === undefined || p === '') return null;
  return [Number(p), 100];
}

function scoreDe(cle) {
  const sections = (cle === 'TOTAL')
    ? Object.keys(NOTATION).map(k => NOTATION[k])
    : [NOTATION[cle]];
  let num = 0, den = 0;
  for (const s of sections) {
    if (!s) continue;
    for (const paire of s.questions) {
      const r = pointsDe(paire[0], paire[1]);
      if (!r) continue;
      num += r[0]; den += r[1];
    }
  }
  return den ? String(Math.round(100 * num / den)) : '—';
}

// Rejoue les calculs du XLSForm cites dans les consignes.
function calcule(nom) {
  if (ETIQ[nom]) {
    const tab = (LANG === 'en' && ETIQ_EN[nom]) ? ETIQ_EN[nom] : ETIQ[nom];
    return (R[nom] !== undefined && tab[R[nom]]) || '—';
  }
  const d = CALCULS[nom];
  if (!d) return '—';
  if (d.t === 'score') return scoreDe(d.cle);
  if (d.t === 'special') {
    if (nom === 'jour_semaine') {
      if (!R.date_evaluation) return '—';
      const j = new Date(R.date_evaluation + 'T00:00:00');
      return isNaN(j) ? '—' : t('jours').split(' ')[(j.getDay() + 6) % 7];
    }
    // Memes seuils que le formulaire : minuit sert de coupure, une heure hors
    // 07h-22h est rattachee a la tranche la plus proche.
    if (nom === 'tranche_horaire') {
      const h = Number(String(R.heure_debut || '').slice(0, 2));
      if (!R.heure_debut || isNaN(h)) return '—';
      return TRANCHES[h < 12 ? '1' : h < 18 ? '2' : '3'];
    }
    return '—';
  }
  if (d.t === 'table') {
    const cle = R[d.champ];
    const ligne = cle && TABLES[d.liste] && TABLES[d.liste][cle];
    return (ligne && ligne[d.col]) || '—';
  }
  for (const [champ, table] of d.c) {
    const v = R[champ];
    if (v !== undefined && table[v] !== undefined) return table[v];
  }
  return '—';
}

// Cascade generique heritee du JOB 001/26 : elle sert ici aux trois listes
// emboitees de la page 2, region -> departement -> ville.
function majFiltres() {
  document.querySelectorAll('.choix-liste[data-filtre]').forEach(l => {
    const champs = JSON.parse(l.dataset.filtre);
    const attendus = champs.map(c => R[c]);
    let visibles = 0;
    l.querySelectorAll('.choix').forEach(b => {
      // « * » : modalite qui echapperait au filtre (aucune aujourd'hui).
      const f = JSON.parse(b.dataset.f);
      const joker = f.every(x => x === '*');
      // La colonne peut lister plusieurs reponses (« 1 2 »), comme selected().
      const ok = attendus.every((v, i) => f[i] === '*'
        || (v !== undefined && String(f[i]).split(' ').includes(v)));
      b.hidden = !ok;
      if (ok && !joker) visibles++;      // le joker ne compte pas comme un choix
    });
    const vide = l.querySelector('.choix-vide');
    if (vide) vide.hidden = visibles > 0;
  });
}

function majCalculs() {
  document.querySelectorAll('.calc').forEach(s => {
    s.textContent = calcule(s.dataset.calc);
  });
}

function majRecap() {
  const corps = document.getElementById('recap-corps');
  const vide = document.getElementById('recap-vide');
  const lignes = [];
  document.querySelectorAll('.q[data-name]').forEach(q => {
    if (q.hidden || q.closest('.sous[hidden]')) return;
    const n = q.dataset.name, v = R[n];
    if (q.dataset.auto) {
      const d = calcule(n);
      if (d !== '—') {
        lignes.push('<tr><td class="mono">' + n.replace(/_/g, ' ') +
                    '</td><td>' + d + '</td></tr>');
      }
      return;
    }
    if (estVide(v)) return;
    const libelles = [].concat(v).map(x => {
      const b = q.querySelector('.choix[data-v="' + CSS.escape(x) + '"]');
      return b ? b.lastElementChild.textContent : x;
    }).join(' · ');
    const c = q.querySelector('.q-code');
    lignes.push('<tr><td class="mono">' + (c ? c.textContent : n) +
                '</td><td>' + libelles.replace(/[<>&]/g, ch =>
                  ({ '<': '&lt;', '>': '&gt;', '&': '&amp;' }[ch])) + '</td></tr>');
  });
  corps.innerHTML = lignes.join('');
  vide.hidden = lignes.length > 0;
}

function toast(msg) {
  const t = document.getElementById('toast');
  t.textContent = msg; t.classList.add('on');
  clearTimeout(t._h); t._h = setTimeout(() => t.classList.remove('on'), 2600);
}

// --- reponses
document.addEventListener('click', ev => {
  const b = ev.target.closest('.choix');
  if (!b) return;
  const q = b.closest('.q'), n = q.dataset.name;
  const multi = b.parentElement.dataset.multi === 'true';
  const v = b.dataset.v;
  if (multi) {
    const set = new Set([].concat(R[n] || []));
    set.has(v) ? set.delete(v) : set.add(v);
    R[n] = [...set];
    if (!R[n].length) delete R[n];
  } else {
    R[n] = (R[n] === v) ? undefined : v;      // reclic = deselection
    if (R[n] === undefined) delete R[n];
  }
  q.querySelectorAll('.choix').forEach(x => {
    const on = Array.isArray(R[n]) ? R[n].includes(x.dataset.v) : R[n] === x.dataset.v;
    x.setAttribute('aria-pressed', on ? 'true' : 'false');
  });
  sauver(); majEtat();
});

document.addEventListener('input', ev => {
  const s = ev.target.closest('.saisie');
  if (!s) return;
  const n = s.closest('.q').dataset.name;
  if (s.value === '') delete R[n]; else R[n] = s.value;
  sauver(); majEtat();
});

// --- navigation verrouillee
// Une etape incomplete OU mal remplie ne se quitte pas vers l'avant : le
// probleme est surligne et nomme ici, au moment ou l'enqueteur change de page,
// et non a la fin du questionnaire quand tout est a relire.
document.getElementById('suivant').addEventListener('click', () => {
  if (signalerEtape(ETAPES[etape], true)) return;
  if (etape === DERNIERE) { toast(t('complet')); return; }
  afficherEtape(etape + 1);
});

// Revenir en arriere reste toujours possible -- c'est souvent ce qu'il faut
// faire pour corriger --, mais l'etape quittee part surlignee et marquee dans
// le sommaire : on la retrouve sans l'avoir cherchee.
document.getElementById('precedent').addEventListener('click', () => {
  signalerEtape(ETAPES[etape], false);
  afficherEtape(etape - 1);
});

document.querySelectorAll('.rail a').forEach(a => a.addEventListener('click', ev => {
  ev.preventDefault();
  const n = Number(a.dataset.etape);
  if (n === etape) return;
  if (n > maxEtape) {
    toast(t('verrou'));
    return;
  }
  if (n > etape) {
    if (signalerEtape(ETAPES[etape], true)) return;
  } else {
    signalerEtape(ETAPES[etape], false);
  }
  afficherEtape(n);
}));

document.getElementById('raz').addEventListener('click', () => {
  if (!confirm(t('confirm_raz'))) return;
  R = {}; maxEtape = 0;
  document.querySelectorAll('.choix').forEach(b => b.setAttribute('aria-pressed', 'false'));
  document.querySelectorAll('.saisie').forEach(s => { s.value = ''; });
  document.querySelectorAll('.q.manque, .q.invalide').forEach(q =>
    q.classList.remove('manque', 'invalide'));
  afficherEtape(0); toast(t('efface'));
});

document.getElementById('copier').addEventListener('click', () => {
  const l = [t('entete_copie'), ''];
  document.querySelectorAll('.q[data-name]').forEach(q => {
    if (q.closest('.sous[hidden]')) return;
    if (!visible(q)) return;
    const n = q.dataset.name, v = R[n];
    if (estVide(v)) return;
    const t = [].concat(v).map(x => {
      const b = q.querySelector('.choix[data-v="' + CSS.escape(x) + '"]');
      return b ? b.lastElementChild.textContent : x;
    }).join(' · ');
    const c = q.querySelector('.q-code');
    l.push((c ? c.textContent : n) + ' : ' + t);
  });
  navigator.clipboard.writeText(l.join('\\n'))
    .then(() => toast(t('copie_ok')))
    .catch(() => toast(t('copie_ko')));
});

// --- restauration du brouillon
document.querySelectorAll('.q[data-name]').forEach(q => {
  const n = q.dataset.name, v = R[n];
  if (estVide(v)) return;
  q.querySelectorAll('.choix').forEach(b => {
    const on = Array.isArray(v) ? v.includes(b.dataset.v) : v === b.dataset.v;
    if (on) b.setAttribute('aria-pressed', 'true');
  });
  const s = q.querySelector('.saisie');
  if (s && !Array.isArray(v)) s.value = v;
});
// --- bascule FR / EN : chaque texte porte sa version anglaise en data-en
function appliquerLangue(l) {
  LANG = (l === 'en') ? 'en' : 'fr';
  document.documentElement.lang = LANG;
  document.querySelectorAll('[data-en]').forEach(el => {
    if (el.dataset.fr === undefined) el.dataset.fr = el.innerHTML;
    el.innerHTML = (LANG === 'en') ? el.dataset.en : el.dataset.fr;
  });
  document.querySelectorAll('[data-ph-en]').forEach(el => {
    if (el.dataset.phFr === undefined) el.dataset.phFr = el.placeholder;
    el.placeholder = (LANG === 'en') ? el.dataset.phEn : el.dataset.phFr;
  });
  const b = document.getElementById('langue');
  b.textContent = t('bouton_langue');
  b.title = t('titre_langue');
  b.setAttribute('aria-pressed', LANG === 'en' ? 'true' : 'false');
  try { localStorage.setItem(CLE_LANGUE, LANG); } catch (e) {}
  majEtat();
}

document.getElementById('langue').addEventListener('click', () => {
  appliquerLangue(LANG === 'en' ? 'fr' : 'en');
});

appliquerLangue(LANG);
afficherEtape(etape, false);
"""

# Tables passees au navigateur : chaines de if() des calculs et libelles des
# modalites citees dans les consignes.
I18N = {cle: list(paire) for cle, paire in traductions.JS_TEXTES.items()}

# Libelles des tranches horaires : le navigateur redit la meme chose que le
# `calculation` du formulaire, en lisant la meme liste de choix.
TRANCHES_JS = {c["name"]: c["label"] for c in CHOICES
               if c["list_name"] == "tranche_horaire"}

JS_TABLES = (f"const TRANCHES = {json.dumps(TRANCHES_JS, ensure_ascii=False)};\n"
             f"const NOTATION = {json.dumps(NOTATION, ensure_ascii=False)};\n"
             f"const CALCULS = {json.dumps(CALCULS, ensure_ascii=False)};\n"
             f"const TABLES = {json.dumps(TABLES, ensure_ascii=False)};\n"
             f"const ETIQ = {json.dumps(ETIQ_JS, ensure_ascii=False)};\n"
             f"const ETIQ_EN = {json.dumps(ETIQ_EN, ensure_ascii=False)};\n"
             f"const I18N = {json.dumps(I18N, ensure_ascii=False)};\n")

# Compteur de la barre de progression, dans les deux langues.
NOTE_CPT = ("sur {n} au total, conditionnelles comprises — une étape ne se "
            "quitte qu'une fois complète")
CPT_FR = ('<b id="faits">0</b> / <span id="vus">0</span> renseignées'
          f'<span class="cpt-note">{NOTE_CPT.replace("{n}", str(TOTAL))}</span>')
CPT_EN = (f'<b id="faits">0</b> / <span id="vus">0</span> {T("renseignées")}'
          f'<span class="cpt-note">{T(NOTE_CPT).replace("{n}", str(TOTAL))}</span>')

PIED_FR = """
      <p><strong>Périmètre de cette version.</strong> Toutes les sections du questionnaire
      papier de septembre 2026 sont couvertes : A à H, puis la synthèse qualitative. Le
score de chaque section et le score total sont <strong>calculés en arrière-plan</strong>
      avec le barème du PDF : <strong>aucun chiffre n'est montré à l'enquêteur</strong>,
      ni pendant la saisie ni à la dernière étape. Les scores partent avec la soumission
      et se lisent dans la base MDS. Un critère
      <em>non applicable</em>, ou masqué parce que la situation ne s'est pas produite,
      sort du calcul au lieu de compter zéro.</p>
      <p>Les <strong>données factuelles</strong> — attente, durée, mises en attente,
      transferts, renvoi — sont relevées à part et ne sont pas notées. Un critère
      <em>non conforme</em> ouvre un <strong>commentaire obligatoire</strong> ; c'est le
      seul endroit où il est demandé. Le jour de la semaine et la durée totale de l'appel sont
      <strong>déduits</strong> et ne sont pas saisis. <strong>Les scénarios restent à
      fournir par MDS</strong> : ils s'affichent « En attente du Scenario ». La version
      anglaise est une traduction de travail : en cas d'écart, le questionnaire français
      fait foi.</p>
"""

PIED_EN = """
      <p><strong>Scope of this version.</strong> Every section of the September 2026 paper
      questionnaire is covered: A to H, then the qualitative summary. The score for each
      section and the total score are <strong>calculated in the background</strong> using
      the scale in the PDF: <strong>no figure is ever shown to the auditor</strong>,
      neither while the form is filled in nor on the last step. The scores travel with
      the submission and are read in the MDS database. A criterion marked
      <em>not applicable</em>, or hidden because the situation did not arise, drops out of
      the calculation instead of counting as zero.</p>
      <p>The <strong>factual data</strong> — waiting time, length, holds, transfers,
      referral — are recorded separately and are not scored. A criterion marked
      <em>not compliant</em> opens a <strong>mandatory comment</strong>; that is the only
      place one is asked for. The day
      of the week and the total length of the call are <strong>derived</strong> and are not
      entered. <strong>The scenarios are still to be supplied by MDS</strong>: they show as
      “Scenario pending”. The English version is a working translation: in case of any
      discrepancy, the French questionnaire prevails.</p>
"""

PAGE = (
    "<title>Questionnaire GHOST Check Call Center</title>"
    + theme.POLICES
    + "<style>" + theme.TOKENS + theme.BASE_CSS + CSS + "</style>"
    + theme.bandeau(
        sp("Questionnaire GHOST Check Call Center"),
        sp("Fiche de collecte enquêteur — Orange · MTN"),
        [(sp("Questions"), str(TOTAL)), (sp("Étapes"), str(N_RECAP + 1)),
         (sp("Terrain"), sp("Septembre 2026"))])
    + """
<div class="progres">
  <div class="progres-in">
    <span class="compteur" """ + bi_html(CPT_FR, CPT_EN) + """>""" + CPT_FR + """</span>
    <div class="jauge" role="progressbar" aria-label="Progression du questionnaire"><span></span></div>
    <div class="actions">
      <button type="button" class="btn btn-lang" id="langue" aria-pressed="false"
              title="Afficher le questionnaire en anglais">English</button>
      <button type="button" class="btn" id="raz" """ + bi("Réinitialiser", txt) + """>Réinitialiser</button>
      <button type="button" class="btn btn-1" id="copier" """ + bi("Copier les réponses", txt) + """>Copier les réponses</button>
    </div>
  </div>
</div>

<div class="wrap">
  <nav class="rail" aria-label="Étapes">
    """ + sp("Étapes", "h4") + """
    <ul>""" + "".join(index) + """</ul>
  </nav>

  <main>
    """ + "".join(corps) + """

    <section class="section bloc" id="recap" data-etape=\"""" + str(N_RECAP) + """\" hidden>
      """ + sp("Récapitulatif des réponses", "h2") + """
      <p class="recap-vide" id="recap-vide" """ + bi("Aucune réponse saisie pour le moment.", txt) + """>Aucune réponse saisie pour le moment.</p>
      <table id="recap-table"><tbody id="recap-corps"></tbody></table>
    </section>

    <div class="nav-bas">
      <button type="button" class="btn" id="precedent" """ + bi("← Précédent", txt) + """>← Précédent</button>
      <span class="nav-etape">""" + sp("Étape") + """ <b id="etape-n">1</b> / """ + str(N_RECAP + 1) + """</span>
      <button type="button" class="btn btn-1" id="suivant">Suivant →</button>
      <p class="nav-alerte" id="nav-alerte"></p>
    </div>

    <footer""" + bi_html(PIED_FR, PIED_EN) + """>""" + PIED_FR + """</footer>
  </main>
</div>

<div class="toast" id="toast" role="status"></div>
<script>""" + JS_TABLES + JS + """</script>
""")

if CONTRAINTES_INCONNUES:
    print(f"  ATTENTION : {len(CONTRAINTES_INCONNUES)} contrainte(s) du "
          f"formulaire ne sont pas rejouées dans la page — la saisie ne les "
          f"signalera pas :")
    for _nom, _expr in CONTRAINTES_INCONNUES:
        print(f"    - {_nom} : {_expr}")

SORTIE.write_text(PAGE, encoding="utf-8")
print(f"OK : {SORTIE.name} ({TOTAL} questions, {N_RECAP + 1} étapes, "
      f"{len(PAGE)//1024} Ko)")
