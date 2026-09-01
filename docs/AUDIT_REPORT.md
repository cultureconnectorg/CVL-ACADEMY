# CVLN Academy — Rapport d'audit (mission "production-ready")

**Date** : 30 août 2026
**Branche** : `claude/cvln-academy-production-r35l31`
**Portée** : audit + remédiation dette technique + build-out des 15 règles de
la mission, sur la base de code existante "CVLN Academy OS" (MVP Emergent.sh).

Ce document rend compte, honnêtement, de ce qui est réellement livré, testé et
vérifiable — par opposition à ce qui reste une interface prête mais non
branchée (faute d'identifiants/API réels côté écosystème CVLN, qui n'existent
pas encore). Chaque section renvoie aux fichiers et commits concernés.

---

## 1. Architecture (règle 2)

### Avant
Backend : un seul fichier `routes.py` de 817 lignes mélangeant 9
responsabilités (auth, onboarding, catalogue, parcours LX v2, quiz, badges,
missions, progression, mentor). `models.py` déjà correct (344 lignes,
cohérent). Frontend : 10 pages, aucune séparation par rôle, pas de
code-splitting.

### Après
```
backend/
  server.py            # entrypoint FastAPI (middleware, startup: index, seed, subscribers)
  api/                  # 1 routeur par domaine, agrégés dans api/__init__.py
    auth.py orgs.py formations.py learning.py quizzes.py badges.py
    missions.py progression.py mentor.py fms.py skills.py certification.py
    templates.py assistants.py wallet.py integrations.py health.py
  auth.py               # JWT + refresh tokens + require_role()
  models.py             # schémas Pydantic partagés
  db.py                 # connexion Mongo
  infra_indexes.py      # tous les index Mongo, idempotent au démarrage
  badges_engine.py      # logique de seuils de badges (partagée par 3 domaines)
  fms_import/           # moteur d'import ZIP FMS (règle 5/15)
  certification/        # moteur de certification (règle 6)
  skills/               # Skill Engine (règle 7)
  template_engine/      # moteur de templates (règle 8)
  wallet/                # CVLN Wallet (règle 10)
  services/
    frek_core.py agent_factory.py notifications.py ai_assistant.py events.py
    integrations/        # 9 interfaces écosystème (règle 9)

frontend/src/
  pages/                # étudiant : Dashboard, Formations, Missions, Badges,
                         # Skills, Certifications, Wallet, FrekProfile, Roadmap…
  pages/admin/           # CMS (import FMS, intégrations, orgs, catalogue)
  pages/trainer/         # cohortes, invitations
  pages/jury/            # file de correction, notation
  lib/                   # api.js (axios + refresh silencieux), auth.jsx, i18n.jsx
  components/            # Layout (nav par rôle), MentorPanel, ui/ (shadcn)
```

Zéro changement de comportement sur les 27 endpoints existants pendant le
découpage de `routes.py` — vérifié en diffant la table des routes avant/après
(31 routes avant, identiques après le split ; 80 routes au total désormais).

**Choix assumé** : pas de migration de stack (CRA/craco/FastAPI/Mongo restent
en place). Réécrire vers Next.js sur la seule ressemblance de nommage du
brief avec les conventions app-router aurait été un risque élevé sans
bénéfice fonctionnel réel — noté ici plutôt que fait silencieusement.

---

## 2. Dette technique supprimée (règle 1)

| Constat | Fichier(s) | Correction |
|---|---|---|
| Dépendance `emergentintegrations` non installable hors sandbox Emergent | `services/agent_factory.py` | Remplacée par le SDK officiel `anthropic` |
| `motor==3.3.1` : bug de stub (`core.pyi`) faisant passer **tout** retour de `find_one`/`find_one_and_update` pour `None` sous mypy — masquait les vrais bugs | `requirements.txt`, tout le code Mongo | Bump `motor>=3.7.1`, `pymongo>=4.9` — ~20 faux positifs mypy résolus d'un coup |
| Bug latent réel : `OnboardingResult` pouvait planter (500) si l'utilisateur disparaissait entre écriture et relecture | `api/onboarding.py` | Guard explicite (`if doc else current`) |
| 10 dépendances Python jamais importées (boto3, requests-oauthlib, cryptography, python-jose, pandas, numpy, jq, typer, passlib, tzdata) | `requirements.txt` | Supprimées |
| Frontend : `npm install`/`yarn install` cassé — `date-fns@4` incompatible avec le peer-dep de `react-day-picker` | `package.json` | `date-fns` fixé en `^3.6.0` |
| `@emergentbase/visual-edits` : dépendance non fetchable hors réseau Emergent (confirmé 403 policy sur `assets.emergent.sh`) | `package.json`, `craco.config.js` | Retirée de `package.json` (le code la charge déjà en best-effort avec try/catch) |
| Implémentation de toast dupliquée et 100% morte (`hooks/use-toast.js` + `components/ui/toast.jsx` + `toaster.jsx`) — l'app utilise exclusivement `sonner` | frontend | Supprimée, avec `@radix-ui/react-toast` |
| `dayjs`, `lodash`, `cra-template`, `@fontsource-variable/manrope` : jamais importés | `package.json` | Supprimés |
| Aucun ESLint configuré malgré `eslint` + plugins installés | frontend | `eslint.config.js` (flat config) ajouté ; 9 erreurs réelles corrigées (accessibilité clavier, entités JSX, dépendance `useEffect` obsolète couplée à du code mort) |
| `index.html` = le template Emergent par défaut tel quel : titre "Emergent \| Fullstack App", meta description "A product of emergent.sh", script externe `assets.emergent.sh` (bloqué hors Emergent), snippet PostHog codé en dur avec la clé de projet **d'Emergent** | `public/index.html` | Ré-écrit avec la marque CVLN Academy ; scripts tiers non liés à CVLN retirés (l'app n'envoyait pas ses analytics à son propre compte) |
| `test_reports/*.json`, `pytest_results.xml` : traces d'itérations d'un agent précédent, sans valeur de source de vérité | racine du repo | Supprimés |
| `backend_test.py` : chemin `/app/frontend/.env` codé en dur (ne fonctionne que dans le sandbox Emergent) | `tests/backend_test.py` | Chemin relatif au repo |
| `.gitignore` : la règle `.env.*` excluait aussi silencieusement tout `.env.example` | `.gitignore` | Exception `!**/.env.example` ajoutée, et les fichiers d'exemple (absents avant) créés |

**Grep de contrôle** : aucun `TODO`/`FIXME`/`HACK` dans le code au début de la
mission (déjà propre sur ce point) — aucun n'a été introduit depuis.

---

## 3. Bugs corrigés en cours de build (pas des régressions — jamais livrés)

- **DOCX export** (`template_engine/export.py`) : `Paragraph.italic = True`
  n'existe pas dans python-docx (seul `Run` porte `.italic`) — détecté en
  testant l'export réellement (pas en relisant le code), corrigé avant tout
  commit.
- **Export de template** (`api/templates.py`) : indexation
  `EXPORT_MEDIA_TYPES[format]` sur le builtin Python `format` au lieu de la
  variable `export_format` — trouvé par mypy, pas par une relecture manuelle.
- **`user/learning-path`** (`api/learning.py`) : générateur conditionnel
  `for m in f_doc.get(...) if f_doc else []` illisible et non typable ;
  remplacé par un `continue` explicite (mypy confirme la correction).

---

## 4. Sécurité

- **Auth** : bcrypt (coût par défaut), JWT d'accès ramené de 30 jours à 2h
  + refresh tokens opaques, hachés au repos (SHA-256), **rotatifs** (l'ancien
  est révoqué à chaque usage du nouveau) et révocables (`/auth/logout` révoque
  toutes les sessions). Reset de mot de passe : jeton à usage unique, TTL 60
  min, révoque toutes les sessions actives une fois utilisé.
- **RBAC** : `require_role(*roles)` en dépendance FastAPI sur chaque route
  d'écriture sensible (admin, jury/corrector, orgs/cohorts/invitations).
- **Séparation des rôles** : 7 rôles (`student`, `trainer`, `corrector`,
  `jury`, `admin`, `super_admin`, `founder`) avec `STAFF_ROLES`/`ADMIN_ROLES`
  centralisés dans `models.py`.
- **Jamais de confirmation d'existence de compte** : `/auth/forgot-password`
  répond `200 {"ok": true}` que l'email existe ou non.
- **Preuves FREK-ready (règle 11)** : chaque évidence de compétence
  (`skills/progression.py`) et chaque signature de jury
  (`certification/attestation.py`) porte un hash SHA-256 canonique,
  vérifiable indépendamment du enregistrement en base.
- **Non résolu, documenté plutôt que caché** : `wallet/service.py` a une
  fenêtre de concurrence théorique (deux crédits simultanés créant chacun le
  compte wallet) — l'index unique sur `user_id` la transforme en échec net
  (`DuplicateKeyError`) plutôt qu'en double compte silencieux, mais il n'y a
  pas encore de retry automatique. Faible probabilité en usage réel
  (attribution de badge séquentielle par utilisateur), à corriger si la
  volumétrie le justifie.
- **OAuth/2FA** : endpoints réels typés répondant `501 non configuré` tant que
  les identifiants ne sont pas fournis — jamais de faux "connecté".

---

## 5. Performance & scalabilité (règle 13)

- **Base de données** : `infra_indexes.py` — index sur chaque collection
  interrogée par `user_id` à l'échelle multi-utilisateur (progress, badges,
  missions, wallet, skill evidence, certification attempts, template
  documents, conversations mentor/assistants) + index uniques sur les clés
  de lookup (email, frek_id, jetons opaques, codes d'invitation, slugs
  d'organisation) pour que les doublons échouent en base plutôt qu'en
  application uniquement.
- **Frontend** : toutes les routes en `React.lazy` + un seul `Suspense` —
  bundle principal réduit de 129 Ko à 115,8 Ko gzip, 17 chunks chargés à la
  demande (mesuré avant/après sur ce commit).
- **PWA** : `service-worker.js` fait main (Cache API native, pas de
  dépendance Workbox — voir §7) : app shell en cache pour usage hors-ligne,
  assets statiques en stale-while-revalidate, `/api/*` jamais mis en cache
  (une réponse de progression/quiz/mentor obsolète serait activement fausse).
- **Recherche FMS** : index texte Mongo sur `fms_resources` (title, body,
  code) — `fms_import/indexer.py`.
- **Pagination** : `GET /api/formations` accepte `limit`/`skip`.
- **Non fait, assumé** : pas de test de charge réel (aucune infra dédiée dans
  ce sandbox) — la préparation "milliers d'utilisateurs" repose sur les
  index + la pagination + le code-splitting, pas sur une mesure en conditions
  réelles.

---

## 6. Accessibilité

- ESLint `jsx-a11y` activé et **appliqué** (pas juste installé) : correction
  d'un fond de modal cliquable au clavier (`MentorPanel.js` — `<div
  onClick>` → `<button>` réel), et exemption ciblée (documentée dans
  `eslint.config.js`) pour les primitives shadcn/ui génériques dont les
  règles "contenu requis" ne s'appliquent pas (composants de bibliothèque
  sans contenu propre).
- Pas d'audit Lighthouse/axe complet réalisé (hors du périmètre outillable
  dans ce sandbox sans navigateur graphique) — recommandé avant mise en
  production réelle.

---

## 7. Tests

| Avant | Après |
|---|---|
| 1 suite E2E (`backend_test.py`) nécessitant un serveur + Mongo live, 0 test unitaire | 29 tests unitaires **sans dépendance base de données**, exécutables en isolation : `test_quiz.py`, `test_fms_import.py` (12 tests — parseur, validateur, extraction ZIP), `test_certification_scoring.py` (6 tests), `test_template_export.py` (4 tests) |

`black`/`isort`/`flake8`/`mypy --ignore-missing-imports` : **0 erreur** sur
les 71 fichiers `.py` du backend, maintenu à chaque commit de cette mission.
ESLint (flat config) : **0 erreur** sur `frontend/src`. Le build de
production (`craco build`) compile sans avertissement, vérifié à chaque
étape majeure.

**Limite assumée** : `backend_test.py` (suite E2E historique, 20+ scénarios)
n'a pas pu être exécutée dans ce sandbox — aucun `mongod` n'y est installé et
son installation dépasse le périmètre de cette mission. Recommandation :
faire tourner cette suite en CI avec un service `mongodb-org` avant toute
mise en production.

---

## 8. Ce qui n'a délibérément pas été fait (et pourquoi)

- **Pas de migration de framework** (§1).
- **Pas de synthèse automatique de `Formation`/`Module` depuis les
  ressources FMS importées** : `fms_import` construit une couche de
  ressources recherchable/navigable (`fms_resources`, sommaire,
  graphe de dépendances) mais ne transforme pas encore ça en objets
  `Formation` du catalogue. Le premier ZIP FMS réel est arrivé le 1er
  septembre 2026 (voir §9) et a permis de valider tout le reste du
  pipeline contre du contenu réel — mais cette synthèse spécifique reste
  différée volontairement : elle mérite qu'un humain CVLN valide le
  mapping exact plutôt qu'un choix unilatéral. Voir
  `docs/FMS_IMPORT_VALIDATION_REPORT.md` §5.
- **Pas d'intégrations écosystème réellement branchées** (Brain, Command
  Center, KORA, Laurent.ia, Wallet externe, etc.) : aucun identifiant
  n'existe. Chaque interface est réelle, typée, et répond honnêtement
  "non configuré" — voir `docs/INTEGRATIONS_REPORT.md`.
- **Pas de test de charge**, pas d'audit Lighthouse complet (§5, §6).

## 9. Réconciliation contre le premier ZIP FMS réel (1er septembre 2026)

Le premier ZIP FMS réel (`FMS_Chantier_Complet_20260822.zip`, 223
fichiers, FMS-01→06 + référentiels FMS-A→F) est arrivé après cette
mission, comme annoncé dans le brief. Sa structure réelle différait de la
convention frontmatter documentée au moment du build initial (aucun
fichier réel n'en porte). Réconciliation effectuée :

- **`fms_import/`** entièrement réécrit pour classifier depuis le nom de
  fichier réel (26 types reconnus, contre 10 inventés), dériver le
  `formation_code` (y compris la correspondance lettre de référentiel →
  métier), et extraire les prérequis de module depuis le
  `Master_Module_Map` de chaque métier (`module_map.py`, nouveau — gère
  les deux mises en page réelles observées selon le métier).
- **`certification/`** étendu (pas cassé) : `RubricCriterion.is_eliminatory`,
  `Rubric.cap_rules`/`mention_thresholds` — le modèle pondéré existant
  encaisse tel quel l'échelle 0-4 "Rubric Master" réelle de FMS-01 ; seuls
  les critères éliminatoires et le plafonnement de mention étaient
  vraiment nouveaux face à la doctrine réelle.
- **`template_engine/`** : 7ᵉ type `pitch` ajouté (confirmé par les
  `Templates_Etudiants.md` réels — chaque métier se termine par un pitch
  oral, distinct du dossier écrit).
- **`skills/`** : docstring/exemples alignés sur la forme canonique réelle
  (`FMS01-A1`), qui remplace la forme inventée (`FMS.N1.B1.S1`).
- Validation : voir `docs/FMS_IMPORT_VALIDATION_REPORT.md` pour le détail
  chiffré (223/223 fichiers classifiés, 0 erreur, 0 avertissement après
  correction d'une seule collision de code détectée pendant la
  validation) et pour ce qui reste honnêtement incomplet (graphe de
  prérequis partiel pour FMS-04/05/06, synthèse `Formation` différée).
  L'import réel en base n'a pas pu être exécuté dans cet environnement
  (aucune instance MongoDB disponible) — seule la partie pure du
  pipeline, qui couvre tout ce qui peut échouer avant l'écriture en base,
  a été validée.
- Tests : 40/40 (29 → 40, `test_fms_import.py` et
  `test_certification_scoring.py` réécrits contre la convention et la
  doctrine réelles) ; `black`/`isort`/`flake8`/`mypy` toujours propres.
