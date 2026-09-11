# CVLN Academy — audit général des routes, page par page

Date: 2026-09-11
Base auditée: `main` @ `410be58eb1a99798c5aa2612f168fc8e146e5adb`
Branche de travail: `audit/routes-page-by-page-20260911`

## Méthode

Evidence First: une page n'est marquée **câblée** que si la route React existe et que ses appels API observables correspondent à une surface backend montée sous `/api`. Les validations runtime/browser restent distinctes de l'inspection statique.

## Route map frontend

| Route | Page | Guard | État statique | Smoke E2E ajouté |
|---|---|---|---|---|
| `/` | Landing | public | branchée | déjà couvert |
| `/legal/accept` | LegalAcceptance | public/bootstrap | branchée | couverture légale existante à conserver |
| `/legal/:slug` | LegalHub | public | branchée | couverture légale existante à conserver |
| `/onboarding` | Onboarding | LegalGuard | branchée | oui |
| `/dashboard` | Dashboard | Protected + LegalGuard | branchée | oui |
| `/roadmap` | Roadmap | Protected + LegalGuard | branchée | oui |
| `/formations` | Formations | Protected + LegalGuard | branchée | oui |
| `/formations/:code` | FormationDetail | Protected + LegalGuard | branchée | oui |
| `/formations/:fc/modules/:mc` | ModuleJourney | Protected + LegalGuard | branchée | oui |
| `/missions` | Missions | Protected + LegalGuard | branchée | oui |
| `/badges` | Badges | Protected + LegalGuard | branchée | oui |
| `/frek-profile` | FrekProfile | Protected + LegalGuard | branchée | oui |
| `/wallet` | Wallet | Protected + LegalGuard | branchée | oui |
| `/skills` | Skills | Protected + LegalGuard | branchée | oui |
| `/certifications` | Certifications | Protected + LegalGuard | branchée | oui |
| `/trainer` | TrainerDashboard | trainer/admin/super_admin/founder | branchée | oui, rôle trainer |
| `/jury` | JuryDashboard | jury/admin/super_admin/founder | branchée | oui, rôle jury |
| `/admin` | AdminDashboard | admin/super_admin/founder | branchée | oui, rôle admin + panneaux |
| `*` | redirect `/` | — | branchée | déjà couvert |

## Câblage backend observé

Le routeur backend agrège `health`, `auth`, `legal`, `orgs`, `formations`, `badges`, `fms`, `fms_lineage`, `skills`, `templates`, `assistants`, `integrations`, `onboarding`, `learning`, `quizzes`, `missions`, `progression`, `mentor`, `certification` et `wallet` sous `/api`.

Les surfaces de parcours sensibles (`onboarding`, `learning`, `quizzes`, `missions`, `progression`, `mentor`, `certification`, `wallet`) ont en plus une dépendance serveur `require_legal_acceptance`: la protection légale n'est donc pas seulement visuelle côté React.

## Vérifications page → API confirmées

### Dashboard
Appels observés: `/frek/profile`, `/missions`, `/badges/mine`, `/progression/summary`, `/user/learning-path`.

- `/frek/profile` et `/progression/summary` sont implémentés dans `backend/api/progression.py`.
- `/user/learning-path` est implémenté dans `backend/api/learning.py`.
- `/missions` et `/badges/mine` sont montés par leurs routeurs dédiés.

**Câblage statique confirmé.** Risque restant: `Promise.all` rend le chargement du dashboard tout-ou-rien si un seul service échoue.

### Formations
Appels observés: `/user/learning-path` et `/poles`.

- `/user/learning-path` existe côté learning.
- `/poles` existe côté formations.

**Câblage statique confirmé.**

### FormationDetail
Appel observé: `/formations/{code}`.

- Endpoint correspondant présent dans `backend/api/formations.py`, avec calcul serveur de verrouillage et statuts module par utilisateur.

**Câblage statique confirmé.**

### ModuleJourney
Appels observés:

- `GET /modules/{formation}/{module}`
- `POST /modules/{formation}/{module}/phase`
- `POST /modules/{formation}/{module}/deliverable`
- `GET /formations/{formation}/modules/{module}/quiz`
- `POST /formations/{formation}/modules/{module}/quiz/submit`
- `POST /modules/{formation}/{module}/mini-mission/commit`

Les chemins correspondent aux routeurs `learning.py` et `quizzes.py`. Les gates de quiz et mini-mission sont également vérifiés côté serveur.

**Câblage statique confirmé.**

### Badges
Appels observés: `/badges` et `/badges/mine`. Les deux endpoints existent dans `backend/api/badges.py`.

**Câblage statique confirmé.**

### Skills
Appel observé: `/skills/mine`. Endpoint correspondant présent dans `backend/api/skills.py`.

**Câblage statique confirmé.**

### Wallet
Appels observés: `/wallet/me` et `/wallet/pass/{provider}`. La page possède déjà `loading`, `catch` et feedback utilisateur.

**Route frontend confirmée; backend à garder dans la passe endpoint exhaustive.**

### Certifications
Appels observés: attempts mine, rubrics, création d'attempt et attestation PDF. La page possède un état de chargement et une gestion explicite des erreurs.

**Route frontend confirmée; backend à garder dans la passe endpoint exhaustive.**

### Trainer / Jury / Admin
Les trois routes sont protégées par listes de rôles distinctes dans `App.js`. Un smoke test par rôle a été ajouté. Le test Admin exige aussi le rendu des quatre panneaux (`FMS import`, `integrations`, `orgs`, `catalogue`) pour éviter qu'un simple shell vide soit considéré comme fonctionnel.

## Nouvelle preuve automatique

Ajout de `frontend/e2e/page-route-wiring.spec.js`.

Ce test couvre les routes authentifiées page par page avec la fixture Playwright test-only existante. Il valide que chaque URL résout jusqu'au composant attendu et fournit des contrats de payload minimaux aux pages qui exigent des tableaux (`badges`, `skills`, `certifications`, jury, admin) afin de détecter les crashes de rendu liés au câblage.

Cette couverture complète `auth-guards.spec.js`: le premier prouve qu'une route protégée est inaccessible sans session; le nouveau prouve qu'une session autorisée atteint effectivement la bonne page.

## Risques / enrichissements à traiter

1. **Gestion d'erreurs page par page** — Dashboard, Formations, FormationDetail, Missions, Badges, FrekProfile et ModuleJourney contiennent encore des chargements sans fallback d'erreur complet. Une panne d'endpoint peut laisser un écran incomplet ou sur `…`.
2. **Route inconnue** — le wildcard renvoie systématiquement vers `/`; ce comportement est actuellement testé et donc intentionnel. Une vraie 404 serait un changement produit, pas une correction silencieuse.
3. **Guards** — `Protected` et `LegalGuard` retournent `null` pendant certains chargements. Un skeleton accessible serait préférable mais doit être traité comme enrichissement UX dédié.
4. **Contrat endpoint exhaustif** — continuer jusqu'à Wallet, Certifications, Trainer, Jury et Admin côté backend afin de documenter chaque verbe HTTP, auth et rôle.
5. **QA runtime obligatoire avant “full live”** — le fichier E2E a été poussé, mais son exécution réelle doit encore être observée via un runner/CI. Ne pas confondre test écrit et test passé.

## Definition of Done pour chaque page

`route déclarée` → `guard correct` → `page importable` → `API appelée` → `endpoint monté` → `auth/role correct` → `loading/error/empty state` → `navigation aller/retour` → `test E2E` → `CI verte` → `runtime vérifié`.

## Décision actuelle

Le squelette de routage est cohérent et les parcours pédagogiques principaux sont correctement alignés frontend/backend. Une couverture E2E authentifiée page-par-page existe maintenant sur la branche d'audit.

**Pas encore de déclaration “full live”** tant que le nouveau test n'a pas été exécuté réellement et que la passe endpoint exhaustive des surfaces Wallet/Certification/Staff n'est pas terminée.