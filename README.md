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
> conditionnel : 23 critères de comportement plus les 3 à 5 critères du
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
`Q1`…`Q23` ne portent plus les mêmes intitulés, l'échelle passe de Oui / Non à
100 / 50 / 0 / N/A, et les variables `Q24`…`Q38`, `Q1a`, `Q1b`, `*_Bis` du
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

**Redéployé le 22/09/2026 — le renvoi fusionné en une seule question.** `RENVOI_CANAL` et
`RENVOI_AGENCE`, les deux cases oui / non de la page « Mesures », sont remplacées
par une liste unique `RENVOI` à quatre modalités : `0` aucun renvoi, `1` vers un
autre canal, `2` vers une agence, `3` vers un point de vente physique. L'agence
et le point de vente, que `RENVOI_AGENCE` confondait, se distinguent ; « Aucun
renvoi » devient une réponse au lieu de deux « Non » cochés. **Deux colonnes
disparaissent, une apparaît**, et les anciennes valeurs ne se convertissent pas
toutes seules :

| Avant | Après |
|---|---|
| `RENVOI_CANAL = Oui` | `RENVOI = 1` |
| `RENVOI_AGENCE = Oui` | `RENVOI = 2` ou `3` — `RENVOI_PRECISION` tranche |
| les deux à `Oui` | une seule destination code, l'autre reste dans `RENVOI_PRECISION` : voir le point ouvert 13 |
| les deux à `Non` | `RENVOI = 0` |
| les deux absents (appel non transféré) | `RENVOI` absent |

Q15 et `RENVOI_PRECISION` changent de condition en conséquence — trois
déclencheurs deviennent deux, énumérés en `OU` sur les trois destinations.

**Aucune donnée n'était en jeu** : le projet comptait **0 soumission** au moment
du redéploiement, les 7 des versions précédentes ayant été supprimées entre-temps
(`data/soumissions.json` est vide lui aussi). La conversion décrite ci-dessus n'a
donc eu à s'appliquer à aucun enregistrement — elle reste la règle si d'anciennes
données devaient être réimportées.

**Redéployé le 22/09/2026 — « Aucune alerte critique » retirée des critères.** Les listes
proposées en face d'un critère noté 0 ne contiennent plus que des cas : la liste
générale se dédouble en `alertes_nc` (les cinq cas, sur les critères) et
`alertes` (les cinq cas **plus** `aucune`, sur la page 13 seulement), et
`alertes_a` perd la modalité. La question `Q<n>_ALERTE` restant obligatoire,
**tout 0 nomme désormais un cas d'alerte**. Son libellé change en conséquence —
« quel cas d'alerte critique ce constat révèle-t-il ? » au lieu de « ce constat
relève-t-il d'un cas d'alerte critique ? ». **Aucun nom de variable ne bouge et
aucune question ne s'ajoute** ; `ALERTES` et `ALERTES_COM` sont inchangées, avec
leur `aucune` et leur contrainte d'exclusivité.

Là encore **aucune donnée n'était en jeu**, le projet étant à 0 soumission. La
règle vaut pour l'avenir : un `Q<n>_ALERTE = aucune` réimporté garderait sa
valeur en base et `alertes_de()` continuerait de l'écarter, mais le code n'a plus
de libellé dans les exports pour ces champs, et rouvrir une telle soumission dans
Enketo **viderait le champ** — désormais obligatoire et sans réponse possible. À
l'analyse, **le compte d'alertes suit maintenant le compte de 0** : voir *Alertes
critiques*.

Les deux changements ont été déployés ensemble. Version déployée
`vENhg39rLNYPLE3voJauAH` — 511 lignes de formulaire, deux langues nommées
(`Français (fr)`, `English (en)`), logo `mds_logo.png` toujours attaché, lien de
collecte inchangé (`https://ee.kobotoolbox.org/52lAclB6`). Classeur converti hors
ligne par pyxform 4.5.0 avant l'envoi, et le formulaire déployé contrôlé après :
`RENVOI` est bien un `select_one` sur une liste de 4 modalités, `RENVOI_CANAL` et
`RENVOI_AGENCE` ont disparu, `Q15` porte la condition en `OU` sur les trois
destinations, et les listes d'alerte des critères (`alertes_nc`, `alertes_a`) ne
contiennent plus `aucune` — que seule `alertes`, en page 13, conserve.

**Redéployé le 22/09/2026 — la page « Alertes critiques » de fin de
questionnaire est supprimée.** Les cas d'alerte se cochent désormais **sur le
critère noté 0 qui les révèle, et là seulement**. La page qui les redemandait
juste avant la synthèse disparaît avec ses deux questions, `ALERTES` et
`ALERTES_COM`, et avec la modalité « Aucune alerte critique », qui n'existait
plus que pour elle : la liste `alertes` et la contrainte d'exclusivité qui
l'accompagnait sont retirées du formulaire. Le questionnaire passe de 16 à
**15 pages**.

**Deux variables disparaissent de l'export** — `ALERTES` et `ALERTES_COM`. C'est
le premier changement de cette série à retirer des colonnes : une soumission
antérieure les porterait encore, sans que rien ne les relise.
`alertes_de()` dans `build_dashboard.py` ne lit plus que les `Q<n>_ALERTE`, ce
qui reste exact pour les anciennes données à un reliquat près — les cas observés
hors d'un critère noté 0, qui n'étaient de toute façon pas rattachables à un
point de contrôle. Le projet était **à 2 soumissions de test**, sauvegardées
avant l'envoi dans `data/soumissions_avant_retrait_alertes.json` ; aucune donnée
d'analyse n'était en jeu.

Version déployée `vYmfKahX4C2NDiiENdNPRb` — 506 lignes de formulaire, deux
langues nommées (`Français (fr)`, `English (en)`), logo `mds_logo.png` toujours
attaché, lien de collecte inchangé (`https://ee.kobotoolbox.org/52lAclB6`), les
2 soumissions conservées. Formulaire déployé relu après l'envoi : **15 groupes
`field-list`** et plus de `grp_alertes`, plus aucun champ `ALERTES` ni
`ALERTES_COM`, plus aucune modalité `aucune` dans les listes de choix (il ne
reste que `alertes_nc` et `alertes_a`), et les 128 `Q<n>_ALERTE` avec leurs 128
`Q<n>_COM` toujours en place.

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
| `questionnaire_audit_call_center.xlsx` | XLSForm à déployer (408 questions saisies, 15 pages, FR + EN) |
| `theme.py` | Identité visuelle MDS (couleurs du logo, bandeau, logo embarqué) |
| `logo_mds_blanc.txt` / `logo_mds_couleur.txt` | Logo MDS en data URI |
| `build_guide.py` | Génère `guide_enqueteur.html` (questionnaire remplissable, bouton FR / EN ; scores calculés en arrière-plan, jamais affichés) |
| `build_correspondance.py` | Génère `correspondance_variables.xlsx` (noms de variables à valider) |
| `correspondance_variables.xlsx` | Nom exporté de chaque question ; lignes jaunes = nom déduit, à valider par MDS |
| `build_dashboard.py` | Génère `suivi_collecte.html` depuis l'API Kobo |
| `test_scores.py` | Rejoue les calculs de score du formulaire et vérifie 29 cas |
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

15 pages, 408 questions saisies, 3 champs déduits.

| Page | Contenu | Noté |
|---|---|---|
| 1 | Consignes : **1.** principes d'utilisation · **2.** repères pour le calibrage · **3.** dans ce formulaire — puis type d'interview | — |
| 2 | Identification de l'enquêteur (nom, opérateur, date, horaires, langue, conseiller) — jour de la semaine et **tranche horaire déduits** | — |
| 3 | **Mesures** : attente avant conseiller, durée de l'appel, mises en attente, transferts, puis — *sur transfert seulement* — renvoi, escalade | — |
| 4 | **Scénario joué** — `S01` à `S25` | — |
| 5 | **A.** Accessibilité & serveur vocal — Q1 à Q3 | 3 |
| 6 | **B.** Accueil & posture du conseiller — Q4, Q5 | 2 |
| 7 | **C.** Compréhension du besoin — Q6 à Q8 | 3 |
| 8 | **D.** Expertise & exactitude de la réponse — Q9 à Q11 | 3 |
| 9 | **E.** Résolution / FCR & ownership — Q12 à Q16 | 5 |
| 10 | **F.** Effort client & simplicité — Q17, Q18 | 2 |
| 11 | **G.** Empathie & confiance — Q19, Q20 | 2 |
| 12 | **H.** Clôture de l'entretien — Q21 à Q23 | 3 |
| 13 | **I.** Maîtrise du scénario — les 25 blocs `grp_s01` … `grp_s25`, un seul visible | 3 à 5 |
| 14 | Synthèse qualitative — Q24 à Q26 | — |
| 15 | Fin de l'évaluation — heure de fin (les scores sont calculés ici, sans être affichés) | — |

### La page de consignes est un script de terrain, pas une note de méthode

Elle tient en **deux blocs courts**, écrits pour être lus debout, le téléphone à
la main :

1. **Comment remplir** — un scénario par appel, questionnaire renseigné après
   avoir raccroché, commencer par les « Mesures », une question qui ne s'affiche
   pas n'est pas à renseigner, les quatre réponses possibles, les deux champs
   qu'ouvre un « non conforme », rien à calculer, ne jamais révéler qu'on est
   enquêteur.
2. **Comment qualifier** — ne noter que ce qui a été observé et entendu, N/A
   seulement si le critère n'a pas pu être observé, ce que décrit un
   « partiellement conforme », l'obligation d'étayer un « non conforme », et la
   définition du FCR.

**Ce qui en a été retiré** : tout ce qui relève de l'analyse et non de la
collecte — lecture du score par opérateur et par scénario, cible de médiane de
complétion, mécanique du numérateur et du dénominateur, ancien bloc « Dans ce
formulaire ». L'enquêteur décrit ce qu'il a entendu ; l'interprétation des
chiffres se fait dans la base, pas dans le questionnaire. Les retoucher =
retoucher `note_principes` et `note_calibrage` dans `build_form.py`.

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
| Renvoi — autre canal, agence ou point de vente *(posée si `NB_TRANSFERTS > 0`)* | `RENVOI` | `RENVOI_PRECISION`, **Q15** |
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

Le questionnaire compte **408 questions saisies, dont 264 conditionnelles**. Elles
se rangent en trois familles, et la liste est close :

| Famille | Questions | Déclencheur |
|---|---|---|
| Une donnée n'a d'objet que si l'événement a eu lieu | `T_ATTENTES`, `RENVOI`, `ESCALADE`, `RENVOI_PRECISION` | `NB_ATTENTES > 0`, `NB_TRANSFERTS > 0`, une destination de renvoi cochée |
| Un critère n'a d'objet que si l'événement a eu lieu | **Q15**, **Q18** | `ESCALADE` ou `RENVOI` ; `NB_ATTENTES > 0` ou `NB_TRANSFERTS > 0` |
| Un bloc de critères n'a d'objet que pour le scénario joué | les 25 blocs de la section I, `grp_s01` … `grp_s25` | `SCENARIO = S01` … `SCENARIO = S25` |
| Une non-conformité doit être qualifiée puis décrite | `Q1_ALERTE` … `Q23_ALERTE`, `S01_1_ALERTE` … `S25_4_ALERTE`, et les `_COM` correspondants | le critère vaut `0` |

**Aucun autre critère ne dépend d'un fait relevé.** Le balayage a repris les 23
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
ses critères entrent dans `SCORE_TOTAL` au même titre que Q1 à Q23. Un appel est
donc noté sur **23 + 3 à 5 critères**, jamais sur 129. `SCORE_I` porte le score
de la section, calculé en arrière-plan comme `SCORE_A` … `SCORE_H`.

**Noms d'export** : `S01_1` … `S25_5`, avec `S01_1_ALERTE` et `S01_1_COM` sur
toute non-conformité, comme les 23 autres. Le fichier reste plat : 106 colonnes
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

Les **129 critères** — les 23 critères de comportement des sections A à H, plus
les 106 critères de scénario de la section I — partagent **une seule échelle**,
ce qui rend les sections directement comparables : totalement conforme, partiellement conforme /
perfectible, non conforme, non applicable — valant respectivement **100**, **50**,
**0** et rien.

**Le barème ne s'affiche jamais à l'enquêteur.** Ni le chiffre au bout de la
modalité — les libellés sont les quatre formulations ci-dessus, sans « (100) » ni
« (N/A) » — ni le score de section pendant la saisie. Il coche ce qu'il a
entendu ; la conversion se fait en arrière-plan et **aucun score ne s'affiche
nulle part dans le questionnaire**, pas même à la dernière page : les scores
partent avec la soumission et se lisent dans la base et sur le tableau de
bord. Le code stocké (`100`, `50`, `0`, `na`) et la
colonne `points` sont inchangés : l'export, le tableau de bord et le site de
suivi ne voient aucune différence.

**Le barème est déclaré une seule fois**, dans la colonne `points` de la liste
`conformite` de `build_form.py`. Il alimente trois choses sans être recopié :

| Sortie | Ce qu'elle en fait |
|---|---|
| `questionnaire_audit_call_center.xlsx` | `SCORE_A` … `SCORE_I` **et** `SCORE_TOTAL` en `calculate` — calculés en XPath, exportés, jamais affichés |
| `guide_enqueteur.html` | Le même calcul, rejoué en JavaScript, également en arrière-plan : aucun score n'est montré |
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
fabriquées, et vérifie 29 cas — dont l'exclusion des N/A, celle des questions
masquées, l'arrondi et l'absence de division par zéro sur formulaire vierge :

```
$ python test_scores.py
  OK   Appel parfait : les 23 criteres a 100, escalade et renvoi survenus
  OK   N/A sort du denominateur : Q2 = N/A, A ne porte que sur Q1 et Q3
  OK   Q15 masquee (ni escalade ni renvoi) : E porte sur Q12, Q13, Q14 et Q16
  …
29/29 cas conformes
```

## Sur un 0 : qualifier, puis décrire

Consigne du PDF : « tout score de 0 ou toute situation exceptionnelle doit être
étayé par un fait observé ou une formulation exacte du conseiller ». L'enquêteur,
lui, ne lit pas « 0 » mais **« non conforme »** : c'est le même code stocké, avec
le vocabulaire de la page.

Un « non conforme » ouvre donc **deux champs, dans cet ordre** :

| Ordre | Champ | Rôle |
|---|---|---|
| 1 | `Q<n>_ALERTE` — choix multiple | Quel cas d'alerte critique ce constat révèle-t-il ? Un des cas nommés proposés par la section — la liste n'en propose pas d'autre. |
| 2 | `Q<n>_COM` — texte | Le fait observé ou la formulation exacte du conseiller. |

**L'alerte est posée avant le commentaire, délibérément.** L'enquêteur qualifie
le constat avant de le décrire : la description qu'il rédige ensuite sait ce
qu'elle doit établir. Décrire d'abord et classer après produit des commentaires
qui n'étayent pas le cas coché.

Les deux champs ne s'affichent **que lorsque la réponse est 0**, et sont alors
obligatoires. Les libellés sont les mêmes pour les 129 critères — « Non conforme —
quel cas d'alerte critique ce constat révèle-t-il ? » puis « Non conforme —
décrivez le fait observé ou rapportez la formulation exacte du conseiller » — ce
qui en fait deux libellés à traduire et à relire, pas quarante-quatre.

**Tout 0 est une alerte critique.** La question ne demande pas *si* le constat
en est une, mais *lequel* il révèle : « Aucune alerte critique » a été retirée
des listes proposées sur les critères. La question restant obligatoire,
un 0 nomme forcément un cas — c'est la règle voulue, un « non conforme »
n'étant pas une note basse parmi d'autres mais un manquement à signaler.

Deux conséquences à connaître avant d'exploiter les données :

- **le compte d'alertes suit désormais le compte de 0.** Un appel qui porte
  trois non-conformités déclare au moins trois alertes. Les alertes ne
  distinguent plus le manquement grave du manquement ordinaire : c'est le
  *cas coché* qui porte cette information, plus le fait qu'une alerte existe ;
- **la liste reste fermée.** Un 0 qu'aucun des cas nommés ne décrit
  exactement oblige l'enquêteur à rattacher son constat au cas le moins
  éloigné. `Q<n>_COM`, obligatoire juste en dessous, reste l'endroit où le fait
  réel est consigné — c'est lui qu'il faut lire pour interpréter le cas coché.

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

Elle se coche **là où elle se révèle**, et nulle part ailleurs : sur le
**critère noté 0** qui la révèle, dans le champ `Q<n>_ALERTE`. Voir *Sur un 0 :
qualifier, puis décrire*.

Rattacher l'alerte au critère qui la révèle donne deux choses qu'une page dédiée
ne donnait pas : le **commentaire qui l'étaye est déjà là**, juste en dessous, et
l'analyse sait **quel point de contrôle** a produit l'alerte.

> **La page « Alertes critiques — à signaler obligatoirement » a été
> supprimée.** Placée avant la synthèse, elle reposait la question à chaque
> appel pour ne ramasser qu'un reliquat — les cas observés hors d'un critère
> noté 0 — et faisait rouvrir, une fois par appel, une saisie déjà faite.
> Ses deux variables, `ALERTES` et `ALERTES_COM`, ont disparu de l'export, et
> « Aucune alerte critique », qui n'existait plus que pour elle, a disparu des
> listes.

**Six listes, une par point de contrôle.** Le PDF de septembre 2026 ne donne pas
un seul bloc d'alertes mais **quatre** : les cinq cas généraux, six cas propres à
l'accessibilité et au serveur vocal, six cas propres à la compréhension du
besoin, puis — pour l'expertise — trois cas **par critère**, Q9, Q10 et Q11
séparément. Chaque critère noté ne se voit proposer que les cas qu'il peut
réellement révéler :

| Liste | Proposée sur | Cas |
|---|---|---|
| `alertes_nc` | `Q4`, `Q5`, `Q12` … `Q23` et les 106 critères de scénario | les 5 cas généraux |
| `alertes_a` | `Q1`, `Q2`, `Q3` — **A.** Accessibilité & serveur vocal | 6 cas, **à la place** des généraux |
| `alertes_c` | `Q6`, `Q7`, `Q8` — **C.** Compréhension du besoin | 5 + 6 = **11** |
| `alertes_q9` | `Q9` — maîtrise des offres et procédures | 5 + 3 = **8** |
| `alertes_q10` | `Q10` — exactitude et cohérence | 5 + 3 = **8** |
| `alertes_q11` | `Q11` — pédagogie et clarté | 5 + 3 = **8** |

La liste **générale** — les cinq cas du document — est celle de `alertes_nc` :

| Code | Cas |
|---|---|
| `confidentialite` | Violation ou exposition de données personnelles / défaut manifeste de confidentialité |
| `info_erronee` | Information manifestement erronée susceptible d'entraîner une perte financière ou un préjudice client |
| `irrespect` | Propos irrespectueux, agressifs, discriminatoires ou attitude manifestement non professionnelle |
| `promesse` | Promesse de délai / de traitement non maîtrisée ou engagement trompeur |
| `abandon` | Transfert, renvoi en agence ou abandon de prise en charge manifestement non justifié |

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

Elle ne se propose que sur des critères notés 0 : « Aucune alerte critique » n'y
figure pas.

**Elle remplace les cinq cas généraux, elle ne s'y ajoute pas** — c'est la seule
des six listes dans ce cas. La section A se joue **avant toute prise de ligne** :
les cinq cas généraux sont tous des faits du conseiller, et aucun n'y est
observable — proposer « propos irrespectueux » sur un menu vocal n'a pas de sens.
À l'inverse, une boucle IVR sans sortie ou une coupure avant mise en relation n'a
d'équivalent nulle part ailleurs dans le questionnaire.

### C et D complètent les cas généraux au lieu de les remplacer

Sur `Q6`, `Q7` et `Q8` — **C. Compréhension du besoin** — un conseiller est en
ligne : les cinq cas généraux y sont tous observables. Les six cas du PDF
**s'ajoutent** donc aux cinq (liste `alertes_c`, 11 modalités). Le document ne
les détaille pas critère par critère : la section n'a qu'une liste.

| Code | Cas |
|---|---|
| `interruption` | Interruption répétée ou inappropriée du client, empêchant l'expression complète du besoin |
| `sans_ecoute` | Absence totale d'écoute active : le conseiller ne manifeste aucun intérêt ou ne tient pas compte des propos du client |
| `questions_hors_sujet` | Questions non pertinentes ou hors sujet, traduisant une mauvaise qualification du problème |
| `sans_reformulation` | Absence de reformulation ou de validation, entraînant une mauvaise compréhension du motif d'appel |
| `besoin_mal_compris` | Erreur manifeste d'interprétation du besoin, conduisant à une réponse ou une action inadaptée |
| `demande_ignoree` | Demande du client ignorée ou détournée, sans justification ni orientation vers une solution appropriée |

Pour **D. Expertise & exactitude de la réponse**, le PDF va plus loin : il donne
les cas **critère par critère**, trois pour chacun. Chaque critère a donc sa
propre liste, elle aussi ajoutée aux cinq cas généraux :

| Critère | Liste | Code | Cas |
|---|---|---|---|
| `Q9` — offres, services, procédures | `alertes_q9` | `offre_fausse` | Information fausse ou incohérente sur une offre ou un service |
| | | `procedure_mal_expliquee` | Procédure mal expliquée, entraînant une mauvaise orientation du client |
| | | `promesse_irrealiste` | Promesse non maîtrisée : délai irréaliste ou engagement impossible à tenir |
| `Q10` — exactitude et cohérence | `alertes_q10` | `reponse_contradictoire` | Réponse contradictoire par rapport aux procédures officielles |
| | | `erreur_manifeste` | Erreur manifeste dans les informations fournies (tarifs, conditions, délais) |
| | | `engagement_trompeur` | Engagement trompeur pouvant induire le client en erreur |
| `Q11` — pédagogie et clarté | `alertes_q11` | `explication_confuse` | Explication confuse ou trop technique, incompréhensible pour le client |
| | | `sans_etapes` | Absence d'étapes ou d'alternatives claires pour résoudre le problème |
| | | `jargon` | Langage inadapté : jargon interne, termes non vulgarisés |

**Remplacer ou compléter, la règle est la même** : un critère ne propose que ce
qu'il peut révéler. La section A ne remplace les cas généraux que parce qu'aucun
n'y est observable ; partout ailleurs ils le sont, et les cas nommés viennent en
plus.

Aucune des six ne porte `aucune` : toutes ne se proposent qu'en face d'un critère
noté 0, où la question doit nommer un cas. Le tableau de bord les agrège sans cas
particulier, et chaque cas n'a qu'une traduction quelle que soit la liste qui le
porte. Le paramètre `alertes=` de `critere()` choisit la liste ; un critère qui
aurait besoin de la sienne se traite de la même façon.

**« Aucune alerte critique » n'existe plus.** La modalité était un ajout au
document : cinq cases seules ne disent pas si un questionnaire sans case cochée
signifie « aucune alerte » ou « l'enquêteur a sauté la question ». Elle n'avait
donc de sens que sur une question posée à **tous** les appels — la page dédiée,
aujourd'hui supprimée. En face d'un critère noté 0, la question ne demande pas
*si* le constat est une alerte mais **lequel** il révèle : une sortie y serait
une échappatoire, et la modalité en avait déjà été retirée.

**La liste reste fermée sur les cas nommés.** Une modalité « Autre cas » avait
été ajoutée puis retirée : les cas à signaler sont ceux du document, et un
manquement grave qui n'y entre pas se décrit dans le commentaire plutôt que
dans une case fourre-tout que le dépouillement ne sait pas agréger.

**Toute alerte est étayée par le `Q<n>_COM` du critère**, obligatoire juste en
dessous. Il n'existe plus de commentaire d'alerte séparé : la description est là
où le cas a été coché.

Un manquement grave qu'aucun des cas nommés ne décrit se consigne dans ce même
`Q<n>_COM` — la liste reste fermée sur les cas du document, et une modalité
« Autre cas » avait été ajoutée puis retirée parce que le dépouillement ne sait
pas l'agréger.

Le tableau de bord leur consacre **une tuile et un panneau à part** : nombre
d'appels portant au moins une alerte, et répartition par cas. `alertes_de()`
dans `build_dashboard.py` relit tous les `Q<n>_ALERTE`, quelle que soit la liste
dont le cas provient, et dédoublonne : le même cas signalé sur deux critères
reste une alerte pour l'appel.

## Questions conditionnelles

Consigne MDS : « escalade, renvoi en agence, mise en attente ou demande de
pièces ne doivent être renseignés que si l'événement s'est produit ; un
questionnaire digital doit masquer automatiquement les questions non
applicables ». Cinq familles de champs sont conditionnelles :

| Champ | S'affiche si |
|---|---|
| `T_ATTENTES` — durée cumulée des mises en attente | `NB_ATTENTES > 0` |
| `RENVOI` — autre canal, agence ou point de vente | `NB_TRANSFERTS > 0` |
| `ESCALADE` — dossier transmis ou rappel promis | `NB_TRANSFERTS > 0` |
| `RENVOI_PRECISION` — canal, agence ou point de vente indiqués | `RENVOI` vaut `1`, `2` **ou** `3` |
| **Q15** — motif, étapes, pièces et délai de l'escalade / du renvoi | `ESCALADE = Oui` **ou** `RENVOI` vaut `1`, `2` ou `3` |
| **Q18** — mises en attente, transferts et changements de canal | `NB_ATTENTES > 0` **ou** `NB_TRANSFERTS > 0` |
| **Q26_TXT** — pourquoi le client devrait rappeler ou changer de canal | `Q26 = Oui` |
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
| Un code du PDF est repris tel quel | `Q1` → `Q1`, `Q23` → `Q23` |
| Une durée prend le préfixe `T_` | `T_ATTENTE`, `T_ATTENTES`, `T_DUREE_APPEL` |
| Un champ d'identification prend un nom parlant | `IDENT_CONSEILLER`, `TRANCHE_HORAIRE`, `ESCALADE`, `RENVOI` |
| *(nouveau)* Un commentaire suffixe la question qu'il justifie | `Q15` → `Q15_COM`, `ALERTES` → `ALERTES_COM` |
| *(nouveau)* Une alerte critique suffixe le critère qui la révèle | `Q15` → `Q15_ALERTE` |
| *(nouveau)* Un verbatim suffixe sa question | `Q26` → `Q26_TXT` |
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

1. **Pas de page suivante sans page précédente correctement remplie.**
   `settings.style = pages`, un groupe `field-list` par section, et toutes les
   questions sont `required` — sans exception. Enketo et KoboCollect bloquent
   alors la navigation ; le guide HTML fait de même, et le contrôle y porte sur
   **deux choses** :
   - ce qui **manque** — les réponses obligatoires visibles de l'étape sont
     surlignées, les étapes suivantes restent verrouillées ;
   - ce qui est **faux** — les `constraint` du formulaire (date dans le futur,
     durée hors bornes, heure de fin antérieure à l'heure de début) sont
     **rejouées dans le navigateur**. La faute est surlignée **dès la saisie**,
     nommée par le message de contrainte du formulaire, et retient à l'étape
     tant qu'elle n'est pas corrigée.

   Tout se dit donc **au changement de page**, pas à la fin : le sommaire marque
   en rouge l'étape fautive, et revenir en arrière reste possible — c'est
   justement ce qu'il faut faire pour corriger — mais l'étape quittée part
   marquée. `attr_contrainte()` dans `build_guide.py` traduit les contraintes du
   XLSForm ; **une forme qu'il ne saurait pas rejouer est signalée à la
   génération** plutôt qu'ignorée en silence.
2. **Saisie libre limitée à ce que le PDF exige.** Le formulaire compte 135
   champs texte, dont **129 qui ne s'ouvrent que sur un incident** : le
   commentaire de chacun des 129 critères notés, ouvert sur un 0 et sur lui
   seul. Sur un appel sans non-conformité, l'enquêteur n'en voit aucun. Les 6
   autres sont le nom de l'enquêteur, l'identification du conseiller, la
   précision du renvoi et les trois champs de la synthèse qualitative (Q24, Q25,
   Q26 « pourquoi »). Ce dernier est lui aussi conditionnel : il ne s'ouvre que
   si Q26 vaut **Oui** — si le client n'a pas à rappeler, il n'y a rien à
   expliquer.
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
| Q1 « Oui, totalement **conformes** / Partiellement **conformes** » *(pluriel sur cette seule question)* | Singulier, comme les 22 autres — une seule liste de modalités pour tout le questionnaire |
| Q25 « … effort subi par le client » *(sans point d'interrogation)* | « … effort subi par le client **?** » |
| **Le numéro `Q23` est employé deux fois** : le critère « sondage de satisfaction » de la section H, puis la première question de la synthèse qualitative | Le critère garde `Q23` ; la synthèse se décale en **`Q24`, `Q25`, `Q26`**. Voir *Le PDF v1.2 numérote deux questions Q23*. |
| Sections numérotées A à H | Reprises telles quelles |

### 4. Ajouts

| Ajout | Motif |
|---|---|
| **Type d'interview** (TEST / Live) | Consigne MDS du JOB 001/26 : les interviews de test ne se reconnaissent plus à l'analyse. Absent du PDF. |
| **Toutes les durées en secondes** | Le PDF collecte la durée de l'appel au format « ___ min ___ sec », l'attente et les mises en attente en secondes. Une seule unité partout : l'enquêteur convertit sa lecture de chronomètre une fois, à la saisie, et le dépouillement n'a plus de conversion à faire. `TEMPS_TOTAL` (minutes) reste déduit, pour le JOB 001/26. |
| **Le renvoi en une liste de destinations**, `RENVOI`, **posée après un transfert seulement** — comme `ESCALADE` | Une case unique « autre canal / agence » sortait un `RENVOI_CANAL = Oui` sans dire si le client avait été envoyé sur l'application ou en boutique — deux traitements qui n'ont ni le même coût pour lui ni la même lecture à l'analyse. Deux cases oui / non l'ont dit un temps, au prix de deux « Non » à cocher pour signifier qu'il n'y avait pas eu de renvoi du tout. Une liste unique énonce les destinations et met « Aucun renvoi » parmi elles : une question, une réponse, une colonne — et l'agence se distingue enfin du point de vente, ce que les deux cases confondaient. La condition `NB_TRANSFERTS > 0` est une consigne MDS : voir le point ouvert 11. |
| **`TRANCHE_HORAIRE` déduite de `HEURE_DEBUT`** au lieu d'être cochée | Le PDF fait cocher la tranche alors que l'heure est déjà saisie juste au-dessus : deux champs pour une même information, qui peuvent se contredire. Le calcul supprime l'écart et une saisie. Les heures hors `07h - 22h`, que le PDF ne prévoit pas, sont rattachées à la tranche la plus proche. Voir *La tranche horaire se déduit de l'heure de début*. |
| **Une liste d'alertes par point de contrôle** — `alertes_a` sur `Q1` à `Q3`, `alertes_c` sur `Q6` à `Q8`, `alertes_q9` / `alertes_q10` / `alertes_q11` sur leur seul critère | Le PDF donne quatre blocs d'exemples d'alertes sans dire où les poser. Ils sont rattachés aux critères qu'ils décrivent : un critère ne propose que les cas qu'il peut révéler. La section A **remplace** les cinq cas généraux, faute qu'aucun y soit observable ; C et D les **complètent**. Voir *Alertes critiques*. |

### 5. Le PDF v1.2 numérote deux questions Q23

La version 1.2 ajoute en section **H. Clôture de l'entretien** un critère noté
qu'elle numérote `Q23` :

> *Le conseiller a-t-il informé le client qu'il recevra un sondage de
> satisfaction afin de partager son avis ?*

Mais la **Synthèse qualitative**, juste après, repart elle aussi de `Q23` — le
document porte donc deux questions sous le même numéro, l'une notée sur
100 / 50 / 0 / N/A, l'autre en texte libre. Un même code ne peut pas nommer deux
colonnes d'export.

**Le critère garde `Q23`** : il est noté, il appartient à une section notée, et
c'est lui que le barème et les scores citent. La synthèse qualitative se décale
d'un rang — `Q23`, `Q24`, `Q25` du PDF deviennent **`Q24`, `Q25`, `Q26`**, le
verbatim du dernier devenant `Q26_TXT`. Aucun libellé n'est modifié, seul le
numéro qui les préfixe l'est.

Conséquence sur le score : la section H passe de 2 à **3 critères**, et le
questionnaire de 128 à **129 critères notés** — 23 de comportement plus les 106
de scénario. Un appel reste noté sur 23 + 3 à 5 critères.

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
    `RENVOI` et `ESCALADE` ne s'affichent que si
    `NB_TRANSFERTS > 0`, à la demande de MDS. Les deux cas se produisent
    pourtant sans transfert, et **les données le montrent déjà** :
    - un **renvoi** sans transfert — le conseiller répond lui-même puis oriente
      vers l'agence ou l'application. La première soumission de la collecte est
      exactement ce cas (`NB_TRANSFERTS = 0`, renvoi vers un autre canal, précision
      « Canal Principal ») ;
    - une **escalade** sans transfert — « je transmets au service technique, on
      vous rappelle sous 48 h », l'appel n'ayant été passé à personne. Une autre
      soumission est ce cas (`NB_TRANSFERTS = 0`, `ESCALADE = Oui`).

    Ces colonnes sortiront désormais vides sur les appels non transférés, et
    **Q15 ne s'ouvrira plus du tout sans transfert** — ses deux déclencheurs
    sont derrière la même condition. La section E y porte alors sur 4 critères
    au lieu de 5 : le conseiller qui escalade ou oriente mal sans transférer
    n'est plus évalué là-dessus. À rouvrir si le pilote montre des escalades ou
    des renvois manquants — le correctif tient en deux conditions.
12. **Cible de complétion ≤ 5 minutes.** Le PDF la fixe « après calibrage et
    paramétrage de la logique conditionnelle ». Elle est atteignable : sur un
    appel sans non-conformité, l'enquêteur saisit 22 boutons radio, les mesures,
    le scénario, une case « aucune alerte » et trois champs texte — ni alerte
    ni commentaire ne s'ouvre. Chaque 0 coûte en revanche deux saisies de plus,
    la qualification puis la description. À mesurer au pilote.
13. **Le renvoi ne déclare qu'une destination.** `RENVOI` est un choix unique :
    un appel qui en porte deux — « faites-le sur l'appli, sinon passez en
    agence » — n'en code qu'une, et la seconde ne se lit que dans
    `RENVOI_PRECISION`, en texte libre. Arbitrage assumé au profit d'une
    colonne unique et d'une saisie unique. À rouvrir en `select_multiple` si le
    pilote montre des renvois doubles fréquents : le correctif tient en une
    ligne de `build_form.py`, mais il change le format de la colonne — Kobo
    exporte alors une liste de codes séparés par des espaces — et donc la
    lecture de `n_renvoi` dans `build_dashboard.py`.
