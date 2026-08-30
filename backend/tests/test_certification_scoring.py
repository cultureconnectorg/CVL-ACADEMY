"""Pure unit tests for the certification scoring engine — no DB required."""

from __future__ import annotations

from certification.models import Rubric, RubricCriterion
from certification.scoring import compute_scores


def _rubric(pass_threshold_pct: float = 80.0) -> Rubric:
    return Rubric(
        certification_code="FMS-N1",
        level="N1",
        formation_code="FMS-01",
        pass_threshold_pct=pass_threshold_pct,
        criteria=[
            RubricCriterion(id="C1", label="Univers artistique", bloc="B1", max_score=10, weight=1),
            RubricCriterion(id="C2", label="Storytelling", bloc="B1", max_score=10, weight=2),
            RubricCriterion(id="C3", label="Plan marketing", bloc="B2", max_score=20, weight=1),
        ],
    )


class TestComputeScores:
    def test_perfect_scores_pass(self):
        rubric = _rubric()
        by_c, by_bloc, global_pct, passed = compute_scores(
            rubric, {"C1": 10, "C2": 10, "C3": 20}
        )
        assert by_c == {"C1": 100.0, "C2": 100.0, "C3": 100.0}
        assert by_bloc == {"B1": 100.0, "B2": 100.0}
        assert global_pct == 100.0
        assert passed is True

    def test_weighted_bloc_average(self):
        rubric = _rubric()
        # B1: C1=50% (weight 1), C2=100% (weight 2) -> (50*1 + 100*2) / 3 = 83.3
        by_c, by_bloc, global_pct, passed = compute_scores(
            rubric, {"C1": 5, "C2": 10, "C3": 20}
        )
        assert by_bloc["B1"] == 83.3
        assert by_bloc["B2"] == 100.0

    def test_below_threshold_fails(self):
        rubric = _rubric(pass_threshold_pct=80.0)
        _, _, global_pct, passed = compute_scores(rubric, {"C1": 0, "C2": 0, "C3": 0})
        assert global_pct == 0.0
        assert passed is False

    def test_missing_criterion_score_defaults_to_zero(self):
        rubric = _rubric()
        by_c, _, _, _ = compute_scores(rubric, {"C1": 10})  # C2, C3 omitted
        assert by_c["C2"] == 0.0
        assert by_c["C3"] == 0.0

    def test_raw_score_is_clamped_to_max(self):
        rubric = _rubric()
        by_c, _, _, _ = compute_scores(rubric, {"C1": 999, "C2": -5, "C3": 20})
        assert by_c["C1"] == 100.0  # clamped, not >100%
        assert by_c["C2"] == 0.0  # clamped, not negative

    def test_exact_threshold_passes(self):
        rubric = _rubric(pass_threshold_pct=50.0)
        _, _, global_pct, passed = compute_scores(rubric, {"C1": 5, "C2": 5, "C3": 10})
        assert global_pct == 50.0
        assert passed is True
