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

```env
# backend/.env (obligatoire)
MONGO_URL, DB_NAME
JWT_SECRET
ANTHROPIC_API_KEY  # (mentor fallback, official Anthropic SDK)

# backend/.env (optionnel — plug remote quand prêt)
FREK_CORE_BASE_URL, FREK_CORE_API_KEY
CVLN_AGENT_FACTORY_URL, CVLN_AGENT_FACTORY_API_KEY

# frontend/.env
REACT_APP_BACKEND_URL
```
