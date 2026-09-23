#!/usr/bin/env python3
"""Referentiel geographique du questionnaire : region, departement, ville.

Source : le fichier des agences MDS (colonnes REGION_ADMINISTRATIVE, VILLE,
DEPPARTEMENT). Ce questionnaire ne visite aucune agence -- il situe
L'ENQUETEUR pendant l'appel -- mais il reprend le meme referentiel, pour que
les deux collectes se croisent sans table de passage.

  /!\\ LISTE PARTIELLE, A COMPLETER PAR MDS. Elle a ete relevee sur des
  captures du fichier agences, triees par VILLE et coupees avant KOUSSERI :
  tout ce qui precede alphabetiquement manque, DOUALA et GAROUA en tete. Pour
  la completer, ajouter les lignes manquantes ci-dessous puis relancer
  `python build_form.py` -- rien d'autre n'est a toucher.

L'ORTHOGRAPHE EST CELLE DU FICHIER MDS, y compris « MFOUDI » (l'orthographe
officielle est « MFOUNDI ») : les deux collectes doivent exporter la meme
chaine. A trancher avec MDS.

Les trois listes sont EMBOITEES : une ville appartient a un departement, qui
appartient a une region. Le questionnaire les enchaine par `choice_filter`,
l'enqueteur ne voit donc que les departements de sa region et que les villes de
son departement.
"""

# (code, libelle)
REGIONS = [
    ("adamaoua", "ADAMAOUA"),
    ("centre", "CENTRE"),
    ("extreme_nord", "EXTREME-NORD"),
    ("nord_ouest", "NORD-OUEST"),
    ("ouest", "OUEST"),
    ("sud", "SUD"),
    ("sud_ouest", "SUD-OUEST"),
]

# (code, libelle, code de la region)
DEPARTEMENTS = [
    ("vina", "VINA", "adamaoua"),
    ("mfoudi", "MFOUDI", "centre"),
    ("diamare", "DIAMARE", "extreme_nord"),
    ("logone_et_chari", "LOGONE ET CHARI", "extreme_nord"),
    ("mezam", "MEZAM", "nord_ouest"),
    ("bamboutos", "BAMBOUTOS", "ouest"),
    ("ocean", "OCEAN", "sud"),
    ("fako", "FAKO", "sud_ouest"),
    ("meme", "MEME", "sud_ouest"),
]

# (code, libelle, code du departement)
VILLES = [
    ("ngaoundere", "NGAOUNDERE", "vina"),
    ("yaounde", "YAOUNDÉ", "mfoudi"),
    ("maroua", "MAROUA", "diamare"),
    ("kousseri", "KOUSSERI", "logone_et_chari"),
    ("bamenda", "BAMENDA", "mezam"),
    ("mbouda", "MBOUDA", "bamboutos"),
    ("kribi", "KRIBI", "ocean"),
    ("limbe", "LIMBE", "fako"),
    ("tiko", "TIKO", "fako"),
    ("kumba", "KUMBA", "meme"),
]

# Tous les libelles : ils servent aux controles de traduction de build_form.py.
LIBELLES = ([l for _c, l in REGIONS]
            + [l for _c, l, _p in DEPARTEMENTS]
            + [l for _c, l, _p in VILLES])


def controle():
    """Verifie que chaque rattachement pointe sur un code existant."""
    regions = {c for c, _l in REGIONS}
    departements = {c for c, _l, _p in DEPARTEMENTS}
    for code, libelle, parent in DEPARTEMENTS:
        assert parent in regions, f"{libelle} : region inconnue {parent!r}"
    for code, libelle, parent in VILLES:
        assert parent in departements, f"{libelle} : departement inconnu {parent!r}"
    orphelins = departements - {p for _c, _l, p in VILLES}
    return sorted(orphelins)


if __name__ == "__main__":
    orphelins = controle()
    print(f"{len(REGIONS)} régions · {len(DEPARTEMENTS)} départements · "
          f"{len(VILLES)} villes")
    if orphelins:
        print("  départements sans ville : " + ", ".join(orphelins))
