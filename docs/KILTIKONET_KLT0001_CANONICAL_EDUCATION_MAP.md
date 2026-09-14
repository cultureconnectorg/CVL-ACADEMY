# KLT-0001 — Kiltikonet Canonical Education Map

```
WORKSTREAM = KLT (new, separate from ACA/FMS)
FMS_CLOSED = TRUE
KLT_WORKSTREAM = ACTIVE
NO_CROSS-CONTAMINATION = TRUE
METHOD = AUDIT -> CANONICALIZE -> FREEZE -> BUILD -> TEST -> VERIFY -> STOP
THIS_TICKET_PHASE = AUDIT + CANONICALIZE + FREEZE (top-level map only)
MODULES_WRITTEN = FALSE (explicitly out of scope for KLT-0001, per Founder instruction)
DB_MUTATION = FALSE (documentation-only deliverable)
STOP_AFTER_DELIVERY = TRUE
```

**Source of truth for this ticket**: `CVLN_Academy_Kiltikonet_Formation_
Master_Plan.xlsx` (uploaded this session), 6 sheets — *Vue d'ensemble*,
*Architecture documentaire*, *Plan modules*, *Cas fil rouge*, *Production
documentaire*, *Dépendances produit*. Every fact below cites the sheet it
came from, or the exact repo file/line it was cross-checked against — no
concept is asserted from memory.

---

## 1. Headline finding — a real code collision, not yet resolved

**`KLT-01` through `KLT-05` are not new codes.** They already exist, live,
in this repo — seeded formations with their own titles, badges, and
module sets — predating this master plan. The new canonical plan reuses
the same 5 codes for **different-scoped formations**, and adds 3 new ones
(`KLT-06`/`07`/`08`).

| Code | **Legacy (live in repo)** | **Canonical (this master plan)** | Same code, different scope? |
|---|---|---|---|
| KLT-01 | *Fondamentaux de la médiation culturelle caribéenne* — 42h, 9 modules (M01–M09), badge `Kiltikonet Ambassador` (`seed_data.py:606-618`, `seed_modules.py:551-634`) | *Médiateur culturel* — 8 modules (M01–M08) planned | **YES** — same job family (médiation), different title, different module count/boundary |
| KLT-02 | *Montage et gestion de projets culturels* — 56h, 10 modules, badge `Cultural Project Manager` (`seed_data.py:620-632`) | *Chef de projet culturel* — 8 modules planned | **YES** — same job family, different title/scope |
| KLT-03 | *Stratégie institutionnelle et partenariats* — 44h, 9 modules, badge `Institutional Strategist` (`seed_data.py:634-646`) | *Responsable partenariats institutionnels culturels* — 8 modules planned | **YES** |
| KLT-04 | *Gouvernance associative et juridique culturelle* — 38h, 8 modules, badge `Governance Associative` (`seed_data.py:648-660`) | *Gouvernance des organisations et réseaux culturels* — 8 modules planned | **YES** — legacy is association-law-specific; canonical is broader network governance |
| KLT-05 | *Kiltikonet comme plateforme* — 40h, 8 modules, badge `Kiltikonet Platform Operator` (`seed_data.py:662-674`) | *Opérateur Kiltikonet / Cultural Platform Operator* — 9 modules planned | **YES**, closest match of the five, but module count/boundary still differs |
| KLT-06 | *(does not exist — confirmed, zero hits anywhere in the repo)* | *Analyste Observatory / Cultural Data Analyst* — 8 modules planned | No collision — genuinely `NEW` |
| KLT-07 | *(does not exist)* | *Responsable déploiement territorial culturel* — 8 modules planned | No collision — `NEW` |
| KLT-08 | *(does not exist)* | *Responsable qualité, conformité & audit réseau* — 8 modules planned | No collision — `NEW` |

Legacy `KLT-01..05` are also referenced beyond `seed_data.py`/
`seed_modules.py`: `catalog_cartography.py:197-287` (cartography, incl. a
real `contexts` field — see §3), `external_calibration.py:374-479`
(strategic sizing estimates), and `MIS-KLT-01` (a mission,
`seed_data.py:1160-1186`, `backend_test.py:391-394`). No frontend surface
exists for Kiltikonet under any code (`frontend/src` — zero hits for
`Kiltikonet`/`KLT-0`), so the collision is a backend/catalog fact only,
not a rendered-UI one.

**This mirrors exactly the FMS legacy-vs-canonical collision resolved by
ACA-0005/0006** (legacy dashed codes vs. canonical filenames, module
lineage). Per `NO_CROSS-CONTAMINATION = TRUE`, this document does **not**
merge, rename, or otherwise touch the legacy KLT-01..05 records — they
stay exactly as seeded, untouched, per `DB_FORMATIONS_MUTATION =
FORBIDDEN` (carried over from the FMS-era binary rules; no reason to
believe it lapsed for a new workstream). **A `KLT`-equivalent of ACA-0005
(a collision/lineage strategy) will be needed before any canonical KLT
formation is bound into the runtime** — flagged here as a prerequisite for
a future ticket, not resolved by this one.

## 2. KLT_MASTER_MAP_v1 — the 8 canonical formations (FROZEN)

Source: *Vue d'ensemble* sheet, rows 1–8.

| # | Code | Formation / spécialisation | Type (raw, source) | Statut | Niveau | Priorité | Dépendance Kiltikonet |
|---|---|---|---|---|---|---|---|
| 1 | KLT-01 | Médiateur culturel | Formation publique | KEEP | Fondamentaux | P0 | Culture Connect / terrain / réseau |
| 2 | KLT-02 | Chef de projet culturel | Formation publique | KEEP | Professionnalisation | P0 | Programmes / Culture Connect / gouvernance |
| 3 | KLT-03 | Responsable partenariats institutionnels culturels | Formation publique | KEEP | Avancé | P1 | Institutions / financement / territoires |
| 4 | KLT-04 | Gouvernance des organisations et réseaux culturels | Formation publique | UPGRADE | Professionnalisation | P1 | Network / gouvernance / comités |
| 5 | KLT-05 | Opérateur Kiltikonet / Cultural Platform Operator | Formation hybride CVLN | UPGRADE MAJEUR | Opérationnel | P0 | Plateforme / communauté / badges / support / réseau |
| 6 | KLT-06 | Analyste Observatory / Cultural Data Analyst | Formation / spécialisation | NEW | Avancé | P1 | Observatory / data lineage / signaux |
| 7 | KLT-07 | Responsable déploiement territorial culturel | Spécialisation professionnelle | NEW | Avancé | P2 | Network / territoires / opérateurs / licences |
| 8 | KLT-08 | Responsable qualité, conformité & audit réseau | Spécialisation pro/interne | NEW | Avancé | P2 | Compliance / audits / formation opérateurs |

`KEEP` = the boundary/title changes but the code stays central to the
métier (KLT-01/02/03). `UPGRADE`/`UPGRADE MAJEUR` = KLT-04/05 get a
materially larger real scope than their legacy version. `NEW` = KLT-06/07/08
have no prior existence anywhere.

The sheet's own synthesis tile reads: `Formations/spécialisations = 8`,
`Formations publiques = 6`, `Spécialisations avancées = 2`, `Nouvelles
créations = 3`, `Upgrades majeurs = 2`. The raw `Type` column text alone
(4× "Formation publique") does not sum to 6 — the reconciliation that
does work is `Formations publiques = KLT-01..06` (6) and `Spécialisations
avancées = KLT-07/08` (2), which also matches `Nouvelles créations = 3`
= {KLT-06, KLT-07, KLT-08} (all `Statut = NEW`) and `Upgrades majeurs = 2`
= {KLT-04 `UPGRADE`, KLT-05 `UPGRADE MAJEUR`}. This reconciliation is
**inferred from the numbers, not stated explicitly anywhere in the
source** — flagged as evidence, not asserted as confirmed intent.

## 3. PUBLIC / EXTERNAL / BRIDGE type — derived, with one open question

Per the same rule already frozen for FMS in `ACA-0004`
(`docs/ACADEMY_ACA0004_DELIVERY_ARCHITECTURE_TRUTH_REPORT.md`), delivery/
boundary type is not invented per formation — it is read from the real
`contexts` field where one already exists.

**Legacy `KLT-01..05` already carry real `contexts`**
(`catalog_cartography.py:197-287`, same `AcademyContext =
Literal["INTERNAL","EXTERNAL","BRIDGE"]` shape used everywhere else in
the repo):

| Code | Legacy `contexts` (real, live) |
|---|---|
| KLT-01 | `EXTERNAL, BRIDGE` |
| KLT-02 | `EXTERNAL, BRIDGE` |
| KLT-03 | `INTERNAL, EXTERNAL, BRIDGE` |
| KLT-04 | `EXTERNAL, BRIDGE` |
| KLT-05 | `INTERNAL, BRIDGE` |

Per §1, these are the **legacy** formations' contexts — they describe the
formation as currently seeded, not the canonical KLT-01..05 this master
plan defines. Whether the canonical formations inherit these exact
contexts, or get their own (given their boundaries differ), is
**precisely the kind of question the KLT-equivalent of ACA-0005 needs to
answer** — not assumed here.

**`KLT-06/07/08` have no `contexts` anywhere** (they don't exist in
`catalog_cartography.py`). The master plan's own `Type` column gives a
partial, non-`INTERNAL/EXTERNAL/BRIDGE`-shaped signal for these three:

- `KLT-06` = `"Formation / spécialisation"` — no explicit public/internal
  marker. Its subject matter (Observatory data lineage/signals — reading
  `events`, `sessions`, `actors`, `signals`) leans operationally internal,
  but the *Vue d'ensemble* synthesis groups it with the 6 "publiques", not
  the 2 "avancées" (§2) — a real tension between the subject matter and
  the numeric grouping.
- `KLT-07` = `"Spécialisation professionnelle"` — no explicit marker.
- `KLT-08` = `"Spécialisation pro/interne"` — the label itself contains
  **"interne"**, the one explicit internal-facing signal in the whole
  sheet for these three.

**Verdict: `PUBLIC`/`HYBRID`/`INTERNAL` classification is FROZEN for
KLT-01..05 as inherited-pending-confirmation from their legacy `contexts`,
and left `UNRESOLVED` for KLT-06/07/08** — no default is fabricated here.
This is the one open question this ticket surfaces rather than answers;
recommended to settle explicitly before `KLT-0006`+ (when those three
formations' referentials come up).

## 4. Real Kiltikonet dependencies — cross-checked against this repo

Source: *Dépendances produit* sheet, cross-checked against
`backend/` (grep for the literal collection/domain names it lists).

| Domaine (sheet) | Real state **inside CVL-ACADEMY** (this repo, verified) | Sheet's own "État actuel" |
|---|---|---|
| Culture Connect | No `culture_connect`-shaped collection in `db`. One typed integration-shim exists: `services/integrations/registry.py:28` (`EcosystemIntegration("Culture Connect", "CULTURE_CONNECT")`), env-gated (`CULTURE_CONNECT_URL`/`CULTURE_CONNECT_API_KEY`, `.env.example:64-65`), unconfigured — local-fallback only. | "Existe" |
| Network (territories/operators/licenses/training/technology) | **Zero hits** for `territories`, `operators`, `licenses` as `db.*` collections anywhere in `backend/`. Not present in this repo at all — presumably lives in a separate Network system/repo this session has no access to. | "Partiel / foundations" |
| Observatory (events/sessions/territories/actors/signals/adapters) | **Zero hits** for `observatory_events`, `signals`, `adapters` as `db.*` collections. Not present in this repo. | "Existe" |
| Gouvernance | **Zero hits** for a `committees`/`governance` collection. Not present as data in this repo — only as cartography metadata (`meta_entities` strings). | "Existe / dispersé" |
| Pro / communauté | **Zero hits** for `pro_space`/`support_tickets`-shaped collections. Not present in this repo. | "Existe" |
| Badges / identité | **Real and present** — `badges_engine.py`, `api/badges.py`, `db.badges`/`db.user_badges` (confirmed live in this repo, incl. the legacy `Kiltikonet Ambassador`/`Cultural Project Manager`/`Kiltikonet Platform Operator` badges already seeded). FREK-ID linkage: interface-level (`services/frek_core.py`), not a live external call. | "Existe" |
| Opportunities | **Zero hits** for `network_opportunities`. Not present in this repo. | "Prévu/partiel" |

**Conclusion, stated plainly to preempt `NO_FAKE_INTEGRATIONS`
violations later**: within CVL-ACADEMY's own codebase, only **Badges**
is a real, live, in-repo domain among the seven the sheet lists; **Culture
Connect** and **Kiltikonet** itself have real, honest, unconfigured
interface shims (same "ready but decoupled" pattern as `frek_core.py`/
`agent_factory.py`); **Network, Observatory, Gouvernance-as-data, Pro/
communauté, and Opportunities have no footprint in this repo at all** —
whatever real state they have lives entirely outside what this session
can see or verify. Any future KLT ticket that claims to "read Network/
Observatory data" must either (a) get real access to those systems, or
(b) build the same typed-interface-with-local-fallback pattern already
used for Culture Connect/Kiltikonet — never a fabricated in-repo
substitute presented as real.

## 5. Relation to Academy — what already exists, what doesn't

- **Formations/modules**: legacy `KLT-01..05` are live in `db.formations`
  (via `seed_data.py`) with real module sets (via `seed_modules.py`) — see
  §1. These are ordinary Academy formations today, indistinguishable at
  the API level from FMS ones.
- **Missions**: `MIS-KLT-01` ("Charte IA culturelle pour Kiltikonet",
  `entity: "Kiltikonet"`) exists and is covered by an existing test
  (`backend_test.py:391-394`) — pre-dates this master plan and stands
  outside the 8-formation scope; untouched by this ticket.
- **Frontend**: no Kiltikonet-specific page, route, or component exists —
  legacy KLT formations render through the same generic `Formations`/
  `ModuleJourney` surfaces every other formation does. This means the
  canonical rebuild, whenever authorized, inherits the same generic
  runtime FMS canonical formations use — no separate UI debt to carry.
- **Certification/skills**: no `KLT`-specific skill-ID or certification
  scaffolding exists (unlike FMS's `FMSxx-Ay` shape) — this is genuinely
  greenfield for the certification layer, consistent with `Architecture
  documentaire` sheet row 14 ("Skill IDs / preuves ... Connexion FREK").

## 6. Documentary architecture standard (frozen reference, not yet produced)

Source: *Architecture documentaire* sheet — 20 mandatory layers per
formation (`KLT-01→08`), explicitly modeled on the FMS discipline
("Réutiliser discipline FMS", row 8; "Standard FMS", row 15). Reproduced
here as the frozen checklist future KLT-000x referential tickets will be
measured against: référentiel métier, Master Learning Map, Master Module
Map, doctrine + frontières, cas fil rouge, Case Competency Matrix,
matrice de traçabilité, blueprints modules, modules complets, banques N1,
évaluations N2, assessment certificatif N3, grilles de correction, skill
IDs/preuves, guides candidat/correcteur/jury, templates/livrables,
package vidéo expert, package promo/com, intégration Academy, FREK/
progression/certification. None of these 20 layers has been produced for
any KLT formation yet (*Production documentaire* sheet: all 8 formations
show `À produire` across every column) — this ticket does not change that.

## 7. Cas fil rouge — frozen shape, not yet written

Source: *Cas fil rouge* sheet. One shared fictional-but-realistic
"territoire culturel" case spans all 8 formations, each drawing a
different angle from the same universe (organisation/opérateur local,
institution/financeur, publics, programme, plateforme Kiltikonet,
données, réseau, incident, opportunité, certification). Status on every
row: `À formaliser`. Frozen as a reference shape; not written by this
ticket.

## 8. What this ticket explicitly did NOT do

- No module content written (`Plan modules`/*Production documentaire*
  sheets stay `À produire`).
- No code changed, no collection written, no `db.formations` mutation.
- No collision resolved between legacy and canonical KLT-01..05 (§1) —
  surfaced, not fixed.
- No PUBLIC/EXTERNAL/BRIDGE decision forced for KLT-06/07/08 (§3) —
  surfaced as open, not fabricated.
- No new integration built for Network/Observatory/etc. — their absence
  from this repo is reported, not patched with a mock.

## 9. Gate status

**KLT-0001 = FROZEN.** `KLT_MASTER_MAP_v1` (8 formations, boundaries,
priorities, real repo-cross-checked dependencies) is canonicalized in
this document. Two open items block clean progression to formation-level
work: the legacy/canonical code collision (§1) and the KLT-06/07/08
boundary-type gap (§3) — both explicitly named, neither invented around.

`STOP = TRUE.` Proposed next step, **pending your go-ahead**: `KLT-0002 —
KLT-01 Médiateur culturel / Référentiel canonique` — the first of the 20
documentary layers (§6) for the first formation, same AUDIT→CANONICALIZE→
FREEZE discipline, still no code/module content. No further KLT or ACA
scope taken beyond what's in this document.
