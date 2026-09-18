# Prompt — site de suivi de collecte en direct (MDS JOB 002/26)

> À copier tel quel dans une session de développement neuve, dans un dossier vide.
> Tout ce dont l'agent a besoin est ci-dessous : il n'a pas accès au projet Python.

---

## Contexte

MDS (Marketing & Distribution Services, Cameroun) conduit **MS Ghost Check** : un
audit client mystère des call center **Orange** et **MTN**. Les enquêteurs
appellent, jouent un scénario, raccrochent, puis remplissent un questionnaire
dans **KoboCollect**. Le questionnaire est déjà déployé et opérationnel.

Je veux un **site web indépendant**, hébergé sur **Vercel**, qui se branche sur
cette collecte KoboToolbox et sert d'**écran de pilotage du terrain en direct** :
combien d'appels, par qui, sur quel opérateur, avec quel score, et surtout quelles
alertes critiques remontent.

Ce n'est pas un outil d'analyse : pas de filtres complexes, pas d'export. C'est un
écran qu'on laisse ouvert pendant le terrain et qui se met à jour tout seul.

---

## Contraintes non négociables

1. **Le jeton Kobo ne doit JAMAIS atteindre le navigateur.** Pas de
   `NEXT_PUBLIC_KOBO_TOKEN`, pas d'appel `fetch` vers Kobo depuis du code client.
   C'est un jeton de **compte** : il ouvre tous les projets de l'organisation. Le
   navigateur appelle une route serveur Next.js, qui seule détient le jeton. Cela
   règle aussi le CORS, qui bloquerait un appel direct navigateur → Kobo.
2. **Ne jamais recopier le barème dans le code.** Il est lu dans l'API Kobo — voir
   « Barème » plus bas. Si MDS fait corriger un score, le site doit suivre sans
   modification de code.
3. **Ne jamais inventer de données.** Le projet peut compter zéro soumission : la
   page affiche alors un état vide honnête (« en attente des premiers appels »),
   jamais un jeu de démonstration.
4. **Exclure les interviews de test.** Toute soumission dont `TYPE_INTERVIEW` vaut
   `test` est écartée de tous les calculs. C'est une consigne MDS ferme : ces
   appels ne sont pas du terrain.
5. **Accès protégé par un mot de passe unique**, partagé dans l'équipe MDS. Ce sont
   des données d'audit confidentielles sur deux opérateurs concurrents.

---

## Pile technique

- **Next.js (App Router) + TypeScript**, déployé sur Vercel.
- Aucune base de données. Aucune authentification tierce.
- `middleware.ts` : Basic Auth sur tout le site, comparée à `SITE_PASSWORD`.
- Graphiques en **SVG écrit à la main** (pas de librairie de charts) — le rendu
  doit rester léger et maîtrisé.
- Variables d'environnement :

```
KOBO_URL=https://kf.kobotoolbox.org
KOBO_TOKEN=          # jeton API, côté serveur uniquement
KOBO_UID=            # uid du projet (22 caractères, commence par « a »)
SITE_PASSWORD=       # mot de passe unique du site
```

Livre un `.env.example` avec ces quatre clés et un `README.md` qui explique le
déploiement Vercel (import du dépôt, saisie des variables, `Deployment
Protection` en complément si souhaité).

---

## L'API KoboToolbox

Authentification : en-tête `Authorization: Token <KOBO_TOKEN>` sur chaque appel.

### 1. Définition du formulaire — le barème et les libellés

```
GET {KOBO_URL}/api/v2/assets/{KOBO_UID}/?format=json
```

La réponse contient `content` avec trois clés utiles :

- **`content.translations`** — l'ordre des langues :
  `["Français (fr)", "English (en)"]`. Tous les libellés sont des **tableaux
  indexés sur cet ordre** : `label[0]` = français, `label[1]` = anglais.
- **`content.survey`** — les lignes du questionnaire, dans l'ordre. Exemple :

```json
{ "name": "Q1", "type": "select_one", "select_from_list_name": "conformite",
  "label": ["Q1 Le message d'accueil et les menus du serveur vocal…",
            "Q1 Did the welcome message and the IVR menus…"],
  "required": true }
```

  Les groupes apparaissent comme `{"type": "begin_group", "name": "grp_a",
  "label": ["A. ACCESSIBILITÉ & SERVEUR VOCAL", …]}` et se ferment par
  `{"type": "end_group"}`. Les champs calculés portent `"read_only": "yes"` et une
  `calculation`.
- **`content.choices`** — les modalités. **La colonne `points` porte le barème** :

```json
{ "list_name": "conformite", "name": "100", "points": "100",
  "label": ["Oui, totalement conforme (100)", "Yes, fully compliant (100)"] }
```

Mets cette réponse en cache **5 minutes** : la définition ne change qu'à un
redéploiement.

### 2. Les soumissions

```
GET {KOBO_URL}/api/v2/assets/{KOBO_UID}/data/?format=json
```

Réponse : `{ "count": n, "results": [ … ] }`. Chaque soumission est un objet plat
dont les clés sont **préfixées par le groupe** : `grp_a/Q1`, `grp_mesures/T_ATTENTE`.
Écris un accesseur qui compare le **dernier segment** de la clé, pas la clé
entière — les préfixes changeraient si le questionnaire était réorganisé.

Champs système utiles : `_id`, `_submission_time` (ISO), `_submitted_by`.

Mets cette réponse en cache **30 secondes**. Le client interroge la route serveur
toutes les 30 s.

---

## Le barème — la règle de calcul

Elle est **essentielle** et se trompe facilement. Reproduis-la exactement.

Les critères notés utilisent tous la même liste `conformite`. Il y en a **128** :
les 22 critères de comportement `Q1` … `Q22`, posés à chaque appel, et les 106
critères de scénario `S01_1` … `S25_5`, dont **seuls ceux du scénario joué sont
posés** — 3 à 5 par appel, les autres étant masqués. Ne déduis pas la liste de
leur nom : prends tout critère dont la question tire sa liste de `conformite`.

| Réponse | `points` | Effet |
|---|---|---|
| `100` | `100` | 100 au numérateur, 100 au dénominateur |
| `50` | `50` | 50 au numérateur, 100 au dénominateur |
| `0` | `0` | 0 au numérateur, 100 au dénominateur |
| `na` | *(vide)* | **exclu du numérateur ET du dénominateur** |

```
score = 100 × (Σ points obtenus) / (Σ 100 par critère effectivement noté)
```

Trois pièges, tous du même côté :

- **Une réponse absente de la soumission n'est pas un zéro.** Elle a été masquée
  par la logique conditionnelle (`Q15` sans escalade ni renvoi, `Q18` sans mise en
  attente ni transfert, et surtout **les 101 critères des scénarios non joués**,
  absents de toute soumission) : elle sort des deux sommes. C'est le cas le plus
  fréquent, pas un cas limite — un appel porte 25 à 27 critères sur 128.
- **`na` n'est pas un zéro non plus** — sa colonne `points` est vide.
- **Dénominateur nul → pas de score**, affiche « — ». Jamais 0, jamais une
  division par zéro.

Le dénominateur se déduit de `points !== ""`, jamais d'une liste écrite en dur.

**Sections.** Les critères se répartissent en 9 sections A→I. Déduis-les de la
structure `begin_group` / `end_group` de `content.survey` : tout critère noté
rencontré entre l'ouverture d'un groupe dont le libellé commence par une lettre
suivie d'un point (`A.`, `B.`, …) et sa fermeture appartient à cette section.
N'écris pas la table des sections en dur.

**La section I est imbriquée d'un niveau.** Elle contient 25 sous-groupes, un par
scénario (`grp_s01` … `grp_s25`), dont le libellé est celui du scénario et non
une lettre suivie d'un point. Compte donc les `begin_group` / `end_group` avec
une pile : un critère appartient à la section de la **lettre la plus proche en
remontant**, pas du groupe qui l'entoure directement.

---

## Les données à afficher

Variables exportées (nom = dernier segment de la clé de soumission) :

| Variable | Contenu |
|---|---|
| `TYPE_INTERVIEW` | `test` / `live` — **filtrer sur `live`** |
| `NOM_ENQ` | nom de l'enquêteur |
| `DATE_INTERVIEW`, `JOUR_SEMAINE`, `HEURE_DEBUT`, `HEURE_FIN` | horodatage déclaré |
| `OPERATEUR` | `orange` / `mtn` |
| `LANGUE_ENQ` | `fr` / `en` |
| `IDENT_CONSEILLER` | nom ou matricule du conseiller |
| `TRANCHE_HORAIRE` | `1` = 07h-12h, `2` = 12h-18h, `3` = 18h-22h — **déduite de `HEURE_DEBUT`**, jamais saisie ; une heure hors 07h-22h est rattachée à la tranche la plus proche |
| `SCENARIO` | `S01` … `S25` — libellé « code · famille · scénario » dans les choices |
| `T_ATTENTE` | attente avant conseiller, en secondes |
| `T_ATTENTES` | cumul des mises en attente, en secondes |
| `T_DUREE_APPEL` | durée de l'appel, **en secondes** |
| `TEMPS_TOTAL` | la même durée **en minutes**, déduite — seule valeur du questionnaire qui ne soit pas en secondes, conservée pour empiler la collecte avec le JOB 001/26 |
| `NB_ATTENTES`, `NB_TRANSFERTS` | nombre de mises en attente et de transferts |
| `RENVOI_CANAL`, `RENVOI_AGENCE`, `ESCALADE` | `1` = Oui, `2` = Non. Les trois ne sont posés que si `NB_TRANSFERTS > 0` : absents sinon, ce qui n'est pas un « Non ». `RENVOI_CANAL` a porté « canal **ou** agence » jusqu'au 16/09/2026 — ne compare pas les deux périodes sur cette colonne |
| `RENVOI_PRECISION` | texte libre, présent si l'un des deux renvois vaut Oui |
| `Q1` … `Q22` | les 22 critères de comportement, posés à chaque appel |
| `S01_1` … `S25_5` | les 106 critères de scénario ; **seuls ceux du scénario joué sont renseignés**, les autres sont absents de la soumission |
| `Q1_ALERTE` … `Q22_ALERTE`, `S01_1_ALERTE` … `S25_5_ALERTE` | choix multiple, présent **uniquement** si le critère vaut `0` : le ou les cas d'alerte critique que ce 0 révèle, ou `aucune` |
| `Q1_COM` … `Q22_COM`, `S01_1_COM` … `S25_5_COM` | commentaire obligatoire, présent **uniquement** si le critère vaut `0` : le fait qui étaye le 0 et l'alerte ci-dessus |
| `ALERTES` | choix multiple, **le reliquat seul** : les cas observés hors d'un critère noté `0`. Mêmes codes |
| `ALERTES_COM` | description factuelle des cas cochés dans `ALERTES` |

**Codes d'alerte**, séparés par des espaces. Liste **générale**, proposée sur
les critères des sections B à I et dans `ALERTES` : `confidentialite`,
`info_erronee`, `irrespect`, `promesse`, `abandon`.

`Q1_ALERTE`, `Q2_ALERTE` et `Q3_ALERTE` — **A. Accessibilité & serveur vocal** —
portent une **autre liste**, et sont les seuls champs où ces codes apparaissent :
`accueil_incoherent`, `menus_errones`, `langue_indisponible`, `boucle_ivr`,
`coupure_redirection`, `attente_non_signalee`. La section se joue avant toute
prise de ligne : les cas généraux sont des faits du conseiller et n'y sont pas
observables.

Les deux listes partagent `autre` — une alerte réelle qui n'entre dans aucun des
cas nommés, qualifiée par le commentaire du critère — et `aucune`. **Ne suppose
pas quelle liste porte un champ** : lis les codes tels qu'ils arrivent, tous
sont des cas d'alerte sauf `aucune`.

> **Les alertes d'un appel se lisent dans tous les champs `*_ALERTE`, pas un.**
> Union de chaque `<critère>_ALERTE` — `Q1` à `Q22` comme `S01_1` à `S25_5` — et
> de `ALERTES`, `aucune` écartée, **dédoublonnée** : le même cas coché sur deux
> critères reste une alerte pour l'appel. Ne compte pas `ALERTES` seul — la
> plupart des alertes sont rattachées au critère qui les révèle. Repère ces
> champs par leur suffixe `_ALERTE`, jamais par une liste écrite en dur.
> `alertes_de()` dans `build_dashboard.py` fait exactement cela.
| `Q23`, `Q24` | point fort / principal irritant (texte libre) |
| `Q25`, `Q25_TXT` | le client doit-il rappeler ? (`1`/`2`) et pourquoi |
| `SCORE_A` … `SCORE_I`, `SCORE_TOTAL` | scores calculés par le formulaire — **recalcule-les toi-même** plutôt que de les lire, pour rester juste si un formulaire ancien est soumis |

---

## L'écran

Une seule page, qui se rafraîchit seule toutes les 30 s, avec un indicateur
discret « mis à jour il y a N s ». De haut en bas :

1. **Bandeau** — titre, période couverte, horodatage de mise à jour, témoin
   « en direct ».
2. **Tuiles de tête** — gros chiffres : appels aujourd'hui / total, enquêteurs
   actifs aujourd'hui, score total moyen, **alertes critiques** (nombre d'appels
   concernés), appels où le client devra rappeler (`Q25 = 1`).
3. **Alertes critiques — le panneau le plus important.** Liste des appels portant
   au moins une alerte, le plus récent en tête : date/heure, enquêteur, opérateur,
   scénario, puis **une ligne par alerte** — le cas coché, le critère qui l'a
   révélée (`Q14`, `Q20`…) ou « hors critère noté » pour celles de `ALERTES`, et
   le commentaire qui l'étaye en entier (`Q<n>_COM`, ou `ALERTES_COM` pour le
   reliquat). C'est ce qu'un responsable terrain doit voir sans cliquer.
4. **Volume par jour** — barres, depuis le premier appel.
5. **Orange vs MTN** — volume et score moyen côte à côte.
6. **Par enquêteur** — nombre d'appels aujourd'hui et au total, score moyen.
7. **Répartition des notes** — barre empilée 100 / 50 / 0 / N/A sur tous les
   critères renseignés.
8. **Score par section** — les 9 sections A→I, Orange face à MTN. Rappelle le
   nombre de critères derrière chaque moyenne : la section I n'en porte que
   3 à 5 par appel, sa moyenne est plus fragile que les autres.
9. **Dernières soumissions** — 15 lignes : heure, enquêteur, opérateur, scénario,
   attente, durée, score, pastille d'alerte.

États vides : chaque panneau dit « aucune donnée » plutôt que d'afficher un zéro.

---

## Identité visuelle

Reprends l'identité MDS des livrables existants.

```css
--mds-navy:#1E428A;  --mds-amber:#F6AE42;  --mds-cyan:#1EA8DE;
--plane:#EDF1F7; --card:#FBFCFE; --ink:#16233F; --ink-2:#3E4E70; --muted:#6B7A96;
--rule:#D3DCE9; --rule-soft:#E4EAF3;
```

Polices : **Archivo** (titres), **IBM Plex Sans** (texte), **IBM Plex Mono**
(chiffres et codes, avec `font-variant-numeric: tabular-nums`).

Bandeau navy, filet ambre de 3 px en bas. Mode sombre pris en charge, avec ses
propres valeurs — jamais une inversion automatique.

### Couleurs de données — règles vérifiées, à ne pas modifier

- **Opérateurs (série catégorielle)** : Orange `#eb6834`, MTN `#1baf7a` en clair ;
  `#d95926` et `#199e70` en sombre. Paire validée pour les daltonismes
  (ΔE deutan 9,2). Le vert MTN passe sous 3:1 de contraste sur fond clair :
  **étiquette chiffrée systématique à côté de chaque barre**, et un tableau en
  regard. Ne remplace pas ces teintes.
- **Échelle 100 / 50 / 0 / N/A (série ordinale)** : **rampe bleue monochrome**,
  du foncé (100, le plus conforme) au clair (0) : `#104281`, `#2a78d6`, `#86b6ef`,
  et gris `#6B7A96` pour N/A.
  **N'utilise surtout pas vert / ambre / rouge** : cette combinaison a été mesurée
  et échoue en deutéranopie (ΔE 1,6 à 2,8 entre le vert et l'ambre) — un lecteur
  daltonien ne distingue pas « totalement conforme » de « perfectible ».
- **Alertes critiques** : rouge `#d03b3b`, réservé à cet usage, **toujours
  accompagné d'un libellé ou d'une icône**, jamais la couleur seule.
- **Volumes** : une seule teinte, le navy `#1E428A`.

### Règles de graphiques

- Jamais deux axes verticaux. Deux mesures d'échelles différentes = deux
  graphiques.
- La couleur suit l'entité, jamais son rang : filtrer ne doit pas repeindre les
  survivants.
- Marques fines, extrémités arrondies à 4 px ancrées à la ligne de base, 2 px de
  fond entre deux segments empilés.
- Grille et axes discrets ; le texte porte les couleurs d'encre, jamais la couleur
  de série.
- Survol : infobulle sur chaque marque, cible de survol plus grande que la marque.
- Légende présente dès deux séries, doublée d'étiquettes directes.

---

## Critères d'acceptation

- [ ] `grep -r "KOBO_TOKEN" app/ components/` ne renvoie **aucun** fichier client.
- [ ] Le barème n'apparaît nulle part en dur : changer un `points` dans Kobo change
      le score affiché, sans toucher au code.
- [ ] Un critère absent d'une soumission, et un `na`, sortent du dénominateur.
      Écris un test qui le prouve sur une soumission fabriquée.
- [ ] Les soumissions `TYPE_INTERVIEW = test` n'apparaissent dans aucun chiffre.
- [ ] Projet à zéro soumission : la page se charge et affiche un état vide clair.
- [ ] Sans mot de passe, toutes les routes répondent 401, `/api/*` comprise.
- [ ] La page se met à jour seule, sans rechargement complet.
- [ ] Mode clair et mode sombre lisibles tous les deux.
- [ ] `npm run build` passe sans erreur TypeScript.

## À ne pas faire

- Écrire le jeton, même « temporairement », dans du code client.
- Recopier la liste des critères notés, les sections, les 25 scénarios ou le barème
  dans le code : tout se lit dans l'API.
- Afficher des données de démonstration quand il n'y a pas de soumission.
- Ajouter une librairie de graphiques, une base de données, ou un fournisseur
  d'authentification : rien de tout cela n'est nécessaire ici.
