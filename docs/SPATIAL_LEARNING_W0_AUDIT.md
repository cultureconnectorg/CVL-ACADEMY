# Spatial Learning — Audit W0 (complet, lecture seule)

**Baseline auditée :** commit `ede26f4` (branche `claude/cvln-academy-production-r35l31`),
working tree propre au moment de cet audit (`git status --porcelain` ne
liste que ce document lui-même, non suivi).

**Statuts binaires de cette étape :**

```
SECONDMENT_PROTOCOL_STATUS   = CONCEPTUAL_TARGET
AGENT_FACTORY_INTEGRATION    = BLOCKED_EXTERNAL_DEPENDENCY
  REASON                     = NO_ACCESSIBLE_CANONICAL_AGENT_REGISTRY
REAL_AGENT_FACTORY_BINDING   = BLOCKED
FAKE_AGENT_FACTORY_BINDING   = FORBIDDEN
SPATIAL_LEARNING_IMPLEMENTATION = AUDITED_NOT_STARTED
CODE_CHANGES                 = FORBIDDEN
W1                           = NOT_AUTHORIZED
CURRENT_BASELINE             = FROZEN (ede26f4)
```

Aucun fichier de code n'a été modifié pour produire ce document. Toute
commande exécutée (lint, build, tests) est en lecture seule et n'a laissé
aucune trace dans l'arbre de travail.

---

## 0. Agent Secondment Protocol — statut

Confirmé avec toi : traité comme **architecture cible conceptuelle**, pas
comme un système à auditer ou simuler maintenant.

- Aucun registre `CVLN_AGENT_FACTORY` réel n'est accessible depuis cette
  session (ni dans ce dépôt, ni via un accès externe donné).
- `backend/services/agent_factory.py` reste la seule réalité vérifiable :
  une interface typée avec fallback SDK Anthropic — jamais un multi-agents.
- Les 21 rôles du protocole (`CVLN-AF-ACA-00` à `-20`) sont traités comme
  des **capability profiles temporaires** appliqués à mon propre travail
  de session (séparation des responsabilités, evidence-first, aucune
  auto-certification), jamais comme des agents réellement assignés,
  détachés ou retournés.
- Le protocole lui-même (fichiers `.xlsx`/`.pptx` sources) n'est ni
  supprimé ni remplacé par une implémentation locale factice — il reste
  la cible pour un vrai `W0-FACTORY-AUDIT`, séparé, le jour où un accès
  réel à CVLN Agent Factory est fourni.

Le reste de ce document couvre exclusivement le premier classeur (231
exigences Spatial Learning) contre l'état réel du dépôt Academy.

---

## 1. Frontend — architecture générale

| OBSERVED | FILE_PATH | CURRENT_BEHAVIOR | RISK | DECISION |
|---|---|---|---|---|
| Stack | `frontend/package.json` | React 19, CRA via craco, Tailwind, shadcn/Radix, React Router v7, TanStack Query, react-hook-form/zod | Aucun | REUSE |
| Point d'entrée app | `frontend/src/App.js` | `I18nProvider > AuthProvider > BrowserRouter > Suspense > Routes` | Aucun | REUSE |
| Découpage par route | `frontend/src/App.js:11-27` | 15 routes en `React.lazy`, un seul `PageFallback` générique (`…`) partagé | Faible — le fallback est minimal, pas de squelette par page | REUSE (EXTEND si un fallback plus riche est requis par UX-021) |
| Garde d'accès | `frontend/src/App.js:35-40` (`Protected`) | Enchaîne loading → auth → onboarding → RBAC par rôle → `Layout` | Aucun | REUSE |
| Shell applicatif | `frontend/src/components/Layout.js` | Sidebar fixe + FREK-ID card + sélecteur de langue + `<nav>`/`<main>` sémantiques déjà présents | Faible | REUSE |
| CSS/design tokens | `frontend/src/index.css` | Variables CSS pour couleurs/rayons (`--cvln-orange`, `--radius`, etc.) ; **aucun token de timing/easing/depth** | Moyen — MOT-026 (tokens de timing centraux) n'a rien à étendre, tout est à créer | EXTEND (nouveau bloc de tokens, même fichier ou nouveau `motion-tokens.css`) |
| Composants partagés | `frontend/src/components/` (`Layout.js`, `MentorPanel.js`, `BackButton.js`, `ui/*` shadcn) | Aucun encore ne modélise "focus/depth/contexte" (MOTION_SYSTEM primitives) | — | Nouveaux composants requis, au-dessus de l'existant (EXTEND, pas REPLACE) |

---

## 2. Routing & navigation (ARC-001 à 004, UX-011 à 015)

| OBSERVED | FILE_PATH | CURRENT_BEHAVIOR | RISK | DECISION |
|---|---|---|---|---|
| URLs canoniques | `App.js:53-71` | `/`, `/onboarding`, `/dashboard`, `/roadmap`, `/formations`, `/formations/:code`, `/formations/:fc/modules/:mc`, `/missions`, `/badges`, `/frek-profile`, `/wallet`, `/skills`, `/certifications`, `/trainer`, `/jury`, `/admin` | Aucun | REUSE |
| Retour navigateur | `BrowserRouter` (natif) | Historique standard du navigateur, pas de surcouche custom | Aucun aujourd'hui — mais tout mécanisme de "RETURN to exact context" (MOT-017) à ajouter devra composer avec l'historique natif, pas le remplacer (ARC-004) | EXTEND avec prudence |
| Retour contextuel après un module | Aucun mécanisme dédié constaté | Le retour se fait par navigation standard (`BackButton` → `nav(-1)` ou route de repli) | — | `frontend/src/components/BackButton.js` : logique déjà correcte pour un retour simple ; MOT-017/UX-015 (position de scroll exacte, état de contexte restauré) demandent une extension, pas un remplacement |
| Deep-link | Non testé en E2E (voir §12) | Chaque route étant une URL directe sans état requis en amont (hors `Protected`), les deep-links fonctionnent structurellement | Non mesuré formellement — pas de preuve E2E encore | REUSE, à couvrir par un test avant W1 exit |

---

## 3. Motion — état réel (domaine le plus vide du dossier, 30 exigences)

| OBSERVED | FILE_PATH | CURRENT_BEHAVIOR | RISK | DECISION |
|---|---|---|---|---|
| Bibliothèque installée | `frontend/package.json` | `framer-motion@11.18.0` présent en dépendance | — | **Déjà là, jamais câblée** — confirmé par `grep -rl framer-motion frontend/src` → aucun résultat |
| Transitions actuelles | `frontend/src/index.css:99,113,123,151-157` | CSS pur : `transition: transform 240ms ease...`, `.fade-in` (`animation: fadeIn 500ms ease both`) | — | Aucune sémantique de focus/profondeur ; ce sont des micro-interactions décoratives (hover carte, hover bouton), pas un système |
| Primitives sémantiques (FOCUS/APPROACH/ENTER/RECEDE/REVEAL/RETURN/CONFIRM/HORIZON) | — | **Aucune trace dans le dépôt** | Élevé — c'est le cœur de la doctrine Spatial Learning, actuellement à 0% | NEW — construction complète requise |
| `prefers-reduced-motion` | — | **Zéro occurrence dans tout `frontend/src`** (`grep -rn prefers-reduced-motion` → vide) | **Critique** — bloque A11Y-005, A11Y-006, MOT-029 ; c'est une précondition avant d'ajouter le moindre mouvement supplémentaire | NEW — doit être la toute première pièce de W1, avant tout autre travail de motion |
| WebGL/3D | `frontend/package.json` | Aucune dépendance (`three`, `@react-three/fiber`, etc. absents) | Aucun — conforme à "ne pas ajouter par défaut" | NOT ADDED — reste hors scope tant qu'aucun ADR ne prouve un besoin (W4 uniquement) |

---

## 4. Auth / RBAC (SEC-001, SEC-002, INT-003, INT-004)

| OBSERVED | FILE_PATH | CURRENT_BEHAVIOR | RISK | DECISION |
|---|---|---|---|---|
| Schéma d'auth | `backend/auth.py` | JWT d'accès (HS256, courte durée) + refresh token opaque stocké hashé, rotatif à chaque usage | Aucun | REUSE |
| Rôles | `backend/models.py:123-125` | `Role = Literal["student","trainer","corrector","jury","admin","super_admin","founder"]` — 7 rôles typés strictement | Aucun | REUSE |
| Garde de rôle | `backend/auth.py:229` (`require_role`) | Factory de dépendance FastAPI, utilisée par chaque routeur staff/admin | Aucun | REUSE |
| Garde frontend | `frontend/src/App.js` (`Protected`, `ADMIN_ROLES`/`TRAINER_ROLES`/`JURY_ROLES`) | Redirige si rôle non autorisé, avant même le rendu de la page | Aucun | REUSE — toute évolution motion doit envelopper ce composant (WRAP), jamais le contourner |

---

## 5. FREK-ID (INT-001, INT-002, ARC-025)

| OBSERVED | FILE_PATH | CURRENT_BEHAVIOR | RISK | DECISION |
|---|---|---|---|---|
| Génération | `backend/auth.py:197` (`next_frek_id`) | Délègue à `frek_core.mint_frek_id()` | Aucun | REUSE |
| Intégration FrekCore | `backend/services/frek_core.py` | Interface typée avec fallback local (compteur Mongo séquentiel) tant que `FREK_CORE_BASE_URL` n'est pas configuré — documenté dans `docs/INTEGRATIONS_REPORT.md` | Aucun nouveau — état déjà honnête (INT-002 déjà respecté : pas d'état FREK fictif, juste un fallback local assumé) | REUSE |
| Affichage frontend | `frontend/src/components/Layout.js`, `frontend/src/pages/FrekProfile.js` | FREK-ID affiché comme identité persistante, jamais recalculé côté client | Aucun | REUSE |

---

## 6. FMS01–FMS06 (LRN-001 à 008) — le point le plus important de cet audit

| OBSERVED | FILE_PATH | CURRENT_BEHAVIOR | RISK | DECISION |
|---|---|---|---|---|
| Import réel validé | `backend/fms_import/`, `docs/FMS_IMPORT_VALIDATION_REPORT.md` | 223/223 fichiers réels du ZIP FMS_Chantier_Complet importables sans erreur (validé aujourd'hui même, pipeline complet y compris écriture DB testée en mémoire) | Aucun sur le moteur d'import lui-même | REUSE |
| **Contenu réellement affiché à l'apprenant** | `backend/api/learning.py:28` (`get_module_journey`), `backend/seed_modules.py`, `backend/seed_data.py` | Le parcours étudiant (`ModuleJourney.js` → `/api/modules/{fc}/{mc}`) lit `db.formations`, **pas** `db.fms_resources`. Le contenu de module vu par l'utilisateur est le contenu générique seedé en février, pas le corpus FMS réel | **Élevé pour LRN-012** ("Render real module content") : le corpus FMS réel validé n'est **pas encore** ce que l'étudiant voit — c'est deux couches distinctes, jamais fusionnées | **REPLACE-BLOCKED tant que non arbitré** — synthétiser `Formation`/`Module` depuis `fms_resources` est un chantier de contenu (mapping éditorial), explicitement différé dans `docs/AUDIT_REPORT.md` §8 et `docs/FMS_IMPORT_VALIDATION_REPORT.md` §5 en attendant une validation humaine CVLN. **Ne pas déclencher cette fusion comme effet de bord d'un chantier motion.** |
| Frontières FMS01–06 | `backend/fms_import/` (types réels, métier→formation mapping) | Les frontières inter-métiers sont documentées dans le contenu FMS lui-même (référentiels), pas encore encodées comme règle applicative empêchant un mélange dans l'UI | Moyen — LRN-002 à LRN-008 supposent des frontières déjà "actives" dans le produit ; aujourd'hui elles n'existent que comme texte dans les fichiers importés | À déterminer en W1 selon si la doctrine s'applique à la doc importée (déjà vrai) ou à un mécanisme UI (n'existe pas encore) |

---

## 7. Skill Engine (LRN-014, INT-005)

| OBSERVED | FILE_PATH | CURRENT_BEHAVIOR | RISK | DECISION |
|---|---|---|---|---|
| Modèle | `backend/skills/models.py` | `Skill`, `EvidenceEntry` (hash SHA-256, append-only), `UserSkill` dérivé des preuves | Aucun | REUSE |
| Progression | `backend/skills/progression.py` | `record_evidence()` recalcule l'état à partir des preuves, jamais d'état déclaré directement | Aucun | REUSE |
| Affichage frontend | `frontend/src/pages/Skills.js` | Lit `/skills/mine`, aucune donnée inventée côté client | Aucun | REUSE |

---

## 8. Certification Engine (LRN-009, LRN-010, LRN-016, INT-006)

| OBSERVED | FILE_PATH | CURRENT_BEHAVIOR | RISK | DECISION |
|---|---|---|---|---|
| Notation | `backend/certification/scoring.py` | Pur, testé (40 tests unitaires backend passent — voir §12) ; gère score pondéré + critères éliminatoires + plafonnement de mention (ajouté aujourd'hui même, réconcilié contre la vraie grille FMS-01) | Aucun | REUSE |
| Statuts | `backend/certification/models.py` (`AttemptStatus`) | `in_progress → submitted → graded (passed\|failed)`, jamais de succès optimiste côté client | Aucun | REUSE — c'est la garantie structurelle derrière ARC-009 "No optimistic certification" |
| Attestation | `backend/certification/attestation.py` | PDF avec hash de signature jury imprimé, vérifiable | Aucun | REUSE |
| Frontend | `frontend/src/pages/Certifications.js`, `frontend/src/pages/jury/JuryDashboard.js` | Lit/écrit uniquement via l'API ; aucun état de réussite calculé côté client | Aucun | REUSE |

---

## 9. Progression / badges / missions (SYS-008 à 020)

| OBSERVED | FILE_PATH | CURRENT_BEHAVIOR | RISK | DECISION |
|---|---|---|---|---|
| Badges | `backend/badges_engine.py` (`award_threshold_badges`) | Seuils CC réels, attribution idempotente | Aucun | REUSE |
| Missions | `backend/api/missions.py` | Accept/submit réels, CC crédités par le backend | Aucun | REUSE |
| CC/JCC | `backend/wallet/` (grand livre) | Soldes réels, pas de "monnaie XP" fictive séparée | Aucun — SYS-010 "No fake XP currency" déjà respecté structurellement | REUSE |
| Boucles internes (Core/Learning/Progress/Opportunity/Social/Ecosystem) | — | Les boucles "Core" et "Learning" existent en substance (progression réelle, feedback pédagogique) ; "Opportunity"/"Social"/"Ecosystem" (SYS-005/006/007, P1) n'ont pas d'équivalent produit aujourd'hui | Faible (P1, pas P0) | Hors scope W1-W3 sauf décision contraire |

---

## 10. PWA / offline (INT-011, ARC-024, QA-012)

| OBSERVED | FILE_PATH | CURRENT_BEHAVIOR | RISK | DECISION |
|---|---|---|---|---|
| Manifest | `frontend/public/manifest.json` | Présent, marque CVLN (pas de branding Emergent résiduel) | Aucun | REUSE |
| Service worker | `frontend/public/service-worker.js`, `frontend/src/serviceWorkerRegistration.js` | Maison (pas Workbox généré), cache applicatif de base | Non mesuré : comportement offline précis non re-testé dans cet audit | REUSE, à re-vérifier par un test QA-012 dédié avant toute modification du shell |

---

## 11. Accessibilité — état réel (15 exigences, toutes P0/CRITICAL selon le dossier source)

| OBSERVED | FILE_PATH | CURRENT_BEHAVIOR | RISK | DECISION |
|---|---|---|---|---|
| Landmarks sémantiques | `components/Layout.js:51,102`, `pages/Landing.js:43,167` | `<nav>`, `<main>`, `<header>`, `<footer>` déjà posés sur les deux shells principaux | Faible | REUSE |
| `aria-*` | Comptage direct | Seulement **7 fichiers sur 19** utilisent un attribut `aria-*` | Moyen — pas un échec en soi (beaucoup de HTML natif n'en a pas besoin), mais aucun audit fin (rôle par rôle) n'a été fait | Non mesuré finement — nécessite une revue composant par composant en W1/W2, pas une estimation globale |
| Focus clavier visible | Comptage direct | `outline-none` utilisé **44 fois dans 28 fichiers** ; seuls **11 fichiers** compensent avec un `focus:ring`/`focus:border` explicite | **Élevé pour A11Y-003** — le différentiel (~17 usages `outline-none` sans remplacement visible confirmé) est un risque réel de perte de focus clavier visible, à vérifier fichier par fichier, pas supposé | Risque réel, priorité haute pour W1 |
| `prefers-reduced-motion` | — | Absent à 100% (voir §3) | Critique, précondition bloquante | NEW |
| Images | — | Aucun `<img>` dans tout le frontend (icônes = composants SVG `iconoir-react`) | Aucun — pas de dette `alt=` manquant, car pas d'`<img>` du tout | N/A |
| Cible tactile / mobile | — | Non mesuré (nécessite un test sur device réel ou matrice, QA-009) | Non mesuré | À couvrir en W1 exit criteria, pas supposé conforme |

---

## 12. Build / lint / types / tests — état réel, vérifié à l'instant (lecture seule)

| OBSERVED | COMMANDE | RÉSULTAT |
|---|---|---|
| Backend format | `black --check .` | ✅ 72 fichiers, aucun changement requis |
| Backend imports | `isort --profile black --check .` | ✅ propre |
| Backend lint | `flake8 .` | ✅ aucune erreur |
| Backend types | `mypy --ignore-missing-imports .` | ✅ aucune erreur, 72 fichiers |
| Backend tests unitaires | `pytest tests/ -n 0 --ignore=tests/backend_test.py` | ✅ 40/40 passent |
| Backend tests E2E | `tests/backend_test.py` | **Non exécuté ici** — nécessite un backend + Mongo réellement démarrés, absents de cet environnement d'audit |
| Frontend lint | `npx eslint src` | ✅ aucune erreur |
| Frontend build prod | `yarn build` (exécuté juste avant ce document, même baseline) | ✅ compile sans warning — `main.js` 129.24 kB gzippé + 17 chunks de route (1-6 kB chacun) |
| Frontend tests | — | **Aucun test unitaire ni E2E n'existe** (`find frontend -iname "*.test.js" -o -iname "*.spec.js"` → vide, pas de Playwright installé) | Gap réel, bloquant pour QA-005/006/008/009/011 |

---

## 13. Classification de synthèse (REUSE / EXTEND / WRAP / REPLACE-BLOCKED)

| Composant | Classification | Note |
|---|---|---|
| Router, `Protected`, RBAC, auth, FREK-ID, Skill Engine, Certification Engine, badges, missions, Wallet | **REUSE** | Vérité backend déjà systématique ; le risque du chantier Spatial Learning est de régresser ceci, pas de le reconstruire |
| CSS tokens (couleurs/rayons existants) | **EXTEND** | Ajouter un bloc de tokens de mouvement à côté, ne pas réécrire |
| `framer-motion` | **REUSE** | Déjà en dépendance, jamais câblé — aucune nouvelle librairie à ajouter pour la 2D |
| `BackButton`, navigation retour | **EXTEND** | Logique de base saine ; contexte exact de retour (scroll, focus) à ajouter par-dessus |
| Primitives motion sémantiques (FOCUS/APPROACH/ENTER/…) | **NEW** (pas de composant existant à classer) | 0% du système présent |
| `prefers-reduced-motion` | **NEW**, bloquant | Précondition avant tout le reste du motion |
| Fusion `fms_resources` → `Formation`/`Module` visibles étudiant | **REPLACE-BLOCKED** | Nécessite un arbitrage humain CVLN séparé (voir §6), pas une décision technique de ce chantier |
| Infrastructure E2E/visuelle | **NEW** | Absente, bloquante pour toute la vague QA (W6) et pour prouver `VERIFIED` sur les exigences motion |
| WebGL/3D | **NOT ADDED** | Hors scope tant qu'aucun ADR ne le justifie (W4 uniquement) |
| Agent Secondment Protocol | **CONCEPTUAL_TARGET** | Voir §0 |

---

## 14. W1_PRECONDITIONS

```
READY = NO
```

Blocages exacts avant que W1 (fondations : tokens de mouvement, support
`prefers-reduced-motion`, wrapper de routing pour les transitions) puisse
démarrer *avec preuve*, pas par confiance :

1. **`CODE_CHANGES = FORBIDDEN` tant que tu n'as pas validé cet audit** —
   condition posée par toi, toujours active.
2. **Aucune infrastructure de test E2E/visuelle** n'existe pour prouver
   qu'un changement de motion ne casse rien (QA-005/006/008/009/011) —
   sans ça, aucune exigence motion ne pourra jamais passer `VERIFIED`
   avec preuve, seulement "implémenté sans régression connue".
3. **`outline-none` sur ~17 usages non compensés par un focus visible
   confirmé** (§11) — à vérifier avant d'ajouter la moindre nouvelle
   interaction motion, sinon le risque d'accessibilité se creuse encore.
4. **Le contenu FMS réel n'est pas ce que l'étudiant voit aujourd'hui**
   (§6) — si le chantier Spatial Learning touche `ModuleJourney`/`FormationDetail`,
   il faut décider explicitement : travailler sur le contenu seedé actuel
   tel quel (le plus sûr, ne touche pas à un chantier de contenu séparé),
   ou inclure la fusion FMS comme sous-chantier — **ce n'est pas une
   décision technique, c'est un arbitrage produit qui t'appartient**.
5. Aucun blocage sur le reste (routeur, auth, RBAC, moteurs Skill/Certification,
   PWA) — tous classés REUSE avec preuve à l'appui.

Une fois ces points arbitrés/résolus et une fois que tu donnes le feu vert
explicite, W1 peut commencer par la pièce la plus sûre et la plus
indépendante de tout le reste : **les tokens de mouvement centraux + le
support `prefers-reduced-motion`**, sans toucher à un seul écran visible
utilisateur.
