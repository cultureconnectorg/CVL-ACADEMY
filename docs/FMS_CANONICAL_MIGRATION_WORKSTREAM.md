# FMS Canonical Migration — Workstream de conception (DESIGN_ONLY)

```
WORKSTREAM_STATUS        = SEPARATE_WORKSTREAM
DESIGN_STATUS             = DESIGN_REQUIRED
IMPLEMENTATION            = NOT_AUTHORIZED
STRATEGY_SELECTED         = NONE — décision humaine requise
DB_FORMATIONS_MUTATION    = FORBIDDEN (toujours actif, hérité du freeze W1)
DB_PROGRESS_MUTATION      = FORBIDDEN (toujours actif, hérité du freeze W1)
MODULE_CODE_REMAP         = FORBIDDEN (toujours actif, hérité du freeze W1)
FMS_CORPUS_IMPORT         = FORBIDDEN (toujours actif, hérité du freeze W1)
LEGACY_FMS_DELETION       = FORBIDDEN (toujours actif, hérité du freeze W1)
```

Ce document ne fait rien — il ne modifie ni code, ni schéma, ni données.
Il pose les options pour résoudre le conflit identifié en W0.5
(`docs/SPATIAL_LEARNING_W0.5_FMS_SOURCE_AUDIT.md`) et **ne tranche
délibérément aucune d'entre elles** : c'est la décision produit du
demandeur, pas une décision technique que ce document doit prendre à sa
place.

---

## Rappel du problème (voir W0.5 pour la preuve complète)

```
seed_data.py       FMS-01-M01 … FMS-01-M12   (12 modules, contenu générique, seedé février 2026)
Corpus FMS réel     FMS-01-M01 … FMS-01-M15   (15 modules + A01, contenu réel validé)
```

`FMS-01-M01` existe des deux côtés avec une pédagogie totalement
différente. `db.progress` est indexé par ce même `module_code`. Toute
stratégie de branchement du corpus réel doit donc répondre à une seule
question centrale : **que devient une ligne `db.progress` déjà associée
à `FMS-01-M01` (contenu seedé) le jour où `FMS-01-M01` désigne le
contenu réel ?**

Rappel du périmètre déjà safe (W0.5) : `db.skills` et
`db.certification_rubrics` sont vides par défaut — un branchement y est
un remplissage, jamais une migration à risque. Le conflit de code
concerne strictement `db.formations` / `db.progress` sur FMS-01…06.

`db.missions` (missions écosystème CVLN, ex. `MIS-FMS-01`) et les "cas"
pédagogiques FMS (Cas Fil Rouge, Cas Inédit) restent deux concepts
produits distincts qui ne doivent **jamais** être fusionnés par
proximité lexicale — chaque stratégie ci-dessous laisse cette séparation
intacte par construction, elle n'a rien à voir avec le problème de code.

---

## Stratégie 1 — Versioning de code

Ajouter un suffixe de version au `module_code` du contenu réel plutôt
que de réutiliser le code existant : `FMS-01-M01` (seed, inchangé) reste
tel quel ; le contenu réel devient `FMS-01-M01-v2` (ou un schéma de
version équivalent, ex. `FMS-01-M01@2`).

- **Conséquence sur `db.progress`** : aucune collision possible — les
  lignes existantes restent attachées au code seed sans ambiguïté ; les
  nouvelles progressions sur le contenu réel démarrent sous un nouveau
  code, à zéro.
- **Conséquence produit** : un utilisateur qui avait terminé
  `FMS-01-M01` (seed) n'a *pas* automatiquement terminé
  `FMS-01-M01-v2` (réel) — c'est un module différent avec un contenu
  différent, donc c'est cohérent pédagogiquement, mais ça peut se lire
  comme une régression ("j'avais déjà validé ce module") si non
  communiqué.
- **Réversibilité** : totale — supprimer les entrées `-v2` n'affecte
  rien côté seed.
- **Effort** : faible techniquement (aucun remap, juste de nouveaux
  documents `db.formations` avec un nouveau code) ; effort de
  communication produit non négligeable.
- **Risque principal** : prolifère les codes dans le temps si une v3
  était un jour nécessaire ; les URLs (`/formations/:fc/modules/:mc`)
  changent, donc tout lien externe/partagé vers `FMS-01-M01` reste
  valide mais pointe vers l'ancien contenu — potentiellement trompeur
  à moyen terme si le seed n'est jamais retiré.

---

## Stratégie 2 — Espace de noms legacy / canonique

Renommer explicitement le contenu seedé sous un préfixe distinct (ex.
`LEGACY-FMS-01-M01`) au lieu de laisser le contenu réel prendre un
suffixe — le contenu réel hérite du code "propre" `FMS-01-M01`.

- **Conséquence sur `db.progress`** : nécessite une mutation des lignes
  existantes (`module_code` seed → `module_code` legacy) pour rester
  cohérentes avec le nouveau code de leur formation — ce n'est *pas*
  un no-op comme la stratégie 1, c'est un vrai remap de données
  existantes, donc `MODULE_CODE_REMAP`/`DB_PROGRESS_MUTATION` seraient
  directement engagés si cette voie était un jour choisie.
- **Conséquence produit** : les nouvelles inscriptions/le catalogue
  pointent naturellement vers le contenu réel sous le code canonique —
  aucune confusion pour un nouvel utilisateur. Un utilisateur existant
  avec de la progression sur l'ancien module la retrouve sous le
  namespace `LEGACY-`, explicitement marqué comme tel.
- **Réversibilité** : partielle — une fois la progression remappée,
  revenir en arrière suppose un remap inverse, pas juste une
  suppression.
- **Effort** : plus élevé (script de migration de données, tests de
  non-régression sur la lecture de progression) mais résultat plus
  propre à long terme (un seul code "actif" par module, pas de suffixe
  de version qui traîne).
- **Risque principal** : toute migration de données réelles
  d'utilisateurs est par nature plus risquée qu'un ajout pur (stratégie
  1) — nécessite un plan de rollback explicite testé avant exécution.

---

## Stratégie 3 — Table de correspondance (mapping table)

Introduire une collection dédiée (ex. `db.module_code_mapping`) qui
relie explicitement `{legacy_code, canonical_code, migration_status}`
sans jamais muter `db.formations`/`db.progress` directement — le moteur
de progression consulterait cette table pour savoir quel code afficher
et si une transition est en cours.

- **Conséquence sur `db.progress`** : aucune mutation directe des
  lignes existantes — la table de mapping est la seule source de vérité
  sur la relation entre les deux mondes, ce qui permet de garder
  `DB_PROGRESS_MUTATION = FORBIDDEN` respecté même après le
  branchement, au prix d'une indirection à maintenir dans le code de
  lecture.
- **Conséquence produit** : le plus flexible des trois — permet un
  affichage "vous aviez terminé l'ancienne version de ce module"
  explicite plutôt qu'un remplacement silencieux, et supporte un futur
  M13-M15/A01 qui n'a aucun équivalent legacy sans cas particulier.
- **Réversibilité** : totale — supprimer une ligne de mapping revient
  exactement à l'état d'avant, aucune donnée `db.progress` n'a été
  touchée.
- **Effort** : le plus élevé des trois à construire correctement (toute
  lecture de progression doit désormais passer par la couche de
  mapping), mais le plus sûr vis-à-vis du freeze de données actuel.
- **Risque principal** : complexité durable dans le code (une
  indirection de plus à comprendre/maintenir) si la table n'est jamais
  nettoyée une fois la transition terminée.

---

## Sous-décision transverse — que faire de la progression existante ?

Les trois stratégies ci-dessus ne répondent pas seules à cette
question ; elle doit être tranchée quelle que soit la stratégie de code
retenue :

- **Préserver telle quelle** (sous son code d'origine ou legacy) — la
  progression seed reste visible et valorisée, jamais réattribuée à un
  contenu qu'elle n'a pas réellement suivi.
- **Geler** — la progression seed devient en lecture seule, non
  transférable, marquée "ancienne édition" sans suppression.
- **Migrer avec mapping explicite** — chaque `progress` seed est
  reliée à son équivalent réel le plus proche par une table de
  correspondance construite manuellement module par module (nécessite
  une analyse pédagogique fine : quel module réel "remplace"
  fonctionnellement quel module seed, ce qui n'est pas garanti 1:1 —
  le corpus réel a 15 modules + A01 contre 12 côté seed).

Aucune de ces trois n'est neutre : "préserver" et "geler" protègent la
donnée utilisateur au prix de deux mondes qui coexistent indéfiniment
dans l'UI ; "migrer" unifie l'expérience au prix d'un jugement
pédagogique explicite sur l'équivalence des modules, qui doit être une
décision humaine et documentée, jamais une heuristique de code.

---

## Coexistence temporaire

Indépendamment de la stratégie de code, une période de coexistence
(seed et réel visibles simultanément, potentiellement au sein de la
même formation) est probable le temps de valider le corpus réel en
conditions réelles. Chaque stratégie la supporte différemment :

- Stratégie 1 (versioning) : coexistence native et sans effort — les
  deux codes existent en parallèle par construction.
- Stratégie 2 (namespace legacy) : coexistence possible mais suppose
  d'exposer volontairement le namespace `LEGACY-` quelque part dans
  l'UI/catalogue, sans quoi le contenu seed devient invisible dès le
  remap.
- Stratégie 3 (mapping table) : coexistence la plus pilotable — le
  statut de migration par module peut être exposé/masqué finement via
  la table elle-même.

---

## Rollback et compatibilité descendante

- **Rollback** : la stratégie 1 est réversible sans risque (suppression
  pure d'un ajout) ; la stratégie 3 l'est presque autant (suppression
  de lignes de mapping, aucune donnée de progression modifiée) ; la
  stratégie 2 est la seule qui suppose un plan de rollback testé avant
  exécution, parce qu'elle mute des données de progression réelles.
- **Compatibilité descendante** : tout lien externe déjà partagé
  (email, export, éventuel futur "wallet"/certificat citant un
  `module_code`) doit continuer à résoudre vers *quelque chose de
  cohérent* — aucune des trois stratégies ne casse une URL existante à
  elle seule, mais seule la stratégie 2 change ce que le code
  `FMS-01-M01` *signifie* pour un lien déjà émis, ce qui est le risque
  de compatibilité le plus concret des trois.

---

## Ce que ce document ne fait pas

- Il ne recommande aucune des trois stratégies.
- Il ne propose pas de calendrier.
- Il ne mute aucun code, schéma ou document `db.formations`/
  `db.progress`.
- Il ne préjuge pas de la sous-décision "préserver / geler / migrer" —
  posée ci-dessus comme une question ouverte, pas une réponse.

`FMS_CANONICAL_MIGRATION` reste un workstream séparé de W1 tant qu'une
stratégie n'a pas été choisie explicitement par le demandeur.

---

## Addendum — DEC-003 (2026-09-03), ACA-0005/G2

**Ceci est un ajout, pas une réécriture** : tout ce qui précède reste
l'analyse originale, non modifiée, telle que produite avant que le
Founder ne tranche. Rien ci-dessus n'a été corrigé ou retiré.

Le Founder a tranché : **`DEC-003 = MAPPING_TABLE + LEGACY_READ_ONLY_FREEZE`**
— c'est la **Stratégie 3** ci-dessus (table de correspondance), avec la
sous-décision transverse résolue en **"préserver telle quelle"** (jamais
"migrer avec mapping implicite", jamais réattribution silencieuse).

Ce que `G2 = AUTHORIZED` a effectivement permis de construire, sous
`ACA-0005` (implémentation complète :
`docs/ACADEMY_FMS_CANONICAL_LINEAGE_IMPLEMENTATION_REPORT.md`) :

- La collection `module_lineage` (`backend/fms_lineage/`) **est**
  exactement la "table de correspondance" décrite en Stratégie 3 —
  `{legacy_formation_code, legacy_module_code, canonical_formation_code,
  canonical_module_code, canonical_version, relation, status}` — jamais
  de mutation de `db.formations`/`db.progress`.
- Relation par défaut `NO_EQUIVALENCE` partout (jamais une équivalence
  positionnelle implicite) — plus stricte que ce que Stratégie 3
  décrivait initialement, précisément pour honorer
  `POSITIONAL_EQUIVALENCE_INFERENCE = FORBIDDEN` posé dans le mandat
  `ACA-0005`.
- `SUPERSEDED_BY` et `MANUAL_EQUIVALENCE` existent dans le modèle pour
  supporter une future transition pilotée module par module — mais
  **aucune progression `db.progress` n'a été migrée ni réattribuée par
  ce chantier**. La question "que devient une ligne `db.progress`
  existante" reste répondue par **"préserver telle quelle"** : rien ne
  la touche, `module_lineage` est une couche de lecture additionnelle,
  jamais une réécriture.

**Ce que `G3 = NOT_AUTHORIZED` signifie concrètement** : la table de
correspondance existe et peut déjà être interrogée/enrichie par un
humain (API `POST/PATCH /api/fms/lineage`), mais **rien ne la consulte
encore pour changer ce qu'un apprenant voit ou peut faire** — le
"branchement du corpus réel sur le runtime" (`ACA-0006`) reste une
étape séparée, non commencée, qui devra elle-même être explicitement
autorisée.
