# W0.5 — FMS Source-of-Truth Audit (lecture seule, aucun code)

**Autorisation :** `W0.5_FMS_SOURCE_OF_TRUTH_AUDIT = AUTHORIZED`,
`W1_IMPLEMENTATION = NOT_AUTHORIZED`. Rien n'a été modifié dans le repo
pour produire ce document — uniquement des lectures et des commandes
d'inspection (greps, un script Python en lecture seule sur
`seed_data.py`).

**But :** répondre à une seule question, avec preuve — *comment le corpus
FMS canonique (validé le même jour dans
`docs/FMS_IMPORT_VALIDATION_REPORT.md`) pourrait un jour se brancher sans
casser les IDs, la progression, les utilisateurs ni les routes existantes
— sans migrer quoi que ce soit maintenant.*

```
SILENT_FUSION           = FORBIDDEN   (respecté — rien fusionné)
GENERIC_SEED_DELETION   = FORBIDDEN   (respecté — rien supprimé)
FMS_REPLACEMENT_IN_W1   = FORBIDDEN   (respecté — aucun code touché)
```

---

## Constat central — un conflit de code, pas juste un manque de contenu

Les deux couches ne sont pas seulement "séparées" (déjà noté en W0) — sur
FMS-01, **elles utilisent littéralement les mêmes codes pour un contenu
différent** :

```
seed_data.py       FMS-01-M01 … FMS-01-M12   (12 modules, contenu générique 2026)
Corpus FMS réel     FMS-01-M01 … FMS-01-M15   (15 modules + A01, contenu réel verrouillé)
```

`FMS-01-M01` existe des deux côtés. Côté seed : *"Identité artistique et
culturelle"*, 6h, hook *"Extrait artiste martiniquais inconnu"*. Côté
corpus réel : *"Introduction au métier d'Artist Development & méthode
transversale"*, 45 min, méthode OBSERVER→DISTINGUER→FORMULER→CONFRONTER→ARBITRER→DOCUMENTER,
micro-cas "Le trio des Mornay". **Même identifiant, deux pédagogies
incompatibles.** Toute fusion naïve écraserait soit l'un soit l'autre sous
le même code — exactement le risque que `SILENT_FUSION = FORBIDDEN`
anticipe.

`db.progress` (progression réelle des utilisateurs) est indexé par
`module_code` — donc toute ligne de progression existante sur
`FMS-01-M03`, par exemple, deviendrait silencieusement rattachée à un
contenu différent si le code était réutilisé pour le corpus réel sans
plan de migration explicite.

---

## Table de correspondance

| SCREEN | FRONTEND_COMPONENT | API_ROUTE | DB_COLLECTION | RECORD_TYPE | CURRENT_SOURCE | TARGET_FMS_SOURCE | STATUS |
|---|---|---|---|---|---|---|---|
| Catalogue formation | `frontend/src/pages/Formations.js` | `GET /api/formations` (`backend/api/formations.py:27`) | `db.formations` | `Formation` (30 documents, 8 pôles) | `backend/seed_data.py::FORMATIONS` (rédigé en février 2026) | 6 référentiels métier (`type=referentiel`) + le gabarit de nommage (`00_GABARIT_Construction_Metier.md`) | **CONFLICT** pour les 6 lignes FMS-01…06 (mêmes codes, contenu distinct) · **CORRECT** pour les 24 autres formations (aucun équivalent FMS, hors périmètre) |
| Fiche formation | `frontend/src/pages/FormationDetail.js` | `GET /api/formations/{code}` (`backend/api/formations.py:81`) | `db.formations` (+ `db.progress` pour le déverrouillage par utilisateur) | Formation détaillée, `modules[]` intégré | `seed_data.py` (description, `objective_strategic`, `modules[]` statiques) | Référentiel (fiche 20 points) + Master Learning Map + Master Module Map | **CONFLICT** (FMS-01…06) |
| ModuleJourney | `frontend/src/pages/ModuleJourney.js` | `GET/POST /api/modules/{fc}/{mc}/...` (`backend/api/learning.py`) | `db.formations` (contenu du module), `db.progress` (avancée réelle par utilisateur) | Module LX v2 (phases hook/objectives/course/workshop/deliverable), gabarit générique (`backend/lx.py::enrich_module`) | `seed_data.py` + `seed_modules.py` | Blueprint (`type=blueprint`) + Contenu complet (`type=module`) — structure et doctrine réelles, différentes du gabarit LX v2 actuel | **CONFLICT** pour M01–M12 (code identique, contenu différent) · **UNMAPPED** pour M13–M15 + A01 (existent dans le corpus réel, aucun équivalent seed) |
| Quiz | `PhaseQuiz` dans `ModuleJourney.js` | `GET/POST /api/formations/{fc}/modules/{mc}/quiz(/submit)` (`backend/api/quizzes.py`) | Aucune persistance du contenu (généré à la volée) ; `db.progress.quiz_passed` pour le résultat | 8 questions gabarit, générées par `backend/quiz.py::build_quiz()` à partir des champs génériques du module | `backend/quiz.py` (générateur de gabarit, pas un contenu rédigé) | `Banque_N1_Consolidee` / `Banque_N2_Consolidee` (vraies banques par métier, distracteurs = erreurs professionnelles réelles) + `Rubric_Master` pour la notation N2 | **DUPLICATE** — un mécanisme réel existe et fonctionne, mais produit un contenu générique sans rapport avec les vraies banques FMS ; à remplacer, pas à fusionner |
| Progression | `frontend/src/pages/Dashboard.js`, `frontend/src/pages/FrekProfile.js` | `GET /api/progression/summary` (`backend/api/progression.py:55`), `GET /api/frek/profile` (`backend/api/progression.py:24`), `GET /api/user/learning-path` (`backend/api/learning.py:257`) | `db.progress`, `db.frek_signals`, `db.users` | Progression réelle par utilisateur/module, signaux FREK réels | Événements réels de l'utilisateur (aucune donnée inventée) | Sans objet directement — le mécanisme n'a pas besoin d'une "source FMS", il a besoin que les `module_code` sur lesquels il s'appuie restent stables | **CORRECT (mécanisme)** / **AT RISK (clés)** — la logique est saine, mais indexée sur des `module_code` qui collisionnent avec le corpus réel (voir Constat central) |
| Missions / cas | `frontend/src/pages/Missions.js` | `GET/POST /api/missions...` (`backend/api/missions.py`) | `db.missions`, `db.user_missions` | Missions écosystème CVLN réelles (ex. `MIS-FMS-01` "Prod caribéenne pour KORA", pôle `FMS`, entité `KORA`) | `backend/seed_data.py::MISSIONS` (8 missions seedées) | **Aucun** — les "cas" du corpus FMS (Cas Fil Rouge "Anaïs Solaine", Cas Inédit "Nell Auberon") sont des exercices pédagogiques internes à un module/certification, pas des missions écosystème CVLN | **UNMAPPED / CONCEPT DIFFÉRENT** — ne pas fusionner ces deux notions, même si le mot "cas" apparaît des deux côtés ; le recouvrement est purement lexical |
| Compétences | `frontend/src/pages/Skills.js` | `GET /api/skills`, `GET /api/skills/mine` (`backend/api/skills.py`) | `db.skills` (registre), `db.user_skills` (dérivé des preuves) | `Skill` / `UserSkill` | **Vide par défaut** — `db.skills` n'est jamais seedé (`grep` confirmé sur `seed.py`), seule `register_skill()` (`backend/skills/progression.py:35`) peut y écrire, appelée uniquement via une création manuelle admin | `Skill_IDs_Registry.md` par métier — 19 Skill IDs canoniques par métier (`FMS01-A1`…`F1`), 86 identifiants distincts détectés au total par le parseur d'import (voir `docs/FMS_IMPORT_VALIDATION_REPORT.md`) | **UNMAPPED** — le moteur est réel et solide, son registre est juste vide ; les Skill IDs réels ont été indexés pour la recherche (`FmsResource.skill_ids`) mais jamais enregistrés comme entrées du Skill Engine |
| Certifications | `frontend/src/pages/Certifications.js`, `frontend/src/pages/jury/JuryDashboard.js` | `/api/certifications/...` (`backend/api/certification.py`) | `db.certification_rubrics` (**vide par défaut**, création admin uniquement), `db.certification_attempts` | `Rubric`/`RubricCriterion`, `CertificationAttempt` | Aucun — pas une seule grille n'est seedée, y compris pour FMS-01 | `49_FMS01_A01_Grille_Certificative_V1.md` — grille réelle à 19 Skill IDs, échelle 0-4, critères éliminatoires, plafonnement de mention. Le modèle du moteur (`is_eliminatory`, `cap_rules`, `mention_thresholds`) a été réconcilié pour la représenter **aujourd'hui même**, mais aucune ligne réelle n'existe encore dans `db.certification_rubrics` | **UNMAPPED** — capacité du moteur désormais alignée, donnée réelle absente |

---

## Ce que ça implique pour un futur branchement (pas une recommandation d'exécution — juste ce que l'évidence montre)

- **Le seul endroit avec un vrai conflit de clé** (pas juste une absence)
  est `db.formations` / `db.progress` sur les codes `FMS-01-M01`…`M12`.
  Tout le reste (`db.skills`, `db.certification_rubrics`) est **vide**,
  donc un branchement futur n'y écraserait rien — c'est un remplissage,
  pas une migration à risque.
- Un branchement qui réutiliserait les codes `FMS-0X-MXX` existants pour
  le contenu réel devrait explicitement décider du sort des lignes
  `db.progress` déjà associées à ces codes (les préserver comme legacy
  sous un espace de noms distinct ? les geler ? les migrer avec mapping
  explicite ?) — **question produit, pas technique**.
- Le mécanisme de progression, de verrouillage (`lx.py`), de badges et de
  signaux FREK n'a besoin d'aucune modification pour fonctionner avec un
  contenu FMS réel — il consomme `db.formations`/`db.progress` par code,
  peu importe l'origine du contenu à ce code. C'est une bonne nouvelle
  structurelle : le moteur n'est pas à reconstruire, seule la donnée
  qu'il sert doit être décidée.
- Les missions et les "cas" FMS ne doivent **jamais** être fusionnés — ce
  sont deux concepts produits différents qui partagent un mot, pas une
  structure.

Aucune recommandation de séquencement n'est faite ici — c'est
explicitement la décision qui t'appartient, comme tu l'as indiqué.
