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
- ✅ Mentor IA : passer par Agent Factory. Fallback local temporaire → Emergent LLM
  Claude Sonnet 4.6.
- ✅ FREK-ID (identifiant culturel unique séquentiel) délivré par FrekCore. Fallback
  local temporaire → compteur Mongo.
- ✅ 30 formations, 8 pôles principaux (+13 avec extensions), stades végétaux
  Graine → Pousse → Racine → Branches → Arbre → Forêt.
- ✅ Trilinguisme FR/EN/KR (kréyòl).

## Ce qui a été livré — 21 Feb 2026 (Iteration 1)

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
  Emergent LLM Key, en attendant Agent Factory.
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

### P1 (dès que APIs fournies)
- Câbler `FREK_CORE_BASE_URL` + clé → Academy switch automatiquement.
- Câbler `CVLN_AGENT_FACTORY_URL` + clé pour le mentor + futurs agents pôles.
- Enrichir modules "coming_soon" (24 formations sans modules détaillés).

### P2
- Quiz : bank multi-questions dynamique (au lieu du template 8 questions/module).
- Marketplace missions (statuts avancés : review, paiement CC, etc.).
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
EMERGENT_LLM_KEY  # (mentor fallback)

# backend/.env (optionnel — plug remote quand prêt)
FREK_CORE_BASE_URL, FREK_CORE_API_KEY
CVLN_AGENT_FACTORY_URL, CVLN_AGENT_FACTORY_API_KEY

# frontend/.env
REACT_APP_BACKEND_URL
```
