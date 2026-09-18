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
    "**LISEZ CES CONSIGNES AVANT DE COMMENCER L'ÉVALUATION.**":
        '**READ THESE INSTRUCTIONS BEFORE STARTING THE ASSESSMENT.**',

    "**1. PRINCIPES D'UTILISATION**\n\n"
    "• **Un seul scénario par appel.** Le questionnaire est renseigné "
    "immédiatement après avoir raccroché.\n"
    "• Les données factuelles (**temps d'attente, durée, transferts, mises en "
    "attente**) sont collectées séparément du score comportemental.\n"
    "• Pour les critères évalués, quatre réponses : **totalement conforme**, "
    "**partiellement conforme / perfectible**, **non conforme**, **non "
    "applicable**. Le formulaire les convertit lui-même en score : vous n'avez "
    "aucun chiffre à manipuler.\n"
    "• Les **questions conditionnelles** ne sont renseignées que lorsque la "
    "situation se produit (**mise en attente, escalade, renvoi en agence, "
    "etc.**).\n"
    "• **Tout « non conforme »** ou **toute situation exceptionnelle** doit "
    "être étayé par un fait observé ou une formulation exacte du "
    "conseiller.\n"
    "• **Le score final** mesure la performance de l'expérience par opérateur "
    "et par scénario ; il ne doit pas être utilisé isolément comme mesure de "
    "performance individuelle d'un conseiller.\n"
    "• Cible de complétion post-appel : **médiane ≤ 5 minutes** après "
    "calibrage et paramétrage de la logique conditionnelle.":
        "**1. PRINCIPLES OF USE**\n\n"
        '• **One scenario per call only.** The questionnaire is filled in '
        'immediately after hanging up.\n'
        '• The factual data (**waiting time, length, transfers, holds**) are '
        'collected separately from the behavioural score.\n'
        '• For the criteria being assessed, four answers: **fully compliant**, '
        '**partially compliant / could be improved**, **not compliant**, **not '
        'applicable**. The form turns them into a score itself: you have no '
        'figure to handle.\n'
        '• **Conditional questions** are only filled in when the situation '
        'arises (**hold, escalation, referral to a branch, etc.**).\n'
        '• **Every “not compliant”**, and **every exceptional situation**, must '
        "be backed up by an observed fact or the adviser's exact wording.\n"
        '• **The final score** measures the performance of the experience by '
        'operator and by scenario; it must not be used on its own as a measure '
        "of an individual adviser's performance.\n"
        '• Target post-call completion time: **median ≤ 5 minutes**, once the '
        'conditional logic has been calibrated and set up.',

    "**2. REPÈRES POUR LE CALIBRAGE**\n\n"
    "• La notation doit porter sur ce qui a **effectivement été observé et "
    "entendu** pendant l'appel, pas sur ce que l'enquêteur pense que le "
    "conseiller aurait dû faire en dehors du scénario.\n"
    "• Un critère n'est **non applicable** que s'il n'a réellement pas pu être "
    "observé ou ne s'appliquait pas au parcours.\n"
    "• **Partiellement conforme** doit décrire une conformité partielle "
    "**concrète** : "
    "réponse correcte mais incomplète, personnalisation mécanique, explication "
    "partiellement claire, ownership partiel, etc.\n"
    "• Le **FCR** ne signifie pas nécessairement que toute opération "
    "back-office soit achevée pendant l'appel : il mesure si le client "
    "obtient, dès ce contact, la résolution accessible ou une prise en charge "
    "complète et fiable ne nécessitant pas un nouvel effort évitable.\n"
    "• Les **verbatims exacts** sont à privilégier uniquement lorsqu'ils "
    "illustrent un point exceptionnel, un irritant majeur ou une alerte "
    "critique.":
        '**2. CALIBRATION GUIDANCE**\n\n'
        '• Scoring must cover what was **actually observed and heard** during '
        'the call, not what the auditor thinks the adviser should have done '
        'outside the scenario.\n'
        '• A criterion is **not applicable** only if it genuinely could not be '
        'observed or did not apply to the journey.\n'
        '• **Partially compliant** must describe **concrete** partial '
        'compliance: a '
        'correct but incomplete answer, mechanical personalisation, a '
        'partially clear explanation, partial ownership, and so on.\n'
        '• **FCR** does not necessarily mean that every back-office operation '
        'is completed during the call: it measures whether the customer '
        'obtains, from this contact onwards, the resolution available or a '
        'complete and reliable handling that does not require further '
        'avoidable effort.\n'
        '• **Exact verbatims** are to be favoured only when they illustrate an '
        'exceptional point, a major irritant or a critical alert.',

    "**3. DANS CE FORMULAIRE**\n\n"
    "• Les questions non applicables sont **masquées automatiquement** : "
    "renseignez d'abord les « Mesures », le formulaire ouvre ensuite ce qui "
    "s'applique à cet appel. Une question masquée sort du calcul du score.\n"
    "• Un **non applicable** sort du calcul lui aussi : il ne vaut pas « non "
    "conforme ».\n"
    "• Un **non conforme** ouvre **deux champs** : l'**alerte critique** "
    "éventuelle, puis le **commentaire obligatoire**. Qualifiez avant de "
    "décrire ; si le constat n'est pas une alerte, cochez « Aucune alerte "
    "critique ».\n"
    "• Les **alertes critiques** n'entrent pas dans le score. La page qui leur "
    "est consacrée ne recueille que celles qu'aucun critère non conforme ne "
    "porte.\n"
    "• **Aucune note ne s'affiche pendant la saisie** : le formulaire calcule "
    "tout en arrière-plan et n'affiche le **score de l'appel** qu'à la dernière "
    "page. Vous décrivez ce que vous avez entendu, vous n'additionnez rien.":
        '**3. IN THIS FORM**\n\n'
        '• Questions that do not apply are **hidden automatically**: fill in '
        'the “Measurements” page first, and the form then opens whatever applies to '
        'this call. A hidden question drops out of the score.\n'
        '• A **not applicable** drops out of the calculation too: it does not '
        'count as “not compliant”.\n'
        '• A **not compliant** opens **two fields**: the **critical alert**, if '
        'any, then the **mandatory comment**. Qualify before describing; if '
        'the finding is not an alert, tick “No critical alert”.\n'
        '• **Critical alerts** do not enter the score. The page devoted to '
        'them only collects those that no criterion marked not compliant '
        'carries.\n'
        '• **No mark is shown while you fill the form in**: the form works '
        'everything out in the background and only shows the **score for the '
        'call** on the last page. You describe what you heard; you add nothing '
        'up.',

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
    'Renvoi vers un autre canal (application, USSD, site, réseaux sociaux)':
        'Referral to another channel (app, USSD, website, social media)',
    "Le conseiller a-t-il invité le client à poursuivre sur un canal "
    "numérique plutôt qu'au téléphone ?":
        'Did the adviser invite the customer to carry on through a digital '
        'channel rather than by phone?',
    'Renvoi en agence ou point de vente physique':
        'Referral to a branch or physical outlet',
    "Le conseiller a-t-il invité le client à se déplacer ?":
        'Did the adviser invite the customer to travel there in person?',
    "Préciser le canal ou l'agence indiqués":
        'Specify the channel or branch given',
    'Escalade : le dossier a-t-il été transmis à un autre service ou un rappel '
    'a-t-il été promis ?':
        'Escalation: was the case passed on to another department, or was a '
        'call-back promised?',
    "Question d'aiguillage : avec le renvoi, elle commande la question Q15":
        'Routing question: together with the referral, it drives question Q15',

    # =================================================================
    # ALERTE PUIS COMMENTAIRE OBLIGATOIRES SUR LES CRITERES NON CONFORMES
    # =================================================================
    "Non conforme — ce constat relève-t-il d'un cas d'alerte critique ?":
        'Not compliant — does this finding amount to a critical alert case?',
    "À renseigner avant le commentaire. Plusieurs cas peuvent être cochés ; "
    "« Aucune alerte critique » si le constat n'est pas une alerte.":
        'To be filled in before the comment. Several cases can be ticked; '
        '“No critical alert” if the finding is not an alert.',
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
    "Seuls ceux du scénario coché en page « Scénario joué » s'affichent. Ils "
    "prennent la **même échelle** que les sections A à H et comptent dans le "
    "**même score**.":
        'These criteria cover the **technical handling of the scenario you '
        'played**: what the adviser actually checked, explained or did.\n\n'
        'Only those of the scenario ticked on the “Scenario played” page are '
        'shown. They use the **same scale** as sections A to H and count '
        'towards the **same score**.',
    'Score — Maîtrise du scénario': 'Score — Command of the scenario',

    # =================================================================
    # ALERTES CRITIQUES
    # =================================================================
    'Alertes critiques — à signaler obligatoirement':
        'Critical alerts — must be reported',
    "**Principe.** Une alerte critique doit être **décrite factuellement**, "
    "même si le score global de l'appel reste élevé. Elle fait l'objet d'une "
    "analyse séparée et d'un commentaire obligatoire, et n'entre pas dans le "
    "calcul du score.\n\n"
    "Les alertes déjà cochées sur un critère **non conforme** sont remontées : "
    "**ne les répétez pas ici.** Cette page ne recueille que les cas observés "
    "**en dehors d'un critère non conforme**.":
        '**Principle.** A critical alert must be **described factually**, even '
        'if the overall score for the call remains high. It is analysed '
        'separately and calls for a mandatory comment, and does not enter the '
        'score calculation.\n\n'
        'Alerts already ticked on a criterion marked **not compliant** are '
        'reported: **do not repeat them here.** This page only collects cases '
        'observed **outside a criterion marked not compliant**.',
    "Autres cas d'alerte critique observés pendant cet appel":
        'Other critical alert cases observed during this call',
    "Hors de ceux déjà signalés sur un critère non conforme. Plusieurs cas "
    "peuvent être cochés. Cocher « Aucune alerte critique » si aucun autre "
    "ne s'est produit.":
        'Excluding those already reported on a criterion marked not compliant. '
        'Several cases can be ticked. Tick “No critical alert” if no other one '
        'occurred.',
    "« Aucune alerte critique » ne peut pas être cochée en même temps qu'une "
    "alerte.":
        '“No critical alert” cannot be ticked at the same time as an alert.',
    "Alerte critique — décrivez les faits observés, avec la formulation exacte "
    "du conseiller.":
        'Critical alert — describe the facts observed, with the exact wording '
        'used by the adviser.',
    "Obligatoire dès qu'une alerte est cochée. Décrire ce qui s'est produit, "
    "pas ce qui aurait dû se produire. Sous « Aucune alerte critique » le "
    "champ reste ouvert mais facultatif : servez-vous-en pour un manquement "
    "grave qui n'entre dans aucun des cas listés.":
        'Required as soon as an alert is ticked. Describe what happened, not '
        'what should have happened. Under “No critical alert” the field stays '
        'open but optional: use it for a serious failing that fits none of the '
        'cases listed.',
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
    'Aucune alerte critique': 'No critical alert',

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

    # =================================================================
    # SYNTHESE QUALITATIVE
    # =================================================================
    'Synthèse qualitative': 'Qualitative summary',
    'Q23 Quel est le principal point fort de cet appel ?':
        'Q23 What is the main strength of this call?',
    "Un fait précis, pas une appréciation générale.":
        'A specific fact, not a general impression.',
    'Q24 Quel est le principal irritant ou effort subi par le client ?':
        'Q24 What is the main irritant or effort borne by the customer?',
    "Ce qui a coûté du temps, une répétition ou une inquiétude au client.":
        'Whatever cost the customer time, a repetition or a worry.',
    'Q25 Le client devrait-il rappeler ou contacter un autre canal pour le '
    'même motif ?':
        'Q25 Would the customer have to call again or use another channel for '
        'the same reason?',
    'Q25 Pourquoi ?': 'Q25 Why?',
    "Ce qui reste à faire, ou ce qui rend un nouveau contact inutile.":
        'What is still outstanding, or what makes a further contact '
        'unnecessary.',

    # =================================================================
    # SCORE DE L'APPEL
    # =================================================================
    "Score de l'appel": 'Score for the call',
    "Résultat de l'appel, calculé par le formulaire : rien à saisir. Le score "
    "est la part des points obtenus sur les points réellement en jeu — un "
    "critère **non applicable**, ou masqué parce que la situation ne s'est pas "
    "produite, n'entre ni au numérateur ni au dénominateur.":
        "Result for the call, calculated by the form: nothing to enter. The "
        'score is the share of the points obtained out of the points actually '
        'at stake — a criterion that is **not applicable**, or hidden because '
        'the situation did not arise, enters neither the numerator nor the '
        'denominator.',
    "Score total de l'appel": 'Total score for the call',
    'sur 100, toutes sections confondues': 'out of 100, across all sections',

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
    'Renvoi / autre canal': 'Referral / another channel',
    'Renvoi en agence': 'Referral to a branch',
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
    'Toutes réponses des 22 critères scorés, N/A compris':
        'Every answer to the 22 scored criteria, N/A included',
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

    # --- alertes critiques
    "Posée dès que les alertes critiques sont renseignées":
        'Shown as soon as the critical alerts question is answered',
    "Obligatoire si une alerte est cochée": 'Required if an alert is ticked',
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
