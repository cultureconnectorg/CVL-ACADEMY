# Rail 3 — Finir Spatial Learning : rapport de câblage

**Statut : DONE (scope volontairement resserré, écarts documentés ci-dessous).**
**Date : 2026-09-07.**
**Flags : `REACT_APP_ACADEMY_SPATIAL_HUB_ENABLED`, `REACT_APP_ACADEMY_SPATIAL_ENVIRONMENT` — défaut `false` tous les deux. Aucun comportement existant ne change sans action déployeur explicite.**

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

Modifiés : `frontend/.env.example`, `frontend/src/components/Layout.js`, `frontend/src/lib/featureFlags.js`, `frontend/src/lib/featureFlags.test.js`, `frontend/src/pages/Dashboard.js`, `frontend/src/pages/Roadmap.js`.

Nouveaux : `frontend/src/components/AcademyBackdrop.jsx`, `frontend/src/components/SpatialHub.jsx`, `frontend/src/lib/pedagogicalGraph.js`, `frontend/src/lib/pedagogicalGraph.test.js`, `frontend/src/lib/usePedagogicalGraph.js`.

Backend : aucun fichier touché cette passe.

## 9. Explicitement hors périmètre cette passe (décision de scope assumée, pas un oubli)

Conformément au tableau de verdicts REUSE/EXTEND/WRAP/REPLACE-BLOCKED de `docs/SPATIAL_H1_INTEGRATION_PLAN.md`, cette passe s'est délibérément concentrée sur les deux items les moins risqués et les mieux validés (Dashboard, Roadmap). Restent non traités :

- `Missions.js`, `Badges.js`, `FrekProfile.js`, `ModuleJourney.js` — non convertis au traitement par paliers d'attention.
- Swipe mobile / snap à la vélocité — non câblé.
- Transitions FLIP carte-formation → module — non étendues.
- Assets visuels d'environnement réels (imagerie) — non commandés ; le fond reste un dégradé de couleur de pôle.
- Persistance vraiment inter-route du fond (sans jamais se remonter) — nécessite une restructuration `App.js` en routes de disposition, hors autorisation de cette passe (voir §5).

Ces items restent dans le plan H1 pour une prochaine passe explicitement autorisée.

## 10. Note hors-scope : `context7`

Le serveur MCP `context7` (ajouté lors d'une passe précédente) nécessite une autorisation OAuth interactive que cette session non-interactive ne peut pas effectuer. L'utilisateur doit l'autoriser via `claude mcp` ou `/mcp` dans une session interactive — aucun code/jeton/URL de callback ne doit être demandé ici.
