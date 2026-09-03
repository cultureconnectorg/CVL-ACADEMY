"""Pure scoring logic — no DB access, fully unit-testable.

score_by_competency: each criterion's raw score as a percentage of its max.
score_by_bloc: weighted average of that bloc's criteria percentages.
score_global: weighted average across all criteria.

Two doctrine-accurate additions on top of that weighted-average core (see
models.py's module docstring for where they come from in the real FMS
grading grille):

eliminated: True the instant any `is_eliminatory` criterion scores exactly
0 — that alone fails the attempt, independent of score_global.
mention: the numeric band from `rubric.mention_thresholds` that
score_global falls into, then possibly lowered (never raised) by a
`cap_rules` match — never computed at all while `eliminated` is True,
since an eliminated attempt has no mention, only a fail.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Dict, List, Optional, Tuple

from .models import Rubric


def _resolve_mention(rubric: Rubric, score_global: float) -> Optional[str]:
    if not rubric.mention_thresholds:
        return None
    ordered = sorted(rubric.mention_thresholds, key=lambda t: t.min_pct, reverse=True)
    for band in ordered:
        if score_global >= band.min_pct:
            return band.mention
    return ordered[-1].mention if ordered else None


def compute_scores(
    rubric: Rubric, raw_scores: Dict[str, float]
) -> Tuple[
    Dict[str, float], Dict[str, float], float, bool, bool, Optional[str], Optional[str]
]:
    """Returns (score_by_competency, score_by_bloc, score_global, passed,
    eliminated, eliminated_reason, mention)."""
    score_by_competency: Dict[str, float] = {}
    bloc_weighted_sum: Dict[str, float] = defaultdict(float)
    bloc_weight_total: Dict[str, float] = defaultdict(float)
    global_weighted_sum = 0.0
    global_weight_total = 0.0
    eliminated = False
    eliminated_reasons: List[str] = []

    for c in rubric.criteria:
        raw = max(0.0, min(raw_scores.get(c.id, 0.0), c.max_score))
        pct = (raw / c.max_score * 100) if c.max_score else 0.0
        score_by_competency[c.id] = round(pct, 1)

        if c.is_eliminatory and raw == 0:
            eliminated = True
            eliminated_reasons.append(
                f"{c.id} ({c.label}) — niveau 0, critère éliminatoire"
            )

        bloc_weighted_sum[c.bloc] += pct * c.weight
        bloc_weight_total[c.bloc] += c.weight
        global_weighted_sum += pct * c.weight
        global_weight_total += c.weight

    score_by_bloc = {
        bloc: round(bloc_weighted_sum[bloc] / bloc_weight_total[bloc], 1)
        for bloc in bloc_weighted_sum
        if bloc_weight_total[bloc]
    }
    score_global = (
        round(global_weighted_sum / global_weight_total, 1)
        if global_weight_total
        else 0.0
    )

    eliminated_reason = "; ".join(eliminated_reasons) if eliminated_reasons else None
    passed = (not eliminated) and score_global >= rubric.pass_threshold_pct

    mention: Optional[str] = None
    if not eliminated:
        mention = _resolve_mention(rubric, score_global)
        mention_rank = {
            band.mention: band.min_pct for band in rubric.mention_thresholds
        }
        for cap in rubric.cap_rules:
            raw = raw_scores.get(cap.criterion_id, 0.0)
            if raw <= cap.max_raw_score_to_trigger:
                # A cap can only ever lower the mention, never raise it —
                # compare by the capped mention's own band floor.
                current_floor = (
                    mention_rank.get(mention, float("-inf"))
                    if mention
                    else float("-inf")
                )
                capped_floor = mention_rank.get(cap.capped_mention, float("-inf"))
                if mention is None or capped_floor < current_floor:
                    mention = cap.capped_mention

    return (
        score_by_competency,
        score_by_bloc,
        score_global,
        passed,
        eliminated,
        eliminated_reason,
        mention,
    )
