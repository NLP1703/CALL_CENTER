# Questionnaire GHOST Check Call Center — MDS JOB 002/26

Questionnaires de référence :

- **PDF MDS v1.0 « Questionnaire GHOST Check CALL CENTER », septembre 2026**
  (7 pages : consignes, identification, mesures, sections A à H, synthèse
  qualitative) ;
- **Annexe « LISTE DES SCENARII GHOST CHECK CALL », septembre 2026** — les 25
  scénarios de référence, `S01` à `S25` ;
- **Annexe « Scénarios finaux — Questionnaire Ghost Check Call »** — pour chacun
  de ces 25 scénarios, les **3 à 5 critères propres à son traitement**, soit 106
  critères. Ils forment la section I.

Projet **MS Ghost Check** : audit client mystère des call center **Orange et
MTN** au Cameroun, collecté avec KoboCollect. Le questionnaire est **bilingue**
(français par défaut, anglais au choix) et **noté** : le formulaire calcule
lui-même le score de chaque section et le score total de l'appel.

Ce projet reprend l'architecture du **JOB 001/26** (audit des agences) :
`theme.py` et `kobo.py` en sont repris tels quels, `build_guide.py` en est
l'extension. Les conventions de nommage et les règles de construction sont les
mêmes, ce qui permet d'empiler les deux collectes dans la même base.

> **Cette version remplace intégralement le questionnaire de la v1.0
> précédente** (sections A à F puis J, 38 questions en Oui / Non). Le
> questionnaire de septembre 2026 est plus court, mieux noté et entièrement
> conditionnel : 22 critères de comportement plus les 3 à 5 critères du
> scénario joué, tous sur la même échelle, les données
> factuelles collectées à part, une qualification d'alerte critique suivie d'un
> commentaire obligatoire sur les seuls 0, et des alertes critiques hors score.
> **Le formulaire déployé doit être redéployé** — voir *Redéploiement*.

## Projet KoboToolbox

| | |
|---|---|
| Serveur | `https://kf.kobotoolbox.org` |
| Compte | `mds_cmr` |
| UID du projet | `aMrWStmZLSCTA4yuaBZhxF` |
| Édition | https://kf.kobotoolbox.org/#/forms/aMrWStmZLSCTA4yuaBZhxF |
| Lien de collecte | https://ee.kobotoolbox.org/52lAclB6 |

Bilingue dès le premier import (`Français (fr)` par défaut, `English (en)`),
logo MDS attaché. **Cocher `Type d'interview = TEST`** tant que le terrain n'a
pas commencé, les interviews de test étant écartées à l'analyse.

### Redéploiement

Le questionnaire de septembre 2026 change la **totalité** des variables notées :
`Q1`…`Q22` ne portent plus les mêmes intitulés, l'échelle passe de Oui / Non à
100 / 50 / 0 / N/A, et les variables `Q23`…`Q38`, `Q1a`, `Q1b`, `*_Bis` du
questionnaire précédent disparaissent.

**Fait le 11/09/2026.** Le projet comptait **0 soumission** : il a été
redéployé sur place, sans perte. Version déployée `vPLFd965xoSjhXjv4Tw3sw` —
119 lignes de formulaire, 25 scénarios, deux langues nommées, logo toujours
attaché. Le lien de collecte est inchangé.

**Redéployé le 15/09/2026** pour l'ajout de `Q<n>_ALERTE` — la qualification
d'alerte critique posée sur chaque 0, voir *Sur un 0 : qualifier, puis décrire*.
Changement **purement additif** : aucun nom de variable existant ne bouge, seul
le libellé d'`ALERTES` change, et les 22 nouvelles colonnes apparaissent vides
sur les soumissions antérieures. Les **3 soumissions** présentes — toutes
`TYPE_INTERVIEW = test` — ont été sauvegardées dans
`data/soumissions_avant_alertes.json` puis conservées en place. Version déployée
`vVLYJ5cAVYzVGxPTrkszFV` — 141 lignes de formulaire, deux langues nommées, logo
toujours attaché, lien de collecte inchangé. Classeur validé hors ligne par
pyxform 4.5.0 avant l'envoi.

**Redéployé le 16/09/2026** pour deux retouches demandées par MDS : la modalité
`autre` dans la liste des alertes critiques (voir *Alertes critiques*) et le
**numéro en tête des 106 libellés de scénario** (voir *I. Les critères propres au
scénario*). Changement **additif là aussi** : aucun nom de variable ne bouge,
aucune modalité existante ne change de code — seuls des libellés s'allongent et
une case s'ajoute. Les **5 soumissions** présentes — 4 `TYPE_INTERVIEW = test`
et **1 `live`**, du 16/09/2026 — ont été sauvegardées dans
`data/soumissions_avant_numerotation.json` puis conservées en place : elles
gardent leurs réponses, les libellés ayant seuls changé. Version
déployée `vQvWs9Sy4njr3755KZyiFK` — 511 lignes de formulaire, deux langues
nommées, logo toujours attaché, lien de collecte inchangé
(`https://ee.kobotoolbox.org/52lAclB6`). Classeur validé hors ligne par pyxform
4.5.0 avant l'envoi.

**Redéployé une seconde fois le 16/09/2026** pour les retouches de la page
« Mesures » : le
renvoi scindé en `RENVOI_CANAL` (autre canal) et `RENVOI_AGENCE` (agence), ces
deux cases et `ESCALADE` n'étant plus posées que si `NB_TRANSFERTS > 0`.
**Une colonne s'ajoute** (`RENVOI_AGENCE`) et **`RENVOI_CANAL` change de sens** —
« canal ou agence » avant ce déploiement, « canal » seul après : voir le point
ouvert 11. Les **5 soumissions** présentes ont été sauvegardées dans
`data/soumissions_avant_renvoi_escalade.json` puis conservées en place. Version
déployée `v4BjBXEXvq2ohBMu42Ry9x` — 512 lignes de formulaire, deux langues
nommées, logo toujours attaché, lien de collecte inchangé
(`https://ee.kobotoolbox.org/52lAclB6`). Classeur validé hors ligne par pyxform
4.5.0 avant l'envoi.

**Redéployé le 17/09/2026** pour les **six cas d'alerte propres à la section A**
(accessibilité & serveur vocal), proposés sur `Q1_ALERTE`, `Q2_ALERTE` et
`Q3_ALERTE` **seulement** — voir *La section A a sa propre liste*. **Aucun nom de
variable ne bouge et aucune question ne s'ajoute** : seuls ces trois champs
changent de liste de choix. Les **6 soumissions** présentes — 5
`TYPE_INTERVIEW = test` et 1 `live`, du 16/09/2026 — ont été sauvegardées dans
`data/soumissions_avant_alertes_section_a.json` puis conservées en place.

> **Deux soumissions portent d'anciens codes sur Q1–Q3** : la `live`
> (`Q1_ALERTE = irrespect`, `Q2_ALERTE = irrespect`, `Q3_ALERTE = abandon`) et
> une `test` (`Q1_ALERTE = abandon`). Ces codes ne font plus partie de la liste
> de la section A : les valeurs restent en base et `alertes_de()` les compte
> toujours — elle lit les codes tels qu'ils arrivent — mais elles n'ont plus de
> libellé dans les exports Kobo, et rouvrir l'une de ces soumissions dans
> Enketo en viderait le champ. Ne pas les réenregistrer. Ce cas illustre le
> motif du changement : l'enquêteur n'avait aucune case adaptée pour ce qu'il
> avait constaté sur le serveur vocal.

Version déployée `viyvQph92SXFRm9kmXKkqM` — 512 questions, deux langues nommées,
logo toujours attaché, lien de collecte inchangé
(`https://ee.kobotoolbox.org/52lAclB6`). Classeur validé hors ligne par pyxform
4.5.0 (0 avertissement) avant l'envoi, et le formulaire déployé contrôlé après :
`Q1`–`Q3_ALERTE` pointent bien sur `alertes_a`, `Q4_ALERTE` sur `alertes`.

**Redéployé le 18/09/2026** pour le **retrait de la modalité `autre`** des deux
listes d'alerte, et pour le **commentaire de la page 13 ouvert — mais facultatif
— sous « Aucune alerte critique »** qui la remplace : voir *Alertes critiques*.
**Aucun nom de variable ne bouge et aucune question ne s'ajoute** : `ALERTES_COM`
change de `relevant` et prend un `required` conditionnel, les deux listes perdent
une modalité. Les **7 soumissions** présentes — 6 `TYPE_INTERVIEW = test` et 1
`live` — ont été sauvegardées dans `data/soumissions_avant_retrait_autre.json`
puis conservées en place.

> **Une soumission porte le code retiré** : un `test` du 16/09/2026
> (`S24_1_ALERTE = autre`, commentaire `kjkjkjk`). Comme pour les codes de la
> section A, la valeur reste en base et `alertes_de()` la compte toujours, mais
> elle n'a plus de libellé dans les exports Kobo et rouvrir la soumission dans
> Enketo en viderait le champ. Aucune soumission `live` n'est touchée.

Version déployée `vJX7rtf3zgnmCSvyFtVwpA` — 512 questions, deux langues nommées,
logo toujours attaché, lien de collecte inchangé
(`https://ee.kobotoolbox.org/52lAclB6`). Classeur validé hors ligne par pyxform
4.5.0 (0 avertissement) avant l'envoi, et le formulaire déployé contrôlé après :
les deux listes s'arrêtent à `aucune`, et `ALERTES_COM` porte bien
`required = not(selected(${ALERTES}, 'aucune'))` pour
`relevant = ${ALERTES} != ''`.

**Redéployé le 18/09/2026** pour la **tranche horaire déduite de l'heure de
début** : voir *La tranche horaire se déduit de l'heure de début*. **Aucun nom
de variable ne bouge et aucune question ne s'ajoute** : `TRANCHE_HORAIRE` passe
de case cochée à champ calculé (`calculation` + `readonly`, toujours un
`select_one` sur la même liste), et `HEURE_DEBUT` prend un hint. Les **7
soumissions** présentes — 6 `TYPE_INTERVIEW = test` et 1 `live` — ont été
sauvegardées dans `data/soumissions_avant_tranche_deduite.json` puis conservées
en place.

> **Trois tranches cochées contredisent leur propre heure de début**, dont la
> seule `live` : `18:30` → `12h - 18h` (id 865562758), `19:45` → `12h - 18h`
> (id 870018388, `live`), `15:18` → `07h - 12h` (id 870880152). Les valeurs
> restent en base telles qu'elles ont été saisies. Rouvrir une de ces
> soumissions dans Enketo **recalculerait** le champ et écraserait la valeur —
> cette fois dans le bon sens, mais c'est une modification de donnée. Ne pas
> les réenregistrer sans le vouloir. Ce contrôle est le motif du changement :
> trois erreurs sur sept sur un champ que l'heure saisie donnait déjà.

Version déployée `vn5Czj5TK3rCYJbdNsPwEz` — 512 questions, deux langues nommées,
logo toujours attaché, lien de collecte inchangé
(`https://ee.kobotoolbox.org/52lAclB6`). Classeur validé hors ligne par pyxform
4.5.0 (0 avertissement) avant l'envoi, et le formulaire déployé contrôlé après :
`TRANCHE_HORAIRE` est bien `select_one tranche_horaire` + `readonly`, avec le
`calculation` attendu sur `HEURE_DEBUT`.

Pour toute mise à jour ultérieure, vérifier d'abord le compteur de soumissions
(`python kobo.py list`) : s'il existe des soumissions à conserver, les exporter
(`python kobo.py export <uid>`) ou créer un nouveau projet, car un changement de
variable rend les anciennes colonnes inexploitables.

```bash
python build_form.py
python test_scores.py
python kobo.py redeploy aMrWStmZLSCTA4yuaBZhxF questionnaire_audit_call_center.xlsx
python kobo.py langues aMrWStmZLSCTA4yuaBZhxF   # contrôle des langues, voir plus bas
python kobo.py media aMrWStmZLSCTA4yuaBZhxF     # contrôle du logo attaché
```

## Fichiers

| Fichier | Rôle |
|---|---|
| `build_form.py` | Construit le XLSForm et `form_structure.json` |
| `traductions.py` | Version anglaise de tous les libellés (questionnaire + interface) |
| `questionnaire_audit_call_center.xlsx` | XLSForm à déployer (69 questions saisies, 15 pages, FR + EN) |
| `theme.py` | Identité visuelle MDS (couleurs du logo, bandeau, logo embarqué) |
| `logo_mds_blanc.txt` / `logo_mds_couleur.txt` | Logo MDS en data URI |
| `build_guide.py` | Génère `guide_enqueteur.html` (questionnaire remplissable, score en direct, bouton FR / EN) |
| `build_correspondance.py` | Génère `correspondance_variables.xlsx` (noms de variables à valider) |
| `correspondance_variables.xlsx` | Nom exporté de chaque question ; lignes jaunes = nom déduit, à valider par MDS |
| `build_dashboard.py` | Génère `suivi_collecte.html` depuis l'API Kobo |
| `test_scores.py` | Rejoue les calculs de score du formulaire et vérifie 14 cas |
| `kobo.py` | Client CLI : `list`, `deploy`, `redeploy`, `info`, `media`, `langues`, `data`, `export` |
| `media/mds_logo.png` | Logo attaché au formulaire, affiché en tête dans KoboCollect |
| `.env` | `KOBO_URL` + `KOBO_TOKEN` — **jamais versionné** (`.env.example` sert de modèle) |

## Utilisation

```bash
pip install -r requirements.txt
cp .env.example .env        # puis renseigner KOBO_TOKEN

# Construire le questionnaire, puis vérifier son barème
python build_form.py
python test_scores.py

# Attacher ou remplacer une image du formulaire (sans argument : liste les médias)
python kobo.py media aMrWStmZLSCTA4yuaBZhxF media/mds_logo.png

# Récupérer les données
python kobo.py data aMrWStmZLSCTA4yuaBZhxF      # JSON brut
python kobo.py export aMrWStmZLSCTA4yuaBZhxF    # export XLS Kobo

# Regénérer les livrables
python build_correspondance.py
python build_guide.py
python build_dashboard.py               # l'UID déployé est la valeur par défaut
```

`build_dashboard.py` interroge Kobo ; tant que le projet ne compte aucune
soumission, il produit un jeu de **démonstration** signalé en clair sur la page.

## Structure du questionnaire

15 pages, 69 questions saisies, 11 champs déduits.

| Page | Contenu | Noté |
|---|---|---|
| 1 | Consignes : **1.** principes d'utilisation · **2.** repères pour le calibrage · **3.** dans ce formulaire — puis type d'interview | — |
| 2 | Identification de l'enquêteur (nom, opérateur, date, horaires, langue, conseiller) — jour de la semaine et **tranche horaire déduits** | — |
| 3 | **Mesures** : attente avant conseiller, durée de l'appel, mises en attente, transferts, puis — *sur transfert seulement* — renvoi canal, renvoi agence, escalade | — |
| 4 | **Scénario joué** — `S01` à `S25` | — |
| 5 | **A.** Accessibilité & serveur vocal — Q1 à Q3 | 3 |
| 6 | **B.** Accueil & posture du conseiller — Q4, Q5 | 2 |
| 7 | **C.** Compréhension du besoin — Q6 à Q8 | 3 |
| 8 | **D.** Expertise & exactitude de la réponse — Q9 à Q11 | 3 |
| 9 | **E.** Résolution / FCR & ownership — Q12 à Q16 | 5 |
| 10 | **F.** Effort client & simplicité — Q17, Q18 | 2 |
| 11 | **G.** Empathie & confiance — Q19, Q20 | 2 |
| 12 | **H.** Clôture de l'entretien — Q21, Q22 | 2 |
| 13 | **Alertes critiques** — les cas observés hors d'un critère noté 0 | — |
| 14 | Synthèse qualitative — Q23 à Q25 | — |
| 15 | Score de l'appel (calculé) | — |

### La page de consignes suit les principes MDS

Elle est découpée en trois blocs numérotés :

1. **Principes d'utilisation** — les sept principes MDS, repris mot pour mot :
   un scénario par appel, questionnaire renseigné après avoir raccroché, données
   factuelles séparées du score, barème 100 / 50 / 0 / N/A, questions
   conditionnelles renseignées seulement si la situation se produit, tout 0 ou
   toute situation exceptionnelle étayé par un fait observé, score lu par
   opérateur et par scénario et jamais comme mesure individuelle, médiane de
   complétion ≤ 5 minutes.
2. **Repères pour le calibrage** — les cinq repères de l'annexe scénarios :
   noter ce qui a été observé et entendu, N/A seulement si le critère n'a pas pu
   être observé, ce que doit décrire un 50, la définition du FCR, et l'usage des
   verbatims exacts.
3. **Dans ce formulaire** — ce que le support digital fait de ces principes :
   masquage automatique, N/A hors calcul, alerte critique **puis** commentaire
   ouverts sur les 0, alertes critiques à part, scores calculés.

Les deux premiers blocs sont la consigne MDS ; le troisième dit comment le
formulaire l'applique. Les retoucher = retoucher `note_principes`,
`note_calibrage` et `note_formulaire` dans `build_form.py`.

### Les données factuelles sont collectées à part

Consigne du PDF : « les données factuelles (temps d'attente, durée, transferts,
mises en attente) sont collectées séparément du score comportemental ». La page
**Mesures** les relève et **aucune n'est notée**. Elle est placée avant les
sections notées parce qu'elle commande la logique conditionnelle :

| Mesure | Variable | Ce qu'elle commande |
|---|---|---|
| Temps d'attente avant conseiller | `T_ATTENTE` | — |
| Durée totale de l'appel | `T_DUREE_APPEL` → `TEMPS_TOTAL` | — |
| Nombre de mises en attente | `NB_ATTENTES` | `T_ATTENTES` et **Q18** |
| Durée cumulée des mises en attente | `T_ATTENTES` | — |
| Nombre de transferts | `NB_TRANSFERTS` | **Q18** |
| Renvoi vers un autre canal *(posée si `NB_TRANSFERTS > 0`)* | `RENVOI_CANAL` | `RENVOI_PRECISION`, **Q15** |
| Renvoi en agence *(ajoutée, posée si `NB_TRANSFERTS > 0`)* | `RENVOI_AGENCE` | `RENVOI_PRECISION`, **Q15** |
| Escalade *(ajoutée, posée si `NB_TRANSFERTS > 0`)* | `ESCALADE` | **Q15** |

### La tranche horaire se déduit de l'heure de début

`TRANCHE_HORAIRE` n'est plus cochée : elle est **calculée** à partir de
`HEURE_DEBUT`, saisie quelques lignes plus haut sur la même page. Demander deux
fois la même information ouvrait un écart entre les deux champs, sans rien
apporter — et c'est le champ coché qui aurait fait foi à l'analyse.

| `HEURE_DEBUT` | `TRANCHE_HORAIRE` |
|---|---|
| `07:00` → `11:59` | `1` — 07h - 12h |
| `12:00` → `17:59` | `2` — 12h - 18h |
| `18:00` → `21:59` | `3` — 18h - 22h |
| avant `07:00` | `1` — rattachée à la plus proche |
| `22:00` et après | `3` — rattachée à la plus proche |
| non saisie | vide |

**Les trois tranches du PDF ne couvrent pas la nuit.** Plutôt que de laisser un
trou, une heure hors `07h - 22h` est rattachée à la tranche la plus proche,
**minuit servant de coupure** : le calcul se réduit alors à deux comparaisons
(`< 12`, `< 18`). Un appel nocturne reste donc comptabilisé, dans la tranche
limitrophe. Si MDS préfère une quatrième modalité « hors plage », elle
s'ajouterait à `liste("tranche_horaire", …)` et au calcul en deux lignes.

Le champ reste un `select_one` — et non un `deduit()` texte comme
`JOUR_SEMAINE` — avec `calculation` + `readonly` : l'enquêteur lit « 12h - 18h »
sur une liste grisée, et l'export conserve le code `1` / `2` / `3` attendu par
le tableau de bord et par la table de correspondance MDS. `test_scores.py`
vérifie chacune des bornes, y compris les deux rattachements hors plage.

> **`HEURE_FIN` ne peut pas entrer dans ce calcul.** Elle est posée sur la
> **dernière page** : avec `HEURE_DEBUT`, elle borne la durée de saisie du
> questionnaire — la cible PDF « médiane ≤ 5 minutes » — et non la durée de
> l'appel, relevée à part page *Mesures*. S'en servir laisserait la tranche
> vide pendant toute l'évaluation, puis la ferait changer à la fin.

### Ce qui est conditionnel, et ce qui ne l'est pas

Le questionnaire compte **91 questions saisies, dont 49 conditionnelles**. Elles
se rangent en trois familles, et la liste est close :

| Famille | Questions | Déclencheur |
|---|---|---|
| Une donnée n'a d'objet que si l'événement a eu lieu | `T_ATTENTES`, `RENVOI_CANAL`, `RENVOI_AGENCE`, `ESCALADE`, `RENVOI_PRECISION` | `NB_ATTENTES > 0`, `NB_TRANSFERTS > 0`, un renvoi coché |
| Un critère n'a d'objet que si l'événement a eu lieu | **Q15**, **Q18** | `ESCALADE`, `RENVOI_CANAL` ou `RENVOI_AGENCE` ; `NB_ATTENTES > 0` ou `NB_TRANSFERTS > 0` |
| Un bloc de critères n'a d'objet que pour le scénario joué | les 25 blocs de la section I, `grp_s01` … `grp_s25` | `SCENARIO = S01` … `SCENARIO = S25` |
| Une non-conformité doit être qualifiée puis décrite | `Q1_ALERTE` … `Q22_ALERTE`, `S01_1_ALERTE` … `S25_4_ALERTE`, et les `_COM` correspondants, `ALERTES_COM` | le critère vaut `0` ; une alerte est cochée |

**Aucun autre critère ne dépend d'un fait relevé.** Le balayage a repris les 22
libellés un à un : ceux qui portent une réserve (« lorsque cela était utile »
pour Q8, « lorsque la résolution immédiate était impossible » pour Q13, « en cas
de non-résolution » pour Q16, « au strict nécessaire » pour Q7 et Q17) énoncent
les **deux branches du jugement**, pas un événement extérieur — ils se posent
dans tous les cas.

**Deux critères s'appliquent selon le parcours sans qu'un `relevant` puisse le
dire**, faute de fait qui les déclenche : **Q2** (le choix de langue n'est jugé
que « lorsqu'il était applicable ») et **Q19** (l'empathie se juge sur l'émotion
que le client a exprimée). Ils relèvent de **« Non applicable »**, qui sort du
numérateur comme du dénominateur — donc du même effet qu'un masquage. Les gater
demanderait d'ajouter une question d'aiguillage en page *Mesures* (« Passage par
un serveur vocal ? », « Avez-vous exprimé un mécontentement ? ») : c'est une
décision MDS, pas une correction technique.

### Le scénario, juste avant la notation

Les 25 scénarios de l'annexe MDS sont en place, exportés sous `SCENARIO` avec
leur code d'origine (`S01` … `S25`). La question occupe **sa propre page, juste
avant la section A** : le scénario conditionne la lecture de toute la notation
qui suit — « le score mesure la performance de l'expérience par opérateur **et
par scénario** ».

**Le libellé ne porte que trois colonnes de l'annexe** — code, famille,
scénario :

```
S13 · KYC · Problème d'identification de la ligne
S19 · Mobile Money · Transaction débitée mais non reçue
```

La *formulation client mystère* et *ce que l'on cherche à tester* ne sont pas
repris : ils se lisent dans l'annexe **avant** l'appel, pas dans une liste
déroulante pendant la saisie. Corriger un libellé = corriger une ligne de
`SCENARIOS` dans `build_form.py`.

La page porte les trois consignes de jeu de l'annexe : le script est un
**déclencheur** (ne pas surjouer, ne rien fournir spontanément), les scénarios
sensibles (SIM, KYC, Mobile Money) n'utilisent que des **lignes et comptes de
test autorisés**, sans transaction réelle ni exposition de données personnelles.

### I. Les critères propres au scénario

L'annexe « Scénarios finaux » donne, pour chacun des 25 scénarios, **3 à 5
critères de traitement** : a-t-il vérifié l'activation du forfait, consulté
l'historique, authentifié le client avant de donner le code PUK. Là où A→H
mesure le **comportement** — le même pour tous les appels —, la section I mesure
les **actes que ce scénario appelait**.

Ils sont **106**, répartis ainsi : S18 en porte 3, dix-sept scénarios en portent
4, sept en portent 5.

**Un bloc par scénario, conditionné au scénario joué.** La page « I. MAÎTRISE DU
SCÉNARIO » contient 25 sous-groupes `grp_s01` … `grp_s25`, chacun `relevant` sur
`${SCENARIO} = 'S01'`. L'enquêteur ne voit que les 3 à 5 critères de son appel ;
les 101 autres sont masqués et **sortent du numérateur comme du dénominateur** —
la même mécanique que Q15 ou Q18, et les mêmes tests.

**Même échelle, même score.** La section est déclarée comme les huit autres :
ses critères entrent dans `SCORE_TOTAL` au même titre que Q1 à Q22. Un appel est
donc noté sur **22 + 3 à 5 critères**, jamais sur 128. `SCORE_I` porte le score
de la section, calculé en arrière-plan comme `SCORE_A` … `SCORE_H`.

**Noms d'export** : `S01_1` … `S25_5`, avec `S01_1_ALERTE` et `S01_1_COM` sur
toute non-conformité, comme les 22 autres. Le fichier reste plat : 106 colonnes
de plus, vides pour 24 appels sur 25.

**Le libellé porte son numéro**, comme « Q1 … » le fait depuis le début :
« **S01_1** Diagnostic — Le conseiller a-t-il identifié… ». L'annexe MDS numérote
ses critères scénario par scénario sans leur donner de code, si bien que plusieurs
portent le même intitulé — « Solution », « Pédagogie », « Ownership » reviennent
d'un scénario à l'autre. Exporté sans son numéro, un tel libellé ne dit plus de
quel scénario il vient, et deux colonnes distinctes se lisent pareil. Le préfixe
est exactement le nom de la colonne : la base en sortie se lit sans table de
correspondance, que l'export porte les noms de variables ou les libellés, en
français comme en anglais.

Les libellés sont dans [`criteres_scenario.py`](criteres_scenario.py), français
et anglais côte à côte — une paire de phrases se relit mieux ensemble
qu'éclatée sur deux fichiers. `traductions.py` les verse dans sa table générale,
où le contrôle de couverture les voit comme les autres.

> **Quatre points relevés dans l'annexe, à faire trancher par MDS.**
> 1. **S18 n'a que 3 critères** et aucun ne porte sur la résolution ; les autres
>    scénarios en ont 4 ou 5. Omission probable.
> 2. **S03 « Solution ou escalade »** est à double détente : un conseiller qui
>    n'a pas résolu mais a correctement escaladé se note mal.
> 3. **Recouvrement avec A→H.** Plus de la moitié des 106 reformulent un critère
>    générique dans le vocabulaire du scénario — « Empathie » de S15 reprend
>    Q19, « Ownership » de S25 reprend Q14. Les deux jeux entrant dans le même
>    score, ces critères pèsent deux fois sur les appels concernés. **C'est un
>    arbitrage MDS assumé**, pas un défaut de construction : le score reste
>    comparable entre appels d'un même scénario, moins entre scénarios.
> 4. **Sécurité et authentification** (S11, S12, S19, S20) n'ont aucun
>    équivalent en A→H : sur les autres scénarios, ce point n'est couvert que
>    par l'alerte « confidentialité ».

## Le questionnaire est noté

Les **128 critères** — les 22 critères de comportement des sections A à H, plus
les 106 critères de scénario de la section I — partagent **une seule échelle**,
ce qui rend les sections directement comparables : totalement conforme, partiellement conforme /
perfectible, non conforme, non applicable — valant respectivement **100**, **50**,
**0** et rien.

**Le barème ne s'affiche jamais à l'enquêteur.** Ni le chiffre au bout de la
modalité — les libellés sont les quatre formulations ci-dessus, sans « (100) » ni
« (N/A) » — ni le score de section pendant la saisie. Il coche ce qu'il a
entendu ; la conversion se fait en arrière-plan et **seul le score de l'appel
s'affiche, à la dernière page**. Le code stocké (`100`, `50`, `0`, `na`) et la
colonne `points` sont inchangés : l'export, le tableau de bord et le site de
suivi ne voient aucune différence.

**Le barème est déclaré une seule fois**, dans la colonne `points` de la liste
`conformite` de `build_form.py`. Il alimente trois choses sans être recopié :

| Sortie | Ce qu'elle en fait |
|---|---|
| `questionnaire_audit_call_center.xlsx` | `SCORE_A` … `SCORE_H` en `calculate` — calculés en XPath, exportés, jamais affichés — et `SCORE_TOTAL` en lecture seule sur la dernière page |
| `guide_enqueteur.html` | Le même calcul, rejoué en JavaScript, également en arrière-plan : le score n'apparaît qu'à la dernière étape |
| `suivi_collecte.html` | Les moyennes par section, par opérateur, par critère et **par scénario**, recalculées depuis les soumissions brutes |

**Règle du dénominateur.** Un critère apporte 100 points au dénominateur **dès
qu'il est renseigné par une modalité notée**, et rien sinon :

- **N/A n'est pas un zéro** : sa colonne `points` est vide, il sort du
  numérateur comme du dénominateur. C'est la consigne du PDF — un critère n'est
  noté N/A que s'il n'a réellement pas pu être observé ;
- un critère **masqué** par un `relevant` (Q15 sans escalade ni renvoi, Q18 sans
  attente ni transfert ni changement de canal) sort du calcul de la même façon ;
- un formulaire vierge n'affiche aucun score plutôt qu'un zéro trompeur.

Un appel court, simple et parfaitement traité n'est donc pas pénalisé de n'avoir
donné lieu ni à une escalade ni à une mise en attente.

`test_scores.py` évalue les expressions XPath produites, sur des réponses
fabriquées, et vérifie 14 cas — dont l'exclusion des N/A, celle des questions
masquées, l'arrondi et l'absence de division par zéro sur formulaire vierge :

```
$ python test_scores.py
  OK   Appel parfait : les 22 criteres a 100, escalade et renvoi survenus
  OK   N/A sort du denominateur : Q2 = N/A, A ne porte que sur Q1 et Q3
  OK   Q15 masquee (ni escalade ni renvoi) : E porte sur Q12, Q13, Q14 et Q16
  …
14/14 cas conformes
```

## Sur un 0 : qualifier, puis décrire

Consigne du PDF : « tout score de 0 ou toute situation exceptionnelle doit être
étayé par un fait observé ou une formulation exacte du conseiller ». L'enquêteur,
lui, ne lit pas « 0 » mais **« non conforme »** : c'est le même code stocké, avec
le vocabulaire de la page.

Un « non conforme » ouvre donc **deux champs, dans cet ordre** :

| Ordre | Champ | Rôle |
|---|---|---|
| 1 | `Q<n>_ALERTE` — choix multiple | Ce constat relève-t-il d'un cas d'alerte critique ? L'un des cas nommés proposés par la section, sinon « Aucune alerte critique ». |
| 2 | `Q<n>_COM` — texte | Le fait observé ou la formulation exacte du conseiller. |

**L'alerte est posée avant le commentaire, délibérément.** L'enquêteur qualifie
le constat avant de le décrire : la description qu'il rédige ensuite sait ce
qu'elle doit établir. Décrire d'abord et classer après produit des commentaires
qui n'étayent pas le cas coché.

Les deux champs ne s'affichent **que lorsque la réponse est 0**, et sont alors
obligatoires. Les libellés sont les mêmes pour les 128 critères — « Non conforme —
ce constat relève-t-il d'un cas d'alerte critique ? » puis « Non conforme —
décrivez le fait observé ou rapportez la formulation exacte du conseiller » — ce
qui en fait deux libellés à traduire et à relire, pas quarante-quatre.

**Tout 0 n'est pas une alerte critique.** « Aucune alerte critique » est la
réponse attendue de la plupart des 0 : un accueil bâclé ou une reformulation
absente se note 0 sans rien avoir à signaler. La modalité rend la question
obligatoire sans forcer à déclarer une alerte, et une contrainte l'empêche
d'être cochée en même temps qu'un cas.

La condition des deux champs se réduit à `${Q<n>} = '0'` : une question masquée
par son propre `relevant` est vidée par ODK, l'alerte et le commentaire
disparaissent donc avec elle sans qu'il faille répéter la condition.
`guide_enqueteur.html` reproduit ce vidage.

> **À confirmer :** le PDF demande aussi qu'« un score de 50 décrive une
> conformité partielle concrète ». Aucun champ n'est ouvert sur les 50 — la
> consigne MDS est « commentaire obligatoire uniquement pour 0 ». Ouvrir un
> commentaire facultatif sur les 50 tiendrait en une ligne de `critere()` dans
> `build_form.py`.

## Alertes critiques

Principe repris de la consigne MDS : *une alerte critique doit être décrite
factuellement, même si le score global reste élevé ; elle fait l'objet d'une
analyse séparée et d'un commentaire obligatoire*.

Une alerte **n'entre pas dans le calcul du score** : un appel peut tourner à
92 / 100 et porter une exposition de données personnelles. Les deux informations
doivent remonter séparément, sinon la seconde se dilue dans la première.

Elle se coche **là où elle se révèle**. La liste est donc proposée à deux
endroits, et un même appel peut en porter des deux :

| Où | Champ | Ce qu'il ramasse |
|---|---|---|
| Sur chaque critère noté 0 | `Q<n>_ALERTE` | Le cas que ce 0 révèle. Voir *Sur un 0 : qualifier, puis décrire*. |
| Page 13, avant la synthèse | `ALERTES` | **Le reliquat seul** : les cas observés hors d'un critère noté 0 — pendant une mise en attente, sur un point non scoré. |

Rattacher l'alerte au critère qui la révèle donne deux choses que la seule page
13 ne donnait pas : le **commentaire qui l'étaye est déjà là**, juste en dessous,
et l'analyse sait **quel point de contrôle** a produit l'alerte. La page 13 ne
demande plus de redéclarer ce qui a déjà été coché sur un 0 — pas de double
saisie, et son libellé le dit (« Autres cas d'alerte critique… »).

La liste **générale** — les cinq cas du document, plus une modalité ajoutée —
est proposée sur les critères des sections **B à H** et sur la page 13 :

| Code | Cas |
|---|---|
| `confidentialite` | Violation ou exposition de données personnelles / défaut manifeste de confidentialité |
| `info_erronee` | Information manifestement erronée susceptible d'entraîner une perte financière ou un préjudice client |
| `irrespect` | Propos irrespectueux, agressifs, discriminatoires ou attitude manifestement non professionnelle |
| `promesse` | Promesse de délai / de traitement non maîtrisée ou engagement trompeur |
| `abandon` | Transfert, renvoi en agence ou abandon de prise en charge manifestement non justifié |
| `aucune` | *(ajoutée)* Aucune alerte critique |

### La section A a sa propre liste

`Q1`, `Q2` et `Q3` — **A. Accessibilité & serveur vocal** — ne proposent pas les
cinq cas généraux mais les six cas du serveur vocal (liste `alertes_a` dans
`build_form.py`), et ils sont les **seuls** à les proposer :

| Code | Cas |
|---|---|
| `accueil_incoherent` | Message d'accueil incohérent ou trompeur, ne correspondant pas aux services réellement proposés |
| `menus_errones` | Menus du serveur vocal erronés ou non fonctionnels, entraînant une mauvaise orientation ou une impossibilité d'accès au conseiller |
| `langue_indisponible` | Absence ou dysfonctionnement du choix de langue, créant une barrière de communication pour le client |
| `boucle_ivr` | Boucle IVR bloquante ou confusion dans le parcours, empêchant le client d'obtenir une assistance humaine |
| `coupure_redirection` | Erreur de redirection ou coupure systématique avant mise en relation, générant une rupture de service |
| `attente_non_signalee` | Temps d'attente excessif non signalé, ou absence de message d'information pendant la mise en relation |
| `aucune` | *(ajoutée)* Aucune alerte critique |

**Pourquoi deux listes.** La section A se joue **avant toute prise de ligne** :
les cinq cas généraux sont tous des faits du conseiller, et aucun n'y est
observable — proposer « propos irrespectueux » sur un menu vocal n'a pas de
sens. À l'inverse, une boucle IVR sans sortie ou une coupure avant mise en
relation n'a d'équivalent nulle part ailleurs dans le questionnaire. Chaque
critère ne voit donc que les cas qu'il peut réellement révéler.

`aucune` garde son code, son libellé et sa contrainte dans les deux listes : le
tableau de bord les agrège sans cas particulier, et une seule traduction sert
les deux. Le paramètre `alertes=` de `critere()` choisit la liste ; une section
qui aurait besoin de la sienne se traite de la même façon.

**« Aucune alerte critique » est un ajout.** Le document ne présente que les
cases des cas nommés, et cinq cases seules ne disent pas si un questionnaire
sans case cochée signifie « aucune alerte » ou « l'enquêteur a sauté la
question ». La modalité rend la question obligatoire sans forcer à déclarer une
alerte, et une contrainte l'empêche d'être cochée en même temps qu'une alerte.

**La liste reste fermée sur les cas nommés.** Une modalité « Autre cas » avait
été ajoutée puis retirée : les cas à signaler sont ceux du document, et un
manquement grave qui n'y entre pas se décrit dans le commentaire plutôt que
dans une case fourre-tout que le dépouillement ne sait pas agréger.

`ALERTES_COM` — le commentaire de la page 13 — s'affiche **dès que la question
`ALERTES` est renseignée**, « Aucune alerte critique » comprise, et son
obligation est **conditionnelle** :

| Ce qui est coché dans `ALERTES` | `ALERTES_COM` |
|---|---|
| Un ou plusieurs cas | affiché et **obligatoire** |
| « Aucune alerte critique » | affiché et **facultatif** — c'est là que se décrit un manquement grave hors des cas listés |
| Rien encore | masqué |

C'est ce qui remplace la modalité « Autre cas » : la liste reste fermée, mais
l'enquêteur garde un endroit où consigner ce qui n'y entre pas, et le
dépouillement le lit comme un commentaire plutôt que de l'agréger dans une barre
fourre-tout. Deux conséquences à connaître : un `ALERTES_COM` non vide peut
désormais accompagner un `ALERTES = aucune` — à lire à part, c'est le signal
d'une liste à compléter avec MDS — et un commentaire saisi puis suivi d'un
passage à « Aucune alerte critique » n'est plus effacé par ODK, puisque le champ
reste pertinent.

Les alertes rattachées à un 0 sont étayées par le `Q<n>_COM` du critère, pas par
ce champ.

> **Un `required` porteur d'une expression.** `build_form.py` pose
> `required = "yes"` sur toute question saisie (`OPTIONNELLES` est vide) ;
> `alertes_com` est la seule à poser le sien à la main —
> `not(selected(${alertes}, 'aucune'))` — et la boucle de fin ne l'écrase pas.
> `build_guide.py` relit cette expression avec le même parseur que les
> `relevant` et l'émet en `data-obl-si` : dans le guide, le bouton *Suivant* ne
> se bloque sur ce champ que lorsqu'une alerte est cochée, et l'étape peut
> atteindre « fini » sans lui.

Le tableau de bord leur consacre **une tuile et un panneau à part** : nombre
d'appels portant au moins une alerte, et répartition par cas. `alertes_de()`
dans `build_dashboard.py` relit tous les `Q<n>_ALERTE` **et** `ALERTES`, quelle
que soit la liste dont le cas provient, et dédoublonne : le même cas signalé sur
deux critères reste une alerte pour l'appel.

## Questions conditionnelles

Consigne MDS : « escalade, renvoi en agence, mise en attente ou demande de
pièces ne doivent être renseignés que si l'événement s'est produit ; un
questionnaire digital doit masquer automatiquement les questions non
applicables ». Cinq familles de champs sont conditionnelles :

| Champ | S'affiche si |
|---|---|
| `T_ATTENTES` — durée cumulée des mises en attente | `NB_ATTENTES > 0` |
| `RENVOI_CANAL` — renvoi vers un autre canal | `NB_TRANSFERTS > 0` |
| `RENVOI_AGENCE` — renvoi en agence | `NB_TRANSFERTS > 0` |
| `ESCALADE` — dossier transmis ou rappel promis | `NB_TRANSFERTS > 0` |
| `RENVOI_PRECISION` — canal ou agence indiqués | `RENVOI_CANAL = Oui` **ou** `RENVOI_AGENCE = Oui` |
| **Q15** — motif, étapes, pièces et délai de l'escalade / du renvoi | `ESCALADE = Oui`, `RENVOI_CANAL = Oui` **ou** `RENVOI_AGENCE = Oui` |
| **Q18** — mises en attente, transferts et changements de canal | `NB_ATTENTES > 0` **ou** `NB_TRANSFERTS > 0` |
| `Q<n>_ALERTE` — alerte critique révélée par un score de 0 | `Q<n> = 0` |
| `Q<n>_COM` — commentaire d'un score de 0 | `Q<n> = 0` |
| `ALERTES_COM` — commentaire des alertes de la page 13 | au moins un cas coché |

Les trois supports appliquent la même règle : KoboCollect et Enketo par la
colonne `relevant`, `guide_enqueteur.html` en rejouant ces conditions en
JavaScript (avec le même vidage des réponses devenues non pertinentes), et
`suivi_collecte.html` en traitant une réponse absente comme hors calcul.

## Questionnaire bilingue

Tous les libellés, consignes, modalités et messages de contrôle existent en
français et en anglais. La source unique est `traductions.py` (clé = libellé
français exact) ; `build_form.py` refuse de passer sous silence un libellé sans
traduction : il liste en fin de génération les libellés manquants **et** les
traductions devenues orphelines. `build_dashboard.py` fait le même contrôle sur
ses propres textes.

**Les trois livrables basculent**, chacun avec le mécanisme adapté à son support :

| Sortie | Bascule |
|---|---|
| `questionnaire_audit_call_center.xlsx` | Colonnes `label::Français (fr)` / `label::English (en)` (idem `hint` et `constraint_message`) → **sélecteur de langue natif** de KoboCollect et d'Enketo, français par défaut |
| `guide_enqueteur.html` | Bouton **English / Français** dans la barre de progression |
| `suivi_collecte.html` | Bouton **English / Français** dans la barre d'outils, sous le bandeau |

Les deux pages HTML emploient la même mécanique : chaque texte porte sa version
anglaise dans un attribut `data-en`, chaque infobulle de graphique dans un
`data-tip-en`, et le bouton échange les deux sans rechargement. Le choix est
conservé dans le navigateur. Les libellés d'axes en SVG sont traités à part —
`innerHTML` n'étant pas fiable sur un nœud SVG, la bascule y écrit du texte brut.

Ne basculent pas : les noms d'enquêteurs, les codes de scénario, les marques et
les valeurs chiffrées.

La traduction anglaise est une **traduction de travail** : elle doit être validée
par MDS avant le terrain. En cas d'écart, le questionnaire papier français fait
foi. Vocabulaire retenu : « enquêteur » → *auditor*, « conseiller » → *adviser*,
« serveur vocal » → *IVR*. « Ownership » et « FCR » sont laissés tels quels — ils
le sont déjà dans le questionnaire français.

**Piège Kobo à connaître.** Kobo fusionne les langues à chaque import : un projet
passé de monolingue à bilingue conserve un emplacement de traduction **sans nom**,
et le formulaire refuse alors de s'ouvrir (« There is an unnamed translation in
your form definition »). Le contrôle et la réparation tiennent en une commande :

```bash
python kobo.py langues <uid>            # liste les langues
python kobo.py langues <uid> --nettoyer # retire les anonymes + redéploie
```

## Noms de variables

Le JOB 002/26 **n'a pas de table de correspondance MDS**. Dix noms
d'identification sont repris de celle du JOB 001/26, où ils figurent noir sur
blanc — `NOM_ENQ`, `DATE_INTERVIEW`, `OPERATEUR`, `SCENARIO`, `TYPE_INTERVIEW`,
`HEURE_DEBUT`, `HEURE_FIN`, `TEMPS_TOTAL`, `LANGUE_ENQ`, `JOUR_SEMAINE` — pour
que les deux collectes s'empilent. **Les 93 autres sont déduits de ses
conventions et restent à valider.**

| Convention (JOB 001/26) | Application ici |
|---|---|
| Un code du PDF est repris tel quel | `Q1` → `Q1`, `Q25` → `Q25` |
| Une durée prend le préfixe `T_` | `T_ATTENTE`, `T_ATTENTES`, `T_DUREE_APPEL` |
| Un champ d'identification prend un nom parlant | `IDENT_CONSEILLER`, `TRANCHE_HORAIRE`, `ESCALADE`, `RENVOI_CANAL` |
| *(nouveau)* Un commentaire suffixe la question qu'il justifie | `Q15` → `Q15_COM`, `ALERTES` → `ALERTES_COM` |
| *(nouveau)* Une alerte critique suffixe le critère qui la révèle | `Q15` → `Q15_ALERTE` |
| *(nouveau)* Un verbatim suffixe sa question | `Q25` → `Q25_TXT` |
| *(nouveau)* Un score porte le nom de sa section | `SCORE_A` … `SCORE_H`, `SCORE_TOTAL` |

`renommer()` applique cette table **au seul classeur XLSForm**, en toute fin de
génération : il réécrit le `name` de la question **et toutes les références
`${...}` qui la citent** — les expressions de score et les conditions comprises.
Le reste de la chaîne (code, `traductions.py`, `form_structure.json`, guide,
tableau de bord) continue de travailler avec les noms internes, plus lisibles.

Corriger un nom = corriger une ligne de `NOMS_DEDUITS`, rien d'autre.
`correspondance_variables.xlsx` liste les 103 variables dans l'ordre du
questionnaire, dit lesquelles sont notées, et surligne en jaune les 93 à relire.

## Règles de remplissage

1. **Pas de page suivante sans page précédente complète.** `settings.style =
   pages`, un groupe `field-list` par section, et toutes les questions sont
   `required` — sans exception. Enketo et KoboCollect bloquent
   alors la navigation ; le guide HTML fait de même (bouton *Suivant* qui
   surligne les réponses manquantes, étapes suivantes verrouillées).
2. **Saisie libre limitée à ce que le PDF exige.** Il reste 29 champs texte,
   dont **23 qui ne s'ouvrent que sur un incident** : les 22 commentaires de
   score 0 et celui des alertes critiques. Sur un appel sans non-conformité,
   l'enquêteur n'en voit aucun. Les 6 autres sont le nom de l'enquêteur,
   l'identification du conseiller, la précision du renvoi et les trois champs de
   la synthèse qualitative (Q23, Q24, Q25 « pourquoi »).
3. **Aucune question redondante.** Sont calculés et non saisis : le jour de la
   semaine, la durée totale de l'appel en secondes, le temps total en minutes et
   les neuf scores.
4. **Une seule branche à la fois.** Voir *Questions conditionnelles*.

## Écarts assumés avec le PDF de septembre 2026

Chaque écart se corrige en une ligne si MDS tranche autrement.

### 1. Une question d'aiguillage ajoutée

Q15 n'est posée qu'« en cas d'escalade ou de renvoi en agence ». Le renvoi est
relevé dans le bloc *Mesures* du PDF ; **l'escalade ne l'est nulle part**. Une
question fermée a donc été ajoutée à ce même bloc :

> *Escalade : le dossier a-t-il été transmis à un autre service ou un rappel
> a-t-il été promis ?*

Elle n'est **pas notée** : c'est un aiguillage, pas un point de contrôle.

### 2. Les deux intertitres vides sont absorbés par Q15

Le PDF conserve, entre Q16 et la section F, deux intertitres hérités de la
version précédente — **« EN CAS D'ESCALADE »** et **« SI RENVOI EN AGENCE »** —
qui ne portent plus aucune question. Q15 couvre désormais les deux cas (motif,
prochaines étapes, pièces éventuelles, délai) : les intertitres ne sont pas
repris.

### 3. Coquilles corrigées et libellés normalisés

| PDF de septembre 2026 | Retenu |
|---|---|
| « C. COMPREHENSION DU **BESION** » | « C. COMPRÉHENSION DU **BESOIN** » |
| Q5 « … sans **sur- de scriptage** » | « … sans **sur-scriptage** » |
| Q1 « Oui, totalement **conformes** / Partiellement **conformes** » *(pluriel sur cette seule question)* | Singulier, comme les 21 autres — une seule liste de modalités pour tout le questionnaire |
| Q24 « … effort subi par le client » *(sans point d'interrogation)* | « … effort subi par le client **?** » |
| Sections numérotées A à H | Reprises telles quelles |

### 4. Ajouts

| Ajout | Motif |
|---|---|
| **Type d'interview** (TEST / Live) | Consigne MDS du JOB 001/26 : les interviews de test ne se reconnaissent plus à l'analyse. Absent du PDF. |
| **Toutes les durées en secondes** | Le PDF collecte la durée de l'appel au format « ___ min ___ sec », l'attente et les mises en attente en secondes. Une seule unité partout : l'enquêteur convertit sa lecture de chronomètre une fois, à la saisie, et le dépouillement n'a plus de conversion à faire. `TEMPS_TOTAL` (minutes) reste déduit, pour le JOB 001/26. |
| **Le renvoi scindé en deux cases**, `RENVOI_CANAL` et `RENVOI_AGENCE`, **posées après un transfert seulement** — comme `ESCALADE` | Une case unique « autre canal / agence » sortait un `RENVOI_CANAL = Oui` sans dire si le client avait été envoyé sur l'application ou en boutique — deux traitements qui n'ont ni le même coût pour lui ni la même lecture à l'analyse ; et un appel peut porter les deux (« faites-le sur l'appli, sinon passez en agence »). La condition `NB_TRANSFERTS > 0` est une consigne MDS : voir le point ouvert 12. |
| **« Aucune alerte critique »** ajoutée à la liste | Cinq cases à cocher seules ne distinguent pas « aucune alerte » d'« question sautée ». Voir *Alertes critiques*. |
| **`TRANCHE_HORAIRE` déduite de `HEURE_DEBUT`** au lieu d'être cochée | Le PDF fait cocher la tranche alors que l'heure est déjà saisie juste au-dessus : deux champs pour une même information, qui peuvent se contredire. Le calcul supprime l'écart et une saisie. Les heures hors `07h - 22h`, que le PDF ne prévoit pas, sont rattachées à la tranche la plus proche. Voir *La tranche horaire se déduit de l'heure de début*. |
| **Six cas d'alerte propres à la section A** (accessibilité & serveur vocal), proposés sur `Q1`, `Q2`, `Q3` **seulement** | La section se joue avant toute prise de ligne : les cinq cas généraux sont des faits du conseiller et n'y sont pas observables, tandis qu'une boucle IVR sans sortie ou une coupure avant mise en relation n'a d'équivalent nulle part ailleurs. Voir *La section A a sa propre liste*. |

## Points ouverts

1. ~~**Aucune question propre à un scénario.**~~ **Réglé** par l'annexe
   « Scénarios finaux » : la section I porte 106 critères, 3 à 5 par scénario,
   conditionnés au scénario joué. Voir *I. Les critères propres au scénario* —
   dont les quatre points que l'annexe laisse ouverts.
2. **Variantes relationnelles S15, S23, S24.** L'annexe précise qu'elles
   « peuvent aussi être utilisées comme variantes relationnelles appliquées à un
   scénario fonctionnel ». Le questionnaire n'enregistre **qu'un seul code** :
   sur un S01 joué avec une posture S15, l'enquêteur coche celui qui décrit le
   mieux l'appel, et l'autre information est perdue. Un second champ avait été
   ajouté puis **retiré sur demande MDS**. À rouvrir si la désescalade doit être
   mesurée indépendamment du motif.
3. **Camtel a disparu.** Le PDF de septembre 2026 ne liste que **Orange / MTN**,
   là où la version précédente couvrait aussi Camtel. Le formulaire, le guide et
   le tableau de bord suivent le PDF. Confirmer que Camtel sort bien du périmètre
   — sinon, une ligne de `RESEAUX` dans `build_form.py` et une dans
   `build_dashboard.py`.
4. **Règle du dénominateur** (N/A et questions non posées exclus du score) — voir
   plus haut. C'est le choix qui pèse le plus sur les scores publiés.
5. **Commentaire sur les 50** : non ouvert, sur consigne MDS. Voir plus haut.
6. **Noms de variables** : 71 des 81 sont déduits, à relire dans
   `correspondance_variables.xlsx`.
7. **Traduction anglaise** : traduction de travail, à faire relire par MDS. Les
   25 libellés de scénario en font partie : famille et intitulé sont traduits,
   le code reste tel quel.
8. **Pas de géolocalisation ni de référentiel.** Un appel n'a pas de lieu : ni
   GPS, ni ville, ni agence, contrairement au JOB 001/26. Si MDS veut suivre la
   couverture géographique des enquêteurs, il faudra ajouter une ville de
   passation. Le scénario S22 (« qualité réseau dans une localité précise »)
   rend la question plus concrète.
9. **Numéro appelé.** Le questionnaire n'enregistre pas quel numéro a été composé
   (`3900`, `8888`…). À trancher, notamment pour le contrôle qualité.
10. **Alertes critiques hors score** : elles remontent à part et ne pèsent pas
    sur la note. Si MDS veut qu'une alerte plafonne le score de l'appel (par
    exemple un total borné à 50 dès qu'une alerte est signalée), c'est une règle
    à écrire dans `score()` — elle n'existe pas aujourd'hui.
11. **Le nombre de transferts commande toute la fin de la page « Mesures ».**
    `RENVOI_CANAL`, `RENVOI_AGENCE` et `ESCALADE` ne s'affichent que si
    `NB_TRANSFERTS > 0`, à la demande de MDS. Les deux cas se produisent
    pourtant sans transfert, et **les données le montrent déjà** :
    - un **renvoi** sans transfert — le conseiller répond lui-même puis oriente
      vers l'agence ou l'application. La première soumission de la collecte est
      exactement ce cas (`NB_TRANSFERTS = 0`, `RENVOI_CANAL = Oui`, précision
      « Canal Principal ») ;
    - une **escalade** sans transfert — « je transmets au service technique, on
      vous rappelle sous 48 h », l'appel n'ayant été passé à personne. Une autre
      soumission est ce cas (`NB_TRANSFERTS = 0`, `ESCALADE = Oui`).

    Ces colonnes sortiront désormais vides sur les appels non transférés, et
    **Q15 ne s'ouvrira plus du tout sans transfert** — ses trois déclencheurs
    sont derrière la même condition. La section E y porte alors sur 4 critères
    au lieu de 5 : le conseiller qui escalade ou oriente mal sans transférer
    n'est plus évalué là-dessus. À rouvrir si le pilote montre des escalades ou
    des renvois manquants — le correctif tient en trois conditions.
12. **Cible de complétion ≤ 5 minutes.** Le PDF la fixe « après calibrage et
    paramétrage de la logique conditionnelle ». Elle est atteignable : sur un
    appel sans non-conformité, l'enquêteur saisit 22 boutons radio, les mesures,
    le scénario, une case « aucune alerte » et trois champs texte — ni alerte
    ni commentaire ne s'ouvre. Chaque 0 coûte en revanche deux saisies de plus,
    la qualification puis la description. À mesurer au pilote.
