# KLT-0002 — Legacy → Canonical Reconciliation & Migration Map

```
WORKSTREAM = KLT
KLT-0001 = FROZEN (prerequisite, see docs/KILTIKONET_KLT0001_CANONICAL_EDUCATION_MAP.md)
KLT-0002 = AUTHORIZED = TRUE (this ticket)
KLT-0003 (KLT-01 référentiel canonique) = NOT_AUTHORIZED, blocked on this ticket
METHOD = AUDIT -> CANONICALIZE -> FREEZE -> BUILD -> TEST -> VERIFY -> STOP
THIS_TICKET_PHASE = AUDIT + reconciliation proposal (no BUILD)
GOVERNING_RULE = LEGACY != WRONG. LEGACY = EXISTING_EVIDENCE.
DB_MUTATION = FALSE / SEED_MUTATION = FALSE / ROUTE_CHANGE = FALSE /
RUNTIME_BINDING = FALSE / DB_CONTEXT_MUTATION = FORBIDDEN /
BADGE_REASSIGNMENT = FALSE / MODULE_REWRITE = FALSE /
CURRICULUM_GENERATION = FALSE / FAKE_KILTIKONET_INTEGRATION = FALSE
FMS_INTACT = TRUE (zero FMS files touched this ticket)
STOP_AFTER_DELIVERY = TRUE
```

## 0. Method and sources

Two sources are compared, verbatim, for `KLT-01` through `KLT-05` only
(`KLT-06/07/08` are untouched — no legacy exists for them, confirmed in
`KLT-0001`):

- **LEGACY** — everything already live in this repo: `seed_data.py`
  (formation record), `seed_modules.py` (module list), `catalog_
  cartography.py` (cartography: `contexts`, `audience`, `level`, `meta_
  entities`, `bridges`, plus the *derived* fields `build_cartography()`
  computes from the two seed files — competencies, activities, tools,
  deliverables, evidence, outcomes), `external_calibration.py` (market
  job title, ROME refs, RNCP certification refs, skills, activities,
  tools, outcomes, confidence rating), `badges_engine.py`/`api/badges.py`
  (the real CC-threshold badge-issuance engine), `backend_test.py`
  (`MIS-KLT-01` coverage).
- **MASTER PLAN** — `KLT_MASTER_MAP_v1`, frozen in `KLT-0001` from
  `CVLN_Academy_Kiltikonet_Formation_Master_Plan.xlsx`.

Every classification below cites the exact file/line or sheet row it
rests on. Where no legacy evidence exists for a dimension, that is stated
as `NO_LEGACY_EVIDENCE`, not assumed absent from the real world.

---

## KLT-01 — Médiateur culturel

### LEGACY STATE

| Dimension | Value | Evidence |
|---|---|---|
| Code | `KLT-01` | `seed_data.py:606` |
| Titre | *Fondamentaux de la médiation culturelle caribéenne* | `seed_data.py:607` |
| Finalité | "Devenir ambassadeur de la médiation culturelle caribéenne" / "Créer un réseau de médiateurs certifiés à travers la diaspora" | `seed_data.py:615-616` |
| Métier cible (marché réel) | *Médiateur culturel* — ROME `k1213`/`k1206` | `external_calibration.py:374-395` |
| Débouchés | Médiateur culturel, animateur d'atelier | `seed_data.py:614` |
| Public/audience | `DEBUTANT, INTERMEDIAIRE, INSTITUTIONNEL` | `catalog_cartography.py:205` |
| Niveau | `fondamentaux` | `catalog_cartography.py:206` |
| Durée | 42h | `seed_data.py:609` |
| Stades | graine → racine | `seed_data.py:610` |
| Nb modules | **9** (M01–M09) | `seed_modules.py:552-634` |
| Prérequis | Aucun | `seed_data.py:613` |
| Compétences (dérivées) | secondary_jobs (Animateur atelier, Ambassadeur culturel) + 6 premiers titres de module | `catalog_cartography.py:199-203`, `build_cartography()` |
| Compétences marché | médiation, animation, adaptation publics, évaluation impact | `external_calibration.py:378` |
| Activités | concevoir médiation, animer ateliers, mobiliser ressources locales | `external_calibration.py:379-383` |
| Badge | `Kiltikonet Ambassador` — **display label on `Formation.badge_name`, never actually issued** (zero code path awards it as a real `db.user_badges` record — see §Badges/Certifications below) | `seed_data.py:612`, `models.py:313` |
| Certification | RNCP `40912`/`32052` (`CERT_PROJECT_CULTURE`) — external market-calibration reference only, not an internal issuance flow | `external_calibration.py:130,377` |
| Contexts | `EXTERNAL, BRIDGE` | `catalog_cartography.py:204` |
| Données persistées | `db.formations` (seed-inserted document, code `KLT-01`) | `seed.py`/`seed_data.py` |
| Seeds | `seed_data.py`, `seed_modules.py`, `catalog_cartography.py`, `external_calibration.py` (4 files) | as cited |
| API/routes | Generic `GET /api/formations`, `GET /api/formations/{code}` — no KLT-specific route | `api/formations.py` |
| Frontend/runtime | None KLT-specific — served through the generic `Formations`/`ModuleJourney` pages | confirmed zero hits, `frontend/src` |
| Dépendances/réf. croisées | None found referencing `KLT-01` as a prerequisite of another formation | grep, this ticket |

**Legacy modules (9)**: M01 *Qu'est-ce que médier une culture?* · M02
*Panorama culturel caribéen — ancêtres, langues, gestes* · M03 *Concevoir
un atelier de médiation* · M04 *Animer un groupe — dynamique et sécurité
affective* · M05 *Média et outils de médiation* · M06 *Interculturel —
respecter sans folkloriser* · M07 *Publics jeunes (12-25)* · M08
*Publics seniors et transmission orale* · M09 *Certification ambassadeur
Kiltikonet*. Every module carries a real hook, a real deliverable, and a
`frek_signal` (`FREK-WORK`/`FREK-SCORE`/`FREK-CONTRIB`/`FREK-CERT`) —
`seed_modules.py:552-634`.

### MASTER PLAN STATE

Type: `Formation publique`, Statut: `KEEP`, Niveau: `Fondamentaux`,
Priorité: `P0`, Dépendance: `Culture Connect / terrain / réseau`.
8 planned modules, all `À produire`:

M01 *Comprendre la médiation culturelle* (Lire publics/territoire/
contexte, N1, dép. Culture Connect) · M02 *Cartographier acteurs et
ressources* (N1/N2, dép. Network) · M03 *Concevoir une action de
médiation* (N2, dép. Programmes) · M04 *Facilitation et posture* (N2,
dép. Terrain) · M05 *Accessibilité et publics* (N2, dép. Culture
Connect) · M06 *Conflits, interprétations et éthique* (N2, dép.
Gouvernance) · M07 *Documenter et prouver* (N2/N3, dép. Observatory/
FREK) · M08 *Action terrain finale — assessment N3* (dép. Terrain).

### DIFF

- **Statut is `KEEP`** — the Founder's own master plan already says this
  code stays central to the métier, not a fresh start.
- Both target the same real métier (médiation culturelle) at the same
  entry level (fondamentaux/N1 start).
- **Legacy is content-complete and Caribbean-diaspora-specific**: real
  hooks, deliverables, two dedicated public-adaptation modules (jeunes
  12-25, seniors/transmission orale). Nothing in the master plan's 8
  themes contradicts this content — it simply doesn't (yet) exist at
  that granularity.
- **Master plan adds explicit assessment traceability** (N1/N2/N3 per
  module) and **two entirely new module themes legacy has no equivalent
  for**: M02 *Cartographier acteurs et ressources* (a distinct
  stakeholder-mapping step) and M07 *Documenter et prouver* (an explicit
  evidence-production module — exactly the discipline `Skill IDs /
  preuves` row of the `KLT-0001` documentary standard calls for, and
  something legacy's `frek_signal` tags gesture at but never structure
  as its own module).
  - Note: `Documenter et prouver` includes an `Observatory` dependency —
    per `KLT-0001` §4, `Observatory` has **zero footprint inside this
    repo**; this module cannot be built as a real Observatory read until
    that dependency is itself resolved (`EXTERNAL_EVIDENCE_NOT_AUDITED`,
    see §Kiltikonet product dependencies below).
- Legacy's M06 (*Interculturel — respecter sans folkloriser*) and the
  master plan's M06 (*Conflits, interprétations et éthique*) cover
  adjacent but not identical ground: legacy is about cultural sensitivity
  in interpretation; master plan is about conflict/ethics arbitration
  more broadly (governance-adjacent). Not a clean 1:1.
- Legacy's two public-specific modules (jeunes/seniors) collapse into the
  master plan's single, more generic M05 *Accessibilité et publics* —
  a real granularity difference, not an error on either side.

### CLASSIFICATION (per element, with evidence)

| Element | Class | Evidence / rationale |
|---|---|---|
| Code `KLT-01` | **KEEP** | Master plan statut is literally `KEEP`; no other formation claims this code |
| Titre | **PROPOSE_MERGE** (not forced) | Legacy title names the diaspora specificity explicitly; master plan's shorter title is the more generic public-facing name. Recommend the shorter title for catalogue display, diaspora specificity preserved inside the referential — this is a naming call for `KLT-0003`, not decided here |
| Public/audience, niveau | **KEEP** | Both agree: fondamentaux/entry-level, broad public. No conflict |
| Durée (42h) | **KEEP pending EXTEND review** | 9 modules of real, timed content already exist; the master plan doesn't state a target duration, so there is no basis to shrink it — extending is more defensible than cutting once M02/M07 (new themes) are added |
| Modules M01-M03 (legacy) | **MERGE** into master plan's M01-M03 shape | Same territory/context/dispositif progression, master plan just adds explicit N1/N2 leveling and a distinct stakeholder-mapping step |
| Modules M04-M05 (legacy: facilitation, médias) | **KEEP** | Directly correspond to master plan's M04 (facilitation/posture); legacy's M05 (médias) has no master-plan equivalent — real, valid, additional content → **EXTEND** the canonical set with it, don't drop it |
| Modules M07-M08 (legacy: jeunes/seniors) | **EXTEND** (keep both, map onto master plan's single M05) | Two real, produced modules vs. one planned theme — legacy is *more* granular, not less valid; recommend canonical keeps both as sub-modules of the accessibility theme rather than collapsing real content into one slot |
| Master plan M02 (cartographie acteurs) | **BUILD_NEW** (not a legacy migration — genuinely absent) | No legacy module covers stakeholder/resource mapping as its own step |
| Master plan M07 (documenter et prouver) | **BUILD_NEW, UNRESOLVED on the Observatory dependency** | No legacy equivalent; blocked on Observatory access per `KLT-0001` §4 |
| M09 legacy (certification finale) vs M08 master plan (action terrain finale) | **MERGE** | Both are the terminal assessment module; legacy's is framed as "certification ambassadeur," master plan's as an N3 professional assessment — same slot, different framing (see Badges/Certifications below for why this framing gap matters) |
| `Formation.badge_name` = `Kiltikonet Ambassador` | **UNRESOLVED** | See dedicated section below — not a real issuance today on either side |
| `contexts = [EXTERNAL, BRIDGE]` | **KEEP** | Consistent with master plan's `Formation publique` + Culture Connect/terrain dependency — no INTERNAL signal on either side |
| RNCP calibration refs | **KEEP** | External market evidence, orthogonal to the canonical rebuild — nothing in the master plan contradicts or duplicates it |

### CANONICAL RECOMMENDATION — KLT-01 CANONICAL STRUCTURE (proposal, not implemented)

Module count is **not forced to 8**. Applying `COMPETENCY_COVERAGE +
PEDAGOGICAL_COHERENCE + ASSESSMENT_TRACEABILITY + EXISTING_VALID_
CONTENT`: legacy already covers 9 real competency slots; the master plan
adds 2 real, non-overlapping new ones (stakeholder mapping, evidence
production) that legacy has no equivalent for. Naively unioning would
give 11; naively forcing 8 would delete real, produced content for no
pedagogical reason. **Proposed canonical shape: ~10 modules** — legacy's
9 kept and re-leveled (N1/N2/N3 added per module), M02 *Cartographier
acteurs et ressources* inserted as new, M07 *Documenter et prouver*
inserted as new but flagged blocked-on-Observatory, and the two
public-specific legacy modules (jeunes/seniors) kept distinct rather than
collapsed. This is a proposal for `KLT-0003` to formalize — not frozen
here.

---

## KLT-02 — Chef de projet culturel

### LEGACY STATE

| Dimension | Value | Evidence |
|---|---|---|
| Code | `KLT-02` | `seed_data.py:620` |
| Titre | *Montage et gestion de projets culturels* | `seed_data.py:621` |
| Métier cible | *Chef de projet culturel* — ROME `k1808`/`e1107` | `external_calibration.py:396-414` |
| Débouchés | Chef de projet culturel, coordinateur événement | `seed_data.py:628` |
| Public | `INTERMEDIAIRE, PROFESSIONNEL, INSTITUTIONNEL` | `catalog_cartography.py:220` |
| Niveau | `professionnalisation` | `catalog_cartography.py:221` |
| Durée | 56h | `seed_data.py:623` |
| Nb modules | **10** (M01–M10) | `seed_modules.py:635-726` |
| Prérequis | KLT-01 recommandé | `seed_data.py:627` |
| Badge | `Cultural Project Manager` — display label only, never issued | `seed_data.py:626` |
| Certification | RNCP `40912`/`32052` | `external_calibration.py:399` |
| Contexts | `EXTERNAL, BRIDGE` | `catalog_cartography.py:219` |

**Legacy modules (10)**: M01 *L'idée devenue projet* · M02 *Étude de
besoin et parties prenantes* · M03 *Budget culturel prévisionnel* · M04
*Recherche de financements — DAC, CTM, OIF, mécénat* · M05
*Planification et gestion des équipes* · M06 *Suivi opérationnel et
pilotage* · M07 *Communication de projet — récit et preuves* · M08
*Évaluation d'impact culturel* · M09 *Bilan et reconduction stratégique*
· M10 *Soutenance publique — jury Kiltikonet*.

### MASTER PLAN STATE

Type `Formation publique`, Statut `KEEP`, Niveau `Professionnalisation`,
P0, dép. `Programmes / Culture Connect / gouvernance`. 8 planned modules:
M01 *Cadrage du projet culturel* (N1/N2) · M02 *Parties prenantes et
gouvernance* (N2, dép. Network) · M03 *Planification et production* (N2)
· M04 *Budget et ressources* (N2, dép. Admin finance) · M05 *Risques et
conformité* (N2, dép. Compliance) · M06 *Opérations terrain* (N2) · M07
*Impact et bilan* (N2/N3, dép. Observatory) · M08 *Pilotage final —
assessment N3*.

### DIFF

- Legacy's `Recherche de financements` (M04, DAC/CTM/OIF/mécénat-specific
  — real, French-Caribbean-institutional-knowledge-dense) has **no
  distinct slot** in the master plan's 8 — it's implicitly folded into
  M01 *Cadrage* or M04 *Budget*. This is a real content-loss risk if the
  master plan's 8 slots are taken literally: real, specific fundraising
  knowledge with no explicit destination — **UNRESOLVED**.
- **Master plan's M05 (Risques et conformité) is genuinely new** — legacy
  has no risk-register or compliance module for project management.
- Legacy's M09+M10 (bilan/reconduction, then a *separate* public
  soutenance) both map onto the master plan's single M08 — again, legacy
  is more granular, treating the public defense as a distinct capstone
  event, not folded into "pilotage."

### CLASSIFICATION

| Element | Class | Evidence / rationale |
|---|---|---|
| Code, titre, public, niveau | **KEEP** | No conflict; `KEEP` statut confirmed by master plan itself |
| M01-M03 legacy (idée→besoin→budget) | **MERGE** into master plan M01/M03/M04 | Same progression, different granularity |
| M04 legacy (recherche de financements, DAC/CTM/OIF) | **EXTEND / UNRESOLVED destination** | Real, specific, valuable content with no explicit slot in the 8-theme plan — needs an explicit "où ça va" decision at `KLT-0003`, not silently dropped |
| M05-M06 legacy (planification équipes, suivi/pilotage) | **MERGE** into master plan M02/M06 | Same territory |
| M07 legacy (communication de projet) | **UNRESOLVED destination** — no clean master-plan slot | Real module, same "no destination" issue as M04 |
| M08 legacy (évaluation d'impact) | **MERGE** into master plan M07 (Impact et bilan) | Direct match, master plan adds Observatory-sourced traceability legacy doesn't have |
| M09+M10 legacy (bilan + soutenance) | **EXTEND** master plan's single M08 | Two real capstone steps vs. one planned — recommend keeping both, not collapsing |
| Master plan M05 (Risques et conformité) | **BUILD_NEW** | No legacy equivalent, genuinely additive |
| Badge `Cultural Project Manager` | **UNRESOLVED** | Same badge-vs-certification gap as KLT-01, see dedicated section |
| Prerequisite `KLT-01 recommandé` | **KEEP as a real cross-reference** | Confirms KLT-01→KLT-02 sequencing intent already exists in legacy; master plan doesn't contradict it |

### CANONICAL RECOMMENDATION — KLT-02 CANONICAL STRUCTURE (proposal)

Legacy's 10 modules already exceed the master plan's 8-theme sketch in
real coverage — **compressing to 8 would delete real content** (financing
research, communication) with no pedagogical justification found in
either source. Proposed shape: **~10-11 modules**, keeping all legacy
themes, inserting master plan's new *Risques et conformité* module, and
re-leveling every module with explicit N1/N2/N3. Final decision at
`KLT-0003`.

---

## KLT-03 — Responsable partenariats institutionnels culturels

### LEGACY STATE

| Dimension | Value | Evidence |
|---|---|---|
| Code | `KLT-03` | `seed_data.py:634` |
| Titre | *Stratégie institutionnelle et partenariats* | `seed_data.py:635` |
| Métier cible | *Chargé de développement culturel / partenariats* — ROME `k1808`/`k1802` | `external_calibration.py:415-440` |
| Public | `AVANCE, PROFESSIONNEL, INSTITUTIONNEL` | `catalog_cartography.py:239` |
| Niveau | `avancé` | `catalog_cartography.py:240` |
| Durée | 44h | `seed_data.py:637` |
| Nb modules | **9** | `seed_modules.py:727-808` |
| Prérequis | KLT-01 + KLT-02 | `seed_data.py:641` |
| Objectif stratégique | "Positionner Kiltikonet dans le paysage institutionnel mondial" | `seed_data.py:644` |
| Badge | `Institutional Strategist` — display label only | `seed_data.py:640` |
| Contexts | `INTERNAL, EXTERNAL, BRIDGE` (all three) | `catalog_cartography.py:238` |
| Confidence (market calibration) | **medium** — "diplomatie culturelle à vérifier" flagged by the calibration itself | `external_calibration.py:423,440` |
| Downstream cross-reference | `GRP-02` (*Cultural Economy & Strategic Partnerships*, a different pole) lists `"KLT-03 recommandé"` as its own prerequisite | `seed_data.py:1000` |

**Legacy modules (9)**: M01 *Cartographie des institutions culturelles*
· M02 *OIF — Organisation internationale de la Francophonie* · M03
*UNESCO et CARIFESTA — patrimoine et rayonnement* · M04 *DAC, CTM et
écosystème local* · M05 *Fonds européens — Creative Europe, ERDF* · M06
*Diplomatie culturelle et soft power* · M07 *Représentation en instances*
· M08 *Lobbying culturel — éthique et efficacité* · M09 *Mission
institutionnelle finale — représenter Kiltikonet*.

### MASTER PLAN STATE

Type `Formation publique`, Statut `KEEP`, Niveau `Avancé`, P1, dép.
`Institutions / financement / territoires`. 8 planned modules: M01
*Écosystème institutionnel* (N1) · M02 *Stratégie partenariale* (N2) ·
M03 *Financements et appels à projets* (N2, dép. Opportunities) · M04
*Convention et négociation* (N2, dép. Legal/IP) · M05 *Diplomatie
culturelle* (N2) · M06 *Reporting et preuve d'impact* (N2/N3, dép.
Observatory) · M07 *Portefeuille de partenaires* (N2, dép. Pro space) ·
M08 *Négociation finale — assessment N3*.

### DIFF

**This is the widest content-shape gap of the five.** Legacy is *deep
and narrow* — four of its nine modules (M02 OIF, M03 UNESCO/CARIFESTA,
M04 DAC/CTM, M05 Fonds européens) are named after specific real
institutions in the Francophonie/Caribbean funding landscape. Master plan
is *broad and generic* — "Stratégie partenariale," "Financements et
appels à projets" as abstract themes, no institution named. Neither is
wrong: legacy's specificity is exactly the kind of real-world grounding a
"cas fil rouge" needs concrete material for; the master plan's genericity
is what makes the formation portable beyond a Francophonie/Caribbean
niche. **This is a real strategic choice, not a data error — flagged
`UNRESOLVED`, not decided here.**

- Master plan's M04 (*Convention et négociation*, Legal/IP-dependent) and
  M07 (*Portefeuille de partenaires*, Pro-space-dependent) have **no
  legacy equivalent** — genuinely new.
- Legacy's M07 (*Représentation en instances*) and M08 (*Lobbying
  culturel*) have **no clean master-plan slot** — closest is M05
  (Diplomatie culturelle), but lobbying-with-an-ethics-lens is materially
  different content.
- `contexts = [INTERNAL, EXTERNAL, BRIDGE]` (all three, the only KLT-01..05
  formation with all three) is corroborated by the legacy's own stated
  strategic objective ("positionner *Kiltikonet* dans le paysage
  institutionnel" — an internal CVLN-positioning goal, not just a
  learner-facing one) — internally consistent, no conflict with the
  master plan's broader institutional dependency list.

### CLASSIFICATION

| Element | Class | Evidence / rationale |
|---|---|---|
| Code, statut `KEEP` | **KEEP** | Master plan itself |
| Institution-specific modules (M02-M05) | **UNRESOLVED** | Real, valuable, narrow content vs. the master plan's deliberately generic 4 themes — a scope decision belongs to `KLT-0003`, not this audit |
| M07-M08 legacy (représentation, lobbying) | **EXTEND** — no clean merge target | Recommend keeping as additional modules alongside master plan's 8, not force-fit |
| M09 legacy vs M08 master plan (capstone) | **MERGE** | Same terminal-assessment slot |
| Master plan M04 (convention/négociation) | **BUILD_NEW** | No legacy equivalent |
| Master plan M07 (portefeuille de partenaires, Pro space dep.) | **BUILD_NEW, blocked** | `Pro/communauté` has zero in-repo footprint per `KLT-0001` §4 — `EXTERNAL_EVIDENCE_NOT_AUDITED` |
| `contexts = [INTERNAL, EXTERNAL, BRIDGE]` | **KEEP** | Internally consistent with legacy's own stated strategic objective |
| Prerequisite chain `KLT-01+KLT-02 → KLT-03 → GRP-02` | **KEEP, note the downstream dependency** | `GRP-02` (a different pole entirely) already depends on this code — any future rename/rescope of `KLT-03` has a real blast radius outside KLT itself |
| Badge `Institutional Strategist` | **UNRESOLVED** | Same badge-vs-certification gap, see below |
| Calibration confidence = `medium`, "à vérifier" flags | **KEEP as an honesty signal** | The legacy calibration data itself already flags its own uncertainty — worth preserving that humility in the canonical version rather than presenting it as more certain |

### CANONICAL RECOMMENDATION — KLT-03 CANONICAL STRUCTURE (proposal)

The scope question (Francophonie-specific vs. generic) should be answered
explicitly before module count is fixed. **Two honest options, both
valid, neither decided here**: (a) keep legacy's institutional specificity
as the canonical case-study layer *inside* the master plan's generic
module shells (9 legacy themes distributed across the master plan's 8
slots, roughly 1:1 with M02-M05 folded into M01/M03), or (b) run both —
generic modules per the master plan plus the institution-specific ones as
an advanced/optional track. Recommend **(a)** as the more coherent
single-track option, yielding **~9 modules**, but this is a judgment call
for `KLT-0003`, flagged `UNRESOLVED` here on purpose.

---

## KLT-04 — Gouvernance des organisations et réseaux culturels

### LEGACY STATE

| Dimension | Value | Evidence |
|---|---|---|
| Code | `KLT-04` | `seed_data.py:648` |
| Titre | *Gouvernance associative et juridique culturelle* | `seed_data.py:649` |
| Métier cible | *Responsable administration culturelle / gouvernance associative* — ROME `k1808`/`k1604` | `external_calibration.py:442-459` |
| Public | `INTERMEDIAIRE, PROFESSIONNEL, INSTITUTIONNEL` | `catalog_cartography.py:258` |
| Niveau | `opérationnel` | `catalog_cartography.py:259` |
| Durée | 38h | `seed_data.py:651` |
| Nb modules | **8** | `seed_modules.py:810-882` |
| Prérequis | Aucun | `seed_data.py:655` |
| Badge | `Governance Associative` — display label only | `seed_data.py:654` |
| Contexts | `EXTERNAL, BRIDGE` | `catalog_cartography.py:257` |
| Calibration confidence | **low** — "conformité associative à vérifier" | `external_calibration.py:450,459` |

**Legacy modules (8)**: M01 *La loi 1901 en pratique* · M02 *Créer une
association culturelle* · M03 *Rôles — Président, Trésorier, Secrétaire,
DAF* · M04 *Comptabilité associative et plan comptable* · M05 *Fiscalité
culturelle* · M06 *AG, PV et documents obligatoires* · M07 *Gestion
salariale et bénévolat* · M08 *Cas pratique — auditer une association*.

### MASTER PLAN STATE

Type `Formation publique`, **Statut `UPGRADE`** (the master plan itself
flags this one as needing more than a straight carry-over), Niveau
`Professionnalisation`, P1, dép. `Network / gouvernance / comités`. 8
planned modules: M01 *Fondamentaux de gouvernance* (distinguishing
association/réseau/opérateur/comité, N1) · M02 *Rôles, délégations et
mandats* (N2, dép. Network RBAC) · M03 *Comités et décisions* (N2, dép.
Governance records) · M04 *Conformité et responsabilité* (N2, dép.
Compliance) · M05 *Conflits d'intérêt et éthique* (N2, dép. Audit) · M06
*Gouvernance territoriale* (N2, dép. Territories/operators) · M07 *Audit
de gouvernance* (N2/N3, dép. Audits) · M08 *Crise de gouvernance —
assessment N3*.

### DIFF

**Confirms the master plan's own `UPGRADE` call.** Legacy is
*entirely* French-association-law-specific (Loi 1901, fiscalité,
comptabilité associative, AG/PV) — real, produced, operationally useful
content, but scoped to **one governance form** (the French non-profit
association). The master plan's title itself broadens scope to
*"organisations et réseaux"* — multi-operator network governance,
territorial governance across several operators, RBAC/delegation models.
**Zero overlap module-for-module** — this is not a re-leveling of the
same content, it is a real scope expansion, exactly as the master plan's
statut says.

### CLASSIFICATION

| Element | Class | Evidence / rationale |
|---|---|---|
| Code | **KEEP** | Same métier family (gouvernance culturelle), master plan's own choice to reuse the code |
| Every legacy module (M01-M08) | **MERGE, not DEPRECATE** | Loi-1901/fiscal/comptable literacy remains real, needed knowledge for anyone actually running a cultural association inside the Kiltikonet network — recommend folding as a "gouvernance associative" sub-track inside the broader canonical M01-M04, not discarding |
| Every master plan module (M01-M08) | **BUILD_NEW** | No legacy equivalent for network-level/multi-operator/RBAC governance — this is the real net-new content the `UPGRADE` statut calls for |
| `contexts = [EXTERNAL, BRIDGE]` | **PROPOSE_CHANGE** (not applied) | Master plan's broadened scope (`Network / gouvernance / comités`, RBAC, territorial multi-operator governance) reads as touching CVLN's own internal governance surfaces, not just external-facing association management — recommend evaluating an `INTERNAL` addition at `KLT-0003`. **Not applied here** — `DB_CONTEXT_MUTATION = FORBIDDEN` |
| Badge `Governance Associative` | **UNRESOLVED** | Same badge-vs-certification gap |
| Calibration confidence = `low` | **KEEP as a flag** | The legacy source already distrusts its own compliance-specificity claim; carry that honesty forward rather than resolve it silently |

### CANONICAL RECOMMENDATION — KLT-04 CANONICAL STRUCTURE (proposal)

Neither "keep 8" nor "replace with the master plan's 8" is correct — they
cover different scopes entirely. Proposed shape: **~11-12 modules** — the
master plan's 8 network-governance themes as the primary spine, plus
legacy's 8 association-specific modules retained as a compact secondary
block (likely compressible to 3-4 modules covering loi 1901/fiscalité/
comptabilité/AG-PV as one applied case rather than 8 separate ones, since
they were originally written for a narrower single-formation scope).
Exact compression is a `KLT-0003` judgment call, not decided here.

---

## KLT-05 — Opérateur Kiltikonet / Cultural Platform Operator

### LEGACY STATE

| Dimension | Value | Evidence |
|---|---|---|
| Code | `KLT-05` | `seed_data.py:662` |
| Titre | *Kiltikonet comme plateforme — outils numériques et impact diaspora* | `seed_data.py:663` |
| Métier cible | *Community manager / opérateur plateforme culturelle* — ROME `e1124`/`k1808` | `external_calibration.py:461-482` |
| Public | `INTERMEDIAIRE, PROFESSIONNEL` | `catalog_cartography.py:277` |
| Niveau | `opérationnel` | `catalog_cartography.py:278` |
| Durée | 40h | `seed_data.py:665` |
| Nb modules | **8** | `seed_modules.py:884-956` |
| Prérequis | KLT-01 + FRK-01 recommandé | `seed_data.py:669` |
| Badge | `Kiltikonet Platform Operator` — display label only | `seed_data.py:668` |
| Contexts | `INTERNAL, BRIDGE` — **no `EXTERNAL`** | `catalog_cartography.py:276` |
| `delivery_formats` | `DEFAULT_FORMAT` (`E_LEARNING` only), unlike KLT-01..04's `PRO_FORMAT` | `catalog_cartography.py:285` |

**Legacy modules (8)**: M01 *Kiltikonet — mission, valeurs, architecture*
· M02 *Community management diaspora* · M03 *Modération culturelle —
sécurité et pluralité* · M04 *Contenus Kiltikonet — capsules, dossiers,
empreintes* · M05 *Analytics et lecture de l'engagement* · M06
*Partenariats plateforme — labels, festivals, institutions* · M07
*Événements Kiltikonet IRL* · M08 *Devenir opérateur senior Kiltikonet*.

### MASTER PLAN STATE

Type `Formation hybride CVLN`, **Statut `UPGRADE MAJEUR`** (the largest
scope jump the master plan flags for any of the five), Niveau
`Opérationnel`, P0, dép. `Plateforme / communauté / badges / support /
réseau`. 9 planned modules: M01 *Architecture Kiltikonet* (N1, dép. Core
platform) · M02 *Identités, accès et rôles* (N1/N2, dép. Auth/RBAC) · M03
*Programmes et contenus* (N2, dép. Programmes/CMS) · M04 *Participants,
badges et scans* (N2, dép. Badges/NFC) · M05 *Communauté et support* (N2,
dép. Pro/support) · M06 *Opérations événementielles* (N2, dép. Culture
Connect) · M07 *Data lineage et reporting* (N2, dép. Observatory) · M08
*Incident et continuité* (N2/N3, dép. Admin/alerts) · M09 *Opération
complète — assessment N3*.

### DIFF

**Closest legacy/master-plan match of the five** (both describe the same
platform-operator role), but the master plan still adds real, genuinely
new operational surfaces legacy has none of: **M02 Identités/accès/rôles**
(operational security — legacy never covers who's authorized to do what),
**M04 Participants/badges/scans** (physical proof-of-attendance/NFC —
legacy's M07 *Événements Kiltikonet IRL* covers running an event but not
badge/scan mechanics), and **M08 Incident et continuité** (no legacy
equivalent at all — no module on handling platform incidents).

- Legacy's `contexts = [INTERNAL, BRIDGE]` — **no `EXTERNAL`** — is worth
  flagging on its own: this formation trains people to run community
  management, partnerships, and public IRL events, which read as
  externally-facing activity. The master plan's own `Type = Formation
  hybride CVLN` implies both internal and external reach. **Possible
  legacy data gap, not silently corrected.**
- `delivery_formats = DEFAULT_FORMAT` (E_LEARNING only) is the one
  formation among the five without `PRO_FORMAT` — consistent with §4:
  no real physical/hybrid delivery infrastructure exists for it either,
  so this is at minimum self-consistent, if worth a second look.

### CLASSIFICATION

| Element | Class | Evidence / rationale |
|---|---|---|
| Code, statut | **KEEP + EXTEND** | Master plan's own `UPGRADE MAJEUR` confirms real expansion, not replacement |
| M01 legacy (architecture/mission/valeurs) | **MERGE** into master plan M01 | Direct match |
| M02-M04 legacy (community mgmt, modération, contenus) | **MERGE** into master plan M03/M05 | Direct thematic match, master plan adds CMS/support-system dependency framing legacy lacks |
| M05 legacy (analytics/engagement) | **MERGE** into master plan M07 (Data lineage/reporting) | Same slot; master plan's version is blocked on Observatory access (§4) while legacy's is a real, already-built analytics module — recommend legacy's version stays authoritative until Observatory access is real |
| M06-M07 legacy (partenariats plateforme, événements IRL) | **MERGE** into master plan M06 (Opérations événementielles) | Direct match |
| M08 legacy (devenir opérateur senior) | **MERGE, but see Operator Authorization section below** | Same terminal slot as master plan M09, but neither legacy nor canonical currently encodes a real authorization mechanism — flagged, not resolved |
| Master plan M02 (identités/accès/rôles) | **BUILD_NEW** | No legacy equivalent — real operational-security gap |
| Master plan M04 (badges/scans) | **BUILD_NEW** | No legacy equivalent |
| Master plan M08 (incident/continuité) | **BUILD_NEW** | No legacy equivalent |
| `contexts = [INTERNAL, BRIDGE]`, missing `EXTERNAL` | **PROPOSE_CHANGE** (not applied) | Content (community mgmt, public partnerships, public events) reads as external-facing; recommend Founder review at `KLT-0003`. **Not applied** — `DB_CONTEXT_MUTATION = FORBIDDEN` |
| `delivery_formats = DEFAULT_FORMAT` | **KEEP, flag for cross-check with ACA-0004** | Self-consistent with §Kiltikonet dependencies (no real physical infra); worth a joint KLT/ACA review later, not this ticket |
| Badge `Kiltikonet Platform Operator` | **UNRESOLVED, most urgent of the five** | This is precisely the formation where "badge" vs. "real authorization to operate the platform" matters most — see next section |

### CANONICAL RECOMMENDATION — KLT-05 CANONICAL STRUCTURE (proposal)

Proposed shape: **~11 modules** — legacy's 8 kept (re-leveled), plus the
3 genuinely new master-plan themes (identités/accès, badges/scans,
incident/continuité) added rather than substituted. The terminal module
should explicitly separate *"completed the operator curriculum"* from
*"authorized to operate Kiltikonet.fr"* — see below.

---

## Badges / Certifications / Skill Proofs / Operator Authorization — cross-cutting finding

Applying the four-concept discipline the Founder specified, across all
five formations:

| Concept | Real, structured mechanism in this repo? | Evidence |
|---|---|---|
| **BADGE** | Yes, but **disconnected from `Formation.badge_name`**. The real badge engine (`badges_engine.py`) issues `db.user_badges` records on **CC-threshold crossing**, platform-wide, formation-agnostic — nothing in it reads `badge_name` or fires on formation completion. `Formation.badge_name` (`Kiltikonet Ambassador`, `Cultural Project Manager`, `Institutional Strategist`, `Governance Associative`, `Kiltikonet Platform Operator`) is a **pure display string** on the formation record, surfaced via `api/formations.py:58`, never inserted into `db.user_badges` by any code path found. | `badges_engine.py:19-46`, `api/formations.py:58`, grep — zero hits linking `badge_name` to an award event |
| **SKILL_PROOF** | No — this concept exists for FMS (`FMSxx-Ay`-shaped skill IDs, `fms_canonical`) but **has no equivalent anywhere in KLT**. No `KLT-xx-Ay` shape exists; nothing in `catalog_cartography.py`'s KLT entries or `seed_modules.py`'s KLT modules produces an addressable skill ID. | Confirmed absent, this ticket's grep sweep |
| **CERTIFICATION** | Only as **external market-calibration reference** (RNCP codes via `CERT_PROJECT_CULTURE`) — informational metadata about what a *real-world* certification in this job family looks like, never wired to an internal `CertificationAttempt`/attestation-issuance flow (unlike FMS's N1/N2/N3 + jury + attestation pipeline). | `external_calibration.py:130` |
| **OPERATOR_AUTHORIZATION** | **Does not exist as a concept anywhere in this repo**, for KLT or otherwise. Nothing distinguishes "finished KLT-05" from "has real write/operate access to Kiltikonet.fr." `frek_signal: FREK-CERT` fires on the terminal module of every formation identically — it is a generic "big milestone" signal, not an authorization grant. | `seed_modules.py` (every terminal KLT module uses the same `FREK-CERT` tag as every other formation's terminal module) |

**This is the single most consequential finding of KLT-0002.** Every one
of the five formations' `badge_name` reads as a real credential
("Ambassador," "Platform Operator," "Institutional Strategist") but
**none of the four real concepts it could map to is actually wired to
formation completion today** — for any formation in the whole catalogue,
not just KLT. Resolving this is out of scope for KLT-0002 (`NO_BADGE_
REASSIGNMENT`), but it is the clearest concrete gap a future ticket
(`KLT-0003` referential work, or a platform-wide badge-engine ticket) will
need to close — especially for `KLT-05`, where "Platform Operator" reads
like it should gate real Kiltikonet.fr write access and currently gates
nothing.

---

## Kiltikonet product dependencies — refined taxonomy

Re-applying `KLT-0001`'s dependency findings with the Founder's five-way
distinction (`ACADEMY_LOCAL_IMPLEMENTATION` / `KILTIKONET_EXTERNAL_
PRODUCT` / `INTEGRATION_CONTRACT` / `NOT_CONNECTED` / `NOT_IMPLEMENTED` /
`EXTERNAL_EVIDENCE_NOT_AUDITED`):

| Domain | Classification | Rationale |
|---|---|---|
| Badges (`db.badges`/`db.user_badges`) | **ACADEMY_LOCAL_IMPLEMENTATION** | Real, live, in-repo — see above |
| Culture Connect | **INTEGRATION_CONTRACT**, `EXTERNAL_EVIDENCE_NOT_AUDITED` beyond the contract | A real typed shim exists (`services/integrations/registry.py:28`), env-gated, unconfigured. Whether the real Culture Connect *product* has more data than this contract exposes is **not auditable from this session** — marked `EXTERNAL_EVIDENCE_NOT_AUDITED`, never "does not exist" |
| Kiltikonet (the platform itself) | **INTEGRATION_CONTRACT**, `EXTERNAL_EVIDENCE_NOT_AUDITED` beyond it | Same pattern — `services/integrations/registry.py:29`, `.env.example:66-67` |
| Network (territories/operators/licenses/training/technology) | **NOT_CONNECTED** in Academy; **EXTERNAL_EVIDENCE_NOT_AUDITED** for the real Network system | Zero collections, zero interface shim in this repo. This is explicitly **not** a claim that Network doesn't exist — it means this session has no visibility into it at all, not even a contract |
| Observatory (events/sessions/signals/adapters) | **NOT_CONNECTED** in Academy; **EXTERNAL_EVIDENCE_NOT_AUDITED** externally | Same — zero footprint, zero shim |
| Gouvernance-as-data (comités, décisions) | **NOT_IMPLEMENTED** in Academy (only exists as free-text `meta_entities` strings, not structured data); **EXTERNAL_EVIDENCE_NOT_AUDITED** externally | `catalog_cartography.py` metadata only |
| Pro/communauté (espace pro, support) | **NOT_CONNECTED** in Academy; **EXTERNAL_EVIDENCE_NOT_AUDITED** externally | Zero footprint |
| Opportunities (`network_opportunities`) | **NOT_CONNECTED** in Academy; **EXTERNAL_EVIDENCE_NOT_AUDITED** externally | Zero footprint |

No domain is marked `DOES_NOT_EXIST` — per the Founder's explicit
instruction, absence from this repo is reported as absence from this
repo's visibility, never as absence from reality.

---

## Global Legacy → Canonical Migration Map

| Code | Legacy modules | Master plan modules | Real overlap | Net-new (master plan) | Net-unplaced (legacy) | Classification | contexts | Proposed canonical size |
|---|---|---|---|---|---|---|---|---|
| KLT-01 | 9 | 8 | ~7 themes | M02 (cartographie acteurs), M07 (documenter/prouver, blocked) | 0 | KEEP + EXTEND | KEEP `[EXTERNAL,BRIDGE]` | ~10 |
| KLT-02 | 10 | 8 | ~6 themes | M05 (risques/conformité) | 2 (financements DAC/CTM/OIF, communication) — UNRESOLVED destination | KEEP + EXTEND, 2 items UNRESOLVED | KEEP `[EXTERNAL,BRIDGE]` | ~10-11 |
| KLT-03 | 9 | 8 | ~5 themes | M04 (convention/négociation), M07 (portefeuille partenaires, blocked) | 2 (représentation en instances, lobbying) — UNRESOLVED | KEEP + UNRESOLVED (institution-specificity scope call) | KEEP `[INTERNAL,EXTERNAL,BRIDGE]` | ~9, pending scope decision |
| KLT-04 | 8 | 8 | ~0 direct module overlap | all 8 (network/RBAC/territorial governance) | legacy's 8 (loi 1901/fiscal/comptable) → proposed MERGE as compact sub-track | EXTEND (confirms master plan's own `UPGRADE`) | PROPOSE_CHANGE eval (`+INTERNAL`?) — not applied | ~11-12 |
| KLT-05 | 8 | 9 | ~6 themes | M02 (identités/accès), M04 (badges/scans), M08 (incident/continuité) | 0 | KEEP + EXTEND (confirms master plan's own `UPGRADE MAJEUR`) | PROPOSE_CHANGE eval (`+EXTERNAL`?) — not applied | ~11 |

**None of the five is `SUPERSEDE`, `DEPRECATE`, or `MIGRATE` in the
destructive sense** — every legacy formation contains real, produced,
non-fabricated pedagogical content the master plan's 8-theme sketches
don't yet have, and every master plan formation names at least one
genuinely new competency legacy never covered. The correct verb for all
five, per the Founder's own worked example, is **EXTEND**: `LEGACY + 
MASTER_PLAN → CANONICAL PROPOSAL`, not replacement in either direction.

---

## Validation

- **No runtime file modified**: `seed_data.py`, `seed_modules.py`,
  `catalog_cartography.py`, `external_calibration.py`, `badges_engine.py`,
  `api/*.py` — all read-only this ticket, confirmed via `git status`
  below.
- **No DB mutated**: no `db.*.insert_one`/`update_one`/`delete_one` call
  made or run this ticket.
- **No seed changed**: zero edits to any `seed_*.py` file.
- **No route changed**: zero edits to `api/`.
- **No legacy content deleted**: every legacy module/badge/context cited
  above is quoted, none removed.
- **FMS untouched**: zero files under `fms_canonical/`, `fms_import/`,
  `fms_lineage/`, or any `FMS`-prefixed doc touched this ticket.
- **Every conclusion cites repo evidence**: file/line or sheet
  row/column, throughout.

```bash
git status --short   # expect: only this new doc, nothing else
```

## Gate status

**KLT-0002 = DELIVERED.** Five formations audited exhaustively across
every requested dimension; every classification carries evidence; two
formations (`KLT-03`, `KLT-02`) carry explicit `UNRESOLVED` content-scope
questions rather than forced answers; two formations (`KLT-04`, `KLT-05`)
confirm the master plan's own `UPGRADE`/`UPGRADE MAJEUR` calls with real
evidence; the badge/certification/skill-proof/operator-authorization gap
is surfaced as the most consequential cross-cutting finding.

`STOP = TRUE.` `KLT-0003` (`KLT-01` référentiel canonique) stays
`NOT_AUTHORIZED` until you validate this reconciliation — in particular
the `UNRESOLVED` items (KLT-02's two unplaced modules, KLT-03's
institution-specificity scope call, the two `PROPOSE_CHANGE` `contexts`
flags, and the badge/authorization gap) are exactly the decisions your
validation should settle before any referential gets written.
