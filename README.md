# CVLN Academy

Plateforme d'apprentissage progressive du groupe CVLN — formations, missions,
certifications, culture caribéenne. FR / EN / Kreyòl.

30 formations · 13 pôles · 233 modules · stades végétaux (Graine → Pousse →
Racine → Branches → Arbre → Forêt).

## Stack

- **Backend** : FastAPI + Motor (MongoDB), Python 3.11
- **Frontend** : React 19 (Create React App via craco), Tailwind CSS, shadcn/ui
- **IA** : SDK Anthropic officiel (Claude Sonnet 5) en fallback local, prêt
  pour CVLN Agent Factory dès qu'il sera branché

## Démarrer

Voir **[docs/DEVELOPER_GUIDE.md](docs/DEVELOPER_GUIDE.md)** pour les
instructions complètes (installation, architecture, moteur d'import FMS,
permissions, référence API).

```bash
# Backend
cd backend && pip install -r requirements.txt
cp .env.example .env  # renseigner MONGO_URL / DB_NAME / JWT_SECRET
uvicorn server:app --reload --port 8000

# Frontend
cd frontend && yarn install
cp .env.example .env  # REACT_APP_BACKEND_URL=http://localhost:8000
yarn start
```

## Documentation

| Document | Contenu |
|---|---|
| [docs/DEVELOPER_GUIDE.md](docs/DEVELOPER_GUIDE.md) | Architecture, convention de fichiers FMS, moteur de certification, permissions, référence API |
| [docs/AUDIT_REPORT.md](docs/AUDIT_REPORT.md) | Audit complet : dette technique supprimée, bugs corrigés, sécurité, performance, accessibilité, tests |
| [docs/INTEGRATIONS_REPORT.md](docs/INTEGRATIONS_REPORT.md) | Statut réel de chaque intégration écosystème CVLN |
| [INTEGRATION_CONTRACT.md](INTEGRATION_CONTRACT.md) | Contrat REST exact attendu par FrekCore et CVLN Agent Factory |
| [memory/PRD.md](memory/PRD.md) | Historique produit (décisions, itérations livrées) |

## État du projet

Backend : 80 endpoints, `black`/`isort`/`flake8`/`mypy` propres, 29 tests
unitaires. Frontend : ESLint propre, build de production vérifié, routes en
code-splitting, PWA (service worker + manifest). Détail complet dans
`docs/AUDIT_REPORT.md`.

## Licence

Propriété du groupe CVLN. Usage interne.
