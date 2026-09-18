"""Verifie les scores calcules par le formulaire, sans passer par Kobo.

    python test_scores.py        # sort en code 1 si un cas ne passe pas

Mini-evaluateur du sous-ensemble XPath produit par build_form.py : il rejoue les
expressions de la colonne `calculation` sur des reponses fabriquees et compare
le resultat a ce qu'on attend.

if() est evalue PARESSEUSEMENT, comme le font JavaRosa (KoboCollect) et Enketo :
seule la branche retenue est calculee. C'est ce qui protege
`if(den = 0, '', round(100 * num div den))` de la division par zero.

Une question masquee par son `relevant` est representee par une reponse ABSENTE
du dictionnaire : c'est exactement ce que produit ODK, qui vide un champ des
qu'il cesse d'etre pertinent.
"""
import json
import re
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent

JET = re.compile(r"""\s*(?:
      (?P<var>\$\{\w+\})
    | (?P<num>\d+(?:\.\d+)?)
    | (?P<str>'[^']*')
    | (?P<mot>decimal-time|if|round|div|and|or)
    | (?P<op><=|>=|!=|<|>|[=+\-*(),])
)""", re.X)


def lexer(s):
    i, out = 0, []
    while i < len(s):
        m = JET.match(s, i)
        if not m:
            if s[i].isspace():
                i += 1
                continue
            raise SyntaxError(f"caractere inattendu {s[i]!r} en {i}")
        i = m.end()
        out.append(next(v for v in m.groups() if v is not None))
    return out + [None]


class Parseur:
    """Produit un arbre ; l'evaluation est faite ensuite, a la demande."""

    def __init__(self, toks):
        self.t, self.i = toks, 0

    def pic(self):
        return self.t[self.i]

    def av(self, attendu=None):
        j = self.t[self.i]
        if attendu and j != attendu:
            raise SyntaxError(f"attendu {attendu!r}, trouve {j!r}")
        self.i += 1
        return j

    def primaire(self):
        j = self.pic()
        if j == "if":
            self.av(); self.av("(")
            c = self.expr(); self.av(",")
            a = self.expr(); self.av(",")
            b = self.expr(); self.av(")")
            return ("if", c, a, b)
        if j in ("round", "decimal-time"):
            f = self.av(); self.av("(")
            v = self.expr(); self.av(")")
            return (f, v)
        if j == "(":
            self.av()
            v = self.expr(); self.av(")")
            return v
        if j.startswith("${"):
            return ("var", self.av()[2:-1])
        if j.startswith("'"):
            return ("lit", self.av()[1:-1])
        return ("lit", self.av())

    def mul(self):
        g = self.primaire()
        while self.pic() in ("div", "*"):
            g = (self.av(), g, self.primaire())
        return g

    def add(self):
        g = self.mul()
        while self.pic() in ("+", "-"):
            g = (self.av(), g, self.mul())
        return g

    def cmp(self):
        g = self.add()
        if self.pic() in ("=", "!=", "<=", ">=", "<", ">"):
            g = (self.av(), g, self.add())
        return g

    def et(self):
        g = self.cmp()
        while self.pic() == "and":
            g = (self.av(), g, self.cmp())
        return g

    def expr(self):
        """Niveau le plus bas : `or` lie moins fort que `and`, comme en XPath."""
        g = self.et()
        while self.pic() == "or":
            g = (self.av(), g, self.et())
        return g


def nombre(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def texte(x):
    """Rend un resultat arithmetique comme le fait JavaRosa : 265, pas 265.0."""
    return str(int(x)) if float(x).is_integer() else str(x)


RE_HEURE = re.compile(r"(\d{1,2}):(\d{2})(?::(\d{2}))?")


def heure_decimale(v):
    """decimal-time() : la portion de journee ecoulee, comme JavaRosa.

    Une heure absente ou illisible donne NaN, et toute comparaison avec NaN est
    fausse -- le meme comportement qu'en XPath. Les expressions du formulaire
    ecartent le cas vide avant d'appeler la fonction, `if()` etant paresseux.
    """
    m = RE_HEURE.match(str(v))
    if not m:
        return float("nan")
    h, mi, se = int(m.group(1)), int(m.group(2)), int(m.group(3) or 0)
    return (h * 3600 + mi * 60 + se) / 86400


def evalue_noeud(n, V):
    k = n[0]
    if k == "lit":
        return n[1]
    if k == "var":
        return V.get(n[1], "")
    if k == "if":                                   # <- paresseux
        return evalue_noeud(n[2] if evalue_noeud(n[1], V) else n[3], V)
    if k == "round":
        return str(int(float(evalue_noeud(n[1], V)) + 0.5))
    if k == "decimal-time":
        return texte(heure_decimale(evalue_noeud(n[1], V)))
    if k in ("and", "or"):                          # <- paresseux aussi
        g = bool(evalue_noeud(n[1], V))
        if k == "and":
            return g and bool(evalue_noeud(n[2], V))
        return g or bool(evalue_noeud(n[2], V))
    g, d = evalue_noeud(n[1], V), evalue_noeud(n[2], V)
    if k in ("+", "-", "*", "div"):
        a, b = float(g), float(d)
        return texte({"+": a + b, "-": a - b, "*": a * b,
                      "div": (a / b if b else float("inf"))}[k])
    ng, nd = nombre(g), nombre(d)
    if ng is not None and nd is not None:
        g, d = ng, nd
    return {"=": g == d, "!=": g != d, "<=": g <= d, ">=": g >= d,
            "<": g < d, ">": g > d}[k]


def ev(expr, V):
    return evalue_noeud(Parseur(lexer(expr)).expr(), V)


D = json.loads((RACINE / "form_structure.json").read_text(encoding="utf-8"))
CALC = {r["name"]: r["calculation"] for r in D["survey"] if r.get("calculation")}
NOTEES = [n for s in D["notation"].values() for n, _ in s["questions"]]

# Les 22 criteres A->H sont poses a chaque appel ; les 106 criteres de la
# section I ne le sont que pour le scenario joue -- un appel n'en voit jamais
# plus de cinq. Les fixtures « tous les criteres a X » portent donc sur les
# seuls A->H, et la section I se remplit scenario par scenario.
NOTEES_AH = [n for cle, s in D["notation"].items() if cle != "I"
             for n, _ in s["questions"]]
CRITERES_SC = {}
for _n, _ in D["notation"]["I"]["questions"]:
    CRITERES_SC.setdefault(_n.split("_")[0], []).append(_n)

# Le jour de la semaine repose sur decimal-date-time() et mod : hors du
# sous-ensemble XPath que ce mini-evaluateur couvre, et sans bareme a verifier.
# La tranche horaire, elle, est verifiee : voir les cas de bornes plus bas.
NON_EVALUES = {"jour_semaine"}


def evalue(V):
    """Rejoue tous les champs calcules, dans l'ordre du formulaire."""
    V = dict(V)
    for nom, expr in CALC.items():
        if nom in NON_EVALUES:
            continue
        V[nom] = ev(expr, V)
    return V


def cas(titre, V, attendus):
    r = evalue(V)
    ok = all(str(r.get(k, "")) == str(v) for k, v in attendus.items())
    print(("  OK   " if ok else "ECHEC  ") + titre)
    for k, v in attendus.items():
        marque = "" if str(r.get(k, "")) == str(v) else "   <-- ATTENDU " + str(v)
        print(f"         {k} = {r.get(k, '')!r}{marque}")
    return ok


CENT = {n: "100" for n in NOTEES_AH}
ZERO = {n: "0" for n in NOTEES_AH}
MOITIE = {n: "50" for n in NOTEES_AH}


def scenario(code, *notes):
    """Reponses aux criteres du scenario joue ; les autres restent absents."""
    noms = CRITERES_SC[code]
    assert len(notes) == len(noms), (
        f"{code} porte {len(noms)} critere(s), {len(notes)} fourni(s)")
    return dict(zip(noms, notes))

print("=== SCORES CALCULES PAR LE FORMULAIRE ===\n")
tous = []

tous.append(cas(
    "Appel parfait : les 22 criteres a 100, escalade et renvoi survenus",
    CENT,
    {"SCORE_A": "100", "SCORE_E": "100", "SCORE_F": "100",
     "SCORE_TOTAL": "100"}))

tous.append(cas(
    "Appel non conforme : les 22 criteres a 0",
    ZERO,
    {"SCORE_A": "0", "SCORE_E": "0", "SCORE_TOTAL": "0"}))

tous.append(cas(
    "Conformite partielle : les 22 criteres a 50",
    MOITIE,
    {"SCORE_A": "50", "SCORE_H": "50", "SCORE_TOTAL": "50"}))

tous.append(cas(
    "Section A notee 100 / 50 / 0 : (100 + 50 + 0) / 300",
    {"Q1": "100", "Q2": "50", "Q3": "0"},
    {"SCORE_A": "50"}))

tous.append(cas(
    "N/A sort du denominateur : Q2 = N/A, A ne porte que sur Q1 et Q3",
    {**CENT, "Q2": "na", "Q3": "0"},
    {"SCORE_A": "50"}))

tous.append(cas(
    "Section entierement N/A : le score reste vide, pas de division par zero",
    {**CENT, "Q19": "na", "Q20": "na"},
    {"SCORE_G": "", "SCORE_A": "100"}))

tous.append(cas(
    "Q15 masquee (ni escalade ni renvoi) : E porte sur Q12, Q13, Q14 et Q16",
    {**{k: v for k, v in CENT.items() if k != "Q15"}, "Q16": "0"},
    {"SCORE_E": "75"}))          # 300 / 400

tous.append(cas(
    "Q18 masquee (aucune attente, aucun transfert) : F ne porte que sur Q17",
    {**{k: v for k, v in CENT.items() if k != "Q18"}, "Q17": "50"},
    {"SCORE_F": "50"}))

tous.append(cas(
    "Arrondi : deux criteres a 100 et un a 50 -> round(100 * 250 / 300)",
    {"Q1": "100", "Q2": "100", "Q3": "50"},
    {"SCORE_A": "83"}))

tous.append(cas(
    "Formulaire vierge : scores vides, aucune division par zero",
    {},
    {"SCORE_A": "", "SCORE_E": "", "SCORE_TOTAL": ""}))

tous.append(cas(
    "Section A seule remplie : les autres scores restent vides",
    {"Q1": "100", "Q2": "50", "Q3": "na"},
    {"SCORE_A": "75", "SCORE_B": "", "SCORE_TOTAL": "75"}))

# --- section I : les criteres du scenario joue comptent avec les autres
tous.append(cas(
    "S01 joue, ses 5 criteres a 0 : ils pesent dans le score total "
    "(2200 / 2700)",
    {**CENT, **scenario("S01", "0", "0", "0", "0", "0")},
    {"SCORE_TOTAL": "81", "SCORE_I": "0", "SCORE_A": "100"}))

tous.append(cas(
    "S18 n'a que 3 criteres : le denominateur suit (2200 / 2500)",
    {**CENT, **scenario("S18", "0", "0", "0")},
    {"SCORE_TOTAL": "88", "SCORE_I": "0"}))

tous.append(cas(
    "Les criteres des 24 autres scenarios sont masques : ils ne comptent pas",
    {**CENT, **scenario("S01", "100", "100", "100", "100", "100")},
    {"SCORE_TOTAL": "100", "SCORE_I": "100"}))

tous.append(cas(
    "N/A sur un critere de scenario : il sort des deux sommes (S18 -> 2 sur 3)",
    {**CENT, **scenario("S18", "100", "na", "0")},
    {"SCORE_I": "50", "SCORE_TOTAL": "96"}))   # 2300 / 2400, le N/A hors des deux

tous.append(cas(
    "Aucun scenario joue : la section I reste vide, le total ne bouge pas",
    CENT,
    {"SCORE_I": "", "SCORE_TOTAL": "100"}))

# La duree de l'appel est desormais saisie EN SECONDES, comme toutes les autres
# durees du questionnaire. TEMPS_TOTAL, la variable du JOB 001/26, reste la
# seule valeur en minutes : elle s'en deduit.
tous.append(cas(
    "Duree saisie en secondes : 265 s -> TEMPS_TOTAL de 4 minutes",
    {"duree_appel": "265"},
    {"temps_total": "4"}))

tous.append(cas(
    "270 s : arrondi a 5 minutes (round() XPath, la demie monte)",
    {"duree_appel": "270"},
    {"temps_total": "5"}))

tous.append(cas(
    "Duree non saisie : le temps total reste vide",
    {},
    {"temps_total": ""}))

# TRANCHE HORAIRE. Deduite de l'heure de debut, donc plus saisie. Les bornes du
# PDF sont 07h / 12h / 18h / 22h, mais les tranches ne couvrent pas la nuit :
# une heure hors plage est rattachee a la tranche la plus proche, minuit servant
# de coupure. Ce sont les bornes qui se trompent en silence : on les teste une
# par une.
for _h, _attendu, _titre in [
        ("07:00:00", "1", "07h00 pile : premiere tranche"),
        ("11:59:00", "1", "11h59 : encore la premiere"),
        ("12:00:00", "2", "12h00 pile : bascule sur la deuxieme"),
        ("17:59:00", "2", "17h59 : encore la deuxieme"),
        ("18:00:00", "3", "18h00 pile : bascule sur la troisieme"),
        ("21:59:00", "3", "21h59 : encore la troisieme"),
        ("06:40:00", "1", "06h40, avant 07h : rattachee a la premiere"),
        ("23:10:00", "3", "23h10, apres 22h : rattachee a la troisieme"),
        ("00:05:00", "1", "00h05 : minuit sert de coupure, premiere tranche")]:
    tous.append(cas(f"Tranche horaire — {_titre}",
                    {"heure_debut": _h}, {"tranche_horaire": _attendu}))

tous.append(cas(
    "Heure de debut non saisie : la tranche reste vide",
    {},
    {"tranche_horaire": ""}))

print(f"\n{sum(tous)}/{len(tous)} cas conformes")
sys.exit(0 if all(tous) else 1)
