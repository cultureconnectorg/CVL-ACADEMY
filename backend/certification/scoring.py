"""Pure scoring logic — no DB access, fully unit-testable.

score_by_competency: each criterion's raw score as a percentage of its max.
score_by_bloc: weighted average of that bloc's criteria percentages.
score_global: weighted average across all criteria.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Dict, Tuple

from .models import Rubric


def compute_scores(
    rubric: Rubric, raw_scores: Dict[str, float]
) -> Tuple[Dict[str, float], Dict[str, float], float, bool]:
    """Returns (score_by_competency, score_by_bloc, score_global, passed)."""
    score_by_competency: Dict[str, float] = {}
    bloc_weighted_sum: Dict[str, float] = defaultdict(float)
    bloc_weight_total: Dict[str, float] = defaultdict(float)
    global_weighted_sum = 0.0
    global_weight_total = 0.0

    for c in rubric.criteria:
        raw = max(0.0, min(raw_scores.get(c.id, 0.0), c.max_score))
        pct = (raw / c.max_score * 100) if c.max_score else 0.0
        score_by_competency[c.id] = round(pct, 1)

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
    passed = score_global >= rubric.pass_threshold_pct

    return score_by_competency, score_by_bloc, score_global, passed
