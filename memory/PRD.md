# CVLN Academy OS — PRD

## Problème & Vision (verbatim utilisateur)

Construire **CVLN Academy OS** : une infrastructure d'apprentissage progressive pour les
futures industries **culturelles & technologiques**.

Personas :
- Apprenants caribéens (Martinique/Guadeloupe/Guyane) + diaspora
- Opérateurs des entités CVLN (FMS, KORA, Kiltikonet, FREK, LabelOS, CVLN Brain, LOS, CIP…)
- Institutions partenaires (OIF, UNESCO, CARIFESTA, DAC, CTM…)

Design : **Caribbean Futurism** — blanc + orange caribéen, typographie déclarative,
noise/texture terreuse, chips végétaux pour les stades.

## Décisions produit (verbatim)

- ❌ Ne pas construire FrekCore ni CVLN Agent Factory from scratch. Academy expose
  uniquement des **couches d'abstraction** (`backend/services/frek_core.py`,
  `backend/services/agent_factory.py`).
- ✅ Mentor IA : passer par Agent Factory. Fallback local temporaire → Anthropic SDK
  officiel, Claude Sonnet 5.
- ✅ FREK-ID (identifiant culturel unique séquentiel) délivré par FrekCore. Fallback
  local temporaire → compteur Mongo.
- ✅ 30 formations, 8 pôles principaux (+13 avec extensions), stades végétaux
  Graine → Pousse → Racine → Branches → Arbre → Forêt.
- ✅ Trilinguisme FR/EN/KR (kréyòl).

## Ce qui a été livré — 1er septembre 2026 (Réconciliation contre le premier ZIP FMS réel)

Le premier ZIP FMS réel (`FMS_Chantier_Complet_20260822.zip`, 223
fichiers, FMS-01→06 verrouillés) est arrivé après la mission du 30 août —
exactement comme annoncé dans le brief initial. Détail complet dans
`docs/FMS_IMPORT_VALIDATION_REPORT.md` et `docs/AUDIT_REPORT.md` §9 ;
résumé produit ici :

- **Moteur d'import FMS réécrit** contre la structure réelle (fichiers
  numérotés, sans frontmatter — la convention frontmatter documentée le
  30 août avait dû être inventée faute de ZIP réel à l'époque) : 26 types
  de ressources réels reconnus (contre 10 inventés), dérivation du
  `formation_code` et du graphe de prérequis de module directement depuis
  le contenu réel (`fms_import/module_map.py`, nouveau).
- **Moteur de certification étendu** (sans rien casser) pour la doctrine
  de notation réelle : critères éliminatoires ("verrous doctrinaux"),
  plafonnement de mention indépendant du score — le modèle pondéré
  existant encaissait déjà nativement l'échelle 0-4 "Rubric Master" du
  ZIP réel.
- **Template Engine** : 7ᵉ type `pitch` ajouté (confirmé par le contenu
  réel — chaque métier se termine par un pitch oral).
- **Validation** : 223/223 fichiers réels classifiés sans erreur ni
  avertissement (une collision de code détectée et corrigée pendant la
  validation). L'import réel en base n'a pas pu être exécuté dans cet
  environnement (pas de MongoDB disponible) — seule la partie pure du
  pipeline (couvre tout ce qui peut échouer avant l'écriture en base) a
  été validée contre l'archive réelle.
- Tests unitaires : 29 → 40 (réécrits contre la convention et la doctrine
  réelles, pas de simple ajout par-dessus l'ancien modèle inventé) ;
  qualité (`black`/`isort`/`flake8`/`mypy`) toujours propre.
- **Volontairement pas fait** : synthèse `Formation`/`Module` depuis les
  ressources importées (mérite une validation humaine CVLN du mapping) ;
  graphe de prérequis complet pour FMS-04/05/06 (leur Master Module Map
  ne déclare pas de prérequis module par module pour la majorité de leurs
  modules — un ordre séquentiel implicite aurait été fabriqué, pas lu).

## Ce qui a été livré — 30 août 2026 (Production Hardening Mission)

Mission de mise en production : audit zéro-dette + architecture entreprise +
8 nouveaux moteurs/domaines, sur la base du MVP livré en février. Détail
complet dans `docs/AUDIT_REPORT.md`, `docs/INTEGRATIONS_REPORT.md`,
`docs/DEVELOPER_GUIDE.md` — résumé ici pour l'historique produit :

- **Zéro dette technique** : `emergentintegrations` (non installable hors
  Emergent) remplacé par le SDK Anthropic officiel ; bug de stub motor
  3.3.1 corrigé (bump vers 3.7.x) qui masquait ~20 faux positifs mypy ;
  10 dépendances Python mortes supprimées ; install frontend cassée
  (peer-dep date-fns/react-day-picker) réparée ; toast dupliqué (100%
  mort) supprimé ; branding Emergent par défaut (`index.html`, analytics
  PostHog sous compte Emergent) remplacé par la marque CVLN.
- **Architecture** : `routes.py` (817 lignes, 9 responsabilités) éclaté en
  routeurs par domaine (`backend/api/*.py`) ; 8 nouveaux packages métier
  (`fms_import/`, `certification/`, `skills/`, `template_engine/`,
  `wallet/`, `services/integrations/`, `services/ai_assistant.py`,
  `services/events.py`).
- **Auth & rôles** : 7 rôles, organisations/cohortes/invitations, refresh
  tokens rotatifs, reset mot de passe, vérification email, OAuth/2FA
  prêts (501 tant que non configurés).
- **Moteur d'import ZIP FMS** : parseur Markdown+YAML tolérant aux erreurs,
  validation référentielle, recherche indexée, sommaire auto-généré,
  graphe de prérequis — la plateforme est prête à recevoir FMS-01 à
  FMS-06 (voir `docs/DEVELOPER_GUIDE.md` §3 pour la convention de fichiers).
- **Certification Engine** : N1/N2/A01, rubriques versionnées, notation
  jury signée (hash SHA-256), attestations PDF, reprise d'examen.
- **Skill Engine** : Skill IDs, registre d'évidence hashé (FREK-ready),
  progression automatique.
- **Template Engine** : 6 types (Diagnostic/Univers/Positionnement/
  Storytelling/Roadmap/Dossier), autosave versionné, export MD/PDF/DOCX.
- **Écosystème CVLN** : 9 interfaces génériques (Intelligence OS, Brain,
  Command Center, Laurent.ia, KORA, Factory Maker Studio, Good Mood,
  Culture Connect, Kiltikonet) + bus d'événements in-process.
- **CVLN Wallet** : grand livre JCC/tokens actif, crédité par badges et
  certifications ; payloads Apple/Google Wallet (non signés — voir
  rapport d'intégrations).
- **Assistant IA commun** : 4 personas (student/trainer/jury/corrector)
  définis comme données au-dessus d'un seul transport partagé.
- **Dashboards par rôle** : Wallet, Skills, Certifications (étudiant) ;
  Admin CMS (import FMS, statut intégrations, orgs/cohortes/invitations,
  publication catalogue) ; Trainer (cohortes) ; Jury (file de correction
  + notation).
- **Performance** : code-splitting (React.lazy, bundle -11%), PWA
  (service worker + manifest maison), index Mongo sur toutes les
  collections à volumétrie utilisateur.
- **Tests** : 29 tests unitaires sans dépendance base de données (avant :
  0, seule une suite E2E nécessitant un Mongo live existait).

## Ce qui a été livré — 21 Feb 2026 (Iteration 1 + 2 + 3)

### Iteration 3 — Enrichissement contenu 24+ formations — 21 Feb 2026
- **25 formations** ex-"coming_soon" enrichies avec **~193 modules détaillés** (hook / livrable / durée / stade / signal FREK), ancrés Caraïbe.
- Total plateforme : **30 formations · 13 pôles · 233 modules**.
- Seed idempotent (upsert-safe) : `seed.py` fait un `update_one({...}, {"$set": doc}, upsert=True)` par formation → chaque redémarrage backend propage les changements de contenu sans toucher aux données utilisateurs (progress, badges, missions acceptées).
- Nouvelle organisation : `/app/backend/seed_modules.py` centralise le contenu (mergé dans FORMATIONS via `seed_data.py`) pour faciliter les prochaines révisions éditoriales.
- Frontend : stat headline du catalogue devient dynamique (`30 formations. 13 pôles. 233 modules.`).
- Tests backend : **27/27 pytest ✅** (régression). Quiz auto-généré + submit sur les nouveaux modules validé end-to-end.

### Iteration 2 — FREK Origin Story (onboarding) — 21 Feb 2026
- 5-step wizard (`/onboarding`) : langue → métier visé (pôle) → territoire → objectif → récap.
- Backend `POST /api/onboarding/complete` :
  - Émet **3 signaux FREK-TIME** (langue, territoire, objectif).
  - Attribue le **badge Découverte** (idempotent).
  - Recommande une **première formation** matchée au pôle choisi (préfère celles avec modules détaillés).
  - **Auto-accepte** la première mission du pôle (source="onboarding").
- Backend `GET /api/onboarding/options` : 3 langues, 13 pôles, 7 territoires.
- Gate frontend : tout utilisateur sans `onboarding_completed=true` redirige vers `/onboarding`.
- Tests : backend pytest **27/27** ✅, frontend Playwright ✅ (register → wizard → recos → dashboard).

### Iteration 1 — MVP core

### Backend (FastAPI + MongoDB)
- Auth JWT bcrypt (`/api/auth/register|login|me`) avec FREK-ID auto-généré
  et bonus **+5 CC** à l'inscription.
- 30 formations seedées (`/api/formations`, `/api/formations/{code}`) — 12 modules
  détaillés sur FMS-01, FRK-01, BRN-02 ; autres marquées "coming_soon".
- Quiz sur chaque module (`/api/formations/{fc}/modules/{mc}/quiz|submit`) —
  bonnes réponses masquées côté client ; CC + signal FREK émis à la validation.
- 8 badges seuils (0 → 500 CC) — auto-délivrés (`_award_threshold_badges`).
- 8 missions seedées (`/api/missions`, `/accept`, `/submit`) — CC + signal FREK-WORK.
- Progression (`/api/progression/summary`) + FREK profile (`/api/frek/profile`).
- Mentor IA (`/api/mentor/agents`, `/api/mentor/chat`) — Claude Sonnet 4.6 via
  Anthropic SDK officiel (Claude Sonnet 5), en attendant Agent Factory.
- Couches d'abstraction propres → **basculement remote sans toucher aux routes**.

### Frontend (React + Tailwind + shadcn)
- Landing/Auth trilingue (FR/EN/KR).
- Layout avec sidebar sticky + FREK-ID card + toggle langue.
- Dashboard bento (progression globale, CC, badges, missions à venir, activité
  signaux FREK, derniers badges).
- Roadmap stades végétaux.
- Formations (catalogue 30 items groupé par pôle) + FormationDetail + Quiz modal.
- Missions (accepter / soumettre).
- Badges (locked/earned).
- FREK Profile (identity + signaux + timeline).
- MentorPanel flottant (chat drawer).

### Docs livrées
- `/app/design_guidelines.json` — Design system Caribbean Futurism.
- `/app/INTEGRATION_CONTRACT.md` — Contrat REST pour FrekCore & Agent Factory.
- `/app/memory/test_credentials.md`.

### Tests
- Backend pytest suite 20/20 ✅
- Frontend Playwright E2E ✅ (register → dashboard → formations → quiz → missions → badges → mentor → logout)

## Roadmap

### P1 — Prochain chantier
- **Câbler FrekCore & CVLN Agent Factory** — remplacer les fallbacks par les vraies APIs (variables d'env `FREK_CORE_BASE_URL`, `CVLN_AGENT_FACTORY_URL`) dès que fournies.
- **Bêta fermée & métriques** — instrumenter : taux de complétion, rétention D1/D7/D30, interactions mentor, engagement missions/badges.
- **Revue éditoriale du contenu enrichi** (25 formations × ~8 modules) par un·e directeur·rice pédagogique CVLN avant lancement bêta.

### P2
- Quiz bank multi-questions dynamique (au lieu du template 8 questions/module).
- Certificats FREK exportables (PDF signé) via `frek_core.issue_proof`.
- Timeline stades animée + célébrations de palier.
- Ombré diaspora : carte interactive des apprenants.

### P3
- Passerelle Kiltikonet (importer les empreintes FREK existantes).
- LabelOS metadata cleaner intégré à LOS-02.
- Économie CC → token blockchain via CVLN Blockchain (BCH-01).
- Mentor multi-agents (agents pôles, coach quiz, coach mission).

## Fichiers clefs

- Backend : `/app/backend/{server.py, routes.py, models.py, auth.py, seed.py, seed_data.py, quiz.py, services/*}`
- Frontend : `/app/frontend/src/{App.js, pages/*, components/{Layout,MentorPanel}.js, lib/*}`
- Docs : `/app/INTEGRATION_CONTRACT.md`, `/app/design_guidelines.json`, `/app/memory/*`

## Env vars

Full reference with defaults/comments: `backend/.env.example`, `frontend/.env.example`.

```env
# backend/.env (obligatoire)
MONGO_URL, DB_NAME
JWT_SECRET

# backend/.env (optionnel)
JWT_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS, CORS_ORIGINS, APP_PUBLIC_URL
ANTHROPIC_API_KEY  # (mentor fallback, official Anthropic SDK)
OAUTH_{GOOGLE,APPLE,GITHUB,MICROSOFT}_CLIENT_ID / _CLIENT_SECRET
NOTIFICATIONS_PROVIDER_URL, NOTIFICATIONS_API_KEY
FREK_CORE_BASE_URL, FREK_CORE_API_KEY
CVLN_AGENT_FACTORY_URL, CVLN_AGENT_FACTORY_API_KEY

# frontend/.env
REACT_APP_BACKEND_URL
```
