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
