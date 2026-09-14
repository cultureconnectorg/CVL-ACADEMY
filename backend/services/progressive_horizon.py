"""ACA-0027 — Progressive Horizon: the next relevant learning/
opportunity, composed entirely from real, already-computed signals.

**What this is not**: an invented recommendation engine. Every item
this module can ever produce traces to a real, existing capability
already built elsewhere in this codebase:

- `RESUME_MODULE` — `api/learning.py`'s own `user_learning_path`
  `next_action` (the real continuation-engine/sequential-curriculum
  computation, ACA-0024/ACA-0019) — reused verbatim, never
  recomputed differently here.
- `FORMATION_EXPANSION` — the exact real `EXPANDING` condition
  `lifecycleState.js`/`Dashboard.js`'s existing horizon-card already
  derives (own pole 100% validated, a real unlocked formation exists
  elsewhere) — reproduced server-side so it can be composed with the
  other item types in one ordered list, not a new trigger.
- `CERTIFICATION_ELIGIBLE` — the one genuinely NEW signal this pass
  adds: for every formation (own pole or other) the learner has
  reached 100% progress on, look up its real `Rubric` (by
  `formation_code`, the field every rubric already carries — no
  naming-convention guess), skip it if the learner already has a
  `passed` or in-flight attempt against that `certification_code`,
  and run it through `certification.service.check_full_eligibility` —
  the SAME real gate `start_attempt` itself uses. An item only ever
  appears here because that real function said `True`.

Deliberately bounded, not a full-catalogue scan: this only checks
certification eligibility for formations the learner has actually
completed (typically 0-3 per learner), never the entire rubric
collection — real eligibility for a formation nobody has touched is
never a real "next opportunity" for that specific learner.
"""

from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel

from certification.service import check_full_eligibility
from db import db

HorizonItemType = Literal[
    "RESUME_MODULE", "FORMATION_EXPANSION", "CERTIFICATION_ELIGIBLE"
]


class HorizonItem(BaseModel):
    type: HorizonItemType
    formation_code: Optional[str] = None
    formation_name: Optional[str] = None
    module_code: Optional[str] = None
    module_name: Optional[str] = None
    certification_code: Optional[str] = None
    route: str
    pole_color: Optional[str] = None


# Attempt statuses meaning "the learner is already acting on this
# certification, or already holds it" — an item this far along is
# never a "next opportunity" to surface again.
_ATTEMPT_STATUSES_TO_SKIP = ("in_progress", "submitted", "graded", "passed")


async def _certification_items_for_completed_formations(
    user_id: str, formations: List[Dict[str, Any]]
) -> List[HorizonItem]:
    items: List[HorizonItem] = []
    completed = [f for f in formations if (f.get("progress_pct") or 0) >= 100]
    for f in completed:
        rubric_doc = await db.certification_rubrics.find_one(
            {"formation_code": f["code"]}, {"_id": 0}
        )
        if not rubric_doc:
            continue
        certification_code = rubric_doc["certification_code"]

        existing_attempt = await db.certification_attempts.find_one(
            {
                "user_id": user_id,
                "certification_code": certification_code,
                "status": {"$in": list(_ATTEMPT_STATUSES_TO_SKIP)},
            },
            {"_id": 0, "id": 1},
        )
        if existing_attempt:
            continue

        eligible, _reason = await check_full_eligibility(user_id, certification_code)
        if not eligible:
            continue

        items.append(
            HorizonItem(
                type="CERTIFICATION_ELIGIBLE",
                formation_code=f["code"],
                formation_name=f.get("name"),
                certification_code=certification_code,
                pole_color=f.get("pole_color"),
                route=f"/certifications?formation={f['code']}",
            )
        )
    return items


async def compute_progressive_horizon(
    user_id: str, learning_path: Dict[str, Any]
) -> List[HorizonItem]:
    """Pure composition over an already-fetched `user_learning_path()`
    response plus the one new real DB lookup (certification
    eligibility) — no other network/DB access than what's documented
    above. Returns items in real priority order: resume what's already
    in flight, then a real new-territory opportunity (formation
    expansion or certification), never both kinds of "start something
    new" competing for the same top slot."""
    items: List[HorizonItem] = []

    next_action = learning_path.get("next_action")
    if next_action:
        items.append(
            HorizonItem(
                type="RESUME_MODULE",
                formation_code=next_action.get("formation_code"),
                formation_name=next_action.get("formation_name"),
                module_code=next_action.get("module_code"),
                module_name=next_action.get("module_name"),
                pole_color=next_action.get("pole_color"),
                route=next_action.get("route")
                or f"/formations/{next_action.get('formation_code')}/modules/{next_action.get('module_code')}",
            )
        )

    own = learning_path.get("own_pole") or []
    others = learning_path.get("other_poles") or []

    own_pole_exhausted = len(own) > 0 and all(
        (f.get("progress_pct") or 0) >= 100 for f in own
    )
    if own_pole_exhausted:
        expansion_candidates = [
            f
            for f in others
            if f.get("is_unlocked") and (f.get("progress_pct") or 0) < 100
        ][:3]
        for f in expansion_candidates:
            items.append(
                HorizonItem(
                    type="FORMATION_EXPANSION",
                    formation_code=f["code"],
                    formation_name=f.get("name"),
                    pole_color=f.get("pole_color"),
                    route=f"/formations/{f['code']}",
                )
            )

    items.extend(
        await _certification_items_for_completed_formations(user_id, own + others)
    )

    return items
