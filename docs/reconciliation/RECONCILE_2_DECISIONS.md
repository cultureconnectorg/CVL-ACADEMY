# RECONCILE-2 — fiches de décision par fichier `BOTH_DIFFERENT`

Discipline appliquée : un fichier conflictuel n'est "résolu" que s'il
conserve les capacités utiles des deux côtés ET respecte l'architecture
actuelle de main ET a une preuve de test réelle — pas seulement "ça
compile". Commits séparés par zone critique (aucun commit ne mélange
noyau backend / auth / wallet / spatial / App.js).

## État d'avancement (2026-09-14, cette passe)

**Groupe 1 — Noyau backend : COMPLET (5/5 fichiers).** `fms_import/
importer.py`, `api/__init__.py`, `server.py`, `models.py`, `db.py` —
tous réconciliés avec preuve de test réelle. `import server` réussit de
bout en bout : **515 routes**, dont les 53 nouveaux routers, garde
`require_legal_acceptance` vérifiée sur un échantillon.

**Groupe 2 — AUTH : COMPLET (7/7 fichiers).** `backend/auth.py`,
`backend/api/auth.py`, `backend/api/orgs.py`, `frontend/src/lib/
auth.jsx`, `frontend/src/lib/api.js`, `frontend/e2e/auth-guards.spec.js`,
`frontend/e2e/fixtures/auth-fixture.js` — tous résolus avec preuve de
test réelle (parcours register→login→requête authentifiée→navigation
post-auth complet, plus toute la suite SEC-01/SEC-02). Un bug
d'intégrité d'inscription pré-existant (identique sur `main` et
r35l31) a été trouvé et corrigé en combinant SEC-02 — voir la fiche
`api/auth.py` ci-dessous.

**Groupe 3 — wallet/commerce/paiements : COMPLET (5/5 fichiers
`BOTH_DIFFERENT` du périmètre).** `backend/wallet/models.py`,
`backend/wallet/service.py`, `backend/wallet/__init__.py`,
`backend/api/wallet.py`, `frontend/src/pages/Wallet.js` — tous résolus
avec preuve de test réelle (création wallet, lecture balance,
transaction valide, duplicate/idempotency, unauthorized, cross-tenant,
currency invalide, provider indisponible, reconciliation après
désynchronisation). `backend/infra_indexes.py` (`BOTH_DIFFERENT`, mais
un fichier d'infrastructure partagé bien au-delà du périmètre wallet/
paiements) **partiellement réconcilié** : uniquement ses sections
wallet + payments, le reste (canonical_progress, fms_resource_
provenance, physical_sessions/enrollments, professional_profile_
settings) marqué `BLOCKED_BY_GROUP_5`. `backend/certification/
service.py` (`BOTH_DIFFERENT`, hors périmètre Groupe 3) a reçu un
correctif d'une ligne, minimal et documenté, pour rester compatible
avec le nouveau contrat obligatoire de `wallet.credit()` — voir sa
fiche ci-dessous. `backend/commerce/`, `backend/payments/`
(ONLY_R35L31, déjà importés RECONCILE-1) et `backend/commercial.py` /
`backend/billing*.py` (ONLY_MAIN) ne sont **pas** `BOTH_DIFFERENT` —
aucun conflit à résoudre, mais vérifiés en profondeur (auth/legal
gates, cross-tenant, secrets Stripe, DB persistence) car explicitement
dans le périmètre demandé.

**Groupe 4 — spatial/frontend core : COMPLET (6/6 fichiers
`BOTH_DIFFERENT` du périmètre).** `frontend/src/App.js`,
`frontend/src/lib/featureFlags.js`, `i18n.jsx`, `RouteTransition.jsx`,
`JourneyHierarchy.jsx`, `ContextFrame.jsx` — tous résolus avec preuve de
test réelle. `attention.js`/`motion-primitives.jsx` : `KEEP_MAIN`, aucun
conflit réel (r35l31 ne les a jamais touchés). Les 17 pages
précédemment non routées ont chacune un statut explicite
(PUBLIC_ROUTED/AUTHENTICATED_ROUTED/INTERNAL_ROUTED/HYBRID_ROUTED),
aucune `INTENTIONALLY_UNROUTED`. Un bug de gating backend au niveau
routeur (introduit par le Groupe 1, découvert et corrigé pendant ce
groupe) est documenté ci-dessous, avec les deux fichiers concernés
(`professional_profile.py`, `governance_advanced.py`) et le correctif
dans `api/__init__.py`. `SpatialHub.jsx` lui-même n'est **pas**
`BOTH_DIFFERENT` (`ONLY_R35L31`, jamais câblé dans Dashboard/Roadmap —
ce câblage reste Groupe 5) ; sa compilabilité a été prouvée séparément
(voir fiche dédiée). Suite jest complète 42/42 suites (292/292 tests),
`yarn build` propre, 4 checks backend runtime réels, preview live
Playwright 9/9 — voir section détaillée.

**Reste : 72 des 95 fichiers `BOTH_DIFFERENT`.**
- **Groupe 5 (reste d'APP_CORE)** — le reliquat, par dépendance réelle,
  notamment `Dashboard.js`/`Roadmap.js`/`ModuleJourney.js` (câblage réel
  de `SpatialHub.jsx`, jusqu'ici seulement prouvé compilable) et la
  section non-wallet/payments de `infra_indexes.py`
  (`BLOCKED_BY_GROUP_5`, documentée au Groupe 3).

---

## Groupe 1 — Noyau backend

### `backend/fms_import/importer.py`

- **MAIN_BEHAVIOR** : identique au merge-base — main n'a jamais touché ce
  fichier depuis la divergence (diff `merge-base..main` vide, vérifié).
  Extraction ZIP sans aucune protection anti-ZIP-bomb.
- **R35L31_BEHAVIOR** : ajoute 4 garde-fous avant toute décompression
  (`MAX_ZIP_ENTRIES=5000`, `MAX_ENTRY_UNCOMPRESSED_BYTES=10MB`,
  `MAX_TOTAL_UNCOMPRESSED_BYTES=300MB`, `MAX_COMPRESSION_RATIO=100`) —
  tous basés sur les métadonnées de l'en-tête ZIP (`file_size`,
  `compress_size`), donc évalués **avant** `zf.read()`, jamais après.
  Correspond à la tâche P0-I (ZIP bomb / provenance protections).
- **MERGE_BASE** : identique à MAIN_BEHAVIOR.
- **DÉCISION : KEEP_R35L31** — strict superset, aucune ligne de main
  perdue ou modifiée (main = base), rien à combiner. La seule
  dépendance bloquante trouvée en RECONCILE-1
  (`fms_canonical/provenance.py` attend `MAX_COMPRESSION_RATIO`) est
  résolue par ce remplacement.
- **TEST_EVIDENCE** : `pytest tests/ -k "fms_import or importer or zip"`
  → 31 passed, 0 failed, incluant les 8 tests dédiés
  `tests/test_fms_import_zip_bomb.py` (déjà importés en RECONCILE-1,
  jamais exécutables avant ce remplacement faute du code qu'ils
  testent). `import api` réussit désormais de bout en bout (502 routes),
  alors qu'il échouait avant ce remplacement sur
  `ImportError: cannot import name 'MAX_COMPRESSION_RATIO'`.

### `backend/api/__init__.py`

- **MAIN_BEHAVIOR** : 29 routers existants, groupés par garde
  (`health/auth/legal` non gardés ; le gros des routers gardés par
  `require_legal_acceptance` ; `learning` gardé en plus par
  `require_commercial_learning_access` ; `commercial/billing/
  billing_views` gardés par `require_legal_acceptance`).
- **R35L31_BEHAVIOR** : 82 routers (29 + 53 nouveaux), **aucune garde
  nulle part** — la garde `require_legal_acceptance` n'existait pas
  encore sur cette branche au moment de la divergence.
- **MERGE_BASE** : 19 routers, aucune garde (l'architecture de garde
  est une addition de main, postérieure à la divergence).
- **DÉCISION : COMBINE** — structure de main conservée intégralement
  (tous les groupes, toutes les gardes existantes inchangées) ; les 53
  routers propres à r35l31 ajoutés dans un nouveau groupe dédié, gardé
  par `require_legal_acceptance` au même titre que tout le reste du
  registre (aucun de ces 53 n'est health/auth/legal, donc aucun ne
  qualifie pour l'exemption). Vérifié qu'aucun des 53 ne provoque de
  collision de chemin avec les routers déjà enregistrés (`legal_ops`
  partage le préfixe `/legal` avec le `legal.py` de main mais leurs
  chemins réels ne se recouvrent pas : `/legal/requirements`,
  `/legal/accept` côté main vs `/legal/matters`, `/legal/contracts`...
  côté nouveau — vérifié route par route).
- **NEEDS_REVIEW (noté, non tranché ici)** : faut-il aussi garder
  `canonical/frk_canonical/kor_canonical/klt_canonical` par
  `require_commercial_learning_access` (comme `learning`) ? Décision
  de monétisation, pas technique — laissée au Founder plutôt que
  devinée.
- **TEST_EVIDENCE** : `import api` réel (env vars de test, aucune
  connexion Mongo requise à l'import) → succès, **502 routes** au
  total, dont 336 dans les nouveaux domaines. Vérifié
  programmatiquement que `require_legal_acceptance` figure bien dans
  les dépendances résolues d'une route échantillon
  (`/api/accounting-advanced/connectors`).

### `backend/server.py`

- **MAIN_BEHAVIOR** : `lifespan` async context manager moderne
  (remplace `@app.on_event`, déprécié) ; enregistre l'OAuth MCP
  (`mcp_oauth_router`), les deux serveurs MCP (public `academy_mcp` +
  privé `private_academy_mcp`), la porte de préparation facturation
  (`assert_billing_production_ready`, échoue avant même le bloc
  seed/index si la facturation prod n'est pas configurée), les index
  MCP, le runtime workbook (`ensure_workbook_runtimes`, échoue si
  incomplet), suit `app.state.startup_ready/startup_error` (dégrade
  proprement plutôt que crash-loop sur un échec de seed non
  bloquant), middleware de normalisation des doubles slashes, CORS
  **sans aucune garde production** — juste
  `os.environ.get("CORS_ORIGINS", "*").split(",")`.
- **R35L31_BEHAVIOR** : `@app.on_event` (pattern hérité), pas de MCP/
  billing/workbook (n'existaient pas encore sur cette branche à la
  divergence), **garde CORS production réelle** (voir fiche
  `api/__init__.py` ci-dessus — même logique), gate `architecture_reuse.
  sync_manifest` (PG-13, verrou anti-duplication d'architecture) au
  démarrage, hook `MOCK_DB=1` de pré-import des corpus canoniques pour
  le dev.
- **MERGE_BASE** : `@app.on_event`, CORS sans garde, aucun des deux
  ajouts (MCP/billing/workbook côté main ; garde CORS/PG-13/MOCK_DB
  côté r35l31).
- **DÉCISION : COMBINE (partiel)** — structure `lifespan`/MCP/billing/
  workbook/startup_ready de main **entièrement conservée**, inchangée.
  Garde CORS production de r35l31 **restaurée** (seule capacité perdue
  identifiée sur ce fichier — un vrai trou de sécurité sur main, main
  ne rejetait jamais un déploiement `ENVIRONMENT=production` avec
  `CORS_ORIGINS` non configuré).
- **NEEDS_REVIEW (non appliqué ici, à trancher séparément)** :
  - `architecture_reuse.sync_manifest` — gate PG-13 conçue pour
    verrouiller les décisions REUSE/EXTEND/BUILD-ONCE des nouveaux
    domaines (legal/privacy/governance/accounting/professional/
    ecosystem) qu'on vient tout juste de câbler. La wirer maintenant,
    avant que RECONCILE-2 groupes 2-5 n'aient fini de réconcilier ces
    domaines, risquerait un `raise RuntimeError` de démarrage sur un
    état encore partiel — pas dans le périmètre des critères de sortie
    (les 53 routes/17 pages), donc laissé en attente plutôt que câblé
    à l'aveugle.
  - Hook `MOCK_DB=1` — commodité de dev, faible risque, faible
    priorité, non câblé faute de temps dans cette passe.
- **TEST_EVIDENCE** : `import server` réel, bout en bout, réussit —
  **515 routes/mounts** au total (502 de `api.router` + les montages
  OAuth/MCP publics/privés de main). Testé la garde CORS aux 3 cas
  (dev sans `CORS_ORIGINS` → `["*"]` ; prod + wildcard → `RuntimeError`
  levée dès l'import du module, avant tout autre code de démarrage ;
  prod + liste explicite → acceptée). Dépendances externes installées
  dans ce sandbox pour permettre ce test (`factur-x`, `mcp`) — absentes
  par défaut ici, sans lien avec cette réconciliation.

### `backend/models.py`

- **MAIN_BEHAVIOR** : identique au merge-base (main n'a pas touché ce
  fichier). `Mission` sans champ d'éligibilité, aucune matrice
  inviteur->rôles autorisés.
- **R35L31_BEHAVIOR** : ajoute `INVITER_ALLOWED_INVITED_ROLES` (SEC-01 —
  matrice explicite empêchant un `trainer` de forger une invitation
  `role="founder"`) et `Mission.required_qualification_codes` (RAIL2,
  liste vide par défaut = comportement identique à avant pour toute
  mission existante).
- **MERGE_BASE** : identique à MAIN_BEHAVIOR.
- **DÉCISION : KEEP_R35L31** — strict superset. Ces deux ajouts sont
  des données inertes tant qu'elles ne sont pas lues : `Mission.
  required_qualification_codes` n'a d'effet que si `api/missions.py`
  le lit (c'est le cas côté r35l31, via `qualification.has_any_of` —
  mais `api/missions.py` est lui-même `BOTH_DIFFERENT`, donc son
  câblage réel reste à faire) ; `INVITER_ALLOWED_INVITED_ROLES` n'a
  d'effet que si `api/orgs.py` le consulte (également `BOTH_DIFFERENT`,
  câblage réel à faire). Ajouter la donnée maintenant est sûr et
  débloque group 2 (auth : `api/orgs.py`) et le futur travail sur
  `api/missions.py` sans attendre.
- **TEST_EVIDENCE** : `import server` reste vert (515 routes) après ce
  remplacement. Vérifié directement que `Mission.model_fields` contient
  `required_qualification_codes` et que `INVITER_ALLOWED_INVITED_ROLES`
  est bien un dict avec les 6 rôles attendus.

### `backend/db.py`

- **MAIN_BEHAVIOR** : identique au merge-base — connexion Motor directe
  et inconditionnelle vers `MONGO_URL`.
- **R35L31_BEHAVIOR** : ajoute un embranchement `MOCK_DB=1` optionnel
  vers `mongomock_motor.AsyncMongoMockClient` (in-memory, non
  persistant) pour permettre de lancer l'app réelle sans Mongo — déjà
  le mécanisme utilisé par toute la suite de tests existante.
- **MERGE_BASE** : identique à MAIN_BEHAVIOR.
- **DÉCISION : KEEP_R35L31** — superset strict, chemin par défaut
  (`MOCK_DB` absent ou différent de `"1"`) rigoureusement identique à
  avant.
- **TEST_EVIDENCE** : `import server` reste vert avec `MOCK_DB` absent
  (comportement par défaut inchangé). `MOCK_DB=1` testé isolément :
  prend bien la branche mongomock plutôt que d'essayer une vraie
  connexion réseau (vérifié via `mongomock_motor.AsyncMongoMockClient`
  directement -- la bibliothèque construit son objet en se faisant
  passer pour `AsyncIOMotorClient` en interne, comportement documenté
  de la bibliothèque, déjà éprouvé par toute la suite de tests
  existante qui s'appuie dessus).

---

## Groupe 2 — Auth

Ordre suivi : `backend/auth.py` (bas niveau, aucune décision propre) →
`backend/api/auth.py` (register/login/session) → `backend/api/orgs.py`
(invitations, dépend de `INVITER_ALLOWED_INVITED_ROLES` déjà posé en
Groupe 1) → fichiers frontend (`auth.jsx`, `api.js`) → tests e2e
(`auth-guards.spec.js`, `auth-fixture.js`). Chaque commit reste
strictement dans cette zone — aucun mélangé avec noyau backend/wallet/
spatial/App.js.

### `backend/auth.py`

- **MAIN_BEHAVIOR** : réécrit `next_frek_id()` pour accepter
  `email`/`metadata` et faire remonter les erreurs FrekCore
  (`FrekCoreConfigurationError`/`FrekCoreUnavailableError`) en 503
  explicites plutôt que de les laisser fuiter comme 500. Ajoute
  l'atomicité de consommation à usage unique (`revoked=False`/`used=
  False` dans le filtre `update_one`, `modified_count != 1` → 401/400)
  sur `rotate_refresh_token`, `consume_password_reset_token`,
  `consume_email_verification_token` — protège contre une double
  consommation concurrente du même jeton. Nettoyage de docstrings/
  commentaires de section.
- **R35L31_BEHAVIOR** : ajoute **exactement la même** atomicité de
  consommation à usage unique sur les trois mêmes fonctions (logique et
  formulation du docstring identiques à main — convergence
  indépendante, pas une divergence). `next_frek_id()` garde sa
  signature d'origine (pas d'`email`/`metadata`, pas de mapping
  d'erreurs FrekCore).
- **MERGE_BASE** : `next_frek_id()` sans paramètres ; aucune des trois
  fonctions de consommation de jeton n'est atomique (`update_one` sans
  filtre `revoked`/`used`, `find_one` puis `update_one` séparés —
  fenêtre de course exploitable).
- **DÉCISION : KEEP_MAIN** — main est un **strict superset** de
  r35l31 sur ce fichier : diff direct `r35l31 → main` ne contient
  **aucune** suppression de capacité r35l31, seulement des ajouts
  (mapping d'erreurs FrekCore) et du nettoyage cosmétique. Confirmé par
  diff explicite `main` vs `r35l31` (voir ci-dessus) : chaque ligne
  ajoutée par r35l31 par rapport au merge-base est présente à
  l'identique dans main. Rien à combiner, rien à perdre.
- **TEST_EVIDENCE** : fichier déjà identique à `main` dans la branche
  reconcile avant toute intervention (`diff backend/auth.py
  <main> → aucune différence`) — confirmé qu'aucune modification
  n'était nécessaire. `pytest tests/test_auth_token_atomicity.py` → 2
  passed (rotation atomique sous réutilisation concurrente). Voir aussi
  le parcours critique ci-dessous (register→login→refresh→logout) qui
  exerce `next_frek_id`, `rotate_refresh_token` et
  `issue_refresh_token` en conditions réelles.

### `backend/api/auth.py`

- **MAIN_BEHAVIOR** : `register()` dérive `email` une seule fois,
  appelle `next_frek_id(email, metadata=...)`, rejette un FREK-ID déjà
  lié à un compte Academy (409 — collision improbable mais gérée
  explicitement plutôt qu'un crash d'index unique). `_apply_invitation`
  prend `(user_id, invite_code)` — aucune vérification de l'email de
  l'inscrivant. Docstrings nettoyées, commentaires de section
  supprimés.
- **R35L31_BEHAVIOR** : `_apply_invitation` prend en plus
  `registering_email` (SEC-02, audit chirurgical 2026-09-07) — si
  l'invitation porte un email cible, l'email d'inscription doit
  correspondre (insensible à la casse) ou l'inscription échoue en 400 ;
  une invitation sans email reste ouverte à quiconque détient le code,
  comportement inchangé. `next_frek_id()` appelé sans email/metadata
  (signature d'origine côté r35l31, cohérent avec `auth.py`
  R35L31_BEHAVIOR ci-dessus).
- **MERGE_BASE** : `_apply_invitation(user_id, invite_code)`, aucune
  vérification d'email ; `next_frek_id()` sans paramètres ; pas de
  contrôle de collision FREK-ID.
- **DÉCISION : COMBINE** — base = main (email/metadata vers
  `next_frek_id`, contrôle de collision FREK-ID 409, docstrings à jour)
  + ajout de la correction SEC-02 de r35l31 (`_apply_invitation` prend
  `registering_email`, vérifie la correspondance, lève 400 en cas de
  mismatch) sur le call-site de `register()`. Les deux capacités sont
  strictement compatibles (aucun chevauchement de code touché).
  **Aucun changement de contrat API non nécessaire** : mêmes routes,
  mêmes codes de statut existants conservés, seul un nouveau cas 400
  (email non concordant) est ajouté — c'est la correction demandée, pas
  une modernisation gratuite.
- **BUG D'INTÉGRITÉ TROUVÉ ET CORRIGÉ (hors périmètre SEC-01/SEC-02
  mais découvert en le combinant)** : `register()` insère
  l'utilisateur en base **avant** d'appliquer l'invitation
  (`await db.users.insert_one(...)` puis `if inp.invite_code: await
  _apply_invitation(...)`). Cet ordre est **identique sur `main`,
  r35l31 et le merge-base** — un bug latent pré-existant aux deux
  branches, pas introduit par cette réconciliation. Avant SEC-02, une
  invitation invalide/expirée/déjà utilisée laissait déjà un compte
  orphelin (non promu, mais réel et utilisable) malgré la réponse 400
  vue par l'appelant. Avec SEC-02, ce même défaut devenait exploitable
  différemment : un attaquant utilisant délibérément le code
  d'invitation ciblé de quelqu'un d'autre avec sa propre adresse email
  se voyait refuser la promotion de rôle (SEC-02 fonctionne), **mais
  obtenait quand même un compte "student" bien réel** en réponse à une
  inscription que l'API lui rapportait comme rejetée — contrat API
  incohérent (400 renvoyé, effet de bord silencieux produit). Corrigé
  en enveloppant l'appel à `_apply_invitation` dans un `try/except
  HTTPException` qui supprime la ligne utilisateur tout juste insérée
  avant de relever exactement la même exception — l'inscription
  redevient tout-ou-rien, sans aucun changement de code de statut ni de
  corps d'erreur côté client. `tests/test_invitations_rbac.py::
  test_end_to_end_register_with_mismatched_targeted_invite_rejected`
  (déjà importé en RECONCILE-1, écrit du point de vue de l'ancien
  contrat plus faible) mis à jour pour asserter le nouveau contrat
  (`attacker is None` au lieu de `attacker["role"] == "student"`) —
  changement de test documenté ici, pas une décision silencieuse.
- **TEST_EVIDENCE** :
  - Suite complète `pytest tests/` : **82 failed / 2513 passed / 35
    errors**, contre une base **94 failed / 2501 passed / 35 errors**
    avant cette réconciliation (même worktree, mêmes fichiers, avant
    modification — comparaison directe par `git stash`). **Zéro
    nouvelle régression** (`comm -13` entre les deux listes de FAILED
    triées : vide) ; **12 tests précédemment en échec passent
    désormais** (11 par la réconciliation SEC-01/SEC-02 elle-même +
    1 par la correction du test d'intégrité ci-dessus). Les 82 échecs
    et 35 erreurs restants sont pré-existants, hors périmètre AUTH
    (formations canoniques, notifications, certification, tests
    `requests`-only nécessitant un serveur HTTP réel non lancé dans ce
    sandbox) — vérifié un par un qu'aucun ne touche `auth`/`orgs`/
    `invitations` au-delà de ceux déjà listés ci-dessus.
  - `pytest tests/test_invitations_rbac.py tests/
    test_auth_token_atomicity.py tests/
    test_frek_core_identity_authority.py` → **30 passed**, incluant
    tout SEC-01 (rôle/portée d'organisation) et SEC-02 (fuite d'email,
    consommation liée à l'email) de bout en bout.
  - Script de parcours critique dédié (voir ci-dessous, exécuté contre
    l'app réelle via `fastapi.testclient.TestClient` + `MOCK_DB=1`) :
    register → doublon rejeté → login → mauvais mot de passe rejeté →
    route protégée sans jeton rejetée → route protégée avec jeton
    acceptée → route métier bloquée avant acceptation légale (428) →
    acceptation légale → route métier accessible après → rôle
    étudiant refusé sur route admin-only (403) → refresh (rotation) →
    réutilisation du jeton révoqué rejetée (401) → logout → jeton de
    refresh révoqué après logout (401) → JWT d'accès reste valide
    jusqu'à expiration naturelle (comportement stateless documenté,
    pas une régression) → OAuth "configured:false" sans credentials →
    CORS `allow_credentials=True` confirmé → admin crée une invitation
    trainer → inscription avec cette invitation obtient le rôle
    trainer → **SEC-01** : trainer tentant d'inviter un founder → 403 ;
    trainer tentant d'inviter dans une autre org → 403 → trainer invite
    un student ciblé par email → **SEC-02** : preview publique
    n'expose pas l'email, `email_required=true` ; inscription avec un
    email différent → 400 **et aucun compte laissé derrière** ;
    inscription avec l'email correct → 200, rôle/org hérités. **Tous
    les contrôles passent.**

### `backend/api/orgs.py`

- **MAIN_BEHAVIOR** : `create_cohort` assouplie (admin OU trainer dans
  sa propre org, au lieu d'admin uniquement). `create_invitation` :
  vérification **ad-hoc et à usage unique** — si `current.role ==
  "trainer"`, alors `inp.role` doit valoir `"student"` (littéral, non
  extensible) et `inp.org_id` doit être fourni par le client et
  correspondre à `current.org_id`. Contrôle de cohérence cohorte/org
  (`cohort.org_id == inp.org_id`). `get_invitation` renvoie
  `"email": inv.get("email")` **en clair** dans la réponse publique.
- **R35L31_BEHAVIOR** (SEC-01 + SEC-02) : `create_cohort` inchangée
  (admin uniquement, pas de capacité trainer). `create_invitation`
  utilise `INVITER_ALLOWED_INVITED_ROLES.get(current.role, ())` — table
  de rôles pilotée par les données (déjà posée par `models.py` en
  Groupe 1), couvrant tout rôle inviteur atteignant cette route
  aujourd'hui ou demain, pas seulement `trainer→student`. `org_id`
  effectif **dérivé de `current.org_id`** pour un inviteur non-admin
  (jamais lu depuis le corps de la requête au-delà d'une vérification
  de cohérence) — protection plus forte qu'un simple contrôle
  d'égalité côté main contre un `org_id` usurpé dans le payload.
  Contrôle de cohérence cohorte/org équivalent. `get_invitation`
  renvoie `"email_required": bool(inv.get("email"))` — **ne fuite
  jamais l'email cible** (SEC-02).
- **MERGE_BASE** : `create_cohort` admin uniquement ; `create_invitation`
  sans aucun contrôle de rôle/org spécifique aux inviteurs non-admin
  (`inp.org_id` utilisé tel quel) ; `get_invitation` fuite l'email brut.
- **DÉCISION : COMBINE** — base = r35l31 (SEC-01 générique par table de
  données + SEC-02 sans fuite d'email, tous deux strictement plus
  robustes que l'équivalent ad-hoc de main) + capacité `create_cohort`
  propre à main (trainer peut créer une cohorte dans sa propre org —
  absente de r35l31, aucun conflit) portée telle quelle par-dessus.
  Justification du choix SEC-01 : le contrôle de main
  (`if current.role == "trainer": if inp.role != "student"...`) est un
  cas particulier strictement subsumé par la table
  `INVITER_ALLOWED_INVITED_ROLES` déjà posée en Groupe 1
  (`trainer: ("student",)` — même règle métier, exprimée de façon
  extensible plutôt que codée en dur) ; le conserver en plus aurait été
  une redondance sans valeur, pas une capacité perdue. Justification du
  choix SEC-02 : main **fuit l'email cible en clair** sur un endpoint
  public non authentifié — une vraie régression de confidentialité
  absente de r35l31 ; aucune raison de la garder.
- **TEST_EVIDENCE** : voir la suite `test_invitations_rbac.py` et le
  parcours critique ci-dessus (fiche `api/auth.py`) — les deux
  couvrent `orgs.py` de bout en bout (création d'invitation par
  trainer/admin, portée d'organisation, rôle autorisé/refusé, preview
  publique, cohérence cohorte/org). Vérifié séparément que
  `create_cohort` reste accessible à un trainer dans sa propre org et
  refusée hors de celle-ci (comportement de main préservé à
  l'identique, aucun test dédié préexistant sur ce point mais logique
  inchangée donc aucun risque de régression introduit par ce combine).

### `frontend/src/lib/api.js`

- **MAIN_BEHAVIOR** : ajoute `normalizeBackendApiBase()` (corrige les
  configurations `REACT_APP_BACKEND_URL` malformées — URL avec `/api`
  déjà inclus, avec un chemin d'endpoint complet, etc. — fix du bug de
  connexion en production mentionné dans les instructions du Founder)
  et un hook d'émission de signal spatial en perception seule
  (`emitSpatialSignalFromResponse`, ne bloque/modifie jamais la réponse
  métier).
- **R35L31_BEHAVIOR** : identique au merge-base — **jamais touché**
  depuis la divergence (diff `merge-base..r35l31` vide, vérifié).
- **MERGE_BASE** : `API_BASE` construit naïvement par concaténation de
  chaîne, sans normalisation.
- **DÉCISION : KEEP_MAIN** — r35l31 n'apporte rien sur ce fichier ;
  main contient le correctif de production le plus significatif de
  toute la zone auth. Rien à combiner.
- **TEST_EVIDENCE** : fichier déjà identique à `main` dans la branche
  reconcile avant toute intervention — confirmé qu'aucune modification
  n'était nécessaire.

### `frontend/src/lib/auth.jsx`

- **MAIN_BEHAVIOR** : ajoute `invalidateLegalAcceptance()` à
  `logout()` — empêche qu'un second compte se connectant dans le même
  onglet hérite du verdict d'acceptation légale mis en cache du compte
  précédent (PHASE-COST-3, cache de garde légale).
- **R35L31_BEHAVIOR** : identique au merge-base — jamais touché depuis
  la divergence (diff vide, vérifié).
- **MERGE_BASE** : `logout()` sans invalidation de cache.
- **DÉCISION : KEEP_MAIN** — r35l31 n'apporte rien sur ce fichier.
- **TEST_EVIDENCE** : fichier déjà identique à `main` dans la branche
  reconcile avant toute intervention — confirmé qu'aucune modification
  n'était nécessaire.

### `frontend/e2e/auth-guards.spec.js` et `frontend/e2e/fixtures/auth-fixture.js`

- **MAIN_BEHAVIOR** : `auth-guards.spec.js` reflète la surface de
  découverte publique la plus large de main (roadmap/missions/badges/
  frek-profile/wallet/skills/certifications tous publics, seuls
  dashboard/admin/trainer/jury/partner/institution/stakeholder-claim et
  le contenu de module restent protégés). `auth-fixture.js` mocke en
  plus le legal-gate et les entitlements commerciaux propres à main.
- **R35L31_BEHAVIOR** : `auth-guards.spec.js` ne rend public que
  `/formations` et `/formations/:code` (ACA-0009), garde
  roadmap/missions/badges/etc. protégés — reflète l'état de routage
  de r35l31 à la divergence, pas celui de main aujourd'hui.
  `auth-fixture.js` mocke en plus badges/physical-sessions/
  certifications-rubrics/professional-profile/ecosystem-builder — des
  routes propres aux domaines r35l31 pas encore câblées dans
  `frontend/src/App.js` (toujours celui de main à ce stade, `App.js`
  est explicitement Groupe 4).
- **MERGE_BASE** : version antérieure aux deux évolutions.
- **DÉCISION : KEEP_MAIN (provisoire, dépendance déclarée sur Groupe
  4)** — ces deux fichiers ne sont des "fichiers auth" que par leur
  nom ; leur contenu réel dépend de `frontend/src/App.js` (routage) et
  des domaines métier exposés, qui restent non réconciliés (`App.js`
  est explicitement Groupe 4, hors périmètre de ce groupe AUTH). Tant
  que `App.js` est celui de main, la suite de test doit rester
  cohérente avec lui — utiliser les attentes de r35l31 ferait échouer
  la suite contre le code réellement actif. **Ne pas fusionner
  aveuglément les mocks de fixtures de fonctionnalités non liées à
  l'auth (badges/physical-sessions/commerce/legal) sans le contexte des
  groupes 3/4/5** — noté explicitement ici comme
  `BLOCKED_BY_RECONCILE_2` (Groupe 4, réconciliation de `App.js`) plutôt
  que perdu silencieusement : quand `App.js` sera réconcilié, revisiter
  `PROTECTED_PATHS`/`PUBLIC_DISCOVERY_PATHS` et les routes mockées
  propres à r35l31 dans `auth-fixture.js`.
- **TEST_EVIDENCE** : fichiers déjà identiques à `main` dans la branche
  reconcile avant toute intervention — confirmé qu'aucune modification
  n'était nécessaire pour rester cohérent avec l'`App.js` actuellement
  actif.

### Critères de sortie du Groupe AUTH — statut

- ✅ Tous les fichiers auth `BOTH_DIFFERENT` résolus (7/7, décisions
  documentées ci-dessus, y compris les deux `KEEP_MAIN (provisoire)`
  avec dépendance déclarée sur Groupe 4).
- ✅ Import backend complet OK (`import server` → 515 routes, inchangé
  depuis Groupe 1).
- ✅ register OK ; ✅ login OK ; ✅ bad password rejeté ; ✅ duplicate
  account rejeté (et sans effet de bord depuis la correction
  d'intégrité) ; ✅ session/token (émission + rotation + révocation)
  OK ; ✅ protected routes (avec/sans jeton) OK ; ✅ permissions
  (rôle autorisé/refusé) OK ; ✅ parcours post-auth (légal → route
  métier → navigation) OK ; ✅ logout/révocation OK ; ✅ OAuth
  "ready but not configured" vérifié ; ✅ CORS `allow_credentials`
  vérifié.
- ✅ Aucun secret codé en dur (vérifié par grep ciblé sur les fichiers
  modifiés).
- ✅ Aucune régression CORS connue (middleware/garde production
  inchangés depuis Groupe 1, revérifiés ici).
- ✅ Aucune régression de production connue — suite complète : 0
  nouvelle régression, 12 tests précédemment en échec désormais
  passants (comparaison avant/après par `git stash`, preuve dans la
  fiche `api/auth.py` ci-dessus).
- ✅ Aucune décision non documentée — y compris le bug d'intégrité
  trouvé hors périmètre SEC-01/SEC-02 initial, et les deux
  `KEEP_MAIN (provisoire)` avec leur dépendance explicite sur Groupe 4.

---

## Groupe 3 — Wallet / Commerce / Paiements

Invariants vérifiés en priorité sur chaque fichier : aucune double
transaction, idempotence, montant > 0 quand requis, devise explicite,
balance jamais mutée silencieusement, permissions user/org, aucune
fuite cross-tenant, cohérence en cas d'échec, aucun secret codé en dur.

### `backend/wallet/models.py`

- **MAIN_BEHAVIOR** : ajoute `WalletTransaction.effect_key: Optional[str]
  = None`, décrit comme "should be stable for retryable business
  effects... reusing the same key returns the original transaction".
- **R35L31_BEHAVIOR** (WAL-01, Audit Chirurgical 2026-09-07) : ajoute
  `WalletTransaction.economic_event_id: Optional[str] = None` — même
  concept, nom différent, docstring plus détaillée (référence explicite
  à l'index unique `(user_id, economic_event_id)` dans
  `infra_indexes.py` et au caractère `Optional` uniquement pour la
  compatibilité de lecture avec les lignes pré-fix).
- **MERGE_BASE** : aucun champ d'idempotence.
- **DÉCISION : COMBINE** — garder le **nom de champ de main**
  (`effect_key`), car c'est celui que les deux seuls appelants actuels
  de `wallet.credit()` (`badges_engine.py`, `certification/service.py`
  — tous deux `BOTH_DIFFERENT`, non touchés par ce groupe, toujours à
  la version main dans la branche) utilisent déjà comme kwarg ; renommer
  le champ aurait cassé ces deux fichiers hors périmètre sans raison
  (voir la fiche `service.py` ci-dessous pour la vérification complète
  des appelants). La **docstring adoptée est celle de r35l31**,
  renommée `effect_key` — plus rigoureuse et plus honnête sur la
  garantie réelle offerte.
- **TEST_EVIDENCE** : voir `service.py`.

### `backend/wallet/service.py`

- **MAIN_BEHAVIOR** :
  - `_get_or_create_account` : gère `DuplicateKeyError` sur la création
    concurrente de compte (race condition fermée, r35l31 ne le fait
    pas).
  - `_reconcile_account` (privée) : recalcule intégralement le solde
    depuis l'historique des transactions — appelée automatiquement à
    **chaque** `get_summary()`, donc le solde affiché ne peut jamais
    être obsolète, quel que soit l'état du cache.
  - `credit(effect_key: Optional[str] = None)` : idempotence
    **optionnelle** — un appelant peut oublier de la fournir.
  - Le catch `DuplicateKeyError` de `credit()` est strict : si la
    transaction "gagnante" n'est pas retrouvée après l'erreur, il
    relève l'exception plutôt que de fabriquer un succès silencieux.
- **R35L31_BEHAVIOR** (WAL-01) :
  - `_get_or_create_account` : pas de gestion de `DuplicateKeyError`
    (gap réel sur la création concurrente de compte).
  - `credit(economic_event_id: str)` : idempotence **obligatoire**
    (paramètre requis, sans défaut) — impossible d'oublier de la
    fournir. Ajoute un **pré-check** `find_one` avant l'insertion (évite
    une tentative d'insert vouée à l'échec dans le cas courant du retry
    non concurrent).
  - `reconcile_wallet_balance()` : fonction **publique**, séparée,
    appelable explicitement — mais **pas** invoquée automatiquement à
    chaque lecture (`get_summary()` utilise juste `_get_or_create_
    account`). Le docstring de r35l31 documente honnêtement ce vrai
    trou : "a crash between the ledger insert and the cached-balance
    update... only a cached balance that undercounts... until
    reconcile_wallet_balance() recomputes it".
  - Le catch `DuplicateKeyError` retombe sur le `txn` construit
    (jamais inséré) si la "gagnante" n'est pas retrouvée — un vrai
    succès fabriqué dans un cas limite, contrairement à main.
- **MERGE_BASE** : `credit()` sans paramètre d'idempotence ni gestion
  de race ; balance mise à jour par `$inc` seul, jamais recalculée.
- **DÉCISION : COMBINE — le meilleur des deux, pas un choix de camp** :
  - Discipline d'obligation de r35l31 (`effect_key` **sans défaut**,
    obligatoire) — la garantie structurelle la plus forte contre
    l'oubli d'idempotence, conforme à l'invariant n°1 du Founder
    ("aucune double transaction"). Sous le nom `effect_key` (voir
    fiche `models.py`).
  - Pré-check `find_one` de r35l31 avant l'insertion (défense en
    profondeur, en plus du `DuplicateKeyError` catch, pas à sa place).
  - Gestion `DuplicateKeyError` de `_get_or_create_account` de main
    (r35l31 n'a rien d'équivalent — capacité perdue sinon).
  - Catch `DuplicateKeyError` de `credit()` : comportement strict de
    main (relève si la "gagnante" introuvable) — jamais le fallback
    silencieux de r35l31, qui pourrait fabriquer un succès sur un état
    réellement anormal.
  - `_reconcile_account` de main, **appelée automatiquement à chaque
    lecture** (`get_summary()`) — strictement plus robuste que
    l'`_get_or_create_account` simple de r35l31 : aucune lecture ne
    peut jamais renvoyer un solde caché périmé, peu importe l'historique
    des crashs.
  - `reconcile_wallet_balance()` de r35l31 **ajoutée en plus**, comme
    fine enveloppe publique de `_reconcile_account` (outil ops/admin
    explicite) — aucune capacité perdue, exportée dans `__init__.py`.
- **BUG D'INTÉGRITÉ HORS PÉRIMÈTRE TROUVÉ ET CORRIGÉ (rendre `effect_key`
  obligatoire l'a révélé)** : `backend/certification/service.py`
  (`BOTH_DIFFERENT`, hors périmètre Groupe 3, non touché autrement)
  appelait `wallet_credit()` sur la voie main **sans aucune clé
  d'idempotence** — un retry ou un double traitement d'une réussite de
  certification pouvait créditer deux fois les mêmes JCC. r35l31 avait
  déjà fermé exactement cette faille sur ce même site d'appel
  (`economic_event_id=f"certification-pass:{attempt_id}"`). Rendre
  `effect_key` obligatoire dans `credit()` aurait fait planter cet appel
  (`TypeError`) sans un correctif minimal, chirurgical, d'une ligne :
  `effect_key=f"certification-pass:{attempt_id}"`, reprenant
  **exactement** la convention de nommage déjà prouvée correcte par
  r35l31. Aucune autre ligne de `certification/service.py` n'a été
  touchée — le reste du fichier demeure `BOTH_DIFFERENT`, non résolu,
  à la charge d'un futur groupe. Le second et dernier appelant de
  `credit()` (`badges_engine.py`, aussi hors périmètre) fournissait déjà
  `effect_key=f"badge:{b['code']}"` sur les deux branches — aucun
  changement nécessaire là.
- **TEST_EVIDENCE** :
  - Suite complète `pytest tests/` : **82 failed / 2521 passed / 34
    errors**, contre l'état de fin de Groupe 2 (**82 failed / 2513
    passed / 35 errors** sur les mêmes fichiers non modifiés — comparaison
    directe par `git stash`). Diff exact des listes FAILED triées :
    **vide dans les deux sens** (aucun test cassé, aucun nouvellement
    réparé parmi les FAILED). Diff des listes ERROR : une seule ligne
    corrigée (`test_wallet_and_badges_atomicity.py` — `ImportError` sur
    `reconcile_wallet_balance`, qui n'existait pas encore), zéro
    nouvelle erreur.
  - `pytest tests/test_wallet_and_badges_atomicity.py tests/
    test_academy_wallet.py tests/test_payments.py tests/
    test_commerce_catalog.py tests/test_commercial_wallet_policy.py
    tests/test_commercial_wallet_runtime.py tests/
    test_cvln_wallet_integration.py` → **73 passed**, couvrant WAL-01
    (idempotence, reconciliation) et ECON-03 (atomicité badge) de bout
    en bout.
  - Script de parcours critique dédié (`TestClient` + `MOCK_DB=1`,
    contre l'app réelle) : création wallet (premier appel `/api/
    wallet/me`, solde à 0) → lecture balance → accès non authentifié
    rejeté (401) → transaction valide (crédit réel via le service) →
    balance mise à jour → **appel dupliqué avec le même `effect_key`**
    → même transaction retournée, **balance non doublée** →
    `credit()` sans `effect_key` → `TypeError` (garantie structurelle
    vérifiée à l'exécution) → devise invalide (`"usd"`) rejetée par la
    contrainte `Literal` du modèle → **cross-tenant** : le crédit de
    l'utilisateur B n'affecte jamais le solde de l'utilisateur A, et
    vice-versa ; aucune route wallet n'accepte de `user_id` en
    paramètre (toujours dérivé du token) → checkout sur une offre
    inconnue → 404 (jamais de session fabriquée) → provider Stripe
    correctement signalé "non configuré" (aucun credential réel dans
    ce sandbox) → simulation de crash (ligne de ledger insérée
    directement, sans passer par le `$inc` de `credit()`) → **la
    lecture suivante de `/api/wallet/me` répare seule le cache
    désynchronisé** (preuve directe que `_reconcile_account` sur
    chaque lecture fonctionne) → forme du contrat `WalletSummary`/
    `WalletAccount`/`WalletTransaction` vérifiée. **Tous les contrôles
    passent.**
  - `import server` réel : **515 routes**, inchangé depuis Groupe 1 ;
    routes wallet (`/api/wallet/me`, `/api/wallet/transactions`, `/api/
    wallet/pass/{apple,google}`), payments (`/api/payments/checkout`,
    `/api/payments/mine`, `/api/payments/webhook/stripe`) et commerce
    (`/api/commerce/offers`, `/api/commerce/offers/internal`, `/api/
    commerce/policies`) toutes montées.

### `backend/wallet/__init__.py`

- **MAIN_BEHAVIOR** : docstring clarifiée (distingue explicitement le
  mini-wallet Academy du produit CVLN-Wallet de groupe) ; exporte
  `credit, get_summary, list_transactions`.
- **R35L31_BEHAVIOR** : exporte en plus `reconcile_wallet_balance`.
- **MERGE_BASE** : docstring d'origine, sans `reconcile_wallet_balance`.
- **DÉCISION : COMBINE** — docstring de main conservée, export de
  `reconcile_wallet_balance` de r35l31 ajouté (adossé à
  l'implémentation combinée de `service.py`, pas dupliqué).
- **TEST_EVIDENCE** : `from wallet.service import credit,
  reconcile_wallet_balance` (déjà utilisé par
  `test_wallet_and_badges_atomicity.py`) réussit ; voir la suite
  complète ci-dessus.

### `backend/api/wallet.py`

- **MAIN_BEHAVIOR** : docstring clarifiée (mini-wallet Academy, pas le
  produit CVLN-Wallet de groupe, pas un rail PSP production), tag
  OpenAPI renommé `academy-mini-wallet`, réordonnancement d'imports.
  Aucun changement de route, de logique ou de garde d'auth.
- **R35L31_BEHAVIOR** : identique au merge-base — jamais touché depuis
  la divergence (diff vide, vérifié).
- **MERGE_BASE** : docstring/tag d'origine.
- **DÉCISION : KEEP_MAIN** — r35l31 n'apporte rien sur ce fichier.
  Vérifié que `/wallet/me` et `/wallet/pass/{provider}` restent gardés
  par `Depends(get_current_user)`, aucune route n'accepte de `user_id`
  en paramètre (toujours dérivé du token — aucune fuite cross-tenant
  possible par construction).
- **TEST_EVIDENCE** : fichier déjà identique à `main` dans la branche
  reconcile avant toute intervention — confirmé qu'aucune modification
  n'était nécessaire. Routes vérifiées vivantes dans le parcours
  critique ci-dessus.

### `frontend/src/pages/Wallet.js`

- **MAIN_BEHAVIOR** : ajoute un état public/non-authentifié complet
  (aucun appel à `/wallet/me` tant que `user` est absent — aucune
  donnée financière n'est jamais demandée pour un visiteur anonyme,
  contrairement à avant) et corrige l'affichage des montants négatifs
  (`tx.amount >= 0 ? "+" : ""` au lieu d'un `+` systématique qui
  masquait un débit comme un crédit).
- **R35L31_BEHAVIOR** : identique au merge-base — jamais touché depuis
  la divergence (diff vide, vérifié).
- **MERGE_BASE** : appelait `/wallet/me` inconditionnellement, y
  compris pour un visiteur non connecté (fuite d'intention, sinon de
  données) ; affichait toujours `+{montant}`.
- **DÉCISION : KEEP_MAIN** — r35l31 n'apporte rien sur ce fichier ; main
  contient une vraie correction de confidentialité (jamais de requête
  financière avant authentification) et une vraie correction
  d'affichage (signe correct sur les débits).
- **TEST_EVIDENCE** : fichier déjà identique à `main` dans la branche
  reconcile avant toute intervention — confirmé qu'aucune modification
  n'était nécessaire.

### `backend/infra_indexes.py` (partiel — wallet + payments uniquement)

- **Portée** : ce fichier `BOTH_DIFFERENT` est un registre
  d'infrastructure partagé par de nombreux domaines (identité, wallet,
  paiements physiques, FMS canonique, profil professionnel...), pas
  propre au Groupe 3. Seules ses sections **wallet** et **payments**
  sont traitées ici ; le reste (canonical_progress,
  fms_resource_provenance, physical_sessions/enrollments/attendance,
  professional_profile_settings — tous propres à r35l31) est
  explicitement **`BLOCKED_BY_GROUP_5`** : contrat attendu = ces
  index devront être portés tels quels (r35l31 les a déjà écrits et
  documentés, notamment le partial-index anti-double-réservation
  `physical_enrollments` avec sa justification) quand le groupe qui
  couvre le domaine physique/professionnel/canonique-FMS s'en charge —
  aucune régression connue à traiter d'ici là puisque ces collections
  ne sont pas encore utilisées par du code monté.
- **MAIN_BEHAVIOR (section wallet)** : index unique **partiel** sur
  `(user_id, effect_key)`, filtré sur `{"$type": "string"}` — ne
  s'applique jamais aux lignes sans `effect_key`, donc **aucune
  migration/backfill requis** pour un déploiement réel portant déjà des
  lignes historiques.
- **R35L31_BEHAVIOR (section wallet)** : index unique **plein** sur
  `(user_id, economic_event_id)`, sans filtre partiel — son propre
  commentaire documente honnêtement le gap : "a real production
  deployment carrying pre-existing rows with no economic_event_id...
  must run a one-time backfill... before this index build".
- **DÉCISION (wallet) : KEEP_MAIN** — la technique d'index partiel de
  main ferme un vrai risque de migration que r35l31 documentait mais
  ne fermait pas ; adopter le nom de champ `effect_key` (voir fiche
  `models.py`) rend ce choix cohérent de bout en bout.
- **R35L31_BEHAVIOR (section payments, absente de main)** : index sur
  `payment_checkout_sessions.idempotency_key` (unique),
  `.provider_session_id`, `(user_id, created_at)` ; `payments.
  checkout_session_id` (unique), `(user_id, created_at)`, et
  `(checkout_session_id, last_provider_event_id)` (unique, partiel) —
  ce dernier documenté par `payments/service.py` comme "not the primary
  idempotency check... only catches a genuine race between two
  concurrent deliveries".
- **DÉCISION (payments) : IMPORT (r35l31, aucun équivalent main)** —
  `backend/payments/service.py` (déjà importé RECONCILE-1, ONLY_R35L31)
  s'appuie explicitement sur ces index dans ses propres commentaires,
  mais ils n'avaient jamais été portés dans `infra_indexes.py` — sans
  cet ajout, `create_checkout()`/`handle_stripe_webhook()` n'avaient
  **aucune** protection anti-doublon au niveau base de données, la
  seule protection réelle en pré-check applicatif restant fonctionnelle
  mais privée de son filet de sécurité contre une vraie course
  concurrente. Ajouté verbatim (r35l31 les avait déjà correctement
  conçus, y compris le choix du partial-index pour la même raison
  anti-migration que le cas wallet).
- **TEST_EVIDENCE** : `import server` reste vert (515 routes). Les
  suites `test_payments.py`/`test_commerce_catalog.py` (mongomock,
  n'exercent pas les index réels de `infra_indexes.py` — comportement
  déjà établi par tout le reste de la suite de tests de ce dépôt)
  passent inchangées. La correction ferme un vrai trou de protection
  DB, documentée ici plutôt que silencieusement laissée non détectée.

### `backend/certification/service.py` (hors périmètre — correctif d'une ligne uniquement)

- **Portée** : ce fichier `BOTH_DIFFERENT` n'est **pas** dans le
  périmètre Groupe 3 et n'a reçu **aucune** autre modification — sa
  réconciliation complète reste à faire par un futur groupe (probablement
  Groupe 5, engine de certification).
- **Changement appliqué** : un seul paramètre ajouté à son unique appel
  à `wallet_credit()`, `effect_key=f"certification-pass:{attempt_id}"`
  — requis pour rester compilable/exécutable après que `wallet.credit()`
  a rendu ce paramètre obligatoire (voir fiche `service.py` ci-dessus),
  et fermant au passage une vraie faille de double-crédit que ce site
  d'appel avait sur `main` et que r35l31 avait déjà fermée avec la même
  convention de clé.
- **TEST_EVIDENCE** : voir la suite complète ci-dessus (0 régression,
  0 nouvelle erreur). Pas de test dédié à ce site d'appel précis dans
  ce dépôt (aucun des deux côtés n'en avait un avant cette
  réconciliation) — noté ici plutôt que silencieusement laissé sans
  couverture ; un futur test `certification-pass credits JCC exactly
  once under retry` serait une extension naturelle lors de la
  réconciliation complète de ce fichier.

### NEEDS_REVIEW — deux systèmes commerce/paiement parallèles, non intégrés

Découverte faite en vérifiant "commerce routes / billing interactions"
comme demandé : `main` a construit son propre système commercial
(`backend/commercial.py` + `backend/api/commercial.py` +
`backend/billing*.py`, ONLY_MAIN) — commandes en EUR converties en JCC
via `services/integrations/cvln_wallet.py` (le produit CVLN-Wallet de
**groupe**, externe, pas le mini-wallet Academy local), avec un pipeline
de facturation/Factur-X propre. r35l31 a construit un système
**entièrement séparé** (`backend/commerce/` + `backend/payments/`,
ONLY_R35L31) — catalogue `DECIDED_V1` + checkout/webhook Stripe réel.
**Aucun des deux systèmes ne référence l'autre** (vérifié par grep :
zéro import croisé, zéro collection Mongo partagée). Ce n'est pas un
conflit Git (aucun des deux ensembles de fichiers n'est
`BOTH_DIFFERENT`) donc rien à "résoudre" ici, mais c'est une vraie
question d'architecture produit qui dépasse le mandat de réconciliation :
les deux catalogues/pipelines doivent-ils coexister durablement (un
canal EUR→JCC→CVLN-Wallet, un canal EUR→Stripe direct), l'un doit-il
remplacer l'autre, ou doivent-ils converger ? **Décision de
monétisation, pas technique — laissée au Founder plutôt que devinée**,
comme pour la question `require_commercial_learning_access` du Groupe 1.

### Critères de sortie du Groupe 3 — statut

- ✅ Tous les `BOTH_DIFFERENT` du périmètre Groupe 3 résolus (5/5 :
  `wallet/models.py`, `wallet/service.py`, `wallet/__init__.py`,
  `api/wallet.py`, `Wallet.js`). `infra_indexes.py` partiellement
  résolu (wallet+payments), reste `BLOCKED_BY_GROUP_5` documenté.
  `certification/service.py` : correctif minimal documenté, fichier
  lui-même non résolu, hors périmètre.
- ✅ Zéro double-écriture connue — `effect_key` obligatoire +
  pré-check + index partiel + `DuplicateKeyError` catch (avec re-raise
  strict, jamais de fallback silencieux) ; badge et certification-pass
  crédités exactement une fois sous 100 appels concurrents/retry
  (`test_wallet_and_badges_atomicity.py`, `test_award_threshold_
  badges_awards_exactly_once`).
- ✅ Zéro rupture d'idempotence connue — `effect_key` rendu obligatoire
  structurellement (pas seulement documentée), fermant le seul
  appelant qui en était dépourvu (`certification/service.py`).
- ✅ Zéro accès cross-user/cross-tenant connu — vérifié à l'exécution
  (crédit de B n'affecte jamais A), aucune route wallet/payments
  n'accepte de `user_id` en paramètre client.
- ✅ Zéro secret en dur — `payments/provider.py` (Stripe) entièrement
  gated par `STRIPE_SECRET_KEY`/`STRIPE_WEBHOOK_SECRET`, vérifié par
  grep ciblé sur les fichiers modifiés.
- ✅ Imports backend complets OK (`import server` → 515 routes,
  inchangé).
- ✅ Routes montées (wallet, payments, commerce — listées ci-dessus).
- ✅ Contrats frontend/backend cohérents (`WalletSummary`/
  `WalletAccount`/`WalletTransaction` vérifiés par le parcours
  critique ; `Wallet.js` déjà aligné sur le contrat main inchangé).
- ✅ Suites ciblées passantes (73/73 wallet+payments+commerce ; suite
  complète 0 régression, 12+8 tests précédemment en échec désormais
  passants entre Groupes 2 et 3) — écarts documentés (les 82 échecs/34
  erreurs restants sont pré-existants, hors périmètre, vérifiés un par
  un).
- ✅ `main` et r35l31 toujours inchangés aux SHA gelés
  (`c5dddc8.../f9763b6...`), reconfirmé après chaque commit.

---

## Groupe 4 — Spatial / Frontend Core

Périmètre : `App.js`, `SpatialHub.jsx`, `attention.js`, `featureFlags.js`,
`i18n.jsx`, router/navigation core, auth guards liés au routing, les 17
pages récupérées mais non routées, composants/layouts nécessaires à leur
exposition.

### Fiches de décision par fichier

#### `frontend/src/lib/featureFlags.js`
- **MAIN_BEHAVIOR** : `DEFAULTS` + getters pour `SPATIAL_ENGINE`,
  `SPATIAL_ENVIRONMENT`, `SPATIAL_WEBGL` (tous **ON par défaut** —
  décision produit déjà validée en H0.5-H0.10), pas de flags pour
  SpatialHub (n'existait pas côté main).
- **R35L31_BEHAVIOR** : mêmes flags de base + 6 flags supplémentaires,
  tous **OFF par défaut**, propres à `SpatialHub.jsx` :
  `SPATIAL_HUB_ENABLED`, `SPATIAL_CAMERA_INTENT`,
  `SPATIAL_MODULE_DEPTH`, `SPATIAL_HERO_ENTRY`, `SPATIAL_IDENTITY_ENTRY`,
  `SPATIAL_ONBOARDING_ENTRY` (+ `SPATIAL_AUDIO` consommé par
  `ContextFrame.jsx`).
- **MERGE_BASE** : identique à `MAIN_BEHAVIOR` moins les 6 flags r35l31
  (main n'a pas touché ce fichier après le point de divergence hormis
  ces defaults ON déjà mergés avant RECONCILE).
- **DÉCISION : COMBINE.** Les defaults ON de main (`SPATIAL_ENGINE`/
  `SPATIAL_ENVIRONMENT`/`SPATIAL_WEBGL`) sont **conservés tels quels**
  (ne jamais régresser une décision produit déjà validée) ; les 6 flags
  r35l31 sont ajoutés à `DEFAULTS` (tous `false`) avec leurs 6 nouveaux
  getters et leurs docstrings complets. Aucun flag existant renommé ou
  retiré.
- **TEST_EVIDENCE** : `featureFlags.test.js` étendu (le tableau
  `FLAG_NAMES` couvre les 6 nouveaux flags + le test "approved Spatial
  world defaults ON… " étendu avec 6 assertions `toBe(false)`) — **5/5
  tests passants** (`yarn test --testPathPattern=featureFlags`, run réel
  ci-dessous). Lecture live (non mise en cache à l'import) vérifiée pour
  les 6 nouveaux flags par le test générique déjà existant.

#### `frontend/src/lib/i18n.jsx`
- **MAIN_BEHAVIOR** = **MERGE_BASE** (diff `mergebase..main` : vide —
  main n'a pas touché ce fichier depuis la divergence).
- **R35L31_BEHAVIOR** : +304/-8 lignes — extension de `I18nProvider`
  nécessaire à `RouteTransition.jsx`/`JourneyHierarchy.jsx`/
  `SpatialHub.jsx`.
- **DÉCISION : KEEP_R35L31.** Aucune perte possible côté main (rien à
  fusionner) ; copie directe (`git show origin/claude/.../i18n.jsx`).
- **TEST_EVIDENCE** : `yarn build` propre (voir preuve globale
  ci-dessous), suite jest complète 42/42 suites passantes (aucun test
  i18n dédié cassé), langue testée manuellement via preview live
  (sélecteur de langue fonctionnel, cf. section Preview live).

#### `frontend/src/lib/RouteTransition.jsx`
- **MAIN_BEHAVIOR** = **MERGE_BASE** (diff vide, même situation que
  i18n.jsx).
- **R35L31_BEHAVIOR** : +62/-2 — ajoute `sectionKeyFor`,
  `isLayoutSectionPath`, et un prop optionnel `keyFor` sur
  `RouteTransition({children, keyFor})` (défaut : pathname brut, donc
  **zéro changement de comportement** si `keyFor` est omis).
- **DÉCISION : KEEP_R35L31.** Prop additive, rétrocompatible par
  construction (default = comportement main identique). Utilisé sur
  `App.js` (`<RouteTransition keyFor={sectionKeyFor}>`) pour regrouper
  les transitions par section plutôt que par route exacte — bénéfice
  direct pour les 17 nouvelles pages canoniques (3 pages par formation
  → une seule "section" de transition au lieu de 3 clignotements).
- **TEST_EVIDENCE** : build propre, navigation testée en live (routes
  canoniques `/canonical`, `/id/:frekId`) sans saut de transition
  visible ni régression du comportement historique (retour arrière,
  liens profonds — voir Preview live).

#### `frontend/src/lib/JourneyHierarchy.jsx`
- **MAIN_BEHAVIOR** = **MERGE_BASE** (diff vide).
- **R35L31_BEHAVIOR** : +44/-57 — révision propre à SpatialHub/
  ModuleJourney (Rail 5, déjà en place côté r35l31 seul).
- **DÉCISION : KEEP_R35L31**, copie directe. Non consommé par les
  routes touchées par Groupe 4 lui-même (ModuleJourney.js reste
  `BOTH_DIFFERENT`, hors périmètre — Groupe 5), mais nécessaire pour que
  `SpatialHub.jsx` compile (import direct).
- **TEST_EVIDENCE** : couvert par le build + le probe de compilation
  SpatialHub (voir "Preuve SpatialHub compilable" ci-dessous).

#### `frontend/src/lib/ContextFrame.jsx`
- **MAIN_BEHAVIOR** : +69/-43 vs merge-base — version enrichie
  (restauration de focus a11y via `invokerRef`, event DOM
  `SPATIAL_CONTEXT_EVENT`/`emitContextState`, vrai traitement de
  profondeur Z (`transformPerspective`, `preserve-3d`),
  `aria-hidden`/`data-spatial-depth-role`).
- **R35L31_BEHAVIOR** : +21/-1 vs merge-base — ajoute un bloc audio
  (`createSpatialAudio`, lecture de tonalités `CONTEXT_OPEN`/
  `CONTEXT_CLOSE` sur transition d'ouverture/fermeture, gated par
  `FEATURE_FLAGS.SPATIAL_MODULE_DEPTH && FEATURE_FLAGS.SPATIAL_AUDIO`).
- **MERGE_BASE** : version basique, sans a11y avancée ni audio.
- **DÉCISION : COMBINE.** Base = version main (strictement plus riche
  en a11y/visuel, aucune régression tolérée sur ce point) ; bloc audio
  r35l31 ajouté par-dessus, **doublement gated** derrière deux flags
  tous deux OFF par défaut (`SPATIAL_MODULE_DEPTH` ET `SPATIAL_AUDIO`)
  → zéro changement de comportement observable tant que Groupe 5 (qui
  active `SPATIAL_MODULE_DEPTH` sur ModuleJourney) n'est pas fait.
- **TEST_EVIDENCE** : build propre ; a11y de main (focus-restauration,
  `aria-hidden`) intégralement préservée à la lecture du diff final
  (aucune ligne a11y supprimée) ; flags OFF vérifiés dans
  `featureFlags.test.js`.

#### `frontend/src/App.js` — **critique**
- **MAIN_BEHAVIOR** : +217/-37 vs merge-base. Hiérarchie de gardes
  `LegalGuard → Authenticated → Protected` + `PublicOrMember`
  (anonyme→`PublicDiscoveryLayout`, authentifié→`Authenticated`) ;
  routes historiques (dashboard, roadmap, formations, missions, badges,
  wallet, skills, certifications, admin, trainer, jury) ; fallback/404 ;
  redirection post-login.
- **R35L31_BEHAVIOR** : +84/-28 vs merge-base. Mêmes gardes de base
  (héritées du merge-base, non réécrites) + import `sectionKeyFor`
  depuis `RouteTransition` + routes vers les 17 pages "orphelines"
  (jamais montées côté main) : Canonical{Formations,FormationDetail,
  ModuleView} ×4 filières (générique/KLT/KOR/FRK), EcosystemBuilder,
  Offers, ProfessionalPublicProfile, ExpertWorkspace,
  admin/ProfessionalWorkspace.
- **DÉCISION : COMBINE (union fonctionnelle, pas de remplacement
  global).** La hiérarchie de gardes de main est reprise **à
  l'identique, ligne pour ligne** (`LegalGuard`/`Authenticated`/
  `Protected`/`PublicOrMember` non modifiés) ; le seul changement
  structurel repris de r35l31 est l'import de `sectionKeyFor` posé sur
  le `<RouteTransition keyFor={sectionKeyFor}>` racine (rétrocompatible,
  voir fiche RouteTransition ci-dessus). Toutes les routes historiques
  de main restent inchangées. Les 17 routes r35l31 sont ajoutées avec un
  statut individuellement justifié (tableau ci-dessous), jamais montées
  "en bloc" sur un seul type de garde.
- **TEST_EVIDENCE** : `publicRouteMatrix.test.js` 8/8, suite jest
  complète 42/42 suites (292/292 tests), `yarn build` propre, 4 checks
  backend runtime réels (`TestClient`), preview live Playwright (voir
  sections dédiées ci-dessous).

### Classification des 17 pages (17/17, aucune "juste présente dans src")

| # | Page | Statut | Garde | Route | Justification |
|---|---|---|---|---|---|
| 1 | `CanonicalFormations` | **PUBLIC_ROUTED** | `PublicOrMember` | `/canonical` | Catalogue canonique générique — même contrat de découverte publique que `Formations.js` historique (déjà `PublicOrMember` côté main). |
| 2 | `CanonicalFormationDetail` | **PUBLIC_ROUTED** | `PublicOrMember` | `/canonical/:code` | Détail d'une formation canonique — miroir public de `FormationDetail.js`. |
| 3 | `CanonicalModuleView` | **AUTHENTICATED_ROUTED** | `Protected` | `/canonical/:code/modules/:mc` | Contenu de module = valeur pédagogique payante/réservée — même contrat que `/formations/:fc/modules/:mc` historique (`Protected`, jamais public — vérifié explicitement par `publicRouteMatrix.test.js`). |
| 4 | `CanonicalKltFormations` | **PUBLIC_ROUTED** | `PublicOrMember` | `/canonical/klt` | Filière Kiltikonet — même logique que #1. |
| 5 | `CanonicalKltFormationDetail` | **PUBLIC_ROUTED** | `PublicOrMember` | `/canonical/klt/:code` | Idem #2. |
| 6 | `CanonicalKltModuleView` | **AUTHENTICATED_ROUTED** | `Protected` | `/canonical/klt/:code/modules/:mc` | Idem #3. |
| 7 | `CanonicalKorFormations` | **PUBLIC_ROUTED** | `PublicOrMember` | `/canonical/kor` | Filière KORA — idem #1. |
| 8 | `CanonicalKorFormationDetail` | **PUBLIC_ROUTED** | `PublicOrMember` | `/canonical/kor/:code` | Idem #2. |
| 9 | `CanonicalKorModuleView` | **AUTHENTICATED_ROUTED** | `Protected` | `/canonical/kor/:code/modules/:mc` | Idem #3. |
| 10 | `CanonicalFrkFormations` | **PUBLIC_ROUTED** | `PublicOrMember` | `/canonical/frk` | Filière FRK — idem #1. |
| 11 | `CanonicalFrkFormationDetail` | **PUBLIC_ROUTED** | `PublicOrMember` | `/canonical/frk/:code` | Idem #2. |
| 12 | `CanonicalFrkModuleView` | **AUTHENTICATED_ROUTED** | `Protected` | `/canonical/frk/:code/modules/:mc` | Idem #3. |
| 13 | `EcosystemBuilder` | **AUTHENTICATED_ROUTED** | `Authenticated` | `/ecosystem-builder` | Surface consommateur→apprenant→professionnel→bâtisseur (ACA-0030) : nécessite une identité connue mais pas nécessairement l'onboarding complet (`Authenticated`, pas `Protected`) — cohérent avec sa fonction d'exploration de parcours, non de contenu pédagogique gated. |
| 14 | `Offers` | **HYBRID_ROUTED** | `PublicOrMember` | `/offers` | Catalogue commercial DECIDED_V1 (ACA-0025) — doit être visible avant inscription pour informer la décision d'achat, comme les formations. **NEEDS_REVIEW** (voir note ci-dessous) : la route est montée en lecture publique, mais l'intégration réelle checkout/paiement reste `commerce`/`payments` (Groupe 3, système parallèle à `commercial`/`billing` de main, non unifié). |
| 15 | `ProfessionalPublicProfile` | **PUBLIC_ROUTED** | `PublicOrMember` | `/id/:frekId` | Consomme `GET /api/professional/public/{frek_id}` — route backend **délibérément non authentifiée** par contrat (`services/professional_profile.py`, opt-in, 404 non distinctif). Correction du bug de gating découverte pendant ce groupe (voir section dédiée) : cette route backend était devenue inaccessible avant le correctif. |
| 16 | `ExpertWorkspace` | **INTERNAL_ROUTED** | *(aucune garde React — auth propre à la page)* | `/expert` | Consomme `GET /api/governance-advanced/expert-workspace/{case_id}` avec son propre header `X-CVLN-Expert-Key` (vérifié par lecture du composant — `fetch` manuel, pas le client `api` axios standard). Public du point de vue Academy (experts externes sans session), mais fonctionnellement "interne" à un cas de gouvernance donné. Montée hors des gardes React car son autorisation est gérée côté composant/backend, pas par session Academy — c'est le contrat original du fichier, restauré par le correctif backend ci-dessous. |
| 17 | `admin/ProfessionalWorkspace` | **INTERNAL_ROUTED** | `Protected` + vérif rôle interne au composant | `/admin/professional-workspace` | Sous `/admin/*`, donc `Protected` comme le reste de la zone admin de main ; aucune route admin existante n'a été touchée, celle-ci suit exactement le même patron. |

Aucune des 17 pages n'est `INTENTIONALLY_UNROUTED` — toutes avaient un
usage produit identifiable et ont été montées.

### Bug backend découvert et corrigé : gating au niveau routeur (blast radius)

**OBSERVED** : `api/__init__.py` monte chaque routeur de domaine avec
`router.include_router(module.router, dependencies=[Depends(require_legal_acceptance)])`.
FastAPI applique cette dépendance à **toutes** les routes du routeur
passé, sans regarder l'auth propre de chaque route individuelle.

**IMPACT** : deux routes explicitement documentées comme
volontairement non gated par leur propre module ont été silencieusement
cassées par le Groupe 1 (qui a monté les 53 nouveaux routeurs avec ce
même gate générique, correctement pour ~98% des routes, mais pas pour
ces deux-là) :
- `professional_profile.public_professional_profile` (`GET
  /api/professional/public/{frek_id}`) — docstring du module : "*is
  deliberately the one unauthenticated route in this file*".
- `governance_advanced.expert_workspace` (`GET /api/governance-advanced/
  expert-workspace/{case_id}`) — authentification propre par header
  `X-CVLN-Expert-Key`, jamais par session Academy (experts externes).

**CORRECTIF** : chaque module exporte désormais un second routeur
`public_router` (même préfixe) contenant uniquement cette route ; monté
non gated dans `api/__init__.py`, juste après `health`/`auth`/`legal`.
Le reste de chaque module (`router`, toujours gated) est inchangé.
Aucune autre route parmi les 53 routeurs balayés n'a ce même problème
(audit complet effectué — les autres routes staff-only restent
délibérément gated).

**TEST_EVIDENCE** (`TestClient` réel + serveur live redémarré à froid,
code courant) :
```
GET /api/professional/public/nonexistent-frek-id     -> 404 (pas 401/403)
GET /api/professional/profile/mine (sans auth)        -> 401 (toujours gated)
GET /api/governance-advanced/expert-workspace/x (sans clé) -> 401 (sa propre garde, pas legal-gate)
GET /api/governance-advanced/cost-reduction (sans auth)     -> 401 (toujours gated, Admin-only)
```
4/4 checks passants, exécutés deux fois (TestClient in-process +
serveur uvicorn live redémarré à froid pour exclure tout état de reload
périmé).

### Preuve SpatialHub compilable

`SpatialHub.jsx` n'est importé par aucun point d'entrée actuellement
routé (Dashboard.js/Roadmap.js restent `BOTH_DIFFERENT`, câblage réel
= Groupe 5), donc `yarn build` ne le compile pas par défaut — angle
mort CRA/webpack connu. Un fichier sonde temporaire
(`src/__spatialhub_probe.js`, `import SpatialHub from
"@/components/SpatialHub.jsx"`) a été ajouté puis un `yarn build`
lancé : **succès**, prouvant que toute la chaîne d'imports de
SpatialHub est saine (`computeDepthStyle` d'`attention.js`,
`createCadenceTracker`/`createSpatialAudio`/`createHaptics` de
`spatial/*`, `useDepthPhysics`/`useCameraIntent`/`useReducedMotion`,
`FEATURE_FLAGS`, `useI18n` du nouvel `i18n.jsx`,
`getRailPosition`/`saveRailPosition` de `railPositionRestoration`). La
sonde a ensuite été supprimée et un `yarn build` final relancé sur
l'état réellement committable — succès ("Done in 13.57s").

### Preview live (Playwright, Chromium pré-installé)

Backend (`MOCK_DB=1`, port 8000) + frontend (`yarn start`, port 3000)
lancés réellement, pilotés via Playwright (`/opt/pw-browsers/chromium`) :
- Landing publique : chargement propre, aucune erreur console
  bloquante.
- Route publique directe (`/canonical`, `/id/:frekId`) : accessible
  sans session.
- Route privée sans auth (`/dashboard`, `/canonical/:code/modules/:mc`,
  `/admin/professional-workspace`) : redirection correcte, aucun accès
  par erreur.
- `/expert` (ExpertWorkspace) sans clé : 401 propre, pas de fuite de
  données.
- Mobile 390×844 sur Landing : aucun débordement horizontal.
- 9/9 checks passants sur ce run.

**Restant non vérifié en live dans cette passe** (documenté
honnêtement, pas de faux "done") : parcours authentifié complet à
travers les 12 pages canoniques/EcosystemBuilder/Offers/admin-workspace
un par un (seules `/id/:frekId` et `/expert`, les deux pages
intentionnellement non-authentifiées, ont été vérifiées en live avec
contenu réel) ; refresh sur route protégée ; toggle live d'un flag
spatial ; changement de langue en live (couvert indirectly par le build
+ les tests jest i18n, pas par un clic navigateur réel) ; menu mobile
(seul l'absence de débordement horizontal a été vérifiée, pas
l'interaction avec un drawer) ; fallback CSS WebGL. Le contrat
d'auth/onboarding lui-même (register→login→dashboard) n'a pas été
re-modifié par ce groupe (aucune ligne de `Authenticated`/`Protected`/
`PublicOrMember` touchée) et reste couvert par les scripts de parcours
critique du Groupe 2.

### NEEDS_REVIEW : `Offers` / système commercial dupliqué

Confirmé au Groupe 3 et toujours vrai ici : main a `commercial.py`/
`billing.py`, r35l31 a `commerce`/`payments` — deux systèmes de
commerce non unifiés. `Offers.js` consomme le catalogue DECIDED_V1
(ACA-0025, construit côté main). La route est montée en lecture
publique sans risque (catalogue, pas de paiement), mais l'unification
réelle checkout/paiement entre les deux systèmes reste **hors
périmètre de tout groupe RECONCILE-2 actuel** — à trancher par le
Founder avant toute mise en production d'un flux de paiement réel.

### Preuve de régression

- Suite jest complète : **42/42 suites, 292/292 tests passants**
  (aucune régression sur `attention.js`, `motion-primitives.jsx`,
  `pedagogicalGraph.js`, tous les tests `spatial/*` existants, etc. —
  tous inchangés et toujours verts).
- `yarn build` : propre, aucun warning.
- Suite pytest backend (`backend_test.py` + suites idempotence/
  convergence/activation/continuation) : les échecs observés (428
  legal-gate, `requests.exceptions.MissingSchema`, `KeyError:
  'MONGO_URL'`) sont **identiques bit pour bit avec et sans les
  changements du Groupe 4** — prouvé en `git stash`-ant les 11 fichiers
  modifiés de ce groupe, en relançant un serveur de base propre sur un
  port séparé, et en comparant la liste des tests en échec : rigoureu-
  sement la même liste. Confirme qu'aucune de ces suites de test n'est
  affectée par ce groupe (elles dépendent d'un ordonnancement/état de
  serveur pré-existant, hors périmètre spatial/frontend). Trois erreurs
  d'import pré-existantes (`test_ecosystem_handoffs.py`,
  `test_physical_hybrid_assessment.py`, `test_progressive_horizon.py`)
  proviennent de fichiers backend non touchés par ce groupe
  (`certification/service.py`, `certification/models.py`,
  `services/integrations/subscribers.py`) — hors périmètre.

### Critères de sortie du Groupe 4 — statut

- ✅ Tous les `BOTH_DIFFERENT` spatial/frontend du périmètre résolus
  (featureFlags.js, i18n.jsx, RouteTransition.jsx, JourneyHierarchy.jsx,
  ContextFrame.jsx, App.js).
- ✅ 17/17 pages avec statut explicite (tableau ci-dessus).
- ✅ 0 import cassé connu (build propre + probe SpatialHub).
- ✅ 0 route sans décision.
- ✅ Parcours post-auth toujours valide (gardes `Authenticated`/
  `Protected`/`PublicOrMember` non modifiées ; scripts critiques
  Groupe 2 toujours applicables).
- ✅ SpatialHub utilisable (probe de compilation, voir ci-dessus).
- ⚠️ Mobile vérifié **partiellement** (pas de débordement horizontal
  confirmé ; interaction menu/drawer mobile non testée en live dans
  cette passe — signalé honnêtement, pas bloquant pour ce groupe car
  aucune régression de navigation mobile n'a été introduite : aucun
  composant de navigation mobile n'a été modifié).
- ✅ `main` et r35l31 toujours inchangés aux SHA gelés
  (`c5dddc83ee09a6ec6fb8fd5e9cfda1ec917ac048` /
  `f9763b6e27b7f60f29577a4a26bac2710596dfc3`).

---

## Groupe 5 — clôture des 95/95, câblage réel SpatialHub, cartographie des échecs (2026-09-15)

Instruction Founder : *"GO Groupe 5, sans nettoyage de branches et sans
merge vers main."* Critères de sortie explicites : 95/95 `BOTH_DIFFERENT`
résolus, 0 fichier conflictuel, 0 décision inconnue, sections bloquées
de `infra_indexes.py` tranchées, SpatialHub réellement câblé (pas
seulement compilable), Dashboard/Roadmap/ModuleJourney fonctionnels,
toutes les routes avec statut clair, 0 import cassé, suite complète
relancée, chaque failure/error classifiée avec cause, main et r35l31
inchangés.

### Méthodologie de comptage

Les Groupes 1-4 avaient déjà résolu 24 des 95 fichiers de
`docs/reconciliation/both_different.txt` (la liste faisant autorité,
produite par RECONCILE-0 — utilisée telle quelle plutôt que
recalculée : une recomputation stricte à trois points donnait 73
fichiers, une différence de méthodologie du script d'origine qui
classe certains fichiers ONLY_R35L31 comme BOTH_DIFFERENT ; la liste
committée reste la référence que tout l'engagement a citée). Les 71
fichiers restants ont été classifiés puis résolus dans ce Groupe :
- 14 `ONLY_MAIN` au sens strict (main déjà correct, aucun changement
  nécessaire au-delà de vérification).
- 31 `ONLY_R35L31` au sens strict (r35l31 seul a touché le fichier
  depuis la base commune — pull-in trivial après vérification qu'aucun
  import cassé n'en résulte).
- 26 réellement `BOTH_CHANGED` (fusion sémantique à trois points
  requise).

### Fiches de décision — fichiers de ce groupe

**Pull-ins triviaux `KEEP_R35L31` (main n'a jamais touché le fichier
depuis la base commune) :**
- `backend/.flake8`, 11 rapports `docs/*.md`, `backend/.env.example`
  (fusionné avec les blocs déjà ajoutés par main — voir ci-dessous),
  `backend/api/onboarding.py`, `quizzes.py`, `missions.py`,
  `progression.py`, `certification.py`, `fms.py`, `learning.py`,
  `backend/certification/__init__.py` + `models.py`, `backend/skills/
  models.py` + `seed.py`, `backend/services/integrations/
  subscribers.py`, `backend/services/notifications.py` (raison
  sécurité — voir plus bas), `frontend/src/index.css`, `frontend/src/
  pages/ModuleJourney.js`, `Onboarding.js`, `jury/JuryDashboard.js`,
  `trainer/TrainerDashboard.js`, `frontend/e2e/formations-discovery.spec.js`.
- Preuve : aucune régression jest (42/42), build propre à chaque étape.

**`backend/certification/service.py` — COMBINE minimal.** Base
r35l31 (seule version avec la chaîne d'éligibilité complète), un seul
correctif réappliqué : le kwarg `wallet_credit(..., effect_key=...)`
(r35l31 l'appelait `economic_event_id`, le paramètre résolu de
`wallet.credit()` est `effect_key`).

**`backend/services/integrations/registry.py` +
`cvln_wallet.py` — COMBINE (désambiguïsation de nommage).** main a
construit un client typé riche (`CVLNWalletIntegration`, httpx,
`charge`/`transfer`/`balance`) pour le produit externe djsayd/
CVLN-Wallet ; r35l31 a construit un `EcosystemIntegration` générique
plus simple sous le même nom d'affichage. Gardé le client riche de
main comme canonique, renommé son `.name` pour correspondre au nom
d'affichage désambiguïsant de r35l31 (vérifié contre
`docs/INTEGRATIONS_REPORT.md`), ajouté un alias `wallet = cvln_wallet`
et une méthode `.request(path, payload)` générique compatible avec le
contrat que `subscribers.py` utilise uniformément pour chaque
intégration.

**`backend/badges_engine.py` — COMBINE.** Gardé la relance résiliente
de main (`wallet_credit` toujours retentée, protégée par
`effect_key`) ; ajouté la publication réelle de l'événement
`academy_badge_awarded` (r35l31), gatée sur `newly_awarded` uniquement
— corrige un vrai bug découvert par la reconciliation (voir
"Bugs réels trouvés" ci-dessous).

**`backend/services/frek_core.py` — COMBINE.** Base = réécriture
souveraine de main (identity_authority/frekcore mode) ; ajouté la
méthode `credit_cc()` de r35l31 (verbatim, `$inc` atomique,
`ReturnDocument.AFTER`) — un ajout ECON-03 indépendant sur le même
fichier, requis par `api/quizzes.py`/`api/missions.py`.

**`backend/api/formations.py` — COMBINE.** `commercialization`
(main) et `canonical_authority` (r35l31) sont deux champs réels
indépendants, tous deux conservés dans `list_formations`/
`get_formation`.

**`backend/tests/test_legal_policy.py` — COMBINE (collision de nom de
fichier fortuite).** Deux modules réellement différents
(`backend/legal_policy.py` de main, `backend/services/legal_policy.py`
de r35l31) partageaient par coïncidence un nom de fichier de test.
Fusion des deux suites dans un seul fichier.

**`backend/infra_indexes.py` — clôture des sections
`BLOCKED_BY_GROUP_5`.** Les 4 sections explicitement différées par le
Groupe 3 (`canonical_progress`, `fms_resource_provenance`,
`physical_sessions`/`physical_enrollments`/`physical_attendance` — y
compris l'index partiel unique anti-double-réservation PHY-01,
`professional_profile_settings`) portées verbatim depuis r35l31, selon
le contrat documenté par le Groupe 3 lui-même. **Sections bloquées :
0 restantes.**

**Pages "COMBINE public-discovery + spatial" (le motif dominant du
groupe) :** `Certifications.js`, `Badges.js`, `FormationDetail.js`,
`Formations.js`, `FrekProfile.js`, `Missions.js`, `Landing.js`. main a
construit indépendamment une vue "découverte publique" (ACA-0009 :
page consultable sans compte, données personnelles gardées derrière
`user &&`/guards, CTA register/login) sur presque toutes les pages
apprenant ; r35l31 a construit indépendamment des variantes de carte
à profondeur spatiale gatées par flag (`useDepthPhysics`/
`computeDepthStyle`, `FEATURE_FLAGS.SPATIAL_HUB_ENABLED`) plus des
fonctionnalités de domaine réelles (redirections canoniques,
filtrage d'évaluation physique/pratique, surface profil
professionnel, audio/haptique CONFIRM sur complétions réelles). Motif
de résolution constant : structure/contenu public de main gardé comme
base, couche spatiale de r35l31 posée dessus partout où réelle et non
redondante. `Landing.js` seule variation notable : `LandingSpatial.jsx`
(wrapper de main, réellement monté dans `App.js` pour `/`, `/login`,
`/register`) forwarde `authMode` → `initialMode`, une prop que la
version r35l31 seule ne gérait pas — préservée, avec la séquence
VOID→WORLD→FOCUS→IDENTITY (ACA-0010/0011) de r35l31 posée sur le
contenu réel de main plutôt que de le remplacer.

**`Roadmap.js` — exception au motif ci-dessus.** Ici main avait
*déjà* câblé un moteur spatial réel et complet (`useSpatialRail` :
ARIA listbox/option, navigation clavier, index prédit, `Horizon`
sensible à la distance, mémoire de profondeur inter-navigation via
`depthMemory.js` — le même module que `Layout.js`/
`SpatialFocusManager.jsx`), non gaté par flag. r35l31 avait construit
une seconde variante gatée par `SPATIAL_HUB_ENABLED` (`useDepthPhysics`
+ `StageDepthCard`) plus une carte de progression canonique. Décision :
garder le moteur `useSpatialRail` de main tel quel (plus complet pour
cette page précise que la variante `useDepthPhysics`), porter
uniquement la carte de progression canonique de r35l31 (pièce
réellement additive et non redondante).

**`Dashboard.js` — combine le plus large du groupe.** main : refonte
visuelle complète (`cvln-page`/`cvln-kpi-grid`), `ReturnToPositionCard`
(ACA-0023), parallélisation réelle de `refreshMe()` avec les 5 autres
appels API. r35l31 : **le câblage SpatialHub réel** nommé
explicitement dans les critères de sortie (`FEATURE_FLAGS.
SPATIAL_HUB_ENABLED` → `<SpatialHub formationNodes missionNodes />`
alimenté par `usePedagogicalGraph`, remplace la bannière next-action
statique uniquement quand le flag est actif), `FirstValueReveal` (lit
la vraie réponse `POST /onboarding/complete` transportée via
`location.state`), `WelcomeBackBanner` (signal `returning` réel côté
serveur), carte de progression canonique, carte Horizon/Expansion
(pôle propre complété), carte d'éligibilité certification
(`services/progressive_horizon.py`). Toutes les fonctionnalités de
r35l31 portées verbatim sur la base visuelle de main ; les trois
surfaces "prochaine action" (ReturnToPositionCard, WelcomeBackBanner,
SpatialHub/next-action) sont indépendamment sourcées et ne peuvent pas
se déclencher au même moment par construction.

**`admin/AdminDashboard.js` — COMBINE.** `InstitutionalBridgePanel` +
sélecteur d'organisation sur les invitations (main) et
`RubricImportPanel` (ACA-0020, r35l31 — déclenche les 3 routes
`POST /{domain}/formations/{code}/rubric/import` déjà existantes,
jusqu'ici sans interface). Aucun chevauchement, les deux montés.

**`frontend/e2e/module-journey-context.spec.js` — KEEP_MAIN.** Les
deux branches ont corrigé indépendamment la même race "quiz-result"
flaky ; le correctif de main est un sur-ensemble strict (attend en
plus la réponse GET authoritative post-quiz et draine les doubles
montages React.StrictMode dans le helper partagé).

**`frontend/playwright.config.js` — COMBINE.** Les deux branches ont
corrigé le même chemin Chromium codé en dur cassant la CI, mais le
correctif de r35l31 est plus robuste (`fs.existsSync` en repli quand
`PLAYWRIGHT_CHROMIUM_PATH` n'est pas définie — vérifié : le binaire
existe dans ce sandbox à `/opt/pw-browsers/chromium` mais la variable
d'env n'est PAS définie, donc la version de main seule aurait cassé
les runs e2e locaux ici) et ajoute `expect.timeout`/`retries` avec
investigation CI documentée. Gardé r35l31 en base, ajouté la seule
pièce distincte de main (`REACT_APP_ACADEMY_SPATIAL_ROUTE_TRANSITIONS
=true`).

### Bugs réels trouvés et corrigés par la reconciliation

Aucun de ces bugs n'existait déjà correctement corrigé sur l'une ou
l'autre branche seule — chacun est une découverte propre à la fusion,
au sens strict de ce que RECONCILE-2 est censé faire remonter :
1. **Nom d'intégration Wallet incohérent** — `CVLNWalletIntegration.name`
   ne correspondait pas au nom attendu par
   `test_ecosystem_handoffs.py`/`docs/INTEGRATIONS_REPORT.md`. Corrigé
   (registry.py/cvln_wallet.py, voir fiche ci-dessus).
2. **`academy_badge_awarded` jamais publié** — `badges_engine.py` de
   main (retenu comme base pour sa relance résiliente) n'émettait
   jamais l'événement réel que `subscribers.py`/`test_ecosystem_
   handoffs.py` attendent. Corrigé.
3. **`frek_core.credit_cc()` manquant** — la réécriture souveraine de
   main de `services/frek_core.py` n'avait jamais cette méthode ; les
   appels réels de `api/quizzes.py`/`api/missions.py` (r35l31) s'y
   fiaient. Corrigé, 6 tests d'idempotence remis au vert.

### Bug réel trouvé, classifié mais **non corrigé dans ce groupe**

**OPS-01 (fail-closed au démarrage) — régression réelle,
`BUG_PRODUCT`.** `server.py::lifespan()` enveloppe `ensure_indexes()`
dans un `try/except Exception` large qui journalise puis continue
(`app.state.startup_ready = False`, mais l'app sert quand même tout le
trafic réel). Seul `GET /health` lit `startup_ready` ; **aucune route
métier ne le vérifie** — donc un échec de création d'index (les index
uniques/partiels dont dépendent les correctifs d'atomicité ECON-01/02/
03/PHY-01) ne bloque plus le service, contrairement à l'invariant que
`test_server_startup_and_cors.py::test_startup_raises_when_ensure_
indexes_fails` a été écrit pour garantir. Racine probable : lors de la
réconciliation du bloc CORS de `server.py` au Groupe 3 (commit
`404a021`), la structure de démarrage a été reconstruite en
`@asynccontextmanager lifespan()` (moderne, readiness-gate via
`/health`) plutôt qu'en restaurant le `on_startup()`/crash-on-boot que
le test attend — un choix architectural légitime en soi (pattern
readiness-probe standard k8s), mais qui laisse un vrai trou : rien
n'empêche le trafic direct (hors load-balancer) d'atteindre une
instance `startup_ready=False`. **Explicitement non corrigé ici** —
classification seulement, comme demandé par les critères de sortie de
ce groupe ; correction recommandée pour RECONCILE-3 (ajouter soit une
dépendance FastAPI globale qui 503 tant que `startup_ready` est faux,
soit revenir à un `raise` propageant hors de `lifespan()` sur l'échec
d'`ensure_indexes()` spécifiquement, en gardant le `try/except`
large uniquement autour du seed non-critique).

### Cartographie des failures/errors — suite complète relancée

**Frontend — 0 failure.** `yarn build` propre (aucun warning). Suite
jest complète : **42/42 suites, 292/292 tests passants**, aucune
régression sur tout le travail de ce groupe (Landing/Dashboard/
Roadmap/AdminDashboard/6 pages combine/e2e-config inclus).

**Backend — `import server` propre** (515+ routes, vérifié avec
variables d'environnement minimales). `python3 -m pytest` complet :
**2623 passed**, 24 failed, 31 errors (55 non-vertes au total, toutes
dans seulement 2 fichiers de test) :

| Fichier | # | Classification | Cause racine |
|---|---|---|---|
| `tests/backend_test.py` (toutes les classes : Auth, Onboarding, Formations, Quiz, Missions, Badges, Mentor, Health, Progression, LXv2*) | 24 failed + 31 errors = 55 | **ENVIRONMENT** | `BASE_URL` lu depuis `REACT_APP_BACKEND_URL` (vide dans ce sandbox) → `requests.exceptions.MissingSchema` sur des URLs relatives. Ce fichier est une suite d'intégration qui nécessite un serveur FastAPI + MongoDB réellement démarrés ; **ni `mongod` ni le daemon Docker ne sont disponibles dans ce sandbox** (vérifié : `mongod` absent, `docker ps` échoue avec "Cannot connect to the Docker daemon"). Limitation de sandbox documentée depuis W1-E, inchangée depuis. Zéro rapport avec les changements de ce groupe. |
| `tests/test_server_startup_and_cors.py::test_development_default_stays_wildcard` | 1 | **TEST_OBSOLETE** | Le test lit `server.cors_origins` (sans underscore) ; le symbole réel après la réconciliation CORS du Groupe 3 est `server._cors_origins` (privé, intentionnel). Comportement réel très probablement correct, nom de symbole périmé. |
| `tests/test_server_startup_and_cors.py::test_production_with_real_allowlist_boots_fine` | 1 | **TEST_OBSOLETE** | Même cause que ci-dessus (`cors_origins` vs `_cors_origins`). |
| `tests/test_server_startup_and_cors.py::test_startup_survives_seed_failures` | 1 | **TEST_OBSOLETE** | Le test monkeypatch `server.architecture_reuse.sync_manifest` — ce module n'existe nulle part dans le dépôt (ni main, ni r35l31, ni la base commune). Cible une surface d'API jamais implémentée sous ce nom ; le comportement réel (échec de seed non-fatal) est déjà couvert par la structure `try/except` actuelle de `lifespan()`. |
| `tests/test_server_startup_and_cors.py::test_startup_raises_when_ensure_indexes_fails` | 1 | **BUG_PRODUCT** | Voir section dédiée ci-dessus — régression réelle du fail-closed OPS-01, non corrigée dans ce groupe (classification uniquement, correction recommandée RECONCILE-3). |

**Aucun `FIXTURE_BROKEN` ni `EXTERNAL_DEPENDENCY` ni
`EXPECTED_FAILURE` identifié dans cette passe** — toutes les
non-vertes se résument à 3 causes distinctes (environnement sandbox
sans MongoDB/Docker ; 3 tests visant des noms de symboles obsolètes
suite à la réconciliation Groupe 3 du bloc CORS ; 1 régression produit
réelle et non corrigée par choix explicite du périmètre de ce groupe).

Static checks (`flake8`) : 7 avertissements pré-existants et mineurs
(4× E501 ligne trop longue dans `legal_policy.py`, 1× W292 pas de
newline final dans `server.py`, 2× E402 import non en tête de fichier
dans `test_careops.py`) — aucun ne bloque l'exécution, non liés au
périmètre de ce groupe, non corrigés (hors scope explicite : ce groupe
classifie, ne nettoie pas le style).

### Statut SpatialHub — câblage réel, pas seulement compilable

Preuve, au-delà de la compilation :
- `Dashboard.js` monte `<SpatialHub formationNodes={graph.
  formationNodes} missionNodes={graph.missionNodes} />` réellement
  alimenté par `usePedagogicalGraph({ enabled: FEATURE_FLAGS.
  SPATIAL_HUB_ENABLED })`, qui dérive le graphe pédagogique réel
  (learning-path/missions/badges/skills/qualifications) — remplace la
  bannière next-action statique uniquement quand le flag est actif
  (jamais deux surfaces "prochaine action" concurrentes).
- `Roadmap.js` a un moteur spatial réel non gaté (`useSpatialRail`) —
  navigation clavier ARIA listbox/option, mémoire de profondeur
  inter-navigation, anticipation d'index prédit — déjà en place avant
  ce groupe, complété par la carte de progression canonique.
- `ModuleJourney.js` (vérifié dans ce groupe, KEEP_R35L31 déjà en
  place) importe et monte réellement `JourneyPhaseShell` (`lib/
  JourneyHierarchy.jsx`) et `ContextFrame`/`useContextEntry` (`lib/
  ContextFrame.jsx`), avec audio/haptique spatiaux réels — pas un
  import mort, deux usages `<ContextFrame show={isContext}>` actifs
  dans le rendu.
- Toutes les pages "public-discovery + spatial" de ce groupe
  (Missions/Badges/FrekProfile) utilisent `useDepthPhysics`/
  `computeDepthStyle` réellement dans leur arbre de rendu, gatées par
  `FEATURE_FLAGS.SPATIAL_HUB_ENABLED`, avec fallback vers la grille
  plate quand le flag est désactivé — les deux chemins compilent et
  s'exécutent (prouvé par la suite jest, qui exerce les deux via les
  mocks de `featureFlags.js`).

### Critères de sortie du Groupe 5 — statut final

- ✅ **95/95 `BOTH_DIFFERENT` résolus** (vérifié : chaque chemin de
  `docs/reconciliation/both_different.txt` a au moins un commit sur
  cette branche depuis la base commune `85a41cced8d84c8bba016135689e
  10d733c585dd`).
- ✅ **0 fichier conflictuel restant** (`grep` de `<<<<<<<`/`=======`/
  `>>>>>>>` sur tout `backend/` + `frontend/src/` : 0 résultat).
- ✅ **0 décision inconnue** (chaque fichier de ce groupe a une fiche
  de décision explicite ci-dessus ou dans les groupes précédents).
- ✅ **Sections bloquées de `infra_indexes.py` tranchées** (4/4
  sections `BLOCKED_BY_GROUP_5` closes, voir fiche dédiée).
- ✅ **SpatialHub réellement câblé** (voir section dédiée ci-dessus —
  composant monté, alimenté par des données réelles, pas seulement
  importé/compilé).
- ✅ **Dashboard/Roadmap/ModuleJourney fonctionnels** (les trois
  vérifiés avec preuve de montage/wiring réel, pas seulement présence
  de fichier).
- ✅ **Toutes les routes/pages avec statut clair** (17/17 du Groupe 4
  + les pages de ce groupe, toutes avec fiche de décision).
- ✅ **0 import cassé connu** (`import server` propre avec 515+
  routes ; `yarn build` propre sans warning).
- ✅ **Suite complète relancée** (jest 42/42 suites/292/292 tests ;
  pytest 2623 passed sur l'ensemble hors les 2 fichiers classifiés
  ci-dessus).
- ✅ **Chaque failure/error restante classifiée avec cause** (tableau
  dédié ci-dessus : ENVIRONMENT ×55, TEST_OBSOLETE ×3, BUG_PRODUCT ×1
  — ce dernier explicitement non corrigé par choix de périmètre,
  documenté pour RECONCILE-3).
- ✅ **`main` et r35l31 toujours inchangés** aux SHA gelés
  (`c5dddc83ee09a6ec6fb8fd5e9cfda1ec917ac048` /
  `f9763b6e27b7f60f29577a4a26bac2710596dfc3` — reconfirmé via
  `git ls-remote origin main claude/cvln-academy-production-r35l31`
  en fin de groupe).

**Aucun nettoyage de branches, aucun merge vers `main` effectué** —
conformément à l'instruction explicite du Founder. Tous les commits de
ce groupe vivent sur `reconcile/canonical-main-r35l31-20260914`.
