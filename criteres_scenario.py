#!/usr/bin/env python3
"""Criteres propres a chaque scenario (MDS JOB 002/26).

Source : annexe MDS « Scenarios finaux -- Questionnaire Ghost Check Call »,
25 scenarios, 106 criteres, 3 a 5 par scenario.

La ou les 23 criteres A->H mesurent le COMPORTEMENT -- les memes pour tous les
appels --, ceux-ci mesurent les ACTES que le scenario appelait : a-t-il verifie
l'activation du forfait, consulte l'historique, authentifie le client avant de
donner le code PUK.

Ils prennent la MEME ECHELLE et entrent dans le MEME SCORE que les 23 autres :
build_form.py les declare comme une section notee de plus (section I). Seuls
ceux du scenario joue s'affichent ; les autres sont masques par leur `relevant`
et sortent du numerateur comme du denominateur, exactement comme Q15 ou Q18.

Le libelle reprend l'annexe mot pour mot -- intitule du critere, puis question
-- precede du numero du critere, qui est le nom de sa colonne a l'export :
« S01_1 Diagnostic — Le conseiller a-t-il... ». Meme convention que « Q1 ... »
pour les criteres de comportement, et de quoi lire la base de sortie sans table
de correspondance : sans lui, les « Solution » et « Pedagogie » de deux
scenarios sont indiscernables.
Les traductions anglaises sont dans traductions.py, comme tout le reste.

Nom des variables a l'export : <code du scenario>_<rang>, par exemple S01_1.
"""

CRITERES = {
    "S01": [
        ("Diagnostic",
         "Le conseiller a-t-il identifié clairement la nature du problème et "
         "expliqué les causes possibles de la lenteur d'Internet ?"),
        ("Qualification",
         "Le conseiller a-t-il posé des questions pertinentes pour qualifier le "
         "problème (forfait, téléphone, réseau, configuration) ?"),
        ("Vérification du contexte",
         "Le conseiller a-t-il vérifié votre localisation, le type de terminal "
         "ou d'autres éléments contextuels utiles à l'analyse de votre problème ?"),
        ("Solution",
         "Le conseiller a-t-il proposé une solution concrète et adaptée pour "
         "rétablir la qualité de la connexion ?"),
        ("Pédagogie",
         "Le conseiller a-t-il expliqué les étapes de manière simple et "
         "compréhensible, vous permettant de reproduire la solution en cas de "
         "récurrence ?")],

    "S02": [
        ("Diagnostic des causes",
         "Le conseiller a-t-il cherché à distinguer l'origine du problème "
         "(activation du forfait, configuration du téléphone, couverture réseau "
         "ou anomalie de compte) ?"),
        ("Vérification de l'activation",
         "Le conseiller a-t-il vérifié que le forfait avait bien été activé sur "
         "la ligne ?"),
        ("Vérification technique",
         "Le conseiller a-t-il vérifié la configuration (APN, paramètres réseau) "
         "et la couverture réseau dans la zone du client ?"),
        ("Solution",
         "Le conseiller a-t-il proposé une solution concrète pour rétablir la "
         "navigation ?"),
        ("Alternative",
         "Le conseiller a-t-il proposé une alternative en cas de non-résolution "
         "immédiate (remboursement, geste commercial, délai) ?")],

    "S03": [
        ("Qualification du problème",
         "Le conseiller a-t-il posé des questions pertinentes pour bien cerner "
         "la nature du problème (coupure, durée, fréquence, qualité de la voix) ?"),
        ("Localisation",
         "Le conseiller a-t-il vérifié la zone géographique où le problème "
         "survient afin d'identifier un éventuel incident réseau localisé ?"),
        ("Terminal / SIM",
         "Le conseiller a-t-il demandé des précisions sur le type de téléphone, "
         "l'état de la carte SIM ou les paramètres utilisés ?"),
        ("Incident réseau",
         "Le conseiller a-t-il vérifié s'il existe un incident réseau connu "
         "pouvant expliquer les coupures d'appels ?"),
        ("Solution ou escalade",
         "Le conseiller a-t-il proposé une solution concrète pour résoudre le "
         "problème ou, à défaut, procédé à une escalade appropriée vers un "
         "niveau supérieur de support ?")],

    "S04": [
        ("Vérification de la consommation",
         "Le conseiller a-t-il vérifié la consommation réelle du forfait "
         "(historique, détail par usage) ?"),
        ("Transparence",
         "Le conseiller a-t-il expliqué clairement au client comment son forfait "
         "a été consommé aussi rapidement ?"),
        ("Vérification du disponible",
         "Le conseiller a-t-il vérifié s'il existait un reliquat, un bonus ou un "
         "forfait complémentaire disponible ?"),
        ("Conseils de maîtrise",
         "Le conseiller a-t-il donné des conseils pratiques pour mieux maîtriser "
         "sa consommation à l'avenir (suivi de conso, alertes, applications) ?")],

    "S05": [
        ("Investigation",
         "Le conseiller a-t-il mené une investigation rigoureuse pour identifier "
         "l'origine du débit (détail des consommations) ?"),
        ("Identification des postes de débit",
         "Le conseiller a-t-il vérifié les différentes sources possibles (data "
         "hors forfait, services VAS, appels/SMS hors forfait) ?"),
        ("Exactitude",
         "Le conseiller a-t-il fourni des informations exactes et vérifiées sur "
         "les montants et la nature des débits ?"),
        ("Explication claire",
         "Le conseiller a-t-il expliqué la situation de façon claire et "
         "compréhensible pour le client ?")],

    "S06": [
        ("Identification du service",
         "Le conseiller a-t-il identifié précisément le service VAS concerné et "
         "son mode de souscription ?"),
        ("Désactivation",
         "Le conseiller a-t-il procédé ou proposé la désactivation immédiate du "
         "service ?"),
        ("Procédure de contestation / remboursement",
         "Le conseiller a-t-il expliqué la procédure de contestation et, si "
         "applicable, de remboursement des montants prélevés ?"),
        ("Rassurance",
         "Le conseiller a-t-il rassuré le client et vérifié qu'aucune autre "
         "souscription non désirée n'était active ?")],

    "S07": [
        ("Diagnostic",
         "Le conseiller a-t-il cherché à identifier la cause de l'échec de la "
         "transaction (solde, canal utilisé, incident technique) ?"),
        ("Connaissance du parcours",
         "Le conseiller a-t-il démontré une bonne connaissance des différents "
         "canaux d'achat (USSD, application, agence) ?"),
        ("Alternatives proposées",
         "Le conseiller a-t-il proposé un canal alternatif pour finaliser "
         "l'achat ?"),
        ("Accompagnement",
         "Le conseiller a-t-il accompagné le client pas à pas jusqu'à la "
         "résolution du problème ?")],

    "S08": [
        ("Assistance digitale",
         "Le conseiller a-t-il apporté une assistance technique adaptée au "
         "problème de connexion ?"),
        ("Étapes simples",
         "Le conseiller a-t-il expliqué les étapes de résolution de manière "
         "simple et progressive ?"),
        ("Récupération d'accès",
         "Le conseiller a-t-il aidé le client à récupérer l'accès à son compte "
         "(mot de passe, identifiant, réinstallation) ?"),
        ("Alternative",
         "Le conseiller a-t-il proposé une alternative en cas d'indisponibilité "
         "prolongée de l'application (USSD, agence, autre canal) ?")],

    "S09": [
        ("Découverte du besoin",
         "Le conseiller a-t-il posé des questions pour bien cerner les besoins "
         "et habitudes de consommation du client ?"),
        ("Personnalisation",
         "Le conseiller a-t-il adapté sa réponse au profil et au budget exprimés "
         "par le client ?"),
        ("Connaissance du catalogue",
         "Le conseiller a-t-il démontré une bonne connaissance des offres "
         "disponibles ?"),
        ("Pertinence de la recommandation",
         "Le conseiller a-t-il proposé un forfait réellement adapté aux besoins "
         "exprimés, sans sur-vente ?")],

    "S10": [
        ("Compréhension de l'usage",
         "Le conseiller a-t-il bien compris les habitudes de consommation "
         "actuelles du client ?"),
        ("Présentation des options",
         "Le conseiller a-t-il présenté les différentes options disponibles "
         "correspondant à la demande ?"),
        ("Prise en compte des contraintes",
         "Le conseiller a-t-il tenu compte des contraintes du client "
         "(engagement, coût, conditions de migration) ?"),
        ("Conseil adapté",
         "Le conseiller a-t-il proposé une offre réellement adaptée à la demande "
         "du client ?"),
        ("Absence de vente forcée",
         "Le conseiller a-t-il respecté le choix du client sans forcer une offre "
         "plus chère ou non désirée ?")],

    "S11": [
        ("Authentification",
         "Le conseiller a-t-il procédé à une vérification d'identité conforme "
         "avant de communiquer le code ?"),
        ("Sécurité",
         "Le conseiller a-t-il respecté les procédures de sécurité tout au long "
         "de l'échange ?"),
        ("Rapidité de résolution",
         "Le conseiller a-t-il résolu la situation rapidement et efficacement ?"),
        ("Pédagogie",
         "Le conseiller a-t-il expliqué au client comment éviter ce type de "
         "blocage à l'avenir ?")],

    "S12": [
        ("Priorisation de la sécurité",
         "Le conseiller a-t-il traité la demande en priorité, avec le sérieux "
         "requis par la situation ?"),
        ("Blocage / protection",
         "Le conseiller a-t-il procédé ou guidé le client vers le blocage "
         "immédiat de la ligne ?"),
        ("Authentification",
         "Le conseiller a-t-il vérifié l'identité du client selon la procédure "
         "requise avant toute action ?"),
        ("Procédure de remplacement",
         "Le conseiller a-t-il expliqué clairement la procédure pour obtenir une "
         "nouvelle SIM ?")],

    "S13": [
        ("Maîtrise KYC",
         "Le conseiller a-t-il fait preuve d'une bonne maîtrise des règles "
         "d'identification (KYC) applicables ?"),
        ("Clarté de la procédure",
         "Le conseiller a-t-il expliqué clairement la procédure à suivre pour "
         "régulariser la situation ?"),
        ("Pièces et canal",
         "Le conseiller a-t-il précisé les pièces justificatives nécessaires et "
         "le canal à utiliser ?"),
        ("Minimisation de l'effort",
         "Le conseiller a-t-il proposé la solution la plus simple et la moins "
         "contraignante pour le client ?")],

    "S14": [
        ("Consultation de l'historique",
         "Le conseiller a-t-il consulté l'historique des échanges précédents "
         "avant de répondre ?"),
        ("Reconnaissance de la récurrence",
         "Le conseiller a-t-il reconnu explicitement le caractère récurrent du "
         "problème ?"),
        ("Ownership",
         "Le conseiller a-t-il pris en charge la demande sans renvoyer la "
         "responsabilité au client ?"),
        ("Escalade appropriée",
         "Le conseiller a-t-il procédé à une escalade adaptée si nécessaire ?"),
        ("Délai / next step",
         "Le conseiller a-t-il communiqué un délai clair et une prochaine étape "
         "précise ?")],

    "S15": [
        ("Écoute émotionnelle",
         "Le conseiller a-t-il su écouter le mécontentement du client sans "
         "l'interrompre ni se justifier immédiatement ?"),
        ("Désescalade",
         "Le conseiller a-t-il su désamorcer la tension par son attitude et son "
         "discours ?"),
        ("Empathie",
         "Le conseiller a-t-il exprimé de l'empathie envers la situation vécue "
         "par le client ?"),
        ("Reprise en main",
         "Le conseiller a-t-il repris le contrôle de l'échange de façon "
         "professionnelle et rassurante ?"),
        ("Recherche de solution",
         "Le conseiller a-t-il orienté l'échange vers une recherche concrète de "
         "solution ?")],

    "S16": [
        ("Rapidité",
         "Le conseiller a-t-il répondu rapidement à la demande ?"),
        ("Exactitude",
         "L'information tarifaire communiquée était-elle exacte ?"),
        ("Simplicité",
         "La réponse a-t-elle été formulée de façon simple et directement "
         "compréhensible ?"),
        ("Absence d'informations inutiles",
         "Le conseiller a-t-il évité de noyer la réponse dans des informations "
         "non demandées ?")],

    "S17": [
        ("Maîtrise du roaming",
         "Le conseiller a-t-il démontré une bonne connaissance des conditions "
         "d'utilisation à l'étranger ?"),
        ("Conditions d'activation",
         "Le conseiller a-t-il expliqué les éventuelles conditions d'activation "
         "du roaming ?"),
        ("Tarification",
         "Le conseiller a-t-il communiqué une information tarifaire claire et "
         "exacte pour la destination concernée ?"),
        ("Prévention du hors-forfait",
         "Le conseiller a-t-il alerté le client sur les risques de hors-forfait "
         "et les moyens de les éviter ?"),
        ("Conseil",
         "Le conseiller a-t-il proposé une offre ou un conseil adapté au voyage "
         "du client ?")],

    "S18": [
        ("Connaissance des canaux",
         "Le conseiller a-t-il démontré une bonne connaissance des procédures "
         "via USSD et/ou application ?"),
        ("Explication pas-à-pas",
         "Le conseiller a-t-il expliqué la procédure de manière claire et "
         "détaillée, étape par étape ?"),
        ("Frais et conditions",
         "Le conseiller a-t-il informé le client des éventuels frais ou "
         "conditions applicables au transfert ?")],

    "S19": [
        ("Diagnostic",
         "Le conseiller a-t-il cherché à identifier la cause probable du "
         "problème (délai technique, erreur de numéro, incident) ?"),
        ("Sécurité",
         "Le conseiller a-t-il respecté les procédures de sécurité et de "
         "vérification d'identité propres au Mobile Money ?"),
        ("Traçabilité",
         "Le conseiller a-t-il vérifié la transaction à l'aide des références "
         "fournies par le client ?"),
        ("Procédure de réclamation et délai",
         "Le conseiller a-t-il expliqué la procédure de réclamation et "
         "communiqué un délai de traitement ?")],

    "S20": [
        ("Maîtrise de la procédure",
         "Le conseiller a-t-il connu et expliqué correctement la procédure "
         "applicable à ce type d'incident ?"),
        ("Gestion du risque",
         "Le conseiller a-t-il agi avec la prudence nécessaire compte tenu de la "
         "sensibilité de l'opération ?"),
        ("Transparence",
         "Le conseiller a-t-il été transparent sur les possibilités réelles "
         "d'annulation ou de récupération des fonds ?"),
        ("Accompagnement",
         "Le conseiller a-t-il guidé le client sur les démarches à suivre "
         "(délai, pièces, contact du bénéficiaire) ?")],

    "S21": [
        ("Maîtrise des règles de cycle de vie",
         "Le conseiller a-t-il expliqué correctement les règles de désactivation "
         "et de récupération applicables ?"),
        ("Vérification de la disponibilité",
         "Le conseiller a-t-il vérifié si le numéro était encore disponible pour "
         "une réactivation ?"),
        ("Pièces et canal",
         "Le conseiller a-t-il précisé les pièces justificatives et le canal à "
         "utiliser pour la démarche ?"),
        ("Alternatives",
         "Le conseiller a-t-il proposé une alternative si le numéro n'était plus "
         "récupérable ?")],

    "S22": [
        ("Vérification d'incident",
         "Le conseiller a-t-il vérifié l'existence d'un incident réseau connu "
         "dans la zone concernée ?"),
        ("Collecte de la localisation",
         "Le conseiller a-t-il précisément recueilli la localisation du client "
         "(quartier, ville, repères) ?"),
        ("Communication proactive",
         "Le conseiller a-t-il communiqué de façon proactive sur l'état de la "
         "situation ?"),
        ("Délai / next step",
         "Le conseiller a-t-il donné un délai ou une prochaine étape claire au "
         "client ?")],

    "S23": [
        ("Capacité d'adaptation",
         "Le conseiller a-t-il su adapter sa reformulation à la demande du "
         "client ?"),
        ("Patience",
         "Le conseiller a-t-il fait preuve de patience face à la demande de "
         "réexplication ?"),
        ("Langage simple",
         "Le conseiller a-t-il reformulé son explication avec des mots simples, "
         "sans jargon technique ?"),
        ("Vérification de compréhension",
         "Le conseiller a-t-il vérifié, à la fin de son explication, que le "
         "client avait bien compris ?")],

    "S24": [
        ("Inclusion",
         "Le conseiller a-t-il adapté son discours et son rythme au niveau "
         "d'aisance digitale du client ?"),
        ("Patience",
         "Le conseiller a-t-il fait preuve de patience tout au long de "
         "l'accompagnement ?"),
        ("Guidage étape par étape",
         "Le conseiller a-t-il guidé le client pas à pas dans la réalisation de "
         "l'opération ?"),
        ("Alternative non digitale",
         "Le conseiller a-t-il proposé, si utile, une alternative non digitale "
         "(USSD, agence) ?")],

    "S25": [
        ("Ownership",
         "Le conseiller a-t-il pris la demande en charge sans se défausser "
         "immédiatement ?"),
        ("Capacité d'orientation",
         "Le conseiller a-t-il su orienter le client vers le bon service ou "
         "canal de traitement ?"),
        ("Enregistrement de la plainte",
         "Le conseiller a-t-il procédé ou proposé l'enregistrement formel de la "
         "réclamation ?"),
        ("Absence de renvoi abusif",
         "Le conseiller a-t-il évité tout renvoi injustifié ou toute fin de "
         "non-recevoir ?")],
}


# Version anglaise, dans le meme ordre. Elle vit ici plutot que dans
# traductions.py : une paire de phrases se relit mieux cote a cote qu'eclatee
# sur deux fichiers, et `FR_EN()` la reverse ensuite dans la table generale, ou
# `en()` et le controle de couverture la voient comme les autres.
CRITERES_EN = {
    "S01": [
        ("Diagnosis",
         "Did the adviser clearly identify the nature of the problem and "
         "explain the possible causes of the slow internet?"),
        ("Qualification",
         "Did the adviser ask relevant questions to qualify the problem "
         "(bundle, handset, network, settings)?"),
        ("Context check",
         "Did the adviser check your location, the type of handset or any other "
         "contextual details useful in analysing your problem?"),
        ("Solution",
         "Did the adviser offer a concrete, suitable solution to restore the "
         "quality of the connection?"),
        ("Teaching approach",
         "Did the adviser explain the steps simply and understandably, so that "
         "you could repeat the solution if it happened again?")],

    "S02": [
        ("Diagnosis of the causes",
         "Did the adviser try to distinguish the origin of the problem (bundle "
         "activation, handset settings, network coverage or an account "
         "anomaly)?"),
        ("Activation check",
         "Did the adviser check that the bundle had indeed been activated on "
         "the line?"),
        ("Technical check",
         "Did the adviser check the settings (APN, network parameters) and the "
         "network coverage in the customer's area?"),
        ("Solution",
         "Did the adviser offer a concrete solution to restore browsing?"),
        ("Alternative",
         "Did the adviser offer an alternative where immediate resolution was "
         "not possible (refund, goodwill gesture, timeframe)?")],

    "S03": [
        ("Qualification of the problem",
         "Did the adviser ask relevant questions to pin down the nature of the "
         "problem (dropped calls, duration, frequency, voice quality)?"),
        ("Location",
         "Did the adviser check the geographical area where the problem occurs, "
         "in order to identify a possible localised network incident?"),
        ("Handset / SIM",
         "Did the adviser ask for details about the type of handset, the "
         "condition of the SIM card or the settings in use?"),
        ("Network incident",
         "Did the adviser check whether there was a known network incident that "
         "could explain the dropped calls?"),
        ("Solution or escalation",
         "Did the adviser offer a concrete solution to resolve the problem or, "
         "failing that, escalate appropriately to a higher level of support?")],

    "S04": [
        ("Usage check",
         "Did the adviser check the actual consumption of the bundle (history, "
         "breakdown by usage)?"),
        ("Transparency",
         "Did the adviser clearly explain to the customer how their bundle had "
         "been used up so quickly?"),
        ("Remaining allowance check",
         "Did the adviser check whether any remaining allowance, bonus or "
         "additional bundle was available?"),
        ("Advice on managing usage",
         "Did the adviser give practical advice on managing consumption better "
         "in future (usage tracking, alerts, apps)?")],

    "S05": [
        ("Investigation",
         "Did the adviser investigate rigorously to identify the origin of the "
         "charge (breakdown of usage)?"),
        ("Identification of the charges",
         "Did the adviser check the various possible sources (out-of-bundle "
         "data, VAS services, out-of-bundle calls/SMS)?"),
        ("Accuracy",
         "Did the adviser provide accurate, verified information on the amounts "
         "and the nature of the charges?"),
        ("Clear explanation",
         "Did the adviser explain the situation clearly and understandably for "
         "the customer?")],

    "S06": [
        ("Identification of the service",
         "Did the adviser precisely identify the VAS service concerned and how "
         "it had been subscribed to?"),
        ("Deactivation",
         "Did the adviser carry out, or offer, immediate deactivation of the "
         "service?"),
        ("Dispute / refund procedure",
         "Did the adviser explain the dispute procedure and, where applicable, "
         "how the amounts charged could be refunded?"),
        ("Reassurance",
         "Did the adviser reassure the customer and check that no other "
         "unwanted subscription was active?")],

    "S07": [
        ("Diagnosis",
         "Did the adviser try to identify the cause of the failed transaction "
         "(balance, channel used, technical incident)?"),
        ("Knowledge of the journey",
         "Did the adviser show a good knowledge of the various purchase "
         "channels (USSD, app, branch)?"),
        ("Alternatives offered",
         "Did the adviser offer an alternative channel to complete the "
         "purchase?"),
        ("Support",
         "Did the adviser guide the customer step by step through to the "
         "resolution of the problem?")],

    "S08": [
        ("Digital support",
         "Did the adviser provide technical support suited to the connection "
         "problem?"),
        ("Simple steps",
         "Did the adviser explain the resolution steps simply and "
         "progressively?"),
        ("Recovering access",
         "Did the adviser help the customer recover access to their account "
         "(password, username, reinstallation)?"),
        ("Alternative",
         "Did the adviser offer an alternative in the event of a prolonged app "
         "outage (USSD, branch, another channel)?")],

    "S09": [
        ("Needs discovery",
         "Did the adviser ask questions to pin down the customer's needs and "
         "consumption habits?"),
        ("Personalisation",
         "Did the adviser tailor the answer to the profile and the budget the "
         "customer expressed?"),
        ("Knowledge of the catalogue",
         "Did the adviser show a good knowledge of the bundles available?"),
        ("Relevance of the recommendation",
         "Did the adviser offer a bundle genuinely suited to the needs "
         "expressed, without overselling?")],

    "S10": [
        ("Understanding of usage",
         "Did the adviser properly understand the customer's current "
         "consumption habits?"),
        ("Presentation of the options",
         "Did the adviser present the various options available matching the "
         "request?"),
        ("Account taken of constraints",
         "Did the adviser take the customer's constraints into account "
         "(commitment, cost, migration conditions)?"),
        ("Suitable advice",
         "Did the adviser offer a plan genuinely suited to the customer's "
         "request?"),
        ("No forced selling",
         "Did the adviser respect the customer's choice without pushing a more "
         "expensive or unwanted plan?")],

    "S11": [
        ("Authentication",
         "Did the adviser carry out a compliant identity check before giving "
         "out the code?"),
        ("Security",
         "Did the adviser follow the security procedures throughout the "
         "exchange?"),
        ("Speed of resolution",
         "Did the adviser resolve the situation quickly and efficiently?"),
        ("Teaching approach",
         "Did the adviser explain to the customer how to avoid this kind of "
         "lock-out in future?")],

    "S12": [
        ("Security given priority",
         "Did the adviser handle the request as a priority, with the "
         "seriousness the situation required?"),
        ("Blocking / protection",
         "Did the adviser block the line immediately, or guide the customer to "
         "do so?"),
        ("Authentication",
         "Did the adviser verify the customer's identity in line with the "
         "required procedure before taking any action?"),
        ("Replacement procedure",
         "Did the adviser clearly explain the procedure for obtaining a new "
         "SIM?")],

    "S13": [
        ("Command of KYC",
         "Did the adviser show a good command of the applicable identification "
         "(KYC) rules?"),
        ("Clarity of the procedure",
         "Did the adviser clearly explain the procedure to follow to put the "
         "situation right?"),
        ("Documents and channel",
         "Did the adviser state the supporting documents required and the "
         "channel to use?"),
        ("Keeping effort down",
         "Did the adviser offer the simplest, least demanding solution for the "
         "customer?")],

    "S14": [
        ("Checking the history",
         "Did the adviser look at the history of previous exchanges before "
         "answering?"),
        ("Acknowledging the recurrence",
         "Did the adviser explicitly acknowledge that the problem was "
         "recurring?"),
        ("Ownership",
         "Did the adviser take charge of the request without passing "
         "responsibility back to the customer?"),
        ("Appropriate escalation",
         "Did the adviser escalate appropriately where necessary?"),
        ("Timeframe / next step",
         "Did the adviser give a clear timeframe and a precise next step?")],

    "S15": [
        ("Listening to the emotion",
         "Did the adviser listen to the customer's dissatisfaction without "
         "interrupting or immediately justifying?"),
        ("De-escalation",
         "Did the adviser defuse the tension through their manner and their "
         "words?"),
        ("Empathy",
         "Did the adviser express empathy for what the customer was going "
         "through?"),
        ("Regaining control",
         "Did the adviser regain control of the exchange in a professional, "
         "reassuring way?"),
        ("Search for a solution",
         "Did the adviser steer the exchange towards a concrete search for a "
         "solution?")],

    "S16": [
        ("Speed",
         "Did the adviser answer the request quickly?"),
        ("Accuracy",
         "Was the pricing information given accurate?"),
        ("Simplicity",
         "Was the answer phrased simply and made immediately understandable?"),
        ("No needless information",
         "Did the adviser avoid drowning the answer in information that had not "
         "been asked for?")],

    "S17": [
        ("Command of roaming",
         "Did the adviser show a good knowledge of the conditions for use "
         "abroad?"),
        ("Activation conditions",
         "Did the adviser explain any conditions for activating roaming?"),
        ("Pricing",
         "Did the adviser give clear, accurate pricing information for the "
         "destination concerned?"),
        ("Preventing out-of-bundle charges",
         "Did the adviser warn the customer about the risk of out-of-bundle "
         "charges and how to avoid them?"),
        ("Advice",
         "Did the adviser offer a plan or advice suited to the customer's "
         "trip?")],

    "S18": [
        ("Knowledge of the channels",
         "Did the adviser show a good knowledge of the procedures via USSD "
         "and/or the app?"),
        ("Step-by-step explanation",
         "Did the adviser explain the procedure clearly and in detail, step by "
         "step?"),
        ("Fees and conditions",
         "Did the adviser tell the customer about any fees or conditions "
         "applying to the transfer?")],

    "S19": [
        ("Diagnosis",
         "Did the adviser try to identify the likely cause of the problem "
         "(technical delay, wrong number, incident)?"),
        ("Security",
         "Did the adviser follow the security and identity-checking procedures "
         "specific to Mobile Money?"),
        ("Traceability",
         "Did the adviser check the transaction using the references the "
         "customer provided?"),
        ("Claim procedure and timeframe",
         "Did the adviser explain the claim procedure and give a processing "
         "timeframe?")],

    "S20": [
        ("Command of the procedure",
         "Did the adviser know and correctly explain the procedure applying to "
         "this kind of incident?"),
        ("Risk management",
         "Did the adviser act with the caution the sensitivity of the operation "
         "required?"),
        ("Transparency",
         "Was the adviser transparent about the real chances of cancelling the "
         "transfer or recovering the funds?"),
        ("Support",
         "Did the adviser guide the customer on the steps to take (timeframe, "
         "documents, contacting the recipient)?")],

    "S21": [
        ("Command of the lifecycle rules",
         "Did the adviser correctly explain the applicable deactivation and "
         "recovery rules?"),
        ("Availability check",
         "Did the adviser check whether the number was still available for "
         "reactivation?"),
        ("Documents and channel",
         "Did the adviser state the supporting documents and the channel to use "
         "for the process?"),
        ("Alternatives",
         "Did the adviser offer an alternative if the number could no longer be "
         "recovered?")],

    "S22": [
        ("Incident check",
         "Did the adviser check whether there was a known network incident in "
         "the area concerned?"),
        ("Collecting the location",
         "Did the adviser precisely collect the customer's location "
         "(neighbourhood, town, landmarks)?"),
        ("Proactive communication",
         "Did the adviser communicate proactively about the state of the "
         "situation?"),
        ("Timeframe / next step",
         "Did the adviser give the customer a clear timeframe or next step?")],

    "S23": [
        ("Ability to adapt",
         "Did the adviser manage to adapt the way they rephrased things to the "
         "customer's request?"),
        ("Patience",
         "Was the adviser patient in the face of a request for a further "
         "explanation?"),
        ("Plain language",
         "Did the adviser rephrase the explanation in simple words, without "
         "technical jargon?"),
        ("Checking understanding",
         "Did the adviser check, at the end of the explanation, that the "
         "customer had understood?")],

    "S24": [
        ("Inclusion",
         "Did the adviser adapt their words and their pace to the customer's "
         "level of digital ease?"),
        ("Patience",
         "Was the adviser patient throughout the support given?"),
        ("Step-by-step guidance",
         "Did the adviser guide the customer step by step through the "
         "operation?"),
        ("Non-digital alternative",
         "Did the adviser offer, where useful, a non-digital alternative (USSD, "
         "branch)?")],

    "S25": [
        ("Ownership",
         "Did the adviser take charge of the request without immediately "
         "passing the buck?"),
        ("Ability to direct",
         "Did the adviser manage to direct the customer to the right department "
         "or handling channel?"),
        ("Recording the complaint",
         "Did the adviser formally record the complaint, or offer to?"),
        ("No improper referral",
         "Did the adviser avoid any unjustified referral or outright refusal to "
         "help?")],
}


def nom(code, rang):
    """Nom de variable : S01_1 ... S25_5, repris tel quel a l'export."""
    return f"{code}_{rang}"


def libelle(code, rang, intitule, question):
    """Libelle affiche : le numero du critere, l'intitule de l'annexe, sa question.

    LE NUMERO EST CELUI DE LA COLONNE. « S01_1 Diagnostic — ... » porte le nom
    exact sous lequel la reponse sort a l'export, comme « Q1 ... » le fait pour
    les criteres de comportement. L'annexe MDS numerote ses criteres par
    scenario sans leur donner de code ; deux scenarios ont donc des « Solution »
    ou des « Pedagogie » homonymes, indiscernables dans une base ou un tableau
    croise. Le prefixe rend chaque libelle unique et rattache visiblement le
    critere a son scenario -- la BD en sortie se lit sans table de
    correspondance.
    """
    return f"{nom(code, rang)} {intitule} — {question}"


def traductions():
    """Table FR -> EN des 106 libelles, versee dans traductions.FR_EN."""
    assert set(CRITERES_EN) == set(CRITERES), "un scenario sans version anglaise"
    table = {}
    for code, francais in CRITERES.items():
        anglais = CRITERES_EN[code]
        assert len(anglais) == len(francais), (
            f"{code} : {len(francais)} critere(s) en francais, "
            f"{len(anglais)} en anglais")
        for rang, ((i_fr, q_fr), (i_en, q_en)) in enumerate(
                zip(francais, anglais), start=1):
            table[libelle(code, rang, i_fr, q_fr)] = libelle(
                code, rang, i_en, q_en)
    assert len(table) == sum(len(v) for v in CRITERES.values()), (
        "deux criteres portent le meme libelle francais")
    return table
