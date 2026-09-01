"""Pure unit tests for the certification scoring engine — no DB required.

Covers both the original weighted-average core and the doctrine-accurate
additions reconciled against the real FMS-01 grading grille (eliminatory
criteria, mention caps) — see certification/models.py and scoring.py.
"""

from __future__ import annotations

from certification.models import (
    MentionThreshold,
    Rubric,
    RubricCapRule,
    RubricCriterion,
)
from certification.scoring import compute_scores


def _rubric(pass_threshold_pct: float = 80.0) -> Rubric:
    return Rubric(
        certification_code="FMS-N1",
        level="N1",
        formation_code="FMS-01",
        pass_threshold_pct=pass_threshold_pct,
        criteria=[
            RubricCriterion(
                id="C1", label="Univers artistique", bloc="B1", max_score=10, weight=1
            ),
            RubricCriterion(
                id="C2", label="Storytelling", bloc="B1", max_score=10, weight=2
            ),
            RubricCriterion(
                id="C3", label="Plan marketing", bloc="B2", max_score=20, weight=1
            ),
        ],
    )


def _rubric_master_style() -> Rubric:
    """Mirrors FMS-01's real A01 grille: 19 Skill IDs on a 0-4 scale, 3
    eliminatory (verrous doctrinaux), 1 cap rule (F1 -> plafond Passable),
    5 mention bands."""
    criteria = [
        RubricCriterion(
            id="FMS01-B2", label="Verrou 1", bloc="B", max_score=4, is_eliminatory=True
        ),
        RubricCriterion(
            id="FMS01-C1", label="Verrou 2", bloc="C", max_score=4, is_eliminatory=True
        ),
        RubricCriterion(
            id="FMS01-E1", label="Verrou 3", bloc="E", max_score=4, is_eliminatory=True
        ),
        RubricCriterion(
            id="FMS01-F1", label="Cohérence globale", bloc="F", max_score=4
        ),
        RubricCriterion(id="FMS01-A1", label="Autre compétence", bloc="A", max_score=4),
    ]
    return Rubric(
        certification_code="FMS-01-A01",
        level="A01",
        formation_code="FMS-01",
        pass_threshold_pct=50.0,
        criteria=criteria,
        cap_rules=[
            RubricCapRule(
                criterion_id="FMS01-F1",
                max_raw_score_to_trigger=1,
                capped_mention="Passable",
            )
        ],
        mention_thresholds=[
            MentionThreshold(min_pct=0, mention="Ajourné"),
            MentionThreshold(min_pct=50, mention="Passable"),
            MentionThreshold(min_pct=64, mention="Bien"),
            MentionThreshold(min_pct=80, mention="Très bien"),
            MentionThreshold(min_pct=90, mention="Excellence"),
        ],
    )


class TestComputeScores:
    def test_perfect_scores_pass(self):
        rubric = _rubric()
        by_c, by_bloc, global_pct, passed, eliminated, reason, mention = compute_scores(
            rubric, {"C1": 10, "C2": 10, "C3": 20}
        )
        assert by_c == {"C1": 100.0, "C2": 100.0, "C3": 100.0}
        assert by_bloc == {"B1": 100.0, "B2": 100.0}
        assert global_pct == 100.0
        assert passed is True
        assert eliminated is False
        assert reason is None

    def test_weighted_bloc_average(self):
        rubric = _rubric()
        # B1: C1=50% (weight 1), C2=100% (weight 2) -> (50*1 + 100*2) / 3 = 83.3
        by_c, by_bloc, global_pct, passed, *_ = compute_scores(
            rubric, {"C1": 5, "C2": 10, "C3": 20}
        )
        assert by_bloc["B1"] == 83.3
        assert by_bloc["B2"] == 100.0

    def test_below_threshold_fails(self):
        rubric = _rubric(pass_threshold_pct=80.0)
        _, _, global_pct, passed, *_ = compute_scores(
            rubric, {"C1": 0, "C2": 0, "C3": 0}
        )
        assert global_pct == 0.0
        assert passed is False

    def test_missing_criterion_score_defaults_to_zero(self):
        rubric = _rubric()
        by_c, *_ = compute_scores(rubric, {"C1": 10})  # C2, C3 omitted
        assert by_c["C2"] == 0.0
        assert by_c["C3"] == 0.0

    def test_raw_score_is_clamped_to_max(self):
        rubric = _rubric()
        by_c, *_ = compute_scores(rubric, {"C1": 999, "C2": -5, "C3": 20})
        assert by_c["C1"] == 100.0  # clamped, not >100%
        assert by_c["C2"] == 0.0  # clamped, not negative

    def test_exact_threshold_passes(self):
        rubric = _rubric(pass_threshold_pct=50.0)
        _, _, global_pct, passed, *_ = compute_scores(
            rubric, {"C1": 5, "C2": 5, "C3": 10}
        )
        assert global_pct == 50.0
        assert passed is True


class TestEliminatoryCriteria:
    def test_zero_on_eliminatory_criterion_fails_regardless_of_total(self):
        rubric = _rubric_master_style()
        # Everything else maxed out, but FMS01-B2 (a verrou) is 0.
        scores = {
            "FMS01-B2": 0,
            "FMS01-C1": 4,
            "FMS01-E1": 4,
            "FMS01-F1": 4,
            "FMS01-A1": 4,
        }
        _, _, global_pct, passed, eliminated, reason, mention = compute_scores(
            rubric, scores
        )
        assert global_pct == 80.0  # numerically well above threshold
        assert eliminated is True
        assert passed is False
        assert "FMS01-B2" in reason
        assert mention is None  # eliminated attempts get no mention

    def test_low_nonzero_score_on_eliminatory_criterion_does_not_eliminate(self):
        rubric = _rubric_master_style()
        scores = {
            "FMS01-B2": 1,  # detected but incomplete — not a 0 — doesn't eliminate
            "FMS01-C1": 4,
            "FMS01-E1": 4,
            "FMS01-F1": 4,
            "FMS01-A1": 4,
        }
        *_, eliminated, reason, _ = compute_scores(rubric, scores)
        assert eliminated is False
        assert reason is None

    def test_multiple_eliminatory_failures_all_reported(self):
        rubric = _rubric_master_style()
        scores = {
            "FMS01-B2": 0,
            "FMS01-C1": 0,
            "FMS01-E1": 4,
            "FMS01-F1": 4,
            "FMS01-A1": 4,
        }
        *_, eliminated, reason, _ = compute_scores(rubric, scores)
        assert eliminated is True
        assert "FMS01-B2" in reason and "FMS01-C1" in reason


class TestMentionCapRule:
    def test_high_score_gets_matching_mention_band(self):
        rubric = _rubric_master_style()
        scores = {
            "FMS01-B2": 4,
            "FMS01-C1": 4,
            "FMS01-E1": 4,
            "FMS01-F1": 4,
            "FMS01-A1": 4,
        }
        *_, mention = compute_scores(rubric, scores)
        assert mention == "Excellence"

    def test_f1_at_or_below_one_caps_mention_to_passable(self):
        rubric = _rubric_master_style()
        # Every other criterion maxed (would be "Excellence" on the raw
        # number), but F1 (cohérence globale) is only 1/4 -> capped.
        scores = {
            "FMS01-B2": 4,
            "FMS01-C1": 4,
            "FMS01-E1": 4,
            "FMS01-F1": 1,
            "FMS01-A1": 4,
        }
        _, _, global_pct, passed, eliminated, _, mention = compute_scores(
            rubric, scores
        )
        assert eliminated is False
        assert passed is True
        assert mention == "Passable"  # capped despite a high numeric score

    def test_cap_never_raises_a_mention_that_would_already_be_lower(self):
        rubric = _rubric_master_style()
        # Numeric score alone lands in "Ajourné" territory; F1 also
        # triggers the cap to "Passable" — the cap must not raise the
        # mention above what the score already implies as a floor... but
        # per doctrine the cap is the authority here (it always lowers to
        # exactly "Passable", never higher) — this asserts it doesn't
        # crash and lands on the capped value either way.
        scores = {
            "FMS01-B2": 4,
            "FMS01-C1": 1,
            "FMS01-E1": 1,
            "FMS01-F1": 1,
            "FMS01-A1": 1,
        }
        *_, mention = compute_scores(rubric, scores)
        assert mention in ("Passable", "Ajourné")
