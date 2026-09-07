# Rail 3 — Finir Spatial Learning : rapport de câblage

**Statut : DONE (scope volontairement resserré, écarts documentés ci-dessous).**
**Date : 2026-09-07 (corrigé le même jour, voir §11).**
**Flags : `REACT_APP_ACADEMY_SPATIAL_HUB_ENABLED`, `REACT_APP_ACADEMY_SPATIAL_ENVIRONMENT`, `REACT_APP_ACADEMY_SPATIAL_AUDIO`, `REACT_APP_ACADEMY_SPATIAL_HAPTICS` — défaut `false` pour les quatre. Aucun comportement existant ne change sans action déployeur explicite.**

## 11. Correction post-livraison — "j'ai pas l'impression que c'est au niveau de ce que nous avions commencé"

Retour reçu juste après la première livraison de ce rapport : le niveau de reprise ne correspondait pas au travail H0.8-H0.10 arrêté avant le chantier corpus. Vérification faite (`grep` sur tout le repo) : exact. La première passe ne branchait que `attention.js` (les formules statiques de profondeur), animées par un tween Framer Motion à durée fixe. Restaient **construits, testés, mais jamais importés en production** : `physics.js` (le vrai ressort `rAF`), `cadence.js` (classificateur de cadence), `audio.js` et `haptics.js` (les 8 événements sonores / 5 patterns vibratoires) — zéro import hors leurs propres tests.

Corrigé le même jour :

- **`lib/useDepthPhysics.js`** (nouveau) — enveloppe React de `spatial/physics.js`'s `makeRailPhysics`, sans aucune math propre (le fichier physics.js reste inchangé, constantes STIFFNESS=280/DAMPING=33 non retouchées). Remplace le tween Framer Motion fixe dans `SpatialHub.jsx` (un ressort par nœud) et `Roadmap.js` (un ressort par étape). `reduced` → `jump()` instantané, mais le callback `onSettle` (retour audio/haptique) est quand même appelé — l'accessibilité ne supprime que le mouvement visuel, jamais le retour non-visuel.
- **`SpatialHub.jsx`** — restructuré en `SpatialNode` (un composant par nœud, chacun avec son propre `useDepthPhysics`, puisqu'un hook ne peut pas être appelé par itération dans `.map()` du parent). Cadence réelle trackée sur chaque ArrowLeft/Right (`cadence.js`) ; celle-ci alimente le throttle propre à `audio.js` (`getCadenceState`). Audio/haptique réels tirés sur des événements réels seulement : `NAV_MOVE` (déplacement réel), `FOCUS_LOCK` (le ressort du nœud focalisé se stabilise réellement — jamais au montage), `CONFIRM` (activation réelle), `BLOCKED` (bord du rail atteint, ou activation d'un nœud verrouillé/inéligible). `ENTER_DEPTH`/`RETURN_DEPTH`/`CONTEXT_OPEN`/`CONTEXT_CLOSE` restent non utilisés ici — ils appartiennent aux transitions de route (`RouteTransition.jsx`/`topology.js`), jamais forcés à un sens qu'ils n'ont pas dans ce rail.
- **`lib/usePedagogicalGraph.js`** — ajout d'un refetch réel sur `window.focus` + une fonction `refetch` exposée. Nécessaire pour que le ressort ait une vraie raison de bouger : la distance pédagogique est stable *à l'intérieur* d'un montage tant que rien de réel ne change côté serveur (comportement correct — la distance reflète l'intention réelle, pas le parcours clavier de l'apprenant). Sans un déclencheur réel de re-fetch, `physics.js` n'aurait jamais eu de nouveau `target` à atteindre après le premier rendu, et son intégration serait restée strictement inerte. Revenir sur l'onglet est le déclencheur honnête choisi (une progression réelle peut avoir eu lieu ailleurs pendant l'absence).
- **`pages/Roadmap.js`** — `StageDepthCard` (nouveau) utilise `useDepthPhysics` au lieu du tween fixe, même moteur que SpatialHub.

**Preuve empirique du retarget réel** (backend `MOCK_DB=1`, utilisateur réel onboardé sur KOR) : un deuxième appel réel à `/user/learning-path` (intercepté uniquement pour fournir une deuxième valeur réelle et déterministe de `next_action` — méthode divulguée, pas un flux CI qui fabrique une fausse UI) a été servi après un déclenchement réel de l'événement `window.focus`. Résultat mesuré sur 40 frames : le nœud `aria-current="true"` passe réellement de `spatial-hub-node-formation-KOR-01` à `spatial-hub-node-formation-KOR-02`, avec **14 positions X distinctes** entre les deux (282px → 318px) — un vrai déplacement multi-frame du ressort, jamais un saut instantané. Captures : `04b_dashboard_real_intention_kor01.png` (avant) et `04c_dashboard_after_real_retarget.png` (après, KOR-02 devenu l'intention réelle). `04d_dashboard_rail_edge_blocked.png` prouve que 50 ArrowRight consécutifs atteignent réellement le bout du rail sans crash (chemin BLOCKED).

Vérification technique répétée après correction : Jest 147/147, ESLint propre, build production OK, Playwright e2e 73/73 (flags OFF, zéro régression). Backend non touché par cette correction.

**Fichiers ajoutés/modifiés par cette correction** : nouveau `frontend/src/lib/useDepthPhysics.js` ; modifiés `frontend/src/components/SpatialHub.jsx`, `frontend/src/pages/Roadmap.js`, `frontend/src/lib/usePedagogicalGraph.js`.

Ce que cette correction ne change pas : la doctrine, le graphe pédagogique (`pedagogicalGraph.js`, inchangé), les gates de sortie du §0 — toujours honorés, désormais avec le niveau de moteur réellement attendu.

## 0. Mandat reçu, reproduit intégralement

> Rail 3 — Finir Spatial Learning
> * Ne pas refaire Spatial.
> * Reprendre l'implémentation existante.
> * Connecter Spatial au vrai graphe pédagogique : intention utilisateur, proximité des contenus, progression, missions, preuves, recommandations.
> * Conserver la doctrine déjà fixée : l'espace se réorganise autour de l'intention, le savoir avance vers toi à mesure que tu avances vers lui.
> * Gate de sortie : Spatial n'est plus une couche visuelle indépendante ; il représente réellement l'état pédagogique de l'apprenant.
>
> Doctrine obligatoire : CVLN_ACADEMY = SPATIAL_LEARNING ; le mouvement n'est pas décoratif ; la position représente la relation avec l'apprenant ; l'espace se réorganise autour de l'intention ; le savoir avance vers l'utilisateur à mesure qu'il avance vers lui ; calme par défaut, vivant à l'interaction ; continuité plutôt que rupture ; un seul parcours utilisateur.
>
> Spatial ne doit jamais créer une seconde logique de progression parallèle.
> Gate de sortie : l'espace réagit aux vraies données de progression, d'intention, de missions et de compétences.

Ce rapport démontre, point par point, comment chaque clause a été honorée — et où j'ai délibérément arrêté le périmètre, avec la raison.

## 1. Ce qui n'a **pas** été refait

Rail 3 n'ajoute **aucune** nouvelle formule de physique, de caméra ou d'attention. Tout le calcul de profondeur vient, sans modification, de `frontend/src/lib/spatial/attention.js` (`ATTENTION_TIERS`, `attentionWeight(distance) = 1/(1+distance²·0.55)`, `attentionTier()`, `computeDepthStyle(distance, {mobile})`) — écrit et testé lors du chantier W-FUNNEL-1, avant ce Rail. Aucune ligne de ce fichier n'a changé.

Le seul code nouveau est une **couche de dérivation pure** : elle prend les vraies réponses API et calcule, pour chaque élément réel, un seul nombre — `distance` — qu'elle transmet tel quel à `computeDepthStyle`. Rien d'autre.

## 2. Le graphe pédagogique — `frontend/src/lib/pedagogicalGraph.js`

Nouveau fichier, ~140 lignes, fonctions pures, testées (`pedagogicalGraph.test.js`, 18 tests). Aucun état React, aucun effet de bord.

Entrées réelles consommées (jamais inventées, jamais recalculées côté client) :
- `GET /user/learning-path` → `own_pole`, `other_poles`, `next_action` (chaque formation porte `code`, `name`, `pole`, `pole_color`, `progress_pct`, `is_unlocked`, `is_recommended` — champs backend réels, voir `backend/api/learning.py:255-329`).
- `GET /missions` → champ `eligible` du Rail 2 (défaut `true` si absent, exactement le même comportement rétro-compatible que Rail 2 lui-même).
- `GET /badges/mine`, `GET /skills/mine`, `GET /qualifications/mine` → preuves (`evidence`).

Convention de distance (`GRAPH_DISTANCE`, entiers croissants, jamais arbitraires) :

| Distance | Signification réelle |
|---|---|
| `INTENTION = 0` | la formation/mission qui EST `next_action`, ou une mission urgente/vedette éligible |
| `OWN_POLE_ACTIVE = 1` | recommandée, pôle propre, non terminée |
| `OWN_POLE_LOCKED = 1` | mission éligible non-vedette |
| `OWN_POLE_COMPLETE = 2` | recommandée et déjà à 100% |
| `OTHER_POLE_UNLOCKED = 2` | autre pôle, débloquée, non recommandée |
| `OTHER_POLE_LOCKED = 3` | autre pôle verrouillée, ou mission non-éligible |

Chaque distance est **justifiée par un champ serveur réel et divulgué** — jamais une position de mise en page choisie à la main. C'est la garantie structurelle contre « une seconde logique de progression parallèle » : il n'existe qu'une seule source de vérité (le backend), et une seule fonction de dérivation (`buildPedagogicalGraph`), testée explicitement par un bloc dédié « never a second progression logic » dans `pedagogicalGraph.test.js`.

## 3. La preuve visible — `frontend/src/components/SpatialHub.jsx`

Nouveau composant (~155 lignes) : un rail horizontal combinant `formationNodes` + `missionNodes`, trié par distance réelle, chaque carte stylée via `computeDepthStyle(item.distance)` (formules inchangées). L'élément à distance 0 (l'intention réelle de l'utilisateur) est visuellement le plus grand, le plus net, le plus proche ; chaque autre élément recule exactement selon sa distance réelle.

Monté dans `Dashboard.js`, à la place — jamais en plus — de l'ancien bandeau statique « Next Action » : la doctrine interdit deux surfaces concurrentes « où aller ensuite ». Sous flag OFF, `Dashboard.js` est strictement inchangé (mêmes variables d'état, même effet `Promise.all`, même JSX rendu).

Accessibilité (héritée, non réinventée) : ordre du DOM = ordre de tabulation réel ; roving tabindex avec `nodeRefs` + `.focus()` DOM réel (pas seulement `tabIndex` en mémoire) ; `prefers-reduced-motion` conserve la hiérarchie opacité/saturation/échelle et supprime seulement `translateZ`/`rotateY`/grands déplacements.

## 4. La continuité — `frontend/src/pages/Roadmap.js`

`Roadmap.js` utilisait déjà `FocusFieldItem` (cible/secondaire binaire). Sous flag ON, chaque étape du rail utilise désormais `distance = i - currentIdx` (dérivé du même champ réel `user.stade` que le chemin existant utilisait déjà) → `computeDepthStyle(distance)` → un modèle de profondeur **continu** au lieu de binaire : l'étape courante est pleine échelle, les autres reculent progressivement selon leur distance réelle au stade actuel. Aucune nouvelle source de vérité — `currentIdx` reste l'unique signal, partagé par les deux branches (flag ON/OFF). Le corps de carte (`StageCardBody`) est extrait une fois et partagé pour garantir que le contenu ne diverge jamais entre les deux traitements, seul le mouvement diffère.

## 5. La signature environnementale — `frontend/src/components/AcademyBackdrop.jsx`

Nouveau composant monté dans `Layout.js` : un halo de fond dont la teinte est la vraie couleur de pôle (`pole_color`) de l'intention réelle de l'apprenant — jamais une couleur choisie par page. `pointer-events-none`, z-index bas, ne rend rien tant que `SPATIAL_ENVIRONMENT` est OFF.

**Limite divulguée, non contournée en silence** : l'objectif de `ACADEMY_SPATIAL_END_TO_END_ARCHITECTURE.md` (`ENVIRONMENT_RESET_PER_ROUTE = FORBIDDEN`) demande un fond qui survit aux changements de route sans jamais se réinitialiser. Cela exige de promouvoir `Layout` en route de disposition React Router (`<Outlet/>`) — une vraie restructuration de `App.js`. L'autorisation H1 de cette passe impose que « `<Routes>`... reste byte-identique » ; je n'ai donc **pas** fait cette restructuration unilatéralement. `AcademyBackdrop` est réellement data-driven et correct pour chaque page, mais se réétablit à chaque montage de `Layout` plutôt que de persister sans coupure entre navigations. Documenté dans le docstring du composant, avec la même posture que les deux items REPLACE-BLOCKED du plan H1 (nécessite une autorisation séparée).

## 6. Preuve de sortie de gate

**Gate 1 — « Spatial n'est plus une couche visuelle indépendante » :** `SpatialHub` et le rail continu de `Roadmap.js` ne contiennent aucune donnée inventée ; chaque position vient de `pedagogicalGraph.js`, qui lui-même ne lit que des réponses API réelles. Vérifié par les 18 tests de `pedagogicalGraph.test.js`, dont un test dédié : « never invents a `progress_pct` different from the server's own value ».

**Gate 2 — « L'espace réagit aux vraies données de progression, d'intention, de missions et de compétences » :** démontré en direct (voir captures ci-dessous), backend redémarré avec `MOCK_DB=1` (import KOR/KLT réel), un utilisateur de démonstration réel enregistré + onboardé via les vraies routes API, flags `SPATIAL_HUB_ENABLED`/`SPATIAL_ENVIRONMENT` activés :

1. `rail3_01_dashboard_spatial_hub.png` — le Dashboard réorganise réellement son rail autour de l'intention réelle (KOR-01 le plus grand/net/proche), missions et autres formations reculant selon un vrai dégradé, l'une d'elles partiellement coupée au bord du rail.
2. `rail3_02_roadmap_depth.png` — le modèle de profondeur continu de Roadmap varie réellement opacité/échelle selon la distance réelle à `user.stade` (Graine pleine échelle, Pousse/Racine/Branches progressivement plus petites/atténuées) — désormais continu, plus binaire.
3. `rail3_03_dashboard_keyboard_nav.png` — la navigation clavier ArrowRight déplace réellement un anneau de focus visible via un vrai `.focus()` DOM, pas seulement un état interne.

## 7. Vérification technique complète

- `yarn build` (production) : compilé avec succès, +1.2 kB gzip.
- `yarn test` (Jest) : **147/147** tests passés (18 nouveaux pour `pedagogicalGraph.js`, reste inchangé).
- ESLint (repo entier) : propre, y compris `jsx-a11y/no-noninteractive-element-interactions` et `react-hooks/exhaustive-deps`.
- Playwright e2e : **73/73** passés, flags OFF — zéro régression sur `roadmap-progression.spec.js`, `formations-discovery.spec.js` et le reste de la suite (les attributs `data-focus-role` que ces specs vérifient n'existent que dans la branche flag-OFF, inchangée).
- Backend : `pytest` — **131 passed** (backend non touché cette passe ; relancé en contrôle final).
- Smoke test live flags ON : ci-dessus.

## 8. Fichiers touchés

Modifiés (livraison initiale) : `frontend/.env.example`, `frontend/src/components/Layout.js`, `frontend/src/lib/featureFlags.js`, `frontend/src/lib/featureFlags.test.js`, `frontend/src/pages/Dashboard.js`, `frontend/src/pages/Roadmap.js`.

Nouveaux (livraison initiale) : `frontend/src/components/AcademyBackdrop.jsx`, `frontend/src/components/SpatialHub.jsx`, `frontend/src/lib/pedagogicalGraph.js`, `frontend/src/lib/pedagogicalGraph.test.js`, `frontend/src/lib/usePedagogicalGraph.js`.

Modifiés/nouveaux par la correction du §11 : nouveau `frontend/src/lib/useDepthPhysics.js` ; modifiés `frontend/src/components/SpatialHub.jsx`, `frontend/src/pages/Roadmap.js`, `frontend/src/lib/usePedagogicalGraph.js`.

Backend : aucun fichier touché, ni la livraison initiale ni la correction.

## 9. Explicitement hors périmètre cette passe (décision de scope assumée, pas un oubli)

Conformément au tableau de verdicts REUSE/EXTEND/WRAP/REPLACE-BLOCKED de `docs/SPATIAL_H1_INTEGRATION_PLAN.md`, cette passe s'est délibérément concentrée sur les deux items les moins risqués et les mieux validés (Dashboard, Roadmap) — désormais avec le moteur complet (`physics.js`/`cadence.js`/`audio.js`/`haptics.js`, §11). Restent non traités :

- `Missions.js`, `Badges.js`, `FrekProfile.js`, `ModuleJourney.js` — non convertis au traitement par paliers d'attention, donc n'ont pas non plus le moteur physics/cadence/audio/haptics.
- Swipe mobile / snap à la vélocité — non câblé.
- Transitions FLIP carte-formation → module — non étendues.
- Assets visuels d'environnement réels (imagerie) — non commandés ; le fond reste un dégradé de couleur de pôle.
- Persistance vraiment inter-route du fond (sans jamais se remonter) — nécessite une restructuration `App.js` en routes de disposition, hors autorisation de cette passe (voir §5).
- `topology.js`/`routeTopologyMap.js` restent utilisés uniquement par `RouteTransition.jsx` (câblé lors d'une passe antérieure) — les événements audio `ENTER_DEPTH`/`RETURN_DEPTH`/`CONTEXT_OPEN`/`CONTEXT_CLOSE` n'ont pas de point d'ancrage réel dans ce rail et restent non déclenchés.

Ces items restent dans le plan H1 pour une prochaine passe explicitement autorisée.

## 10. Note hors-scope : `context7`

Le serveur MCP `context7` (ajouté lors d'une passe précédente) nécessite une autorisation OAuth interactive que cette session non-interactive ne peut pas effectuer. L'utilisateur doit l'autoriser via `claude mcp` ou `/mcp` dans une session interactive — aucun code/jeton/URL de callback ne doit être demandé ici.
