# RECONCILE-2 — fiches de décision par fichier `BOTH_DIFFERENT`

Discipline appliquée : un fichier conflictuel n'est "résolu" que s'il
conserve les capacités utiles des deux côtés ET respecte l'architecture
actuelle de main ET a une preuve de test réelle — pas seulement "ça
compile". Commits séparés par zone critique (aucun commit ne mélange
noyau backend / auth / wallet / spatial / App.js).

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
