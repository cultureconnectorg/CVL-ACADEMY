# ACA-0004 — Delivery Architecture Truth: Implementation Report

**Status: VERIFIED.**
**Date: 2026-09-04.**
**Branch: `claude/cvln-academy-canonical-fms`.**

## 1. What this closes

ACA-0004 was blocked (see this session's earlier exchange) because the
canonical FMS ZIP (223 docs) contains **zero** real delivery-mode signal —
confirmed by exhaustive grep against the archive during ACA-0006. No
delivery taxonomy exists anywhere in the curriculum content, and none
should be expected to: the Founder's resolving decision states this
explicitly.

The Founder resolved the blocker with an explicit architecture rule,
verbatim:

```
CURRICULUM_TRUTH = FMS ZIP 223 DOCS

DELIVERY_ARCHITECTURE_TRUTH = INTERNAL / EXTERNAL / BRIDGE

INTERNAL_DELIVERY = E_LEARNING
EXTERNAL_DELIVERY = E_LEARNING + PHYSICAL/PRESENTIEL
                     (as configured by the external offer)
BRIDGE = ENTRY / ARTICULATION LAYER

CURRICULUM != DELIVERY
DELIVERY != COMMERCIAL_OFFER
```

Three distinct truths are now formally separated in the codebase:

| Truth | Source | Package |
|---|---|---|
| **Curriculum** | FMS ZIP (223 docs) | `fms_canonical` (existing, ACA-0005/0006) |
| **Delivery architecture** | `db.formations.contexts` (real, pre-existing field) | `fms_canonical.delivery_architecture` (new, this report) |
| **Commercial offer** | Not built | `ACA-0007`/`ACA-0025` — out of scope |

## 2. Why `contexts` and not a new field

`Formation.contexts: List[AcademyContext]`
(`AcademyContext = Literal["INTERNAL","EXTERNAL","BRIDGE"]`, `backend/
models.py`) is a **real, already-served** field, populated for every
formation — including all 6 FMS métiers — by the existing
`catalog_cartography.py`. It is not new data, not invented, not migrated:
it is the exact shape of truth the Founder's rule names, already sitting
in `db.formations`.

Real values confirmed by direct inspection:

| Formation | `contexts` |
|---|---|
| FMS-01 | `INTERNAL, EXTERNAL, BRIDGE` |
| FMS-02 | `EXTERNAL, BRIDGE` |
| FMS-03 | `EXTERNAL, BRIDGE` |
| FMS-04 | `EXTERNAL, BRIDGE` |
| FMS-05 | `EXTERNAL, BRIDGE` |
| FMS-06 | `INTERNAL, EXTERNAL, BRIDGE` |

No formation has ever had an empty `contexts` list, so `derive_delivery_
architecture` never needs a fabricated default — every real formation
resolves to at least one delivery mode.

This also formally supersedes the `AMBIGUOUS` finding on `catalog_
cartography.DELIVERY_FORMATS` from `docs/ACADEMY_DELIVERY_MODE_AUDIT.md`
(see addendum added to that file). `delivery_formats` (`PRO_FORMAT`/
`DEFAULT_FORMAT`, near-identical across formations) is left exactly as-is
— untouched, per `DB_FORMATIONS_MUTATION = FORBIDDEN` — simply no longer
the input this derivation reads.

## 3. What was built

**`backend/fms_canonical/delivery_architecture.py`** (new):

- `derive_delivery_architecture(formation_code, contexts) ->
  DeliveryArchitecture` — pure function, the Founder's rule applied
  mechanically:
  - `"INTERNAL" in contexts` → `E_LEARNING / INTERNAL / AVAILABLE`
  - `"EXTERNAL" in contexts` → `E_LEARNING / EXTERNAL / AVAILABLE` **and**
    `PHYSICAL / EXTERNAL / ELIGIBLE_PENDING_OFFER`
  - `"BRIDGE" in contexts` → `is_bridge_entry_point = True` (BRIDGE is an
    entry/articulation layer, not itself a delivery mode — it never adds a
    `DeliveryModeEntry`)
- `get_delivery_architecture(formation_code) -> Optional[
  DeliveryArchitecture]` — the **one** read of `db.formations` in the
  entire `fms_canonical` package (every other module in it never touches
  that collection). Read-only, `contexts` field only, no write, `None` on
  unknown formation rather than a fabricated default.

**`DELIVERY != COMMERCIAL_OFFER` enforcement**: `PHYSICAL` is **never**
marked `AVAILABLE` — only `ELIGIBLE_PENDING_OFFER`. This mirrors the
original delivery-mode mission's `PHYSICAL_SESSION_AVAILABILITY =
REAL_DATA_ONLY` rule and holds until `ACA-0007` (physical domain model,
not yet authorized) builds real bookable sessions.

**API**: `GET /api/canonical/formations/{formation_code}/delivery-
architecture` (`backend/api/canonical.py`), authenticated
(`get_current_user`, matching every other route in this router —
`PUBLIC_DISCOVERY_ACTIVATION` stays out of scope here too), 404 on
unknown formation.

**Response model** (`DeliveryArchitecture`):
```json
{
  "formation_code": "FMS-01",
  "contexts": ["INTERNAL", "EXTERNAL", "BRIDGE"],
  "delivery_modes": [
    {"mode": "E_LEARNING", "channel": "INTERNAL", "status": "AVAILABLE"},
    {"mode": "E_LEARNING", "channel": "EXTERNAL", "status": "AVAILABLE"},
    {"mode": "PHYSICAL", "channel": "EXTERNAL", "status": "ELIGIBLE_PENDING_OFFER"}
  ],
  "is_bridge_entry_point": true,
  "curriculum_source": "FMS_ZIP",
  "delivery_source": "ACADEMY_CARTOGRAPHY_CONTEXTS"
}
```

## 4. Tests (10 new, all in `backend/tests/test_fms_canonical.py`)

1. `test_derive_internal_only_context` — INTERNAL-only → exactly one
   `E_LEARNING/INTERNAL/AVAILABLE` mode, nothing else.
2. `test_derive_external_only_context_never_marks_physical_available` —
   EXTERNAL-only → `PHYSICAL` present but `ELIGIBLE_PENDING_OFFER`, never
   `AVAILABLE`.
3. `test_derive_bridge_is_not_a_delivery_mode` — BRIDGE alone yields
   `is_bridge_entry_point=True` and **zero** delivery modes.
4. `test_derive_all_three_contexts_fms01_shape` — reproduces FMS-01/FMS-06's
   real shape (all 3 contexts) → 3 modes, bridge flag true.
5. `test_curriculum_and_delivery_sources_stay_distinct` — `curriculum_
   source == "FMS_ZIP"` and `delivery_source ==
   "ACADEMY_CARTOGRAPHY_CONTEXTS"` are never equal/confused.
6. `test_no_delivery_mode_is_ever_available_without_a_matching_context` —
   property test: no `AVAILABLE` mode appears whose channel isn't in
   `contexts`.
7. `test_get_delivery_architecture_reads_real_db_formations_contexts` —
   end-to-end against a mocked `db.formations` document.
8. `test_get_delivery_architecture_unknown_formation_returns_none` — no
   fabricated default.
9. `test_all_six_real_fms_contexts_never_yield_available_physical` — runs
   the derivation against the real, confirmed `contexts` value for all 6
   FMS métiers; asserts `PHYSICAL` is never `AVAILABLE` for any of them.
10. `test_delivery_architecture_route_requires_real_authentication` — the
    new route 401s without a token, same as every sibling route.

**Results**: `test_fms_canonical.py` 39/39 pass (29 pre-existing + 10 new).
Full backend pure-unit suite: **113/113 pass**. Server boot check confirms
the route registers at `/api/canonical/formations/{formation_code}/
delivery-architecture`. `black --check`, `isort --profile black
--check-only`, `flake8` all clean. `mypy` shows 0 new errors (only the 7
pre-existing, unrelated reportlab/yaml stub errors in `certification/
attestation.py`, `template_engine/export.py`, `fms_import/parser.py`
remain).

## 5. Binary rules honored

- `DB_FORMATIONS_MUTATION = FORBIDDEN` — `delivery_architecture.py` never
  writes to `db.formations`; its one read is a projected, read-only
  `find_one`.
- `PHYSICAL_SESSION_AVAILABILITY = REAL_DATA_ONLY` — `PHYSICAL` is never
  `AVAILABLE`, only `ELIGIBLE_PENDING_OFFER`; no fabricated session data.
- `NO_INVENTED_PRODUCT` — no new field was added to `Formation`/
  `db.formations`; the derivation reads the field that already exists.
- `EVIDENCE_FIRST` — all 6 real `contexts` values were confirmed by direct
  inspection before writing the derivation, and are pinned in test #9.
- `CURRICULUM != DELIVERY`, `DELIVERY != COMMERCIAL_OFFER` — enforced
  structurally: two disjoint source fields (`curriculum_source` /
  `delivery_source`) on the response model, and `PHYSICAL` status never
  reaching `AVAILABLE` without `ACA-0007`.

## 6. Gate status

**ACA-0004 = VERIFIED.**
`CODE_PATH_VERIFIED = TRUE` (full suite + mypy/lint/boot-check, as above).
`STOP = TRUE` — no further scope taken. `ACA-0007` (physical domain
model), `ACA-0019`, and everything else in the backlog remain
`NOT_AUTHORIZED` pending explicit Founder authorization.
