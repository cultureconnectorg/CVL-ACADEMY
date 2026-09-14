# Rail 5 — corriger une hypothèse fausse : le vrai moteur dans ModuleJourney

**Statut : DONE (scope volontairement resserré, écarts documentés ci-dessous).**
**Date : 2026-09-07.**
**Flag : `REACT_APP_ACADEMY_SPATIAL_MODULE_DEPTH` — défaut `false`. Aucun comportement existant ne change sans action déployeur explicite.**

## 0. Mandat reçu

> Pourquoi tu ai loin de ce travail qui avais été fournis ???

En réponse à des captures montrant la richesse réelle du prototype H0.9 (Proof Gallery) : rail Hub avec profondeur 3D visible, `cameraReturnTransition` via le bouton Précédent du navigateur, `--topo-depth` qui varie, panneaux de debug caméra/physique/cadence (12 champs), et surtout un **contexte Quiz** ouvert avec confirmation son+haptique (`CONTEXT_OPEN` puis `CONFIRM`).

Vérification faite : l'écart était réel, et une partie provenait d'une **hypothèse fausse que j'avais moi-même écrite** dans le docstring de `SpatialHub.jsx` (Rail 3) — j'y affirmais que `CONTEXT_OPEN`/`CONTEXT_CLOSE`/`ENTER_DEPTH`/`RETURN_DEPTH` « appartiennent aux transitions de route, pas à ce rail ». C'est faux : `lib/ContextFrame.jsx` (W3-B, déjà construit avant ce chantier) est un système de dock **page-même** — jamais un changement de route — exactement l'endroit où ces événements ont un sens réel. Je ne l'avais tout simplement pas vérifié avant d'écrire cette phrase.

## 1. Diagnostic précis

- `lib/ContextFrame.jsx` / `useContextEntry()` (W3-B) : le vrai système ACTIVE↔CONTEXT, utilisé par `PhaseQuizContext` et `PhaseMiniMission` dans `ModuleJourney.js` — **jamais branché à aucun son/haptique**, jamais vérifié avant ce rapport.
- `lib/JourneyHierarchy.jsx` (`JourneyPhaseShell`, W3-A) : la hiérarchie CURRENT/ACQUIRED/NEXT/LOCKED du stepper de phases utilisait une table statique à 4 valeurs (`opacity`/`scale`/`saturate` fixes par rôle) — exactement la même classe de lacune que Dashboard/Roadmap avant Rail 3 : jamais branchée sur `physics.js`/`attention.js`.
- Confirmé qu'aucune des deux n'a besoin de la restructuration `App.js` déjà différée (App.js/Outlet) : ce sont des systèmes page-même, pas des transitions inter-route.

## 2. Corrigé

- **`JourneyHierarchy.jsx`** : `JourneyPhaseShell` accepte désormais `idx`/`currentIdx` (déjà calculés par `ModuleJourney.js` dans sa propre boucle) et, sous flag, rend chaque carte de phase via `useDepthPhysics` + `spatial/attention.js` (`computeDepthStyle`, formules inchangées) au lieu de la table statique. `deriveJourneyRole` reste la seule source de vérité pour *quelle* distance une phase reçoit — LOCKED lit toujours plus loin que son écart d'index brut (raison réelle et divulguée, jamais arbitraire). `aria-hidden` n'est délibérément jamais appliqué ici (contrairement à `SpatialHub`) : une liste de phases de module est une structure séquentielle réelle qu'un lecteur d'écran doit connaître en entier, pas un rail où « il y en a d'autres sur le côté » est implicite.
- **`ContextFrame.jsx`** : détecte la vraie transition `show` (false→true / true→false) et joue `CONTEXT_OPEN`/`CONTEXT_CLOSE` (`spatial/audio.js`, événements nommés exactement pour cet usage) — audio seul, aucun pattern haptique fabriqué (les 5 patterns de `haptics.js` n'en contiennent aucun dédié à un dock).
- **`ModuleJourney.js`** : `submitQuiz` (réussite) et `commitMiniMission` (réussite) jouent un vrai `CONFIRM` (audio+haptique) — une action réellement accomplie, pas un événement décoratif.

Tout gaté par un nouveau flag unique, `SPATIAL_MODULE_DEPTH` (défaut `false`), cohérent avec la discipline des flags déjà établie.

## 3. Preuve en direct

Backend `MOCK_DB=1`, utilisateur réel onboardé KOR, progression réelle avancée via les vraies routes API (hook/objectifs/atelier validés, cours à 100%, livrable soumis) :

- **Profondeur mesurée en direct** (lecture programmatique du style calculé, pas une capture seule) : la phase ouverte (« Le déclencheur ») lit `PRIMARY_ATTENTION`, opacité 1, `translateZ ≈ 56`. Chaque phase suivante recule continûment : opacité 0.72 → 0.46 → 0.35 → 0.30 → 0.27 → 0.26, `translateZ` de 2 à -88.7 — un vrai dégradé continu, plus la marche à 4 valeurs d'avant.
- Ouverture de la phase « Livrable » → le frontier se déplace réellement, capture à l'appui.
- Ouverture du Quiz → `data-context-state="context"` confirmé programmatiquement (le vrai `ContextFrame` a transitionné), les 5 phases validées reculent visiblement au-dessus, le Quiz s'ouvre au premier plan — exactement la doctrine « le savoir avance vers toi à mesure que tu avances vers lui », maintenant vraie dans ModuleJourney aussi.

## 4. Vérification technique

- Jest : **160/160** (aucun nouveau test structurel ajouté ce rail — `JourneyHierarchy.test.js` existant, qui ne couvre que les fonctions pures `deriveJourneyRole`/`JOURNEY_VARIANTS`, reste vert sans modification, confirmant la non-régression du chemin flag-off).
- ESLint : propre.
- Build production : OK.
- Playwright e2e : **73/73**, y compris les 3 suites ModuleJourney (`module-journey-context`, `module-journey-hierarchy`, `module-journey-navigation`) — zéro régression, flag off.
- Backend : non touché.
- Avertissement console observé (`inert=""`) : préexistant dans `MentorPanel.js` (non touché ce rail), pas une régression introduite ici — vérifié avant d'écrire ce rapport.

## 5. Fichiers touchés

Modifiés : `frontend/src/lib/JourneyHierarchy.jsx`, `frontend/src/lib/ContextFrame.jsx`, `frontend/src/pages/ModuleJourney.js`, `frontend/src/lib/featureFlags.js`, `frontend/src/lib/featureFlags.test.js`.
Aucun nouveau fichier. Backend : aucun fichier touché.

## 6. Ce qui reste réellement hors périmètre (vérifié, pas supposé)

- Le rail Hub avec `perspective`/`translateZ` fortement visible (comme dans les captures H0.9) — Dashboard a déjà ce traitement depuis Rail 3 (`SpatialHub`), donc ce n'était pas un manque réel malgré l'apparence de la comparaison.
- `cameraReturnTransition` (bouton Précédent du navigateur inversant l'ancre caméra) et `--topo-depth` variant par route — genuinement bloqué par l'architecture React Router actuelle (changement de route = démontage réel), nécessite la restructuration `App.js`/`Outlet` déjà différée. Confirmé de nouveau, pas juste répété.
- Panneaux de debug caméra/physique/cadence à 12 champs — explicitement « prototype-only, not a real feature » dans le code source du prototype lui-même ; ne devraient jamais atterrir en production.
- Missions/Badges/FrekProfile n'ont toujours pas le traitement par paliers d'attention.
