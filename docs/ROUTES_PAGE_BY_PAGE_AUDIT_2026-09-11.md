# CVLN Academy — audit général des routes, page par page

Date: 2026-09-11
Base auditée: `main` @ `410be58eb1a99798c5aa2612f168fc8e146e5adb`

## Méthode

Evidence First: une page n'est marquée **câblée** que si la route React existe et que ses appels API observables correspondent à une surface backend montée sous `/api`. Les validations runtime/browser restent distinctes de l'inspection statique.

## Route map frontend

| Route | Page | Guard | État statique |
|---|---|---|---|
| `/` | Landing | public | branchée |
| `/legal/accept` | LegalAcceptance | public/bootstrap | branchée |
| `/legal/:slug` | LegalHub | public | branchée |
| `/onboarding` | Onboarding | LegalGuard | branchée |
| `/dashboard` | Dashboard | Protected + LegalGuard | branchée |
| `/roadmap` | Roadmap | Protected + LegalGuard | branchée |
| `/formations` | Formations | Protected + LegalGuard | branchée |
| `/formations/:code` | FormationDetail | Protected + LegalGuard | branchée |
| `/formations/:fc/modules/:mc` | ModuleJourney | Protected + LegalGuard | branchée |
| `/missions` | Missions | Protected + LegalGuard | branchée |
| `/badges` | Badges | Protected + LegalGuard | branchée |
| `/frek-profile` | FrekProfile | Protected + LegalGuard | branchée |
| `/wallet` | Wallet | Protected + LegalGuard | branchée |
| `/skills` | Skills | Protected + LegalGuard | branchée |
| `/certifications` | Certifications | Protected + LegalGuard | branchée |
| `/trainer` | TrainerDashboard | trainer/admin/super_admin/founder | branchée |
| `/jury` | JuryDashboard | jury/admin/super_admin/founder | branchée |
| `/admin` | AdminDashboard | admin/super_admin/founder | branchée |
| `*` | redirect `/` | — | branchée |

## Câblage backend observé

Le routeur backend agrège `health`, `auth`, `legal`, `orgs`, `formations`, `badges`, `fms`, `fms_lineage`, `skills`, `templates`, `assistants`, `integrations`, `onboarding`, `learning`, `quizzes`, `missions`, `progression`, `mentor`, `certification` et `wallet` sous `/api`.

Les surfaces de parcours sensibles (`onboarding`, `learning`, `quizzes`, `missions`, `progression`, `mentor`, `certification`, `wallet`) ont en plus une dépendance serveur `require_legal_acceptance`: la protection légale n'est donc pas seulement visuelle côté React.

## Vérifications page → API déjà confirmées dans ce passage

### Dashboard
Appels observés: `/frek/profile`, `/missions`, `/badges/mine`, `/progression/summary`, `/user/learning-path`. La page est bien routée. À revalider en runtime pour les cinq appels simultanés, les états vides et les erreurs partielles.

### Badges
Appels observés: `/badges` et `/badges/mine`. Les deux endpoints existent dans `backend/api/badges.py`. **Câblage statique confirmé.**

### Skills
Appel observé: `/skills/mine`. Endpoint correspondant présent dans `backend/api/skills.py`. **Câblage statique confirmé.**

## Risques / enrichissements à traiter

1. **Gestion d'erreurs page par page** — plusieurs écrans utilisent des `Promise.all` ou chargements initiaux sans stratégie visible de dégradation partielle. Une panne d'un endpoint peut rendre une page entière silencieuse ou incomplète.
2. **Route inconnue** — le wildcard renvoie systématiquement vers `/`; pour un produit mature, une vraie page 404 avec retour contextuel et télémétrie serait plus claire.
3. **Guards** — `Protected` et `LegalGuard` retournent `null` pendant le chargement. Remplacer par un état accessible et stable évitera l'impression d'écran vide.
4. **Contrat route/API automatisé** — ajouter un test qui extrait les routes React et vérifie les chemins critiques contre le backend/OpenAPI afin d'empêcher les régressions de câblage.
5. **QA runtime obligatoire avant “full live”** — exécuter les parcours Landing → légal → onboarding → dashboard → formations → module → progression, puis trainer/jury/admin avec rôles réels ou fixtures autorisées.

## Definition of Done pour chaque page

`route déclarée` → `guard correct` → `page importable` → `API appelée` → `endpoint monté` → `auth/role correct` → `loading/error/empty state` → `navigation aller/retour` → `test E2E` → `CI verte` → `runtime vérifié`.

## Décision

Le squelette de routage est cohérent et déjà largement branché. Cet audit **ne déclare pas encore toutes les pages runtime-validées**: la prochaine passe doit ouvrir chaque page, inventorier tous ses appels API, corriger les gaps, puis exécuter les E2E et CI. Aucun enrichissement fonctionnel spéculatif ne doit être ajouté avant cette preuve.