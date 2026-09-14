# GMD-21 — Evidence Model

## Evidence chain

```
COMPETENCY (C1/C2/C3) → MODULE (M1-M4) → ASSESSMENT (N1+N2+livrable M1)
→ EVIDENCE (annotated route map + graded N2 case + N1 score)
→ SKILL_ID (GMD21.SKILL.C1/C2/C3) → QUALIFICATION (internal, GMD-21)
```

## What counts as evidence here

- **N1 score** — a stored score against the 16-item bank, reproducible.
- **N2 graded case** — the corrector's rubric-scored write-up (against
  `ASSESSMENT_AND_RUBRIC.md`), stored with the specific case ID used.
- **The M1 deliverable itself** — the candidate's annotated route map,
  which is directly checkable against `server.py`'s real route table
  (this is the strongest evidence artifact in this formation, since it
  can be re-verified by anyone with repo access, not just trusted on
  the corrector's word).

## What this evidence is NOT

`READY_FOR_FREK_PROOF = FALSE` — none of this evidence is wired to any
FREK proof channel (neither this Academy's `frek_core.issue_proof()`
stub nor Good Mood's own `frek_service.py` outbox, which is a
different system entirely — see `gmd31/REFERENTIAL.md`). This
evidence lives only in this Academy's own certification records.

## Skill ID reservation

`GMD21.SKILL.C1`, `GMD21.SKILL.C2`, `GMD21.SKILL.C3` — registered in
`docs/cvln_academy_master/70_EVIDENCE/EVIDENCE_ARCHITECTURE.md`'s
namespace map (`GMD21.SKILL.*` → `GMD33.SKILL.*`, reserved this
session, no collision with `KOR*`/`KLT*`).

## Status

`STATUS = EVIDENCE_MODEL_V1`. No real candidate evidence exists yet.
