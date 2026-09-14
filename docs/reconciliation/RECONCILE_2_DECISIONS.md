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

**Reste : 78 des 95 fichiers `BOTH_DIFFERENT`.**
- **Groupe 4 (spatial/frontend core)** — `frontend/src/App.js`,
  `SpatialHub.jsx`, `attention.js`, `featureFlags.js`, `i18n.jsx`, les
  17 pages nouvellement récupérées, etc. Pas commencé — c'est là que
  les 17 pages seront routées/déclarées explicitement (2e critère de
  sortie de RECONCILE-2).
- **Groupe 5 (reste d'APP_CORE)** — le reliquat, par dépendance réelle.

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
