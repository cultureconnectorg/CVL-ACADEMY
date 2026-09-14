# Audit performance & réseau — septembre 2026

Répond à la commande du Founder : (1) réduire le coût spatial sans enlever
l'expérience, (2) supprimer les blocages réseau répétitifs après auth,
(3) garder les vérifications juridiques réellement sûres, (4) mesurer les
appels Dashboard/API/Mongo avant d'optimiser à l'aveugle.

Méthode : chaque chiffre ci-dessous est mesuré dans ce sandbox (Playwright,
CPU throttling réel, comptage réseau réel) ou lu directement dans le code
(requêtes Mongo, index). Aucun chiffre n'est estimé sans le dire explicitement.

---

## 1. Coût spatial (WebGL) — réduit sans changer l'expérience visible

Déjà livré ce cycle (`f7f53e6`) : rendu idle-stop + antialiasing/DPR/
anisotropie conditionnés au tier, mesuré ~19-26fps/100% frames saccadées
→ ~60fps/0-2% dans ce sandbox (SwiftShader, donc chiffres absolus non
représentatifs d'un vrai GPU mobile — seule la comparaison relative
avant/après est fiable).

**Nouveau cette session** : chaque photo de fond (`frontend/public/spatial/
backgrounds/*.webp`, ~1570px de large, ~200-320KB) était téléchargée
identique quel que soit l'écran. Un mobile de 390px de large n'a aucun
usage pour un fichier 1570px — le navigateur/GPU le sous-échantillonne de
toute façon. Génération d'une variante `-mobile.webp` (900px de large,
même pipeline WebP q78) pour les 12 photos :

| | Poids desktop | Poids mobile | Ratio |
|---|---|---|---|
| Total (12 photos) | 3466 KB | 1305 KB | 38% |

Sélection automatique par largeur d'écran (`webglSceneMap.js`,
`backgroundForNode(node, { viewportWidth })`, seuil 900px) — capturée une
fois au montage comme le tier de qualité, pas de re-fetch au resize/rotate.
Aucun changement visuel sur desktop ; sur mobile, l'image affichée est déjà
sous-échantillonnée par l'écran donc pas de perte perçue. Test unitaire
dédié (`webglSceneMap.test.js`, 7/7) vérifie la sélection et l'existence
réelle de chaque fichier `-mobile` sur disque.

## 2 & 3. Blocages réseau répétitifs après auth — corrigés sans affaiblir la sécurité juridique

**Constat.** `LegalGuard` (`App.js`) est monté à l'intérieur de chaque
`<Route>`. React Router démonte/remonte ce composant à chaque navigation
entre pages protégées — donc chaque clic relançait `GET /legal/requirements`
et bloquait le rendu (`return null` pendant que `state === "checking"`)
avant que la page suivante ne s'affiche.

**Mesure réelle** (script Playwright, 11 navigations SPA successives sur un
compte déjà "accepted", serveur mocké) :

| | Avant (`main` @ `f7f53e6`) | Après |
|---|---|---|
| Appels `GET /legal/requirements` pour 11 navigations | **17** | **1** |

**Correctif** (`frontend/src/lib/legalGateCache.js`, nouveau) : cache de
session avec TTL de 5 minutes, dédoublonnage des appels concurrents, jamais
d'échec mis en cache. Le serveur reste la seule source de vérité — le
prochain contrôle après TTL repart en réseau, et toute action qui peut
réellement changer la réponse force un contrôle frais immédiat au lieu de
supposer le nouvel état :
- `POST /legal/accept` réussi → `invalidateLegalAcceptance()` avant la
  redirection (`LegalAcceptance.jsx`).
- `logout()` → `invalidateLegalAcceptance()` (`auth.jsx`) — un autre
  compte sur le même onglet n'hérite jamais du verdict précédent.

Un échec (503, 401, réseau) n'est **jamais** mis en cache comme "accepté" —
même comportement qu'avant, vérifié par le test e2e existant
`legal gate backend failure stays technical instead of faking legal
acceptance` (toujours vert). 6 nouveaux tests unitaires
(`legalGateCache.test.js`) couvrent : dédoublonnage, isolation par
utilisateur, non-cache des échecs, invalidation.

**Dashboard.js** avait le même patron à plus petite échelle : `await
refreshMe()` était attendu en séquence *avant* de lancer les 5 appels
`Promise.all` du dashboard, ajoutant un aller-retour réseau complet inutile
à chaque chargement (aucun des 5 appels ne dépend de l'objet `user` frais —
ils sont tous scopés côté serveur par le token). Les 6 appels partent
maintenant ensemble.

## 4. Mesure Dashboard/API/Mongo — avant d'optimiser à l'aveugle

**Limite du sandbox** : pas de `mongod` disponible ici — impossible de
mesurer une vraie latence Mongo en millisecondes dans cet environnement.
Ce qui suit est une lecture directe du code (nombre de requêtes, présence
d'index), pas un chiffre chronométré — l'écart avec un vrai `PROD_RUNTIME`
doit être vérifié en staging avant toute décision de capacité.

**Les 5 appels du Dashboard, un par un** :

| Endpoint | Requêtes Mongo | Index `user_id` ? |
|---|---|---|
| `GET /frek/profile` | 4 (`frek_signals`, `progress`, `user_badges`, `refresh_tokens`) — **séquentielles**, indépendantes | ✅ (toutes) |
| `GET /missions/mine` | 1 | ✅ |
| `GET /badges/mine` | 2 (`user_badges` puis `badges` par `$in`) | ✅ |
| `GET /progression/summary` | 2 (`count_documents` + `aggregate` **sur toute la collection `formations`**) | ✅ pour le count ; l'aggregate n'a pas besoin d'index (scan complet mais petite collection) |
| `GET /user/learning-path` | 2 (`formations` complet + `progress` complet de l'utilisateur), puis calcul Python O(formations) | ✅ |

Tous les champs `user_id` réellement filtrés sont indexés
(`infra_indexes.py`) — pas de scan complet sur une grande collection par
utilisateur. Le point faible n'est donc **pas** l'absence d'index, mais deux
formes de travail répété qui ne servent à rien à chaque chargement :

1. **`/frek/profile` fait 4 requêtes Mongo l'une après l'autre alors
   qu'elles sont indépendantes** (même `user_id`, collections différentes,
   aucune ne dépend du résultat d'une autre) — candidates à
   `asyncio.gather`, comme `Promise.all` côté frontend.
2. **`/progression/summary` recalcule le total de modules du catalogue
   entier (`aggregate` sur toute la collection `formations`) à chaque
   requête, pour chaque utilisateur** — ce total ne change que quand le
   contenu pédagogique change, pas à chaque connexion. Candidat à un cache
   (même en mémoire, invalidé à la publication d'une formation).

**Je n'ai pas touché ces deux points.** Ce sont des changements côté Mongo
(concurrence de requêtes, cache) — exactement ce que le Founder a demandé
de mesurer avant de toucher, pas de deviner. Sans `mongod` ici pour
chiffrer le gain réel, les documenter plutôt que les appliquer à l'aveugle
est le choix cohérent avec la demande. Recommandation pour un prochain
cycle : rejouer cette mesure en staging avec Mongo réel (latence par
requête, `explain()` sur l'aggregate) avant de décider si ça vaut le coût
d'implémentation.

## Constat annexe (hors périmètre de cette commande, signalé pour mémoire)

9 tests e2e spatiaux existants (`spatial-camera-follow.spec.js`,
`spatial-context-environment.spec.js`, `spatial-module-dock.spec.js`,
`spatial-roadmap-rail.spec.js`) échouent déjà sur `main` avant tout
changement de cette session — vérifié en les rejouant sur `f7f53e6` sans
aucune modification. Cause probable : ces tests cherchent
`getByTestId("spatial-background")` (le monde CSS), mais depuis
l'activation du monde WebGL sur Module/Roadmap, Chromium headless (rendu
logiciel SwiftShader) est éligible au WebGL et rend
`spatial-webgl-background` à la place. Pré-existant, non introduit par ce
cycle, aucune correction appliquée ici — signalé pour un prochain cycle.

## Vérification

- Frontend : `yarn test` → 214/215 (1 échec pré-existant sur `main`,
  `publicRouteMatrix.test.js`, confirmé sans rapport avec ce cycle).
- `yarn build` : succès.
- E2E ciblés (`page-route-wiring`, `auth-guards`, `routing`,
  `keyboard-focus`) : 42/42.
- Nouveaux tests : `legalGateCache.test.js` (6/6), `webglSceneMap.test.js`
  (7/7).
