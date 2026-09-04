# KLT-0003 — KLT-01 Médiateur culturel / Référentiel canonique

```
WORKSTREAM = KLT
KLT-0001 = FROZEN · KLT-0002 = VALIDATED (Founder decisions applied below)
KLT-0003 = AUTHORIZED = TRUE (this ticket)
KLT-0004+ = NOT_AUTHORIZED
METHOD (this ticket) = AUDIT KLT-01 -> COMPETENCY MAP -> FINAL MODULE
STRUCTURE -> TRACEABILITY -> REFERENTIEL CANONIQUE -> REVIEW -> FREEZE
SOURCE = LEGACY_VALID_CONTENT + KLT_MASTER_MAP + KLT0002_RECONCILIATION
+ REAL_KILTIKONET_CONTEXT — not rebuilt from zero.
DB_MUTATION = FALSE / RUNTIME_BINDING = FALSE / SEED_REPLACEMENT = FALSE
/ BADGE_REASSIGNMENT = FALSE / CONTEXT_OVERRIDE = FALSE / KLT-02+ BUILD
= FALSE / FAKE_OBSERVATORY = FALSE / FAKE_OPERATOR_AUTHORIZATION = FALSE
STOP_AFTER_DELIVERY = TRUE
```

**Founder decisions applied from `KLT-0002` validation** (verbatim
scope for this ticket): KLT-01 = `KEEP + EXTEND` — keep the 9 legacy
modules as the base, add *cartographie acteurs* and *documenter/prouver*
coverage, do not force a predefined module count; ~10 is indicative,
confirmed (not forced) by the competency matrix below.

---

## 1. AUDIT KLT-01

Everything in this section is `OBSERVED` — read directly from the repo
or from `KLT-0001`/`KLT-0002`, nothing invented.

### 1.1 Métier cible

**Médiateur culturel** (`OBSERVED`, `external_calibration.py:374-395`) —
ROME `k1213`/`k1206`, market confidence `high`. Real-world outcomes:
médiateur culturel, animateur socioculturel, facilitateur patrimoine.

### 1.2 Responsabilités réelles

Derived from the union of legacy module content
(`seed_modules.py:552-634`) and master-plan themes
(`KLT-0001` §2, *Plan modules* sheet), `OBSERVED`+`PROPOSED` mix:

- Concevoir et conduire une action/atelier de médiation adaptée à un
  contexte et un public donnés. `OBSERVED`
- Identifier et mobiliser les acteurs et ressources d'un territoire.
  `PROPOSED` (net-new competency from the master plan, no legacy module
  covered this as its own responsibility before)
- Adapter la médiation à des publics différenciés (jeunes 12-25, seniors/
  mémoire orale, publics institutionnels). `OBSERVED`
- Produire des supports de médiation (livrets, capsules, podcasts).
  `OBSERVED`
- Arbitrer les tensions d'interprétation et les enjeux éthiques de
  représentation, sans folkloriser. `OBSERVED`, `EXTENDED` by the
  master plan's broader "conflits/éthique" framing
- Documenter une action de médiation en preuve exploitable.
  `PROPOSED` (net-new — see §4, module M10)

### 1.3 Activités réelles (situations professionnelles observées)

All `OBSERVED`, drawn from real module hooks/deliverables
(`seed_modules.py:552-634`): mener un diagnostic de territoire/public ·
cartographier acteurs, relais et ressources · concevoir une fiche
atelier détaillée · animer un groupe en gérant la dynamique et la
sécurité affective · produire un livret pédagogique · conduire un
atelier avec un public jeune et en tirer un retour · mener et transcrire
une interview mémorielle avec une personne senior · tenir une grille
d'auto-check interculturelle · constituer un dossier de certification et
le soutenir à l'oral.

### 1.4 Limites du rôle — ce que le métier n'est PAS

`OBSERVED`, cross-referenced against `KLT-0001`/`KLT-0002`'s other four
formations, to keep KLT-01's boundary honest and non-overlapping:

- **N'est pas** un rôle de représentation institutionnelle (négociation
  de conventions, diplomatie culturelle, lobbying) — c'est `KLT-03`.
- **Ne gère pas** un budget de projet ni une recherche de financement
  structurée — c'est `KLT-02`.
- **N'a pas** d'autorité de gouvernance sur une structure associative ou
  un réseau — c'est `KLT-04`.
- **N'opère pas** la plateforme Kiltikonet.fr (pas d'accès
  administrateur, pas de modération de plateforme) — c'est `KLT-05`.
- **Ne peut pas** se prévaloir d'une certification professionnelle
  externe reconnue (RNCP) du seul fait d'avoir terminé `KLT-01` — voir
  §8, le badge reste `DISPLAY_ONLY_LEGACY`.

### 1.5 Publics (de la formation elle-même)

`OBSERVED`, `KEEP` per `KLT-0002`: `DEBUTANT, INTERMEDIAIRE,
INSTITUTIONNEL` (`catalog_cartography.py:205`). Aucun changement proposé
— seuls `KLT-04`/`KLT-05` avaient un `PROPOSE_CHANGE` en attente, pas
`KLT-01`.

### 1.6 Contextes

`OBSERVED`, `KEEP`: `contexts = [EXTERNAL, BRIDGE]`
(`catalog_cartography.py:204`) — `NO_CONTEXT_OVERRIDE` respecté, aucune
mutation, aucune proposition de changement pour `KLT-01`.

### 1.7 Outils

`OBSERVED`: supports pédagogiques, grilles d'animation, questionnaires
d'impact (`external_calibration.py:384-388`) ; livret pédagogique,
fiches objets culturels, protocole d'interview mémorielle
(`seed_modules.py`) ; le système d'évidence `frek_signal`
(`FREK-WORK`/`FREK-SCORE`/`FREK-CONTRIB`/`FREK-CERT`), réel et déjà
utilisé sur chaque module legacy. `PROPOSED` pour le futur module M10 :
un outil de constitution de dossier de preuve structuré (voir §4).

---

## 2. COMPETENCY MAP

Eleven real competencies, each traced to its origin (`OBSERVED` = legacy
module already covers it; `PROPOSED` = net-new from the master plan,
validated by the Founder in `KLT-0002`):

| # | Compétence | Origine | Statut |
|---|---|---|---|
| C1 | Lire et diagnostiquer un territoire/public | legacy M01 | `OBSERVED` |
| C2 | Comprendre le patrimoine et les codes culturels caribéens | legacy M02 | `OBSERVED` |
| C3 | Identifier acteurs, relais et ressources (cartographie) | master plan M02 | `PROPOSED` |
| C4 | Concevoir un dispositif/atelier de médiation | legacy M03 + master plan M03 | `OBSERVED`, `EXTENDED` |
| C5 | Animer/faciliter un groupe avec posture appropriée | legacy M04 = master plan M04 | `OBSERVED` |
| C6 | Mobiliser des médias et outils de médiation | legacy M05 | `OBSERVED` (no master-plan equivalent — kept as real, additional content per `KLT-0002`) |
| C7 | Naviguer l'interculturel avec éthique, arbitrer sans folkloriser | legacy M06 + master plan M06 | `OBSERVED`, `EXTENDED` |
| C8 | Adapter la médiation à un public jeune (12-25) | legacy M07 | `OBSERVED` |
| C9 | Adapter la médiation à un public senior / recueillir la mémoire orale | legacy M08 | `OBSERVED` |
| C10 | Documenter et produire une preuve exploitable de l'action | master plan M07 | `PROPOSED`, `UNRESOLVED` on the Observatory portion (see §4, M10) |
| C11 | Conduire une médiation de bout en bout et la défendre | legacy M09 + master plan M08 | `OBSERVED`, synthesis competency |

No competency from either source is dropped. `C10` is the one carrying
a real, named limitation (below).

---

## 3. FINAL MODULE STRUCTURE

Per the Founder's decision: base = legacy's 9, add cartographie (C3) and
documenter/prouver (C10) coverage, no forced count. Applying `COMPETENCY_
COVERAGE + PEDAGOGICAL_COHERENCE + ASSESSMENT_TRACEABILITY + EXISTING_
VALID_CONTENT` to the 11 competencies above yields **11 modules**, not
10 — the ~10 figure was explicitly indicative in `KLT-0002`, and forcing
a 10th would mean either cutting a real legacy module (forbidden — 
`EXISTING_VALID_CONTENT`) or merging two audience-distinct modules
(jeunes/seniors) that `KLT-0002` explicitly recommended keeping separate
(different real content, not a duplicate). The one real merge opportunity
(interculturel + conflits/éthique, C7 — same underlying competency, not
two different audiences) is taken; that is what keeps this at 11 instead
of 12.

| Module | Titre | Compétence(s) | Niveau éval | Origine | Statut |
|---|---|---|---|---|---|
| M01 | Qu'est-ce que médier une culture ? | C1 | N1 | legacy M01 | `OBSERVED`, `KEEP` |
| M02 | Panorama culturel caribéen — ancêtres, langues, gestes | C2 | N1 | legacy M02 | `OBSERVED`, `KEEP` |
| M03 | Cartographier acteurs et ressources | C3 | N1/N2 | master plan M02 | `PROPOSED`, `BUILD_NEW` |
| M04 | Concevoir une action de médiation | C4 | N2 | legacy M03 + master plan M03 | `OBSERVED`, `MERGE` |
| M05 | Animer un groupe — dynamique et sécurité affective | C5 | N2 | legacy M04 = master plan M04 | `OBSERVED`, `KEEP` |
| M06 | Média et outils de médiation | C6 | N2 | legacy M05 | `OBSERVED`, `KEEP` |
| M07 | Interculturel, conflits et éthique de la représentation | C7 | N2 | legacy M06 + master plan M06 | `OBSERVED`, `MERGE` |
| M08 | Publics jeunes (12-25) — codes et outils | C8 | N2 | legacy M07 | `OBSERVED`, `KEEP` |
| M09 | Publics seniors et transmission orale | C9 | N2 | legacy M08 | `OBSERVED`, `KEEP` |
| M10 | Documenter et prouver | C10 | N2/N3 | master plan M07 | `PROPOSED`, `BUILD_NEW`, `UNRESOLVED` (Observatory portion) |
| M11 | Action terrain finale — certification ambassadeur | C11 | N3 (terminal) | legacy M09 + master plan M08 | `OBSERVED`, `MERGE` |

**M10 — explicit limitation (`NO_FAKE_OBSERVATORY`)**: the master plan
names `Observatory` as this module's dependency. Per `KLT-0001`/`KLT-0002`
§4, Observatory has **zero footprint inside CVL-ACADEMY** — no
collection, no integration shim, `NOT_CONNECTED` in Academy /
`EXTERNAL_EVIDENCE_NOT_AUDITED` externally. This referential does **not**
simulate an Observatory read to fill that gap. M10 is scoped to what is
real today: producing a documented evidence dossier using the existing,
live `frek_signal` stack (`FREK-WORK`/`FREK-SCORE`/`FREK-CONTRIB`) as the
traceable record of the learner's own work across M01–M09, culminating in
`FREK-CERT` at M11. A genuine Observatory-sourced reporting layer stays
`UNRESOLVED` — named as a future capability, not built or faked here.

**Durée**: legacy's 9 modules total 42h (`seed_data.py:609`). M03 and
M10 are net-new, unauthored content — no real duration exists for them
yet. An indicative range (not a claim) of ~50–52h total is offered only
as a planning signal; the real figure is `PROPOSED`/`UNRESOLVED` until
these two modules are actually written (`KLT-0004`+, not this ticket).

---

## 4. TRACEABILITY MATRIX — compétence → module → évaluation → preuve

| Compétence | Module | Évaluation | Preuve (statut) |
|---|---|---|---|
| C1 | M01 | N1 | Note personnelle 500 mots + carte des rôles — `OBSERVED`, `seed_modules.py:559` |
| C2 | M02 | N1 | Fiches 5 objets culturels — `OBSERVED`, `:568` |
| C3 | M03 | N1/N2 | Cartographie acteurs (livrable à produire) — `PROPOSED` |
| C4 | M04 | N2 | Fiche atelier 1h détaillée — `OBSERVED`, `:577` |
| C5 | M05 | N2 | Grille d'animation + posture personnelle — `OBSERVED`, `:586` |
| C6 | M06 | N2 | Livret pédagogique 8 pages — `OBSERVED`, `:595` |
| C7 | M07 | N2 | Grille d'auto-check interculturelle + note d'arbitrage — `OBSERVED` base (`:604`) `EXTENDED` scope |
| C8 | M08 | N2 | Atelier jeune public conduit + retour — `OBSERVED`, `:613` |
| C9 | M09 | N2 | Interview mémorielle 30 min transcrite — `OBSERVED`, `:622` |
| C10 | M10 | N2/N3 | Dossier de preuve, bâti sur les `frek_signal` réels de M01-M09 — `PROPOSED`, Observatory-sourced reporting `UNRESOLVED` |
| C11 | M11 | N3 (terminal) | Dossier certification + soutenance — `OBSERVED`, `:631` |

**Coverage check**: 11/11 competencies have a module, an evaluation
level, and a named (even if `PROPOSED`) evidence artifact. Zero orphan
competencies, zero module without a competency. This is the condition
`§9 FREEZE` below certifies.

---

## 5. Correspondance LEGACY → CANON

| Legacy | Canon | Relation |
|---|---|---|
| M01, M02 | M01, M02 | 1:1, `KEEP` |
| — | M03 | net-new, `BUILD_NEW` |
| M03 | M04 | 1:1 + master plan's N1/N2 leveling, `MERGE` |
| M04 | M05 | 1:1, `KEEP` |
| M05 | M06 | 1:1, `KEEP` (no master-plan equivalent, real content preserved per `KLT-0002`) |
| M06 | M07 | 1:1 + master plan's conflits/éthique framing, `MERGE` |
| M07, M08 | M08, M09 | 1:1 each, `KEEP` distinct (per `KLT-0002`, not collapsed) |
| — | M10 | net-new, `BUILD_NEW`, `UNRESOLVED` on Observatory |
| M09 | M11 | 1:1 + master plan's N3 assessment framing, `MERGE` |

No legacy module is dropped. No canon module lacks a named origin.

---

## 6. Dépendances Kiltikonet (KLT-01 scope only)

Re-applying the `KLT-0002` five-way taxonomy, scoped to what `KLT-01`
actually touches:

| Dépendance | Modules concernés | Classification |
|---|---|---|
| Culture Connect | M01, M08/M09 (terrain, publics) | `INTEGRATION_CONTRACT` (shim exists, unconfigured) |
| Network | M03 | `NOT_CONNECTED` in Academy / `EXTERNAL_EVIDENCE_NOT_AUDITED` externally |
| Observatory | M10 | `NOT_CONNECTED` in Academy / `EXTERNAL_EVIDENCE_NOT_AUDITED` externally — see M10's explicit limitation above |
| Gouvernance | M07 (arbitrage/éthique, conceptually) | `NOT_IMPLEMENTED` as structured data in Academy |
| FREK | M10, M11 (evidence stack, `frek_signal`) | `ACADEMY_LOCAL_IMPLEMENTATION` — real, live, already used |

---

## 7. Livrables et preuves — synthèse

Already itemized per module in §4. All 9 legacy deliverables are real,
produced artifacts (`OBSERVED`). The 2 new modules' deliverables (M03
cartographie, M10 dossier de preuve) are named but not yet authored
(`PROPOSED`) — writing them is `KLT-0004`+ scope, explicitly excluded
from this ticket (`NO_KLT-02+ BUILD` also reads as "no module content
build" here — this ticket freezes the *referential*, not the modules
themselves).

## 8. Prérequis

`Aucun` — `OBSERVED`, `KEEP` (`seed_data.py:613`). `KLT-01` remains the
entry point of the KLT family: `KLT-02` (recommandé), `KLT-03` (requis
avec `KLT-02`), and `KLT-05` (recommandé avec `FRK-01`) all already
depend on it (`seed_data.py:627,641,669`) — none of that changes here.

## 9. Badge / certification / preuve — application de la décision Founder

Per `KLT-0002`'s cross-cutting finding, applied here exactly as the
Founder validated it:

- `badge_name = "Kiltikonet Ambassador"` → **`DISPLAY_ONLY_LEGACY`**.
  Not reassigned, not removed, not presented as a real credential.
  `NO_BADGE_REASSIGNMENT` respected — the field is unchanged in the repo.
- **`SKILL_PROOF`**: still does not exist for `KLT-01` (no `KLT-01-Ay`-
  shaped ID). This referential's traceability matrix (§4) is the
  groundwork for one, but does not itself create it — `PROPOSED` for a
  future ticket.
- **`CERTIFICATION`**: only the existing external RNCP calibration
  reference (`CERT_PROJECT_CULTURE`) — informational, unchanged.
- **`OPERATOR_AUTHORIZATION`**: not applicable to this métier (médiateur
  culturel is not a platform-operator role) — noted `N/A` for
  completeness, consistent with the discipline `KLT-05` will need.

## 10. Ce que le diplômé KLT-01 peut réellement faire

Concevoir et conduire une action de médiation culturelle adaptée à un
territoire et à un public donné · cartographier les acteurs et ressources
d'un contexte local · adapter son intervention à un public jeune (12-25)
ou senior, y compris le recueil de mémoire orale · produire des supports
de médiation (livrets, capsules) · reconnaître et arbitrer une tension
interculturelle sans folkloriser la culture représentée · documenter son
action avec les preuves réellement disponibles aujourd'hui (les
`frek_signal` de son propre parcours).

## 11. Ce qu'il ne peut PAS prétendre faire

Représenter institutionnellement Kiltikonet (`KLT-03`) · gérer un budget
ou un financement de projet (`KLT-02`) · exercer une autorité de
gouvernance associative ou réseau (`KLT-04`) · opérer ou administrer la
plateforme Kiltikonet.fr (`KLT-05`) · se prévaloir d'une certification
professionnelle externe reconnue (RNCP) du seul fait d'avoir terminé
`KLT-01` · produire un rapport sourcé sur des données Observatory réelles
(cette capacité n'existe pas encore, ni pour lui ni pour la plateforme).

## 12. OBSERVED / PROPOSED / UNRESOLVED — synthèse consolidée

| Catégorie | Éléments |
|---|---|
| `OBSERVED` | Métier cible, responsabilités de base, 9 modules legacy et leurs livrables/preuves, publics, contexts, prérequis, badge (en tant que display string existant) |
| `PROPOSED` | M03 (cartographie), M10 (documenter/prouver), la matrice de traçabilité complète, la structure finale à 11 modules, l'estimation indicative de durée |
| `UNRESOLVED` | La portée réelle de M10 une fois Observatory accessible ; la durée réelle de M03/M10 une fois rédigés ; le mécanisme `SKILL_PROOF` futur ; toute réponse à la question `KLT-04`/`KLT-05` `contexts PROPOSE_CHANGE` (hors scope `KLT-01`, non traitée ici) |

## 13. Critères de sortie (exit criteria)

Un diplômé `KLT-01` canonique doit avoir, pour chacune des 11
compétences : un module suivi, une évaluation de niveau cohérent (N1→N3
en progression), et une preuve produite. §4 démontre une couverture
11/11 sans compétence orpheline ni module sans compétence — condition
remplie pour geler ce référentiel (pas les modules eux-mêmes, qui restent
`À produire` pour M03/M10).

---

## REVIEW — validation des contraintes

- `NO_DB_MUTATION` — aucun `insert_one`/`update_one`/`delete_one` exécuté.
- `NO_RUNTIME_BINDING` — aucune route, aucun composant frontend touché.
- `NO_SEED_REPLACEMENT` — `seed_data.py`/`seed_modules.py` non modifiés.
- `NO_BADGE_REASSIGNMENT` — `badge_name` non touché, seulement requalifié
  documentairement en `DISPLAY_ONLY_LEGACY`.
- `NO_CONTEXT_OVERRIDE` — `contexts` non modifié pour `KLT-01`.
- `NO_KLT-02+ BUILD` — seul `KLT-01` est traité dans ce document.
- `NO_FAKE_OBSERVATORY` — M10 ne simule aucune lecture Observatory ; la
  limitation est nommée explicitly (§3).
- `NO_FAKE_OPERATOR_AUTHORIZATION` — non applicable à ce métier, noté
  `N/A` plutôt que passé sous silence.

```bash
git status --short   # expect: only this new doc
```

## FREEZE

**`KLT-01_CANONICAL_REFERENTIAL = FROZEN`** — les 11 compétences sont
toutes couvertes par un module, une évaluation et une preuve nommée
(§4/§13). Le référentiel est gelé ; **les modules M03 et M10 restent `À
produire`** — ce gel porte sur la structure et la traçabilité, pas sur
la rédaction pédagogique, explicitement hors scope de ce ticket.

`STOP = TRUE.` `KLT-0004` non commencé, en attente d'autorisation
explicite.
