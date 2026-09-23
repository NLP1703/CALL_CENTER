#!/usr/bin/env python3
"""Genere le XLSForm du QUESTIONNAIRE GHOST CHECK CALL CENTER (MDS JOB 002/26).

Questionnaire de reference : PDF MDS v1.0 « Questionnaire GHOST Check CALL
CENTER » de septembre 2026 (7 pages, sections A a H puis synthese qualitative).

Regles de construction :
  1. Le formulaire est pagine (settings.style = pages, groupes field-list) : on
     ne passe pas a la page suivante sans avoir rempli la precedente.
  2. Les DONNEES FACTUELLES (temps d'attente, duree, mises en attente,
     transferts, renvoi) sont collectees dans une page a part, SANS score : la
     consigne du PDF les separe explicitement du score comportemental.
  3. Les 23 criteres scores prennent la meme echelle -- totalement conforme,
     partiellement conforme, non conforme, non applicable -- mais LE BAREME NE
     S'AFFICHE JAMAIS A L'ENQUETEUR : ni le chiffre dans la modalite, ni le
     score de section pendant la saisie. Il note ce qu'il a entendu ; le
     formulaire convertit en arriere-plan et ne montre le score de l'appel
     qu'a la derniere page. « Non applicable » sort du numerateur COMME du
     denominateur.
  4. TOUT 0 EST QUALIFIE PUIS ETAYE. Un 0 est une alerte critique : le
     formulaire fait NOMMER le cas qu'il revele -- l'un des cas de la liste de
     sa section, la question etant obligatoire et n'offrant aucune sortie --,
     PUIS le commentaire obligatoire -- un fait observe ou la formulation
     exacte du conseiller. On qualifie avant de decrire. Les deux champs
     n'apparaissent que lorsque la reponse est 0.
  5. LOGIQUE CONDITIONNELLE. Escalade, renvoi en agence / autre canal, mise en
     attente et transferts ne sont renseignes que si l'evenement s'est produit ;
     les questions non applicables sont masquees automatiquement (`relevant`),
     et une question masquee sort du calcul du score.
  6. ALERTES CRITIQUES hors score. Les cas nommes a signaler obligatoirement
     se cochent SUR LE CRITERE QUI LES REVELE, et nulle part ailleurs
     (regle 4) : il n'y a plus de page dediee en fin de questionnaire, elle
     faisait ressaisir ce qui etait deja saisi. Aucun cas n'entre dans le
     calcul : une alerte doit remonter meme quand le score global de l'appel
     reste eleve.

Sortie : questionnaire_audit_call_center.xlsx + form_structure.json
"""
import json
import re
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill

import criteres_scenario
import localites
import traductions

SORTIE = Path(__file__).resolve().parent / "questionnaire_audit_call_center.xlsx"

# Formulaire bilingue : KoboCollect et Enketo affichent alors un selecteur de
# langue. Les libelles anglais viennent de traductions.py.
LANG_FR = "Français (fr)"
LANG_EN = "English (en)"
TRADUITES = ("label", "hint", "constraint_message")
# Le media n'est pas du texte, mais un formulaire bilingue doit le declarer dans
# chaque langue : sans cela pyxform ajoute une langue « default » au selecteur.
IDENTIQUES = ("media::image",)


def col_langues(nom):
    return [f"{nom}::{LANG_FR}", f"{nom}::{LANG_EN}"]


COLONNES = (["type", "name"] + col_langues("label") + col_langues("hint")
            + ["required", "relevant", "constraint"]
            + col_langues("constraint_message")
            + ["appearance", "calculation", "choice_filter", "readonly"]
            + col_langues("media::image"))
# Colonnes de la feuille choices : `points` porte le bareme du PDF (100 / 50 /
# 0). Vide = modalite hors score (« Non applicable »).
# `region` et `departement` rattachent une modalite a celle du niveau au-dessus :
# c'est ce que lisent les `choice_filter` des listes emboitees (voir page 2).
COL_CHOIX = ["list_name", "name"] + col_langues("label") + ["points",
                                                            "region",
                                                            "departement"]

survey = []
choices = []

# Toutes les questions sont obligatoires -- l'alerte et le commentaire d'un
# score de 0 y compris, mais ils ne s'affichent que lorsque le 0 est coche.
# Aucune exception depuis le retrait de l'enregistrement de l'appel. Une
# question peut a la place poser elle-meme son `required` : une EXPRESSION,
# quand l'obligation depend d'une reponse et non de la question. La boucle de
# fin ne l'ecrase pas.
OPTIONNELLES = set()


def q(type_, name, label, hint="", required="", relevant="", constraint="",
      constraint_message="", appearance="", calculation="", choice_filter="",
      readonly="", media=""):
    survey.append({"type": type_, "name": name, "label": label, "hint": hint,
                   "required": required, "relevant": relevant,
                   "constraint": constraint, "constraint_message": constraint_message,
                   "appearance": appearance, "calculation": calculation,
                   "choice_filter": choice_filter, "readonly": readonly,
                   "media::image": media})


def deduit(type_, name, label, calculation, hint=""):
    """Champ non saisi : calcule par le formulaire, affiche et exporte."""
    q(type_, name, label, hint=hint, calculation=calculation, readonly="yes")


def groupe(name, label, relevant="", appearance="field-list"):
    q("begin_group", name, label, relevant=relevant, appearance=appearance)


def fin_groupe():
    q("end_group", "", "")


def liste(nom, items):
    """items : (name, label) ou (name, label, points)."""
    for it in items:
        choices.append({"list_name": nom, "name": it[0], "label": it[1],
                        "points": "" if len(it) < 3 or it[2] is None else it[2]})


def liste_emboitee(nom, items, colonne):
    """Liste filtree par le niveau au-dessus : items = (name, label, parent)."""
    for code, libelle, parent in items:
        choices.append({"list_name": nom, "name": code, "label": libelle,
                        "points": "", colonne: parent})


def si_num(champ, paires, defaut="0"):
    """if() XPath imbriques renvoyant un NOMBRE : (code, valeur) -> expression."""
    expr = defaut
    for code, val in reversed(paires):
        expr = f"if(${{{champ}}} = '{code}', {val}, {expr})"
    return expr


# =====================================================================
# LISTES DE CHOIX ET BAREME
# =====================================================================
# Les points voyagent dans la colonne `points` de la feuille choices ET dans
# BAREME, qui sert a construire les calculs de score et alimente le guide
# enqueteur comme le tableau de bord : le bareme n'est ecrit qu'une fois.
BAREME = {}


def liste_notee(nom, items):
    """Liste dont les modalites portent des points ; None = hors score."""
    liste(nom, items)
    BAREME[nom] = {it[0]: (it[2] if len(it) > 2 else None) for it in items}


# L'ECHELLE DU QUESTIONNAIRE. Elle est unique : les 23 criteres scores la
# partagent, ce qui rend les sections directement comparables entre elles.
# « Non applicable » ne vaut pas zero : la modalite n'a pas de points et sort du
# denominateur (consigne du PDF : N/A seulement si le critere n'a reellement pas
# pu etre observe).
#
# LE LIBELLE NE PORTE PLUS SA VALEUR. Le code (« 100 », « 50 »...) et la colonne
# `points` ne bougent pas -- l'export et le calcul sont inchanges -- mais
# l'enqueteur ne lit plus « (100) » au bout de la modalite : un chiffre affiche
# au moment de cocher invite a viser un total plutot qu'a decrire ce qui a ete
# entendu. Le bareme reste lisible par le tableau de bord et le site de suivi,
# qui le lisent dans `points`.
liste_notee("conformite", [
    ("100", "Oui, totalement conforme", 100),
    ("50", "Partiellement conforme / perfectible", 50),
    ("0", "Non conforme", 0),
    ("na", "Non applicable", None)])

# Oui / Non des questions d'aiguillage : elles ne sont pas notees, ce sont des
# declencheurs de logique conditionnelle, pas des points de controle.
liste("oui_non", [("1", "Oui"), ("2", "Non")])

# LE RENVOI SE COCHE SUR UNE LISTE, PLUS SUR DEUX OUI / NON.
# « Aucun renvoi » est une modalite de la liste, et non l'absence de reponse :
# la question reste obligatoire des qu'elle s'affiche, et le cas « pas de
# renvoi » se lit dans la base au lieu de s'y deviner. Agence et point de vente
# sont distingues : ils n'ont ni le meme maillage ni la meme lecture a l'analyse.
liste("renvoi", [
    ("0", "Aucun renvoi"),
    ("1", "Vers un autre canal (application, USSD, site, réseaux sociaux)"),
    ("2", "Vers une agence"),
    ("3", "Vers un point de vente physique")])

liste("langue", [("fr", "Français"), ("en", "Anglais")])

# REFERENTIEL GEOGRAPHIQUE, repris du fichier des agences MDS (localites.py).
# Les trois listes sont emboitees : le `choice_filter` de la page 2 ne montre
# que les departements de la region cochee, puis que les villes de ce
# departement. La liste est partielle et attend d'etre completee par MDS --
# voir l'avertissement en tete de localites.py.
liste("region", localites.REGIONS)
liste_emboitee("departement", localites.DEPARTEMENTS, "region")
liste_emboitee("ville", localites.VILLES, "departement")

# Test ou live : les interviews de test sont ecartees a l'analyse, on ne les
# reconnait plus a posteriori. Consigne MDS reprise du JOB 001/26.
liste("type_interview", [("test", "TEST - Interview non valide"),
                         ("live", "Live - Interview valide")])

# Le questionnaire de septembre 2026 ne liste plus que deux operateurs :
# Camtel, present dans la version precedente, en a disparu. A CONFIRMER PAR MDS.
RESEAUX = [("orange", "ORANGE"), ("mtn", "MTN")]
liste("reseau", RESEAUX)

# Tranches horaires du PDF de septembre 2026 (07h-12h / 12h-18h / 18h-22h).
# La modalite n'est plus cochee : elle est DEDUITE de l'heure de debut (page 2).
liste("tranche_horaire", [("1", "07h - 12h"), ("2", "12h - 18h"),
                          ("3", "18h - 22h")])

# Les 25 scenarios de reference de l'annexe MDS (« LISTE DES SCENARII GHOST
# CHECK CALL », septembre 2026). Le libelle ne porte QUE les trois colonnes
# utiles a la selection -- code, famille, scenario. La formulation client
# mystere et l'objectif de test restent dans l'annexe : ils se lisent avant
# l'appel, pas dans une liste deroulante.
SCENARIOS = [
    ("S01", "S01 · Data / Réseau · Internet mobile très lent"),
    ("S02", "S02 · Data / Forfait · Forfait acheté mais navigation impossible"),
    ("S03", "S03 · Voix / Réseau · Appels qui coupent / voix dégradée"),
    ("S04", "S04 · Data / Facturation · Forfait consommé trop rapidement"),
    ("S05", "S05 · Crédit / Facturation · Débit inexpliqué du crédit"),
    ("S06", "S06 · VAS · Souscription / débit VAS non souhaité"),
    ("S07", "S07 · Forfait / Achat · Impossible d'acheter un forfait"),
    ("S08", "S08 · Digital · Application opérateur inaccessible"),
    ("S09", "S09 · Conseil / Vente · Choix du meilleur forfait"),
    ("S10", "S10 · Conseil / Offre · Changement d'offre"),
    ("S11", "S11 · SIM / Sécurité · SIM bloquée / PIN-PUK"),
    ("S12", "S12 · SIM / Sécurité · SIM perdue ou volée"),
    ("S13", "S13 · KYC · Problème d'identification de la ligne"),
    ("S14", "S14 · Réclamation · Réclamation récurrente non résolue"),
    ("S15", "S15 · Relationnel · Client mécontent et impatient"),
    ("S16", "S16 · Tarification · Information tarifaire simple"),
    ("S17", "S17 · Roaming · Préparation d'un voyage"),
    ("S18", "S18 · Transfert / Partage · Transfert de crédit ou de data"),
    ("S19", "S19 · Mobile Money · Transaction débitée mais non reçue"),
    ("S20", "S20 · Mobile Money · Envoi au mauvais numéro"),
    ("S21", "S21 · Cycle de vie SIM · Réactivation d'une ligne inactive"),
    ("S22", "S22 · Réseau · Qualité réseau dans une localité précise"),
    ("S23", "S23 · Pédagogie · Client ne comprend pas les instructions"),
    ("S24", "S24 · Inclusion digitale · Client peu à l'aise avec le digital"),
    ("S25", "S25 · Orientation / Réclamation · Demande hors périmètre du conseiller"),
]
liste("scenario", SCENARIOS)

# ALERTES CRITIQUES. Cinq cas nommes a signaler obligatoirement, cochables
# ensemble : une alerte n'est pas une note, elle fait l'objet d'une analyse
# separee et ne depend pas du score. La liste reste fermee sur les cas nommes du
# document : un manquement qui n'y entre pas se decrit dans le commentaire.
#
# ELLE NE SE PROPOSE QU'EN FACE D'UN 0 (`alertes_nc`, voir `critere`). Un 0 doit
# nommer le cas d'alerte qu'il revele ; la question etant obligatoire,
# l'enqueteur en coche forcement un. La liste ne porte donc QUE DES CAS :
# « Aucune alerte critique » ouvrirait une sortie a une question qui n'en veut
# pas. La page dediee qui la posait a tous les appels a ete supprimee -- elle
# rouvrait cette sortie et dupliquait une saisie deja faite sur le critere.
CAS_ALERTES = [
    ("confidentialite",
     "Violation ou exposition de données personnelles / défaut manifeste de "
     "confidentialité"),
    ("info_erronee",
     "Information manifestement erronée susceptible d'entraîner une perte "
     "financière ou un préjudice client"),
    ("irrespect",
     "Propos irrespectueux, agressifs, discriminatoires ou attitude "
     "manifestement non professionnelle"),
    ("promesse",
     "Promesse de délai / de traitement non maîtrisée ou engagement trompeur"),
    ("abandon",
     "Transfert, renvoi en agence ou abandon de prise en charge manifestement "
     "non justifié")]
liste("alertes_nc", CAS_ALERTES)

# ALERTES CRITIQUES PROPRES A LA SECTION A. L'accessibilite et le serveur vocal
# se jouent avant toute prise de ligne : les cinq cas generaux sont tous des
# faits du conseiller et aucun n'y est observable, tandis que les defaillances
# qui s'y signalent -- accueil trompeur, menu mort, boucle sans sortie -- n'ont
# d'equivalent nulle part ailleurs dans le questionnaire. La section a donc sa
# propre liste, cochable sur ses seuls criteres non conformes. Elle ne se
# propose donc jamais qu'en face d'un 0 : « Aucune alerte critique » n'y figure
# pas plus que dans `alertes_nc`.
liste("alertes_a", [
    ("accueil_incoherent",
     "Message d'accueil incohérent ou trompeur, ne correspondant pas aux "
     "services réellement proposés"),
    ("menus_errones",
     "Menus du serveur vocal erronés ou non fonctionnels, entraînant une "
     "mauvaise orientation ou une impossibilité d'accès au conseiller"),
    ("langue_indisponible",
     "Absence ou dysfonctionnement du choix de langue, créant une barrière de "
     "communication pour le client"),
    ("boucle_ivr",
     "Boucle IVR bloquante ou confusion dans le parcours, empêchant le client "
     "d'obtenir une assistance humaine"),
    ("coupure_redirection",
     "Erreur de redirection ou coupure systématique avant mise en relation, "
     "générant une rupture de service"),
    ("attente_non_signalee",
     "Temps d'attente excessif non signalé, ou absence de message "
     "d'information pendant la mise en relation")])




# ALERTES CRITIQUES PROPRES A LA DIMENSION C (comprehension du besoin). Le PDF
# v1.2 nomme six manquements a l'ecoute et a la qualification du besoin. Ils
# S'AJOUTENT aux cinq cas generaux au lieu de les remplacer : contrairement a la
# section A, un conseiller est en ligne et les cinq cas generaux y sont tous
# observables. La section n'a qu'une liste, le document ne detaillant pas par
# critere.
CAS_C = [
    ("interruption",
     "Interruption répétée ou inappropriée du client, empêchant l'expression "
     "complète du besoin"),
    ("sans_ecoute",
     "Absence totale d'écoute active : le conseiller ne manifeste aucun intérêt "
     "ou ne tient pas compte des propos du client"),
    ("questions_hors_sujet",
     "Questions non pertinentes ou hors sujet, traduisant une mauvaise "
     "qualification du problème"),
    ("sans_reformulation",
     "Absence de reformulation ou de validation, entraînant une mauvaise "
     "compréhension du motif d'appel"),
    ("besoin_mal_compris",
     "Erreur manifeste d'interprétation du besoin, conduisant à une réponse ou "
     "une action inadaptée"),
    ("demande_ignoree",
     "Demande du client ignorée ou détournée, sans justification ni "
     "orientation vers une solution appropriée")]
liste("alertes_c", CAS_ALERTES + CAS_C)

# ALERTES CRITIQUES PROPRES A LA DIMENSION D (expertise & exactitude). Le PDF
# v1.2 les donne CRITERE PAR CRITERE -- trois cas pour Q9, trois pour Q10, trois
# pour Q11 -- et non par section : chaque critere a donc sa liste, toujours
# ajoutee aux cinq cas generaux.
CAS_Q9 = [
    ("offre_fausse",
     "Information fausse ou incohérente sur une offre ou un service"),
    ("procedure_mal_expliquee",
     "Procédure mal expliquée, entraînant une mauvaise orientation du client"),
    ("promesse_irrealiste",
     "Promesse non maîtrisée : délai irréaliste ou engagement impossible à "
     "tenir")]
CAS_Q10 = [
    ("reponse_contradictoire",
     "Réponse contradictoire par rapport aux procédures officielles"),
    ("erreur_manifeste",
     "Erreur manifeste dans les informations fournies (tarifs, conditions, "
     "délais)"),
    ("engagement_trompeur",
     "Engagement trompeur pouvant induire le client en erreur")]
CAS_Q11 = [
    ("explication_confuse",
     "Explication confuse ou trop technique, incompréhensible pour le client"),
    ("sans_etapes",
     "Absence d'étapes ou d'alternatives claires pour résoudre le problème"),
    ("jargon",
     "Langage inadapté : jargon interne, termes non vulgarisés")]
liste("alertes_q9", CAS_ALERTES + CAS_Q9)
liste("alertes_q10", CAS_ALERTES + CAS_Q10)
liste("alertes_q11", CAS_ALERTES + CAS_Q11)

# =====================================================================
# CALCUL DES SCORES
# =====================================================================
# Chaque critere apporte 0, 50 ou 100 points au numerateur et 100 au
# denominateur DES QU'IL EST RENSEIGNE. Un critere masque par un `relevant`
# (escalade non survenue, aucune mise en attente...) ou note « Non applicable »
# sort des deux : le score porte sur ce qui s'appliquait reellement a l'appel.
NOTATION = {}


def notees(cle, titre, questions):
    """Declare les questions notees d'une section. `questions` : noms internes."""
    NOTATION[cle] = {"titre": titre, "questions": questions}


def _table(nom):
    """Bareme de la question, lu depuis la liste de choix qu'elle utilise."""
    for ligne in survey:
        if ligne["name"] == nom and ligne["type"].startswith("select"):
            return BAREME[ligne["type"].split()[1]]
    return None


def _termes(noms):
    """(numerateur, denominateur) XPath pour une liste de questions notees."""
    num, den = [], []
    for nom in noms:
        table = _table(nom)
        gagnants = [(c, p) for c, p in table.items() if p]
        notables = [(c, 100) for c, p in table.items() if p is not None]
        num.append(si_num(nom, gagnants))
        den.append(si_num(nom, notables))
    return " + ".join(num), " + ".join(den)


def score(nom, label, noms, hint="", affiche=False):
    """Champ de score : pourcentage des points obtenus sur les points en jeu.

    AUCUN SCORE NE S'AFFICHE DANS LE QUESTIONNAIRE, total compris : un chiffre
    calcule sous les yeux de l'enqueteur est un biais -- il voit sa moyenne
    monter ou descendre et ajuste la note suivante. Les champs restent des
    `calculate` : ils sont calcules et exportes comme avant, ils ne se montrent
    nulle part. Le score se lit dans la base et sur le tableau de bord.
    `affiche` reste disponible pour un besoin futur ; plus aucun appel ne
    l'active.
    """
    num, den = _termes(noms)
    calcul = f"if(({den}) = 0, '', round(100 * ({num}) div ({den})))"
    if affiche:
        deduit("integer", nom, label, calcul, hint=hint)
    else:
        q("calculate", nom, label, calculation=calcul)


# Un score de 0 est une situation exceptionnelle ou une alerte critique : le PDF
# impose de l'etayer. Les champs sont les memes pour tous les criteres -- un seul
# libelle, une seule traduction -- et n'apparaissent que sur un 0.
#
# ORDRE VOULU : l'alerte d'abord, le commentaire ensuite. L'enqueteur qualifie
# le constat -- quel cas a signaler obligatoirement revele-t-il ? -- avant de le
# decrire ; la description qu'il redige ensuite sait alors ce qu'elle doit
# etablir.
#
# LA QUESTION N'A PAS DE SORTIE. Elle ne demande plus SI le constat est une
# alerte mais LEQUEL il revele : la liste n'offre que des cas, et la question
# etant obligatoire, un 0 en nomme forcement un.
LIBELLE_ALERTE = (
    "Non conforme — quel cas d'alerte critique ce constat révèle-t-il ?"
)
HINT_ALERTE = (
    "À renseigner avant le commentaire. Cochez le ou les cas que ce constat "
    "révèle. La liste est fermée : ce qu'aucun cas ne couvre se décrit dans le "
    "commentaire, juste en dessous."
)
LIBELLE_COMMENTAIRE = (
    "Non conforme — décrivez le fait observé ou rapportez la formulation "
    "exacte du conseiller."
)
HINT_COMMENTAIRE = (
    "Obligatoire pour toute non-conformité. Un fait, une phrase entendue : "
    "pas une appréciation générale."
)
def critere(nom, label, relevant="", alertes="alertes_nc"):
    """Critere note, son alerte critique puis son commentaire, sur un 0 seul.

    La condition des deux champs se contente de `= '0'` : une question masquee
    par son propre `relevant` est videe par ODK comme par le guide, l'alerte et
    le commentaire disparaissent donc avec elle sans avoir a repeter la
    condition.

    `alertes` nomme la liste de cas proposee. Par defaut les cinq cas generaux,
    valables partout ou un conseiller est en ligne ; la section A, jouee avant
    toute prise de ligne, passe la sienne (voir `alertes_a`). Ni l'une ni
    l'autre ne porte « Aucune alerte critique » : il n'y a donc pas de
    contrainte d'exclusivite a poser ici.
    """
    q("select_one conformite", nom, label, relevant=relevant)
    q(f"select_multiple {alertes}", f"{nom}_alerte", LIBELLE_ALERTE,
      hint=HINT_ALERTE, relevant=f"${{{nom}}} = '0'")
    q("text", f"{nom}_com", LIBELLE_COMMENTAIRE, hint=HINT_COMMENTAIRE,
      relevant=f"${{{nom}}} = '0'", appearance="multiline")


# =====================================================================
# PAGE 1 — CONSIGNES GENERALES POUR L'ENQUETEUR
# =====================================================================
groupe("grp_consignes", "Consignes générales pour l'enquêteur")
q("note", "note_lecture",
  "**À LIRE AVANT DE COMMENCER.**",
  media="mds_logo.png")
q("note", "note_principes",
  "**1. COMMENT REMPLIR**\n\n"
  "• **Un seul scénario par appel.** Le questionnaire est renseigné "
  "immédiatement après avoir raccroché.\n"
  "• Commencez par la page **« Mesures »** : le formulaire ouvre ensuite les "
  "seules questions qui concernent cet appel. **Une question qui ne s'affiche "
  "pas n'est pas à renseigner.**\n"
  "• Chaque critère a quatre réponses : **totalement conforme**, "
  "**partiellement conforme**, **non conforme**, **non applicable**.\n"
  "• Un **non conforme** ouvre deux champs : le **cas d'alerte critique** que "
  "le constat révèle, puis le **commentaire obligatoire**. Qualifiez d'abord, "
  "décrivez ensuite.\n"
  "• Vous n'avez **rien à calculer** : vous décrivez ce que vous avez "
  "entendu.\n"
  "• Ne **révélez jamais** que vous êtes enquêteur.")
q("note", "note_calibrage",
  "**2. COMMENT QUALIFIER**\n\n"
  "• Notez ce que vous avez **réellement observé et entendu** pendant l'appel, "
  "pas ce que le conseiller aurait pu faire en dehors du scénario.\n"
  "• **Non applicable** : seulement si le critère n'a pas pu être observé ou "
  "ne s'appliquait pas à cet appel. Ce n'est pas un « non conforme ».\n"
  "• **Partiellement conforme** : une conformité réelle mais incomplète — "
  "réponse correcte mais partielle, personnalisation mécanique, explication à "
  "moitié claire, prise en charge partielle.\n"
  "• **Non conforme** : toujours étayé par un **fait observé** ou la "
  "**formulation exacte** du conseiller, jamais par une appréciation "
  "générale.\n"
  "• **FCR** : le client obtient dès cet appel la résolution ou une prise en "
  "charge complète et fiable, sans nouvel effort à fournir — même si une "
  "opération reste à finir en back-office.")
q("select_one type_interview", "type_interview", "Type d'interview",
  hint="TEST tant que la collecte n'est pas ouverte ; Live pour un appel réel",
  appearance="horizontal-compact")
fin_groupe()

# =====================================================================
# PAGE 2 — IDENTIFICATION DE L'ENQUETEUR
# =====================================================================
groupe("grp_identification", "Identification de l'enquêteur")
q("text", "nom_enqueteur", "Nom enquêteur")
# OU SE TROUVE L'ENQUETEUR PENDANT L'APPEL -- pas le client joue, pas une
# agence : le questionnaire n'en visite aucune. Les trois listes s'enchainent,
# chacune filtree par la precedente, si bien qu'un choix incoherent (une ville
# hors de son departement) est impossible a cocher.
q("select_one region", "region", "Région administrative",
  hint="Là où vous vous trouvez pendant l'appel.")
q("select_one departement", "departement", "Département",
  hint="Seuls les départements de la région cochée s'affichent.",
  choice_filter="region=${region}")
q("select_one ville", "ville", "Ville",
  hint="Seules les villes du département coché s'affichent.",
  choice_filter="departement=${departement}")
q("select_one reseau", "reseau", "Opérateur", appearance="horizontal-compact")
q("date", "date_evaluation", "Date",
  constraint=". <= today()",
  constraint_message="La date ne peut pas être dans le futur.")
# Jour de la semaine : deduit de la date. 1970-01-01 etant un jeudi, l'index
# (jours + 3) mod 7 vaut 0 pour Lun ... 6 pour Dim. round() absorbe les decalages
# de fuseau horaire selon les clients.
JOUR_IDX = "((round(decimal-date-time(${date_evaluation})) + 3) mod 7)"
deduit("text", "jour_semaine", "Jour",
       "if(${date_evaluation} = '', '', "
       + "".join(f"if({JOUR_IDX} = {i}, '{j}', "
                 for i, j in enumerate(["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam",
                                        "Dim"]))
       + "''" + ")" * 7 + ")")
q("time", "heure_debut", "Heure début",
  hint="La tranche horaire en est déduite : rien à cocher plus bas.")
# « Heure fin » est posee sur la DERNIERE page : avec l'heure de debut, elle
# borne la duree de l'evaluation -- la cible de completion post-appel du PDF,
# « mediane <= 5 minutes ». La duree de l'APPEL, elle, est relevee a part page
# « Mesures », en minutes et secondes.
q("select_one langue", "langue_enqueteur", "Langue",
  appearance="horizontal-compact")
q("text", "identification_conseiller", "Identification conseiller",
  hint="Nom donné par le conseiller, ou matricule s'il en a communiqué un")
# TRANCHE HORAIRE. Deduite de l'heure de debut, plus choisie : l'enqueteur l'a
# saisie quelques lignes plus haut, la redemander n'ajoute rien et ouvre un
# ecart entre deux champs qui doivent dire la meme chose. Les bornes du PDF
# (07h / 12h / 18h / 22h) ne couvrent pas la nuit : une heure hors plage est
# rattachee a la tranche la plus proche -- avant 07h a la premiere, apres 22h a
# la derniere -- plutot que de laisser le champ vide. Les trois seuils se
# reduisent donc a deux comparaisons, minuit servant de coupure.
# `select_one` + `calculation`, et non le `deduit()` texte de `jour_semaine` :
# l'enqueteur lit « 12h - 18h » tandis que l'export garde le code 1 / 2 / 3
# attendu par le tableau de bord et par la table de correspondance MDS.
HEURE_DEBUT_H = "decimal-time(${heure_debut}) * 24"
q("select_one tranche_horaire", "tranche_horaire", "Tranche horaire",
  hint="Déduite de l'heure de début : rien à cocher.",
  calculation="if(${heure_debut} = '', '', "
              f"if({HEURE_DEBUT_H} < 12, '1', "
              f"if({HEURE_DEBUT_H} < 18, '2', '3')))",
  readonly="yes", appearance="horizontal-compact")
fin_groupe()

# =====================================================================
# PAGE 3 — MESURES : LES DONNEES FACTUELLES DE L'APPEL
# =====================================================================
# Le PDF collecte ces valeurs SEPAREMENT du score comportemental : aucune n'est
# notee. Elles commandent en revanche la logique conditionnelle des sections E
# et F -- d'ou leur place avant les criteres.
groupe("grp_mesures", "Mesures — valeurs observées")
q("note", "note_mesures",
  "Valeurs relevées **chronomètre en main**, immédiatement après l'appel. "
  "Elles ne sont pas notées : elles décrivent l'appel et commandent les "
  "questions conditionnelles qui suivent.\n\n"
  "**Toutes les durées se saisissent en secondes**, sans exception.")
q("integer", "attente_conseiller", "Temps d'attente avant conseiller",
  hint="En secondes, du décroché du serveur vocal à la prise de ligne du conseiller",
  constraint=". >= 0 and . <= 3600",
  constraint_message="Indiquez une durée comprise entre 0 et 3600 secondes.")
# Toutes les durees du questionnaire sont en SECONDES, sans exception :
# l'attente avant conseiller, la duree de l'appel, le cumul des mises en
# attente. Une seule unite, un seul champ par mesure, aucune conversion a faire
# au depouillement. Le PDF collecte la duree au format « ___ min ___ sec » ;
# l'enqueteur convertit sa lecture de chronometre une fois, ici.
q("integer", "duree_appel", "Durée totale de l'appel",
  hint="En secondes, de la prise de ligne du conseiller au raccroché "
       "(3 min 45 s = 225)",
  constraint=". >= 0 and . <= 10800",
  constraint_message="Indiquez une durée comprise entre 0 et 10800 secondes.")
# Exporte sous TEMPS_TOTAL, en minutes : c'est la variable du JOB 001/26, elle
# permet d'empiler les deux collectes. Non affichee, elle se deduit de la duree.
q("calculate", "temps_total",
  "Temps total en minutes passé en ligne avec le conseiller",
  calculation="if(${duree_appel} = '', '', round(${duree_appel} div 60))")
q("integer", "nb_attentes", "Nombre de mises en attente",
  hint="0 s'il n'y a eu aucune mise en attente",
  constraint=". >= 0 and . <= 20",
  constraint_message="Indiquez un nombre compris entre 0 et 20.")
q("integer", "duree_attentes", "Durée cumulée des mises en attente",
  hint="En secondes, toutes mises en attente additionnées",
  relevant="${nb_attentes} > 0",
  constraint=". >= 0 and . <= 3600",
  constraint_message="Indiquez une durée comprise entre 0 et 3600 secondes.")
q("integer", "nb_transferts", "Nombre de transferts",
  hint="0 si l'appel n'a jamais été transféré",
  constraint=". >= 0 and . <= 10",
  constraint_message="Indiquez un nombre compris entre 0 et 10.")
# LE RENVOI SE SAISIT SUR UNE SEULE LISTE, ET APRES UN TRANSFERT SEULEMENT.
#
# Une liste, quatre modalites : « autre canal » et « agence » ont d'abord ete
# reunis dans une question oui / non -- la base sortait un RENVOI a 1 sans dire
# si le client avait ete envoye sur l'application ou en boutique -- puis scindes
# en deux cases oui / non. L'enqueteur y cochait deux « Non » pour dire qu'il
# n'y avait pas eu de renvoi du tout. Une liste unique enonce les destinations
# et met « Aucun renvoi » parmi elles : une question, une reponse, une colonne.
# Agence et point de vente y sont distingues, ce que les deux cases ne
# disaient pas.
#
# A NOTER -- le choix etant unique, un appel qui porte deux destinations
# (« faites-le sur l'appli, sinon passez en agence ») ne peut en declarer
# qu'une ; `renvoi_precision` reste le seul endroit ou la seconde se lit.
# Arbitrage assume, a rouvrir en select_multiple si le pilote montre des
# renvois doubles frequents.
#
# Apres un transfert seulement (`nb_transferts > 0`) : consigne MDS. A NOTER --
# un renvoi sans transfert devient inexprimable, alors qu'il se produit (le
# conseiller repond lui-meme puis oriente vers l'agence) ; la premiere
# soumission de la collecte est exactement ce cas. Arbitrage assume, a rouvrir
# si les donnees montrent des renvois manquants.
q("select_one renvoi", "renvoi",
  "Renvoi : le conseiller a-t-il orienté le client ailleurs qu'au téléphone ?",
  hint="Une seule destination : celle vers laquelle le client a été orienté. "
       "« Aucun renvoi » si le conseiller n'a invité le client ni à poursuivre "
       "sur un canal numérique ni à se déplacer.",
  relevant="${nb_transferts} > 0")
# Les trois destinations sont enumerees plutot qu'ecrites « different de 0 » :
# un renvoi masque -- appel sans transfert -- laisse le champ VIDE, et un vide
# est lui aussi different de '0'. Enumerer ferme la question dans les deux cas.
q("text", "renvoi_precision", "Préciser le canal, l'agence ou le point de vente "
  "indiqués",
  relevant="${renvoi} = '1' or ${renvoi} = '2' or ${renvoi} = '3'")
# Ajout : le PDF conditionne Q15 a « une escalade ou un renvoi en agence » sans
# jamais poser la question qui declenche le premier cas. Aiguillage non note.
#
# Posee apres un transfert seulement, comme le renvoi : consigne MDS. La
# page « Mesures » se lit donc ainsi -- le nombre de transferts commande tout ce
# qui le suit. A NOTER : les deux declencheurs de Q15 etant desormais derriere
# la meme condition, Q15 NE S'OUVRE PLUS SANS TRANSFERT, et sort du score sur
# tout appel non transfere -- la section E y porte sur 4 criteres au lieu de 5.
# Une escalade sans transfert se produit pourtant (« je transmets au service
# technique, on vous rappelle sous 48 h », l'appel n'ayant ete passe a
# personne) : une des cinq soumissions de la collecte est exactement ce cas.
# Arbitrage assume, a rouvrir si le pilote montre des escalades manquantes.
q("select_one oui_non", "escalade",
  "Escalade : le dossier a-t-il été transmis à un autre service ou un rappel "
  "a-t-il été promis ?",
  hint="Question d'aiguillage : avec le renvoi, elle commande la question Q15",
  relevant="${nb_transferts} > 0", appearance="horizontal-compact")
fin_groupe()

# =====================================================================
# PAGE 4 — SCENARIO JOUE
# =====================================================================
# Place juste avant les criteres notes : le scenario conditionne la lecture de
# toute la suite (« le score mesure la performance par operateur ET par
# scenario »), et l'enqueteur le confirme au moment d'attaquer la notation.
groupe("grp_scenario", "Scénario joué")
q("note", "note_scenario",
  "**Un seul scénario par appel.** Le script sert de **déclencheur** : ne "
  "surjouez pas, et ne fournissez pas spontanément d'informations qui ne vous "
  "sont pas demandées.\n\n"
  "**Scénarios sensibles (SIM, KYC, Mobile Money) :** n'utilisez que des lignes "
  "et des comptes de test autorisés. **Aucune transaction réelle**, aucune "
  "exposition de données personnelles sans protocole validé.\n\n"
  "S15, S23 et S24 peuvent aussi être joués comme **variantes relationnelles** "
  "appliquées à un scénario fonctionnel (désescalade, pédagogie, inclusion). Le "
  "formulaire n'enregistre qu'un seul code : cocher celui qui décrit le mieux "
  "l'appel.")
q("select_one scenario", "scenario_joue", "Scénario",
  hint="Code, famille et intitulé du scénario réellement joué pendant cet appel",
  appearance="minimal")
fin_groupe()

# =====================================================================
# PAGE 5 — A. ACCESSIBILITE & SERVEUR VOCAL
# =====================================================================
groupe("grp_a", "A. ACCESSIBILITÉ & SERVEUR VOCAL")
# Les trois criteres de la section portent la liste d'alertes du serveur vocal,
# et sont les seuls : ces cas ne se constatent pas ailleurs.
critere("Q1",
        "Q1 Le message d'accueil et les menus du serveur vocal vous ont-ils "
        "semblé clairs, compréhensibles et cohérents avec les services "
        "annoncés ?", alertes="alertes_a")
critere("Q2",
        "Q2 Le choix de langue vous a-t-il été proposé et a-t-il fonctionné "
        "correctement lorsqu'il était applicable à votre parcours d'appel ?",
        alertes="alertes_a")
critere("Q3",
        "Q3 L'accès à un conseiller vous a-t-il semblé simple et fluide, sans "
        "erreur, ni boucle inutile ni confusion dans le parcours IVR ?",
        alertes="alertes_a")
notees("A", "Accessibilité & serveur vocal", ["Q1", "Q2", "Q3"])
score("SCORE_A", "Score — Accessibilité & serveur vocal",
      NOTATION["A"]["questions"])
fin_groupe()

# =====================================================================
# PAGE 6 — B. ACCUEIL & POSTURE DU CONSEILLER
# =====================================================================
groupe("grp_b", "B. ACCUEIL & POSTURE DU CONSEILLER")
critere("Q4",
        "Q4 Le conseiller vous a-t-il accueilli et s'est-il présenté de "
        "manière claire et professionnelle ?")
critere("Q5",
        "Q5 Le ton du conseiller vous a-t-il semblé courtois, agréable et "
        "disponible, avec une personnalisation naturelle et appropriée de "
        "l'échange, sans sur-scriptage ?")
notees("B", "Accueil & posture du conseiller", ["Q4", "Q5"])
score("SCORE_B", "Score — Accueil & posture du conseiller",
      NOTATION["B"]["questions"])
fin_groupe()

# =====================================================================
# PAGE 7 — C. COMPREHENSION DU BESOIN
# =====================================================================
groupe("grp_c", "C. COMPRÉHENSION DU BESOIN")
# Les trois criteres de la section ajoutent aux cinq cas generaux les six
# manquements a l'ecoute nommes par le PDF v1.2.
critere("Q6",
        "Q6 Le conseiller vous a-t-il écouté attentivement et vous a-t-il "
        "laissé exposer votre besoin sans interruption inappropriée ?",
        alertes="alertes_c")
critere("Q7",
        "Q7 Le conseiller a-t-il posé des questions pertinentes pour qualifier "
        "votre problème et obtenir uniquement les informations réellement "
        "nécessaires ?", alertes="alertes_c")
critere("Q8",
        "Q8 Le conseiller a-t-il reformulé ou validé sa compréhension lorsque "
        "cela était utile, en évitant que vous répétiez inutilement des "
        "informations déjà données ?", alertes="alertes_c")
notees("C", "Compréhension du besoin", ["Q6", "Q7", "Q8"])
score("SCORE_C", "Score — Compréhension du besoin",
      NOTATION["C"]["questions"])
fin_groupe()

# =====================================================================
# PAGE 8 — D. EXPERTISE & EXACTITUDE DE LA REPONSE
# =====================================================================
groupe("grp_d", "D. EXPERTISE & EXACTITUDE DE LA RÉPONSE")
# Seule section dont le PDF v1.2 detaille les cas CRITERE PAR CRITERE : chacun
# porte donc sa propre liste, cinq cas generaux plus les trois qui le visent.
critere("Q9",
        "Q9 Le conseiller a-t-il démontré une bonne maîtrise des offres, "
        "services, procédures et parcours liés au scénario testé ?",
        alertes="alertes_q9")
critere("Q10",
        "Q10 La réponse fournie par le conseiller était-elle correcte, "
        "précise, cohérente et exempte d'informations contradictoires ou "
        "manifestement erronées ?", alertes="alertes_q10")
critere("Q11",
        "Q11 Les explications données vous ont-elles semblé simples, "
        "pédagogiques et adaptées, avec des étapes ou alternatives clairement "
        "présentées ?", alertes="alertes_q11")
notees("D", "Expertise & exactitude de la réponse", ["Q9", "Q10", "Q11"])
score("SCORE_D", "Score — Expertise & exactitude de la réponse",
      NOTATION["D"]["questions"])
fin_groupe()

# =====================================================================
# PAGE 9 — E. RESOLUTION / FCR & OWNERSHIP
# =====================================================================
groupe("grp_e", "E. RÉSOLUTION / FCR & OWNERSHIP")
critere("Q12",
        "Q12 La réponse apportée par le conseiller était-elle concrète, "
        "exploitable et vous a-t-elle permis d'avancer immédiatement vers la "
        "résolution de votre besoin ?")
critere("Q13",
        "Q13 Votre besoin a-t-il été résolu dès le premier contact ou, lorsque "
        "la résolution immédiate était impossible, la meilleure solution "
        "accessible au Call Center a-t-elle été effectivement mise en œuvre ?")
critere("Q14",
        "Q14 Le conseiller a-t-il pris ownership de votre demande, en évitant "
        "les transferts, renvois ou abandons de prise en charge non justifiés ?")
# Conditionnelle : le PDF ne la pose qu'« en cas d'escalade ou de renvoi en
# agence ». Les deux cas sont releves page 3 ; sans eux, la question est masquee
# et sort du score.
#
# Ses deux declencheurs -- escalade et renvoi -- ne sont eux-memes poses que si
# l'appel a ete transfere : Q15 ne peut donc plus s'ouvrir sur un appel sans
# transfert, ou la section E porte sur 4 criteres au lieu de 5. La condition
# reste ecrite en clair plutot que ramenee a `nb_transferts > 0` : un appel
# transfere sans escalade ni renvoi n'a pas non plus d'objet pour Q15. Cote
# renvoi les trois destinations sont enumerees : « Aucun renvoi » (0) est une
# reponse et non un vide, et une condition tout en OU reste lisible par le
# guide, dont le traducteur d'expressions ne melange pas les ET et les OU.
critere("Q15",
        "Q15 En cas d'escalade ou de renvoi en agence, le motif, les prochaines "
        "étapes, les pièces éventuelles et le délai annoncé vous ont-ils semblé "
        "clairs et réalistes ?",
        relevant="${escalade} = '1' or ${renvoi} = '1' "
                 "or ${renvoi} = '2' or ${renvoi} = '3'")
critere("Q16",
        "Q16 Avant de clôturer l'appel, le conseiller a-t-il vérifié que la "
        "solution ou la suite du traitement était bien comprise et, en cas de "
        "non-résolution, vous a-t-il rassuré sans faire de promesse non "
        "maîtrisée ?")
notees("E", "Résolution / FCR & ownership", ["Q12", "Q13", "Q14", "Q15", "Q16"])
score("SCORE_E", "Score — Résolution / FCR & ownership",
      NOTATION["E"]["questions"])
fin_groupe()

# =====================================================================
# PAGE 10 — F. EFFORT CLIENT & SIMPLICITE
# =====================================================================
groupe("grp_f", "F. EFFORT CLIENT & SIMPLICITÉ")
critere("Q17",
        "Q17 Le nombre d'étapes, d'informations demandées et de manipulations "
        "imposées au client vous a-t-il semblé limité au strict nécessaire ?")
# Conditionnelle : sans mise en attente et sans transfert, la question n'a pas
# d'objet. Le renvoi n'a plus a figurer dans la condition -- il ne se saisit que
# sur un appel transfere, `nb_transferts > 0` le couvre donc deja.
critere("Q18",
        "Q18 Les mises en attente, transferts et changements de canal ont-ils "
        "été minimisés et, lorsqu'ils étaient nécessaires, expliqués et "
        "justifiés de manière claire ?",
        relevant="${nb_attentes} > 0 or ${nb_transferts} > 0")
notees("F", "Effort client & simplicité", ["Q17", "Q18"])
score("SCORE_F", "Score — Effort client & simplicité",
      NOTATION["F"]["questions"])
fin_groupe()

# =====================================================================
# PAGE 11 — G. EMPATHIE & CONFIANCE
# =====================================================================
groupe("grp_g", "G. EMPATHIE & CONFIANCE")
critere("Q19",
        "Q19 Le conseiller a-t-il reconnu de façon appropriée l'inconfort, "
        "l'urgence ou l'émotion que vous avez exprimés, notamment en situation "
        "de réclamation ?")
critere("Q20",
        "Q20 L'attitude du conseiller, la transparence de ses explications et "
        "le respect de la confidentialité vous ont-ils inspiré confiance et "
        "professionnalisme ?")
notees("G", "Empathie & confiance", ["Q19", "Q20"])
score("SCORE_G", "Score — Empathie & confiance", NOTATION["G"]["questions"])
fin_groupe()

# =====================================================================
# PAGE 12 — H. CLOTURE DE L'ENTRETIEN
# =====================================================================
groupe("grp_h", "H. CLÔTURE DE L'ENTRETIEN")
critere("Q21",
        "Q21 Le conseiller a-t-il récapitulé brièvement la solution ou les "
        "prochaines étapes, en vérifiant qu'aucun point essentiel ne restait "
        "en suspens ?")
critere("Q22",
        "Q22 La prise de congé du conseiller vous a-t-elle semblé courtoise, "
        "naturelle et professionnelle (remerciement ou souhait adapté), sans "
        "exigence artificielle de répétition de votre nom ?")
# Ajoute par le PDF v1.2. Il prend le numero Q23, qui revenait a la synthese
# qualitative : celle-ci se decale en Q24 / Q25 / Q26 pour que les numeros
# suivent l'ordre du questionnaire, comme partout ailleurs.
critere("Q23",
        "Q23 Le conseiller a-t-il informé le client qu'il recevra un sondage "
        "de satisfaction afin de partager son avis ?")
notees("H", "Clôture de l'entretien", ["Q21", "Q22", "Q23"])
score("SCORE_H", "Score — Clôture de l'entretien", NOTATION["H"]["questions"])
fin_groupe()

# =====================================================================
# PAGE 13 — I. MAITRISE DU SCENARIO
# =====================================================================
# Les criteres de l'annexe MDS « Scenarios finaux », un sous-groupe par
# scenario, chacun conditionne au scenario joue : l'enqueteur ne voit que les
# 3 a 5 criteres de son appel, les 101 autres sont masques et sortent du
# numerateur comme du denominateur -- meme mecanique que Q15 ou Q18.
#
# La section est declaree comme les huit autres (`notees`) : ses criteres
# entrent donc dans SCORE_TOTAL au meme titre que Q1 a Q23. Un appel est ainsi
# note sur 23 criteres de comportement PLUS les 3 a 5 actes que son scenario
# appelait.
groupe("grp_i", "I. MAÎTRISE DU SCÉNARIO")
q("note", "note_criteres_scenario",
  "Ces critères portent sur le **traitement technique du scénario que vous avez "
  "joué** : ce que le conseiller a effectivement vérifié, expliqué ou fait.\n\n"
  "Seuls ceux du scénario coché en page « Scénario joué » s'affichent, et ils "
  "se remplissent **comme les sections A à H**.")
CRITERES_I = []
for _code, _libelle_scenario in SCENARIOS:
    groupe(f"grp_{_code.lower()}", _libelle_scenario,
           relevant=f"${{scenario_joue}} = '{_code}'", appearance="")
    for _rang, (_intitule, _question) in enumerate(
            criteres_scenario.CRITERES[_code], start=1):
        _nom = criteres_scenario.nom(_code, _rang)
        critere(_nom, criteres_scenario.libelle(_code, _rang, _intitule,
                                                _question))
        CRITERES_I.append(_nom)
    fin_groupe()
notees("I", "Maîtrise du scénario", CRITERES_I)
score("SCORE_I", "Score — Maîtrise du scénario", NOTATION["I"]["questions"])
fin_groupe()

# =====================================================================
# PAGE 14 — SYNTHESE QUALITATIVE
# =====================================================================
groupe("grp_synthese", "Synthèse qualitative")
# Q24 a Q26 : anciennement Q23 a Q25, decalees par l'arrivee du critere Q23 en
# section H. Voir le README, « Renumerotation de la synthese ».
q("text", "Q24", "Q24 Quel est le principal point fort de cet appel ?",
  hint="Un fait précis, pas une appréciation générale.", appearance="multiline")
q("text", "Q25",
  "Q25 Quel est le principal irritant ou effort subi par le client ?",
  hint="Ce qui a coûté du temps, une répétition ou une inquiétude au client.",
  appearance="multiline")
q("select_one oui_non", "Q26",
  "Q26 Le client devrait-il rappeler ou contacter un autre canal pour le même "
  "motif ?", appearance="horizontal-compact")
# Le « pourquoi » ne se pose que sur un OUI : si le client n'a pas a rappeler,
# il n'y a rien a expliquer. Sans cette condition le champ s'affichait toujours
# et forcait une justification de l'absence de probleme.
q("text", "Q26_txt", "Q26 Pourquoi ?",
  hint="Ce qui reste à faire, et par quel canal le client devrait le faire.",
  relevant="${Q26} = '1'", appearance="multiline")
fin_groupe()

# =====================================================================
# PAGE 15 — FIN DE L'EVALUATION
# =====================================================================
TOUTES_NOTEES = [n for s in NOTATION.values() for n in s["questions"]]

groupe("grp_score", "Fin de l'évaluation")
q("time", "heure_fin", "Heure fin",
  constraint="decimal-time(.) > decimal-time(${heure_debut})",
  constraint_message="L'heure de fin doit être postérieure à l'heure de début.")
q("note", "note_fin",
  "**C'est terminé.** Vérifiez les questions marquées en rouge, puis "
  "enregistrez et envoyez le formulaire.")
# AUCUN SCORE N'EST MONTRE A L'ENQUETEUR. SCORE_TOTAL reste un `calculate` :
# il est calcule et exporte comme les scores de section, il ne s'affiche
# simplement nulle part dans le questionnaire. Le chiffre se lit dans la base et
# sur le tableau de bord, pas pendant la saisie -- un enqueteur qui voit son
# total monter ou descendre ajuste la note suivante.
score("SCORE_TOTAL", "Score total de l'appel", TOUTES_NOTEES)
fin_groupe()


# OBLIGATOIRE PAR DEFAUT
# =====================================================================
for _l in survey:
    if (_l["type"] in ("note", "calculate") or _l["type"].startswith(("begin_", "end_"))
            or _l.get("readonly") == "yes"):
        continue
    if _l["required"]:
        continue      # obligation conditionnelle posee a la main : on la garde
    _l["required"] = "" if _l["name"] in OPTIONNELLES else "yes"


# =====================================================================
# NOMS DE VARIABLES A L'EXPORT
# =====================================================================
# Le JOB 002/26 n'a pas encore de table de correspondance MDS. Les noms
# d'identification sont repris de celle du JOB 001/26 (audit des agences), ou ils
# figurent noir sur blanc ; tout le reste suit ses conventions et reste A VALIDER.
NOMS_MDS = {
    "nom_enqueteur": "NOM_ENQ",
    "date_evaluation": "DATE_INTERVIEW",
    "reseau": "OPERATEUR",
    # Noms des colonnes du fichier des agences MDS, a ceci pres que son en-tete
    # ecrit « DEPPARTEMENT » : la faute de frappe n'est pas reprise.
    "region": "REGION_ADMINISTRATIVE",
    "departement": "DEPARTEMENT",
    "ville": "VILLE",
    "scenario_joue": "SCENARIO",
    "type_interview": "TYPE_INTERVIEW",
    "heure_debut": "HEURE_DEBUT",
    "heure_fin": "HEURE_FIN",
    "temps_total": "TEMPS_TOTAL",
    "langue_enqueteur": "LANGUE_ENQ",
    "jour_semaine": "JOUR_SEMAINE",
}

NOMS_DEDUITS = {
    "identification_conseiller": "IDENT_CONSEILLER",
    "tranche_horaire": "TRANCHE_HORAIRE",
    # Convention T_ : une duree prend le prefixe, comme T_Q9_1 au JOB 001/26.
    "attente_conseiller": "T_ATTENTE",
    "duree_appel": "T_DUREE_APPEL",
    "duree_attentes": "T_ATTENTES",
    "nb_attentes": "NB_ATTENTES",
    "nb_transferts": "NB_TRANSFERTS",
    "renvoi": "RENVOI",
    "renvoi_precision": "RENVOI_PRECISION",
    "escalade": "ESCALADE",
}

# Tout le reste porte deja son code (Q1, Q15_com -> Q15_COM, SCORE_A...) : la
# base le reprend tel quel, en majuscules. Les `calculate` en font partie : Kobo
# les exporte comme les autres champs, et les scores de section en sont devenus
# -- ils ne s'affichent plus, ils sortent quand meme dans les donnees. Seules les
# notes, qui n'ont pas de valeur, restent dehors.
NOMS_DEDUITS.update({l["name"]: l["name"].upper() for l in survey
                     if l["name"] and l["name"] not in NOMS_MDS
                     and l["name"] not in NOMS_DEDUITS
                     and l["type"] != "note"
                     and not l["type"].startswith(("begin_", "end_"))})

NOMS_BD = {**NOMS_DEDUITS, **NOMS_MDS}


def renommer(lignes):
    """Passe les noms internes aux noms de la base, references comprises."""
    if not NOMS_BD:
        return lignes
    motif = re.compile(r"\$\{(" + "|".join(map(re.escape, NOMS_BD)) + r")\}")
    sorties = []
    for ligne in lignes:
        sortie = {c: (motif.sub(lambda m: "${" + NOMS_BD[m.group(1)] + "}", v)
                      if isinstance(v, str) else v)
                  for c, v in ligne.items()}
        sortie["name"] = NOMS_BD.get(sortie["name"], sortie["name"])
        sorties.append(sortie)
    noms = [l["name"] for l in sorties if l["name"]]
    doublons = {n for n in noms if noms.count(n) > 1}
    assert not doublons, f"noms en double apres renommage : {sorted(doublons)}"
    return sorties


# =====================================================================
# ECRITURE DU CLASSEUR
# =====================================================================
def localiser(lignes):
    """Dedouble les colonnes traduites : francais tel quel, anglais traduit."""
    sorties = []
    for ligne in lignes:
        sortie = {k: v for k, v in ligne.items()
                  if k not in TRADUITES and k not in IDENTIQUES}
        for cle in TRADUITES:
            if cle in ligne:
                sortie[f"{cle}::{LANG_FR}"] = ligne[cle]
                sortie[f"{cle}::{LANG_EN}"] = traductions.en(ligne[cle])
        for cle in IDENTIQUES:
            if cle in ligne:
                sortie[f"{cle}::{LANG_FR}"] = ligne[cle]
                sortie[f"{cle}::{LANG_EN}"] = ligne[cle]
        sorties.append(sortie)
    return sorties


def ecrire(ws, colonnes, lignes):
    ws.append(colonnes)
    for c in ws[1]:
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor="1F5C8B")
        c.alignment = Alignment(horizontal="center")
    for ligne in lignes:
        ws.append([ligne.get(c, "") for c in colonnes])
    largeurs = {"type": 26, "name": 24, "label": 70, "hint": 60, "list_name": 22}
    for i, c in enumerate(colonnes, 1):
        largeur = largeurs.get(c.split("::")[0], 18)
        ws.column_dimensions[ws.cell(row=1, column=i).column_letter].width = largeur
    ws.freeze_panes = "A2"


wb = Workbook()
ecrire(wb.active, COLONNES, renommer(localiser(survey)))
wb.active.title = "survey"
ecrire(wb.create_sheet("choices"), COL_CHOIX, localiser(choices))
# style = pages : une page par groupe field-list, et le bouton Suivant reste
# bloque tant que les questions obligatoires de la page ne sont pas remplies.
ecrire(wb.create_sheet("settings"),
       ["form_title", "form_id", "version", "style", "default_language"],
       [{"form_title": "QUESTIONNAIRE GHOST CHECK CALL CENTER — MDS JOB 002/26",
         "form_id": "audit_call_center_mds_002_26",
         "version": "2026091001",
         "style": "pages",
         "default_language": LANG_FR}])
wb.save(SORTIE)

# Structure exportee en JSON : sert a generer le guide enqueteur et le tableau
# de bord sans redupliquer les libelles ni le bareme.
STRUCTURE = SORTIE.with_name("form_structure.json")
STRUCTURE.write_text(json.dumps(
    {"survey": survey, "choices": choices, "noms_bd": NOMS_BD,
     "noms_mds": sorted(NOMS_MDS), "bareme": BAREME,
     "notation": {cle: {"titre": s["titre"],
                        "questions": [[n, _table(n)] for n in s["questions"]]}
                  for cle, s in NOTATION.items()}},
    indent=2, ensure_ascii=False), encoding="utf-8")

# =====================================================================
# CONTROLES DE GENERATION
# =====================================================================
utilises = {r[c] for r in survey for c in TRADUITES if r.get(c)}
utilises |= {c["label"] for c in choices if c["label"]}
manquantes = sorted(t for t in utilises if not traductions.couverte(t))
orphelines = sorted(set(traductions.FR_EN) - utilises)
if manquantes:
    print(f"  ATTENTION : {len(manquantes)} libellé(s) sans traduction anglaise :")
    for m in manquantes:
        print(f"    - {m[:100]}")
if orphelines:
    print(f"  ATTENTION : {len(orphelines)} traduction(s) orpheline(s) "
          f"(libellé français modifié ou supprimé) :")
    for o in orphelines[:8]:
        print(f"    - {o[:100]}")

nb_questions = sum(1 for r in survey
                   if not r["type"].startswith(("begin_", "end_"))
                   and r["type"] not in ("note", "calculate")
                   and r.get("readonly") != "yes")
nb_deduits = sum(1 for r in survey if r.get("readonly") == "yes")
nb_texte = sum(1 for r in survey if r["type"] == "text" and r.get("readonly") != "yes")
nb_com = sum(1 for r in survey if r["name"].endswith("_com"))
nb_alertes_q = sum(1 for r in survey if r["name"].endswith("_alerte"))
nb_pages = sum(1 for r in survey
               if r["type"] == "begin_group" and r["appearance"] == "field-list")
print(f"OK : {SORTIE.name} + {STRUCTURE.name}")
print(f"  {nb_questions} questions saisies, {nb_deduits} champs déduits, "
      f"{nb_pages} pages, {nb_texte} champs texte libres")
print(f"  {len(TOUTES_NOTEES)} critères notés répartis en {len(NOTATION)} "
      f"sections, {nb_alertes_q} qualifications d'alerte puis {nb_com} "
      f"commentaires, conditionnés à un critère non conforme")
# Les listes des criteres ne portent que des cas : rien a retrancher. Elles ne
# proposent pas toutes les memes : la section A remplace les cinq cas generaux
# par les siens, C et D les completent, critere par critere pour D.
LISTES_ALERTE = ("alertes_nc", "alertes_a", "alertes_c",
                 "alertes_q9", "alertes_q10", "alertes_q11")
nb_cas = {n: sum(1 for c in choices if c["list_name"] == n)
          for n in LISTES_ALERTE}
print(f"  {len(CAS_ALERTES)} cas d'alerte critique généraux, hors score, "
      f"cochables sur chaque non-conformité et là seulement")
print("  " + " · ".join(f"{n} : {nb}" for n, nb in nb_cas.items())
      + f" — {sum(1 for c in choices if c['list_name'] in LISTES_ALERTE)} "
        f"modalités pour {len(LISTES_ALERTE)} listes")
