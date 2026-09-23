#!/usr/bin/env python3
"""Version anglaise du QUESTIONNAIRE GHOST CHECK CALL CENTER (MDS JOB 002/26).

Une seule source pour les trois sorties :
  - build_form.py      : colonnes `label::English (en)`, `hint::English (en)` et
    `constraint_message::English (en)` du XLSForm -- d'ou le selecteur de langue
    de KoboCollect et d'Enketo ;
  - build_guide.py     : bouton FR / EN du questionnaire enqueteur ;
  - build_dashboard.py : bouton FR / EN du tableau de bord.

La cle est le libelle francais EXACT tel qu'il sort de build_form.py.
build_form.py verifie a chaque generation que rien ne manque et signale les
cles orphelines : toute retouche du francais doit etre repercutee ici.

Ne sont pas traduits : les marques (ORANGE, MTN) et les codes de scenario,
laisses tels quels.

A FAIRE VALIDER PAR MDS : traduction de travail. Le questionnaire papier de
reference reste le francais ; en cas d'ecart, c'est lui qui fait foi.
Vocabulaire retenu : « enqueteur » -> auditor, « conseiller » -> adviser,
« serveur vocal » -> IVR, « ownership » et « FCR » laisses tels quels (ils le
sont deja dans le questionnaire francais).
"""
import criteres_scenario

# Libelles, consignes et messages de controle du questionnaire.
FR_EN = {
    # =================================================================
    # PAGE 1 — CONSIGNES GENERALES
    # =================================================================
    "Consignes générales pour l'enquêteur":
        'General instructions for the auditor',
    "**À LIRE AVANT DE COMMENCER.**":
        '**READ THIS BEFORE YOU START.**',

    "**1. COMMENT REMPLIR**\n\n"
    "• **Un seul scénario par appel.** Le questionnaire est renseigné "
    "immédiatement après avoir raccroché.\n"
    "• Commencez par la page **« Mesures »** : le formulaire ouvre ensuite les "
    "seules questions qui concernent cet appel. **Une question qui ne "
    "s'affiche pas n'est pas à renseigner.**\n"
    "• Chaque critère a quatre réponses : **totalement conforme**, "
    "**partiellement conforme**, **non conforme**, **non applicable**.\n"
    "• Un **non conforme** ouvre deux champs : le **cas d'alerte critique** "
    "que le constat révèle, puis le **commentaire obligatoire**. Qualifiez "
    "d'abord, décrivez ensuite.\n"
    "• Vous n'avez **rien à calculer** : vous décrivez ce que vous avez "
    "entendu.\n"
    "• Ne **révélez jamais** que vous êtes enquêteur.":
        '**1. HOW TO FILL IT IN**\n\n'
        '• **One scenario per call only.** The questionnaire is filled in '
        'immediately after hanging up.\n'
        '• Start with the **“Measurements”** page: the form then opens only '
        'the questions that concern this call. **A question that does not '
        'appear is not to be filled in.**\n'
        '• Each criterion has four answers: **fully compliant**, **partially '
        'compliant**, **not compliant**, **not applicable**.\n'
        '• A **not compliant** opens two fields: the **critical alert case** '
        'the finding reveals, then the **mandatory comment**. Qualify first, '
        'describe afterwards.\n'
        '• You have **nothing to work out**: you describe what you heard.\n'
        '• **Never reveal** that you are an auditor.',

    "**2. COMMENT QUALIFIER**\n\n"
    "• Notez ce que vous avez **réellement observé et entendu** pendant "
    "l'appel, pas ce que le conseiller aurait pu faire en dehors du "
    "scénario.\n"
    "• **Non applicable** : seulement si le critère n'a pas pu être observé "
    "ou ne s'appliquait pas à cet appel. Ce n'est pas un « non conforme ».\n"
    "• **Partiellement conforme** : une conformité réelle mais incomplète — "
    "réponse correcte mais partielle, personnalisation mécanique, explication "
    "à moitié claire, prise en charge partielle.\n"
    "• **Non conforme** : toujours étayé par un **fait observé** ou la "
    "**formulation exacte** du conseiller, jamais par une appréciation "
    "générale.\n"
    "• **FCR** : le client obtient dès cet appel la résolution ou une prise "
    "en charge complète et fiable, sans nouvel effort à fournir — même si une "
    "opération reste à finir en back-office.":
        '**2. HOW TO QUALIFY**\n\n'
        '• Score what you **actually observed and heard** during the call, '
        'not what the adviser could have done outside the scenario.\n'
        '• **Not applicable**: only if the criterion could not be observed or '
        'did not apply to this call. It is not a “not compliant”.\n'
        '• **Partially compliant**: genuine but incomplete compliance — a '
        'correct but partial answer, mechanical personalisation, a half-clear '
        'explanation, partial handling.\n'
        '• **Not compliant**: always backed up by an **observed fact** or the '
        "adviser's **exact wording**, never by a general impression.\n"
        '• **FCR**: the customer obtains, from this call onwards, the '
        'resolution or complete and reliable handling, with no further effort '
        'to make — even if an operation remains to be finished in the back '
        'office.',

    "Type d'interview": 'Type of interview',
    "TEST tant que la collecte n'est pas ouverte ; Live pour un appel réel":
        'TEST until collection opens; Live for a real call',

    # =================================================================
    # PAGE 2 — IDENTIFICATION DE L'ENQUETEUR
    # =================================================================
    "Identification de l'enquêteur": 'Auditor identification',
    'Nom enquêteur': 'Auditor name',
    'Opérateur': 'Operator',
    'Date': 'Date',
    'La date ne peut pas être dans le futur.':
        'The date cannot be in the future.',
    'Jour': 'Day',
    'Heure début': 'Start time',
    'Heure fin': 'End time',
    "L'heure de fin doit être postérieure à l'heure de début.":
        'The end time must be later than the start time.',
    'Langue': 'Language',
    'Scénario': 'Scenario',
    'Identification conseiller': 'Adviser identification',
    "Nom donné par le conseiller, ou matricule s'il en a communiqué un":
        'Name given by the adviser, or staff number if they gave one',
    'Tranche horaire': 'Time slot',
    "Déduite de l'heure de début : rien à cocher.":
        'Derived from the start time: nothing to tick.',
    "La tranche horaire en est déduite : rien à cocher plus bas.":
        'The time slot is derived from it: nothing to tick further down.',

    # =================================================================
    # PAGE 4 — SCENARIO JOUE
    # =================================================================
    'Scénario joué': 'Scenario played',
    "**Un seul scénario par appel.** Le script sert de **déclencheur** : ne "
    "surjouez pas, et ne fournissez pas spontanément d'informations qui ne "
    "vous sont pas demandées.\n\n"
    "**Scénarios sensibles (SIM, KYC, Mobile Money) :** n'utilisez que des "
    "lignes et des comptes de test autorisés. **Aucune transaction réelle**, "
    "aucune exposition de données personnelles sans protocole validé.\n\n"
    "S15, S23 et S24 peuvent aussi être joués comme **variantes "
    "relationnelles** appliquées à un scénario fonctionnel (désescalade, "
    "pédagogie, inclusion). Le formulaire n'enregistre qu'un seul code : "
    "cocher celui qui décrit le mieux l'appel.":
        '**One scenario per call only.** The script is a **trigger**: do not '
        'overplay it, and do not volunteer information you have not been '
        'asked for.\n\n'
        '**Sensitive scenarios (SIM, KYC, Mobile Money):** use only authorised '
        'test lines and accounts. **No real transaction**, and no exposure of '
        'personal data without an approved protocol.\n\n'
        'S15, S23 and S24 can also be played as **relational variants** applied '
        'to a functional scenario (de-escalation, teaching, inclusion). The '
        'form records a single code: tick the one that best describes the '
        'call.',
    'Code, famille et intitulé du scénario réellement joué pendant cet appel':
        'Code, family and title of the scenario actually played on this call',

    # =================================================================
    # PAGE 3 — MESURES
    # =================================================================
    'Mesures — valeurs observées': 'Measurements — observed values',
    "Valeurs relevées **chronomètre en main**, immédiatement après l'appel. "
    "Elles ne sont pas notées : elles décrivent l'appel et commandent les "
    "questions conditionnelles qui suivent.\n\n"
    "**Toutes les durées se saisissent en secondes**, sans exception.":
        'Values recorded **with a stopwatch**, immediately after the call. '
        'They are not scored: they describe the call and drive the conditional '
        'questions that follow.\n\n'
        '**Every length of time is entered in seconds**, without exception.',
    "Temps d'attente avant conseiller": 'Waiting time before the adviser',
    'En secondes, du décroché du serveur vocal à la prise de ligne du conseiller':
        'In seconds, from the IVR picking up to the adviser coming on the line',
    'Indiquez une durée comprise entre 0 et 3600 secondes.':
        'Enter a length of time between 0 and 3600 seconds.',
    "Durée totale de l'appel": 'Total length of the call',
    'En secondes, de la prise de ligne du conseiller au raccroché '
    '(3 min 45 s = 225)':
        'In seconds, from the adviser coming on the line to hanging up '
        '(3 min 45 s = 225)',
    'Indiquez une durée comprise entre 0 et 10800 secondes.':
        'Enter a length of time between 0 and 10800 seconds.',
    'Temps total en minutes passé en ligne avec le conseiller':
        'Total time in minutes spent on the line with the adviser',
    'Nombre de mises en attente': 'Number of holds',
    "0 s'il n'y a eu aucune mise en attente": '0 if there was no hold at all',
    'Indiquez un nombre compris entre 0 et 20.':
        'Enter a number between 0 and 20.',
    'Durée cumulée des mises en attente': 'Total time spent on hold',
    'En secondes, toutes mises en attente additionnées':
        'In seconds, all holds added together',
    'Nombre de transferts': 'Number of transfers',
    "0 si l'appel n'a jamais été transféré":
        '0 if the call was never transferred',
    'Indiquez un nombre compris entre 0 et 10.':
        'Enter a number between 0 and 10.',
    "Renvoi : le conseiller a-t-il orienté le client ailleurs qu'au téléphone ?":
        'Referral: did the adviser direct the customer somewhere other than '
        'the phone?',
    "Une seule destination : celle vers laquelle le client a été orienté. "
    "« Aucun renvoi » si le conseiller n'a invité le client ni à poursuivre "
    "sur un canal numérique ni à se déplacer.":
        'A single destination: the one the customer was directed to. '
        '"No referral" if the adviser invited the customer neither to carry on '
        'through a digital channel nor to travel there in person.',
    "Préciser le canal, l'agence ou le point de vente indiqués":
        'Specify the channel, branch or outlet given',
    'Escalade : le dossier a-t-il été transmis à un autre service ou un rappel '
    'a-t-il été promis ?':
        'Escalation: was the case passed on to another department, or was a '
        'call-back promised?',
    "Question d'aiguillage : avec le renvoi, elle commande la question Q15":
        'Routing question: together with the referral, it drives question Q15',

    # =================================================================
    # ALERTE PUIS COMMENTAIRE OBLIGATOIRES SUR LES CRITERES NON CONFORMES
    # =================================================================
    "Non conforme — quel cas d'alerte critique ce constat révèle-t-il ?":
        'Not compliant — which critical alert case does this finding reveal?',
    "À renseigner avant le commentaire. Cochez le ou les cas que ce constat "
    "révèle. La liste est fermée : ce qu'aucun cas ne couvre se décrit dans le "
    "commentaire, juste en dessous.":
        'To be filled in before the comment. Tick the case or cases this '
        'finding reveals. The list is closed: anything no case covers is '
        'described in the comment just below.',
    "Non conforme — décrivez le fait observé ou rapportez la formulation "
    "exacte du conseiller.":
        'Not compliant — describe the observed fact or report the exact wording '
        'used by the adviser.',
    "Obligatoire pour toute non-conformité. Un fait, une phrase entendue : "
    "pas une appréciation générale.":
        'Required for every non-compliance. A fact, a sentence you heard: not a '
        'general impression.',

    # =================================================================
    # SECTION A — ACCESSIBILITE & SERVEUR VOCAL
    # =================================================================
    'A. ACCESSIBILITÉ & SERVEUR VOCAL': 'A. ACCESSIBILITY & VOICE SERVER (IVR)',
    "Q1 Le message d'accueil et les menus du serveur vocal vous ont-ils semblé "
    "clairs, compréhensibles et cohérents avec les services annoncés ?":
        'Q1 Did the welcome message and the IVR menus seem clear, '
        'understandable and consistent with the services announced?',
    "Q2 Le choix de langue vous a-t-il été proposé et a-t-il fonctionné "
    "correctement lorsqu'il était applicable à votre parcours d'appel ?":
        'Q2 Were you offered a choice of language, and did it work properly '
        'where it applied to your call journey?',
    "Q3 L'accès à un conseiller vous a-t-il semblé simple et fluide, sans "
    "erreur, ni boucle inutile ni confusion dans le parcours IVR ?":
        'Q3 Did reaching an adviser feel simple and smooth, with no error, no '
        'pointless loop and no confusion in the IVR journey?',
    'Score — Accessibilité & serveur vocal':
        'Score — Accessibility & voice server (IVR)',

    # =================================================================
    # SECTION B — ACCUEIL & POSTURE DU CONSEILLER
    # =================================================================
    'B. ACCUEIL & POSTURE DU CONSEILLER': 'B. GREETING & ADVISER MANNER',
    "Q4 Le conseiller vous a-t-il accueilli et s'est-il présenté de manière "
    "claire et professionnelle ?":
        'Q4 Did the adviser greet you and introduce themselves clearly and '
        'professionally?',
    "Q5 Le ton du conseiller vous a-t-il semblé courtois, agréable et "
    "disponible, avec une personnalisation naturelle et appropriée de "
    "l'échange, sans sur-scriptage ?":
        'Q5 Did the tone of the adviser seem courteous, pleasant and '
        'attentive, with natural and appropriate personalisation of the '
        'exchange, without sounding over-scripted?',
    'Score — Accueil & posture du conseiller':
        'Score — Greeting & adviser manner',

    # =================================================================
    # SECTION C — COMPREHENSION DU BESOIN
    # =================================================================
    'C. COMPRÉHENSION DU BESOIN': 'C. UNDERSTANDING THE NEED',
    "Q6 Le conseiller vous a-t-il écouté attentivement et vous a-t-il laissé "
    "exposer votre besoin sans interruption inappropriée ?":
        'Q6 Did the adviser listen carefully and let you set out your need '
        'without interrupting inappropriately?',
    "Q7 Le conseiller a-t-il posé des questions pertinentes pour qualifier "
    "votre problème et obtenir uniquement les informations réellement "
    "nécessaires ?":
        'Q7 Did the adviser ask relevant questions to qualify your problem and '
        'collect only the information genuinely needed?',
    "Q8 Le conseiller a-t-il reformulé ou validé sa compréhension lorsque cela "
    "était utile, en évitant que vous répétiez inutilement des informations "
    "déjà données ?":
        'Q8 Did the adviser rephrase or confirm their understanding where it '
        'helped, sparing you from needlessly repeating information you had '
        'already given?',
    'Score — Compréhension du besoin': 'Score — Understanding the need',

    # =================================================================
    # SECTION D — EXPERTISE & EXACTITUDE DE LA REPONSE
    # =================================================================
    'D. EXPERTISE & EXACTITUDE DE LA RÉPONSE':
        'D. EXPERTISE & ACCURACY OF THE ANSWER',
    "Q9 Le conseiller a-t-il démontré une bonne maîtrise des offres, services, "
    "procédures et parcours liés au scénario testé ?":
        'Q9 Did the adviser show a good command of the offers, services, '
        'procedures and journeys involved in the scenario tested?',
    "Q10 La réponse fournie par le conseiller était-elle correcte, précise, "
    "cohérente et exempte d'informations contradictoires ou manifestement "
    "erronées ?":
        'Q10 Was the answer given by the adviser correct, precise, consistent '
        'and free of contradictory or plainly wrong information?',
    "Q11 Les explications données vous ont-elles semblé simples, pédagogiques "
    "et adaptées, avec des étapes ou alternatives clairement présentées ?":
        'Q11 Did the explanations seem simple, instructive and well pitched, '
        'with the steps or alternatives clearly set out?',
    'Score — Expertise & exactitude de la réponse':
        'Score — Expertise & accuracy of the answer',

    # =================================================================
    # SECTION E — RESOLUTION / FCR & OWNERSHIP
    # =================================================================
    'E. RÉSOLUTION / FCR & OWNERSHIP': 'E. RESOLUTION / FCR & OWNERSHIP',
    "Q12 La réponse apportée par le conseiller était-elle concrète, exploitable "
    "et vous a-t-elle permis d'avancer immédiatement vers la résolution de "
    "votre besoin ?":
        'Q12 Was the answer given by the adviser concrete, usable, and did it '
        'let you move forward immediately towards resolving your need?',
    "Q13 Votre besoin a-t-il été résolu dès le premier contact ou, lorsque la "
    "résolution immédiate était impossible, la meilleure solution accessible au "
    "Call Center a-t-elle été effectivement mise en œuvre ?":
        'Q13 Was your need resolved at the first contact or, where immediate '
        'resolution was impossible, was the best solution available to the '
        'call centre actually put in place?',
    "Q14 Le conseiller a-t-il pris ownership de votre demande, en évitant les "
    "transferts, renvois ou abandons de prise en charge non justifiés ?":
        'Q14 Did the adviser take ownership of your request, avoiding '
        'unjustified transfers, referrals or dropped handling?',
    "Q15 En cas d'escalade ou de renvoi en agence, le motif, les prochaines "
    "étapes, les pièces éventuelles et le délai annoncé vous ont-ils semblé "
    "clairs et réalistes ?":
        'Q15 In the event of escalation or referral to a branch, did the '
        'reason, the next steps, any documents required and the timescale '
        'announced seem clear and realistic?',
    "Q16 Avant de clôturer l'appel, le conseiller a-t-il vérifié que la "
    "solution ou la suite du traitement était bien comprise et, en cas de "
    "non-résolution, vous a-t-il rassuré sans faire de promesse non maîtrisée ?":
        'Q16 Before closing the call, did the adviser check that the solution '
        'or the next stage of handling was properly understood and, where the '
        'matter was unresolved, reassure you without making a promise they '
        'could not keep?',
    'Score — Résolution / FCR & ownership': 'Score — Resolution / FCR & ownership',

    # =================================================================
    # SECTION F — EFFORT CLIENT & SIMPLICITE
    # =================================================================
    'F. EFFORT CLIENT & SIMPLICITÉ': 'F. CUSTOMER EFFORT & SIMPLICITY',
    "Q17 Le nombre d'étapes, d'informations demandées et de manipulations "
    "imposées au client vous a-t-il semblé limité au strict nécessaire ?":
        'Q17 Did the number of steps, pieces of information requested and '
        'actions imposed on the customer seem kept to the strict minimum?',
    "Q18 Les mises en attente, transferts et changements de canal ont-ils été "
    "minimisés et, lorsqu'ils étaient nécessaires, expliqués et justifiés de "
    "manière claire ?":
        'Q18 Were holds, transfers and changes of channel kept to a minimum '
        'and, where they were necessary, clearly explained and justified?',
    'Score — Effort client & simplicité': 'Score — Customer effort & simplicity',

    # =================================================================
    # SECTION G — EMPATHIE & CONFIANCE
    # =================================================================
    'G. EMPATHIE & CONFIANCE': 'G. EMPATHY & TRUST',
    "Q19 Le conseiller a-t-il reconnu de façon appropriée l'inconfort, "
    "l'urgence ou l'émotion que vous avez exprimés, notamment en situation de "
    "réclamation ?":
        'Q19 Did the adviser appropriately acknowledge the discomfort, urgency '
        'or emotion you expressed, particularly in a complaint situation?',
    "Q20 L'attitude du conseiller, la transparence de ses explications et le "
    "respect de la confidentialité vous ont-ils inspiré confiance et "
    "professionnalisme ?":
        'Q20 Did the manner of the adviser, the transparency of their '
        'explanations and their respect for confidentiality inspire trust and '
        'come across as professional?',
    'Score — Empathie & confiance': 'Score — Empathy & trust',

    # =================================================================
    # SECTION H — CLOTURE DE L'ENTRETIEN
    # =================================================================
    "H. CLÔTURE DE L'ENTRETIEN": 'H. CLOSING THE CALL',
    "Q21 Le conseiller a-t-il récapitulé brièvement la solution ou les "
    "prochaines étapes, en vérifiant qu'aucun point essentiel ne restait en "
    "suspens ?":
        'Q21 Did the adviser briefly recap the solution or the next steps, '
        'checking that no essential point was left hanging?',
    "Q22 La prise de congé du conseiller vous a-t-elle semblé courtoise, "
    "naturelle et professionnelle (remerciement ou souhait adapté), sans "
    "exigence artificielle de répétition de votre nom ?":
        'Q22 Did the way the adviser signed off seem courteous, natural and '
        'professional (a fitting thank-you or good wish), without artificially '
        'insisting on repeating your name?',
    "Q23 Le conseiller a-t-il informé le client qu'il recevra un sondage de "
    "satisfaction afin de partager son avis ?":
        'Q23 Did the adviser tell the customer that they would receive a '
        'satisfaction survey to share their opinion?',
    "Score — Clôture de l'entretien": 'Score — Closing the call',

    # =================================================================
    # SECTION I — MAITRISE DU SCENARIO
    # =================================================================
    # Les 106 criteres eux-memes sont traduits dans criteres_scenario.py et
    # verses plus bas : seuls l'intitule de la section, sa consigne et son
    # score sont ici.
    'I. MAÎTRISE DU SCÉNARIO': 'I. COMMAND OF THE SCENARIO',
    "Ces critères portent sur le **traitement technique du scénario que vous "
    "avez joué** : ce que le conseiller a effectivement vérifié, expliqué ou "
    "fait.\n\n"
    "Seuls ceux du scénario coché en page « Scénario joué » s'affichent, et "
    "ils se remplissent **comme les sections A à H**.":
        'These criteria cover the **technical handling of the scenario you '
        'played**: what the adviser actually checked, explained or did.\n\n'
        'Only those of the scenario ticked on the “Scenario played” page are '
        'shown, and they are filled in **like sections A to H**.',
    'Score — Maîtrise du scénario': 'Score — Command of the scenario',

    # =================================================================
    # ALERTES CRITIQUES
    # =================================================================
    "Violation ou exposition de données personnelles / défaut manifeste de "
    "confidentialité":
        'Breach or exposure of personal data / manifest failure of '
        'confidentiality',
    "Information manifestement erronée susceptible d'entraîner une perte "
    "financière ou un préjudice client":
        'Manifestly wrong information liable to cause a financial loss or harm '
        'to the customer',
    "Propos irrespectueux, agressifs, discriminatoires ou attitude "
    "manifestement non professionnelle":
        'Disrespectful, aggressive or discriminatory remarks, or manifestly '
        'unprofessional manner',
    "Promesse de délai / de traitement non maîtrisée ou engagement trompeur":
        'Unmastered promise of a timescale or of handling, or misleading '
        'commitment',
    "Transfert, renvoi en agence ou abandon de prise en charge manifestement "
    "non justifié":
        'Transfer, referral to a branch or dropped handling that is manifestly '
        'unjustified',

    # --- cas propres a la section A (accessibilite & serveur vocal)
    "Message d'accueil incohérent ou trompeur, ne correspondant pas aux "
    "services réellement proposés":
        'Inconsistent or misleading welcome message, not matching the services '
        'actually offered',
    "Menus du serveur vocal erronés ou non fonctionnels, entraînant une "
    "mauvaise orientation ou une impossibilité d'accès au conseiller":
        'Wrong or non-working IVR menus, leading to misrouting or making the '
        'advisor unreachable',
    "Absence ou dysfonctionnement du choix de langue, créant une barrière de "
    "communication pour le client":
        'Missing or faulty language choice, raising a communication barrier for '
        'the customer',
    "Boucle IVR bloquante ou confusion dans le parcours, empêchant le client "
    "d'obtenir une assistance humaine":
        'Blocking IVR loop or confusing path, preventing the customer from '
        'reaching human assistance',
    "Erreur de redirection ou coupure systématique avant mise en relation, "
    "générant une rupture de service":
        'Misrouting or systematic cut-off before connection, causing a service '
        'breakdown',
    "Temps d'attente excessif non signalé, ou absence de message d'information "
    "pendant la mise en relation":
        'Excessive waiting time left unannounced, or no information message '
        'while being connected',

    # --- cas propres a la dimension C (comprehension du besoin)
    "Interruption répétée ou inappropriée du client, empêchant l'expression "
    "complète du besoin":
        'Repeated or inappropriate interruption of the customer, preventing '
        'the need from being stated in full',
    "Absence totale d'écoute active : le conseiller ne manifeste aucun intérêt "
    "ou ne tient pas compte des propos du client":
        'No active listening at all: the advisor shows no interest or takes no '
        'account of what the customer says',
    "Questions non pertinentes ou hors sujet, traduisant une mauvaise "
    "qualification du problème":
        'Irrelevant or off-topic questions, reflecting poor qualification of '
        'the problem',
    "Absence de reformulation ou de validation, entraînant une mauvaise "
    "compréhension du motif d'appel":
        'No rephrasing or checking back, leading to a misunderstanding of the '
        'reason for the call',
    "Erreur manifeste d'interprétation du besoin, conduisant à une réponse ou "
    "une action inadaptée":
        'Manifest misreading of the need, leading to an unsuitable answer or '
        'action',
    "Demande du client ignorée ou détournée, sans justification ni "
    "orientation vers une solution appropriée":
        "Customer's request ignored or deflected, with no justification and no "
        'pointer to a suitable solution',

    # --- cas propres a Q9 (maitrise des offres, services et procedures)
    "Information fausse ou incohérente sur une offre ou un service":
        'False or inconsistent information about an offer or a service',
    "Procédure mal expliquée, entraînant une mauvaise orientation du client":
        'Procedure poorly explained, leading the customer the wrong way',
    "Promesse non maîtrisée : délai irréaliste ou engagement impossible à "
    "tenir":
        'Unmastered promise: an unrealistic timescale or a commitment that '
        'cannot be kept',

    # --- cas propres a Q10 (exactitude et coherence de la reponse)
    "Réponse contradictoire par rapport aux procédures officielles":
        'Answer contradicting the official procedures',
    "Erreur manifeste dans les informations fournies (tarifs, conditions, "
    "délais)":
        'Manifest error in the information given (prices, conditions, '
        'timescales)',
    "Engagement trompeur pouvant induire le client en erreur":
        'Misleading commitment liable to mislead the customer',

    # --- cas propres a Q11 (pedagogie et clarte des explications)
    "Explication confuse ou trop technique, incompréhensible pour le client":
        'Confusing or overly technical explanation, incomprehensible to the '
        'customer',
    "Absence d'étapes ou d'alternatives claires pour résoudre le problème":
        'No clear steps or alternatives for solving the problem',
    "Langage inadapté : jargon interne, termes non vulgarisés":
        'Unsuitable language: in-house jargon, terms not put in plain words',

    # =================================================================
    # SYNTHESE QUALITATIVE
    # =================================================================
    'Synthèse qualitative': 'Qualitative summary',
    'Q24 Quel est le principal point fort de cet appel ?':
        'Q24 What is the main strength of this call?',
    "Un fait précis, pas une appréciation générale.":
        'A specific fact, not a general impression.',
    'Q25 Quel est le principal irritant ou effort subi par le client ?':
        'Q25 What is the main irritant or effort borne by the customer?',
    "Ce qui a coûté du temps, une répétition ou une inquiétude au client.":
        'Whatever cost the customer time, a repetition or a worry.',
    'Q26 Le client devrait-il rappeler ou contacter un autre canal pour le '
    'même motif ?':
        'Q26 Would the customer have to call again or use another channel for '
        'the same reason?',
    'Q26 Pourquoi ?': 'Q26 Why?',
    "Ce qui reste à faire, et par quel canal le client devrait le faire.":
        'What is still outstanding, and through which channel the customer '
        'would have to do it.',

    # =================================================================
    # FIN DE L'EVALUATION
    # =================================================================
    "Fin de l'évaluation": 'End of the assessment',
    "**C'est terminé.** Vérifiez les questions marquées en rouge, puis "
    "enregistrez et envoyez le formulaire.":
        '**You are done.** Check any question flagged in red, then save and '
        'send the form.',
    # Libelle d'un `calculate` : jamais affiche, conserve pour l'export et le
    # tableau de bord.
    "Score total de l'appel": 'Total score for the call',

    # =================================================================
    # MODALITES
    # =================================================================
    'Oui, totalement conforme': 'Yes, fully compliant',
    'Partiellement conforme / perfectible':
        'Partially compliant / could be improved',
    'Non conforme': 'Not compliant',
    'Non applicable': 'Not applicable',
    'Oui': 'Yes',
    'Non': 'No',
    'Aucun renvoi': 'No referral',
    'Vers un autre canal (application, USSD, site, réseaux sociaux)':
        'To another channel (app, USSD, website, social media)',
    'Vers une agence': 'To a branch',
    'Vers un point de vente physique': 'To a physical outlet',
    'Français': 'French',
    'Anglais': 'English',
    'TEST - Interview non valide': 'TEST - Invalid interview',
    'Live - Interview valide': 'Live - Valid interview',
    # Marques et codes : repris tels quels dans les deux langues.
    'ORANGE': 'ORANGE',
    'MTN': 'MTN',
    '07h - 12h': '7am - 12pm',
    '12h - 18h': '12pm - 6pm',
    '18h - 22h': '6pm - 10pm',
    'S01 · Data / Réseau · Internet mobile très lent':
        'S01 · Data / Network · Very slow mobile internet',
    'S02 · Data / Forfait · Forfait acheté mais navigation impossible':
        'S02 · Data / Bundle · Bundle bought but browsing impossible',
    'S03 · Voix / Réseau · Appels qui coupent / voix dégradée':
        'S03 · Voice / Network · Calls dropping / degraded voice',
    'S04 · Data / Facturation · Forfait consommé trop rapidement':
        'S04 · Data / Billing · Bundle used up too quickly',
    'S05 · Crédit / Facturation · Débit inexpliqué du crédit':
        'S05 · Credit / Billing · Unexplained credit deduction',
    'S06 · VAS · Souscription / débit VAS non souhaité':
        'S06 · VAS · Unwanted VAS subscription / charge',
    "S07 · Forfait / Achat · Impossible d'acheter un forfait":
        'S07 · Bundle / Purchase · Unable to buy a bundle',
    'S08 · Digital · Application opérateur inaccessible':
        'S08 · Digital · Operator app unreachable',
    'S09 · Conseil / Vente · Choix du meilleur forfait':
        'S09 · Advice / Sales · Choosing the best bundle',
    "S10 · Conseil / Offre · Changement d'offre":
        'S10 · Advice / Offer · Changing offer',
    'S11 · SIM / Sécurité · SIM bloquée / PIN-PUK':
        'S11 · SIM / Security · Blocked SIM / PIN-PUK',
    'S12 · SIM / Sécurité · SIM perdue ou volée':
        'S12 · SIM / Security · SIM lost or stolen',
    "S13 · KYC · Problème d'identification de la ligne":
        'S13 · KYC · Line identification problem',
    'S14 · Réclamation · Réclamation récurrente non résolue':
        'S14 · Complaint · Recurring unresolved complaint',
    'S15 · Relationnel · Client mécontent et impatient':
        'S15 · Relationship · Unhappy and impatient customer',
    'S16 · Tarification · Information tarifaire simple':
        'S16 · Pricing · Simple pricing information',
    "S17 · Roaming · Préparation d'un voyage":
        'S17 · Roaming · Preparing for a trip',
    'S18 · Transfert / Partage · Transfert de crédit ou de data':
        'S18 · Transfer / Sharing · Transferring credit or data',
    'S19 · Mobile Money · Transaction débitée mais non reçue':
        'S19 · Mobile Money · Transaction debited but not received',
    'S20 · Mobile Money · Envoi au mauvais numéro':
        'S20 · Mobile Money · Sent to the wrong number',
    "S21 · Cycle de vie SIM · Réactivation d'une ligne inactive":
        'S21 · SIM life cycle · Reactivating a dormant line',
    'S22 · Réseau · Qualité réseau dans une localité précise':
        'S22 · Network · Network quality in a specific area',
    'S23 · Pédagogie · Client ne comprend pas les instructions':
        'S23 · Teaching · Customer does not understand the instructions',
    "S24 · Inclusion digitale · Client peu à l'aise avec le digital":
        'S24 · Digital inclusion · Customer not comfortable with digital',
    'S25 · Orientation / Réclamation · Demande hors périmètre du conseiller':
        "S25 · Guidance / Complaint · Request outside the adviser's remit",
}

# Les 106 criteres de la section I sont ecrits dans criteres_scenario.py,
# francais et anglais cote a cote : une paire de phrases se relit mieux ensemble
# qu'eclatee sur deux fichiers. Ils rejoignent la table generale pour que `en()`
# et le controle de couverture de build_form.py les voient comme les autres.
FR_EN.update(criteres_scenario.traductions())

# Textes de l'interface du guide enqueteur et du tableau de bord (hors
# questionnaire).
INTERFACE = {
    "Posée si c'est le scénario que vous avez joué":
        'Asked if this is the scenario you played',
    'Scénario': 'Scenario',

    # --- bandeau et compteurs
    "Questionnaire GHOST Check Call Center": 'GHOST Check call centre questionnaire',
    'Fiche de collecte enquêteur — Orange · MTN':
        'Auditor collection sheet — Orange · MTN',
    'Questions': 'Questions',
    'Étapes': 'Steps',
    'Terrain': 'Fieldwork',
    'Septembre 2026': 'September 2026',
    'renseignées': 'answered',
    'Réinitialiser': 'Reset',
    'Copier les réponses': 'Copy answers',
    'Récapitulatif': 'Summary',
    'Récapitulatif des réponses': 'Summary of answers',
    'Aucune réponse saisie pour le moment.': 'No answer entered yet.',
    '← Précédent': '← Previous',
    'Suivant →': 'Next →',
    'Étape': 'Step',
    'Progression du questionnaire': 'Questionnaire progress',
    "sur {n} au total, conditionnelles comprises — une étape ne se quitte "
    "qu'une fois complète":
        'of {n} in total, conditional ones included — a step is only left once '
        'it is complete',

    # --- etiquettes d'une question
    'Un seul choix': 'Single choice',
    'Choix multiple': 'Multiple choice',
    'Texte libre': 'Free text',
    'Nombre': 'Number',
    'Heure': 'Time',
    'Enregistrement': 'Recording',
    'Obligatoire': 'Required',
    'Facultatif': 'Optional',
    'Déduit — non saisi': 'Derived — not entered',
    'Valeur déduite :': 'Derived value:',
    'Cette réponse est obligatoire pour continuer.':
        'This answer is required in order to continue.',
    'Votre réponse…': 'Your answer…',
    "Enregistrement joint dans KoboCollect au moment de l'appel.":
        'Recording attached in KoboCollect at the time of the call.',

    # --- conditions d'affichage
    'Posée si ': 'Shown if ',
    ' et ': ' and ',
    ' ou ': ' or ',
    "Choisissez d'abord : ": 'Choose first: ',
    # Noms courts des champs cites dans les etiquettes « Posée si … ».
    'Escalade': 'Escalation',
    'Renvoi': 'Referral',
    'Mises en attente': 'Holds',
    'Transferts': 'Transfers',

    # =================================================================
    # TABLEAU DE BORD (suivi_collecte.html)
    # =================================================================
    # --- bandeau
    'Suivi de la collecte': 'Collection monitoring',
    'Audit des call center Orange · MTN — Cameroun':
        'Call centre audit — Orange · MTN — Cameroon',
    'Période': 'Period',
    'Projet Kobo': 'Kobo project',
    'Mise à jour': 'Updated',
    'non déployé': 'not deployed',

    # --- bandeau de donnees fictives
    'Données de démonstration': 'Demonstration data',

    # --- tuiles
    'Appels collectés': 'Calls collected',
    'Score total moyen': 'Average total score',
    'Résolution / FCR': 'Resolution / FCR',
    'Attente avant conseiller': 'Wait before the adviser',
    "Durée moyenne d'appel": 'Average call length',

    # --- titres de panneaux
    'Progression quotidienne': 'Daily progress',
    'Score par section et par opérateur': 'Score by section and by operator',
    'Critères les plus défaillants': 'Weakest criteria',
    'Appels par opérateur': 'Calls by operator',
    'Score total par opérateur': 'Total score by operator',
    'Toutes sections confondues': 'All sections combined',
    'Répartition des notes': 'Breakdown of the marks',
    'Toutes réponses des critères scorés, N/A compris':
        'Every answer to the scored criteria, N/A included',
    'Appels par tranche horaire': 'Calls by time slot',
    'Appels par enquêteur': 'Calls by auditor',
    'Dernières soumissions': 'Latest submissions',
    "Moyenne des points obtenus sur les points en jeu, en %. Un critère noté "
    "N/A, ou masqué parce que la situation ne s'est pas produite, sort du "
    "calcul au lieu de compter zéro.":
        'Average of the points obtained out of the points at stake, in %. A '
        'criterion scored N/A, or hidden because the situation did not arise, '
        'drops out of the calculation instead of counting as zero.',

    # --- intitules courts des sections (axes, legendes et tableaux)
    'Accessibilité & serveur vocal': 'Accessibility & voice server (IVR)',
    'Accueil & posture du conseiller': 'Greeting & adviser manner',
    'Compréhension du besoin': 'Understanding the need',
    'Expertise & exactitude de la réponse': 'Expertise & accuracy of the answer',
    'Résolution / FCR & ownership': 'Resolution / FCR & ownership',
    'Effort client & simplicité': 'Customer effort & simplicity',
    'Empathie & confiance': 'Empathy & trust',
    "Clôture de l'entretien": 'Closing the call',
    'Maîtrise du scénario': 'Command of the scenario',

    # --- conditions ecrites a la main (LIBELLE_SPECIAL du guide)
    "Posée si un renvoi a été indiqué": 'Shown if a referral was recorded',
    "Posée en cas d'escalade ou de renvoi":
        'Shown in the event of an escalation or a referral',

    'Obligatoire sous condition': 'Required under a condition',
    'Alertes critiques': 'Critical alerts',
    'Score par scénario': 'Score by scenario',
    'Famille': 'Family',
    'Afficher le détail par scénario': 'Show the breakdown by scenario',
    'Appels portant au moins une alerte critique, par cas signalé':
        'Calls carrying at least one critical alert, by reported case',
    'Confidentialité': 'Confidentiality',
    'Information erronée': 'Wrong information',
    'Propos irrespectueux': 'Disrespectful remarks',
    'Promesse non maîtrisée': 'Unmastered promise',
    'Abandon non justifié': 'Unjustified drop',
    "Accueil incohérent": 'Inconsistent welcome',
    'Menus erronés': 'Wrong menus',
    'Choix de langue': 'Language choice',
    'Boucle IVR': 'IVR loop',
    'Coupure avant mise en relation': 'Cut off before connection',
    'Attente non signalée': 'Unannounced wait',

    # --- legende de la repartition des notes
    '100 — totalement conforme': '100 — fully compliant',
    '50 — partiellement conforme': '50 — partially compliant',
    '0 — non conforme': '0 — not compliant',
    'N/A — non applicable': 'N/A — not applicable',

    # --- en-tetes de tableaux
    'Section': 'Section',
    'Intitulé': 'Title',
    'Score moyen': 'Average score',
    'Critères notés': 'Scored criteria',
    'Code': 'Code',
    'Critère': 'Criterion',
    'Appels': 'Calls',
    'Enquêteur': 'Auditor',
    'Opérateur': 'Operator',
    'Attente (s)': 'Wait (s)',
    'Durée (min)': 'Length (min)',
    'Score': 'Score',
    'Réponses': 'Answers',

    # --- depliants
    'Afficher le score moyen de chaque section':
        'Show the average score for each section',
    'Afficher le détail chiffré': 'Show the detailed figures',
    'Afficher le détail par section': 'Show the breakdown by section',

    # --- badges de gravite
    'Critique': 'Critical',
    'Sérieux': 'Serious',
    'À surveiller': 'To watch',

    # --- etats vides et valeurs manquantes
    'Non renseigné': 'Not specified',
    'Non renseignée': 'Not specified',
    'Aucune donnée.': 'No data.',
    'Aucun appel enregistré.': 'No call recorded.',
    'Aucune réponse.': 'No answer.',
    'appels': 'calls',
    'réponses': 'answers',
    'Tableau de bord bilingue — le choix de langue est conservé dans ce navigateur.':
        'Bilingual dashboard — the language choice is kept in this browser.',
}

# Messages construits par le navigateur : cle -> (francais, anglais).
JS_TEXTES = {
    'manque': ("Répondez d'abord aux {n} question(s) obligatoire(s) de cette étape.",
               'Answer the {n} required question(s) on this step first.'),
    'complet': ('Questionnaire complet. Reportez-le dans KoboCollect.',
                'Questionnaire complete. Enter it in KoboCollect.'),
    'verrou': ("Étape verrouillée : terminez d'abord les étapes précédentes.",
               'Step locked: complete the previous steps first.'),
    'confirm_raz': ('Effacer toutes les réponses saisies sur cet appareil ?',
                    'Erase every answer entered on this device?'),
    'efface': ('Réponses effacées.', 'Answers cleared.'),
    'copie_ok': ('Réponses copiées dans le presse-papiers.',
                 'Answers copied to the clipboard.'),
    'copie_ko': ('Copie impossible sur cet appareil.',
                 'Copying is not available on this device.'),
    'entete_copie': ('QUESTIONNAIRE GHOST CHECK CALL CENTER — MDS JOB 002/26',
                     'GHOST CHECK CALL CENTRE QUESTIONNAIRE — MDS JOB 002/26'),
    'reste_1': ('Il reste 1 réponse obligatoire à renseigner sur cette étape.',
                '1 required answer is still missing on this step.'),
    'reste_n': ('Il reste {n} réponses obligatoires à renseigner sur cette étape.',
                '{n} required answers are still missing on this step.'),
    # Une reponse peut etre presente ET FAUSSE : le message le dit au moment du
    # changement d'etape, la ou l'erreur a ete commise.
    'corriger_1': ('1 réponse de cette étape est à corriger avant de continuer.',
                   '1 answer on this step must be corrected before you '
                   'continue.'),
    'corriger_n': ('{n} réponses de cette étape sont à corriger avant de '
                   'continuer.',
                   '{n} answers on this step must be corrected before you '
                   'continue.'),
    'terminer': ('Terminer', 'Finish'),
    'voir_recap': ('Voir le récapitulatif', 'See the summary'),
    'suivant': ('Suivant', 'Next'),
    'jours': ('Lun Mar Mer Jeu Ven Sam Dim', 'Mon Tue Wed Thu Fri Sat Sun'),
    'bouton_langue': ('English', 'Français'),
    'titre_langue': ('Afficher le questionnaire en anglais',
                     'Afficher le questionnaire en français'),
    # Le tableau de bord partage le libelle du bouton, pas son infobulle.
    'titre_langue_dash': ('Afficher le tableau de bord en anglais',
                          'Afficher le tableau de bord en français'),
}

# Aucun libelle compose sur ce questionnaire (le JOB 001/26 en avait pour son
# tableau Q17 Bis). La mecanique est conservee pour rester interchangeable.
SUFFIXES = {}


def en(fr):
    """Version anglaise d'un libelle ; le francais a defaut de traduction."""
    directe = FR_EN.get(fr) or INTERFACE.get(fr)
    if directe:
        return directe
    for suffixe, traduit in SUFFIXES.items():
        if fr.endswith(suffixe):
            base = fr[: -len(suffixe)]
            return (FR_EN.get(base) or base) + traduit
    return fr


def couverte(fr):
    """Vrai si le libelle a une traduction, directe ou par composition."""
    return (fr in FR_EN or fr in INTERFACE
            or any(fr.endswith(s) for s in SUFFIXES))


def js(cle, langue):
    """Message dynamique du guide, en francais ('fr') ou en anglais ('en')."""
    return JS_TEXTES[cle][0 if langue == "fr" else 1]
