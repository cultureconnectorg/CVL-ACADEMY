"""Pure unit tests for quiz.py — no DB/network required.

Complements backend_test.py (which is a live-server E2E suite) with fast,
isolated coverage of the quiz scoring logic itself.
"""

from __future__ import annotations

from quiz import build_quiz, evaluate

MODULE = {
    "code": "FMS-01-M01",
    "name": "Poser son univers artistique",
    "stade": "graine",
    "deliverable": "Fiche univers artistique v1",
    "hook": "Un artiste martiniquais sans positionnement clair",
    "frek_signal": "FREK-WORK archive_livrable",
}


def _correct_answers(quiz):
    return {
        str(q["n"]): next(c["id"] for c in q["choices"] if c["correct"]) for q in quiz
    }


class TestBuildQuiz:
    def test_returns_eight_questions(self):
        quiz = build_quiz(MODULE)
        assert len(quiz) == 8
        assert [q["n"] for q in quiz] == list(range(1, 9))

    def test_every_question_has_exactly_one_correct_choice(self):
        quiz = build_quiz(MODULE)
        for q in quiz:
            correct = [c for c in q["choices"] if c["correct"]]
            assert (
                len(correct) == 1
            ), f"question {q['n']} has {len(correct)} correct choices"

    def test_unknown_stade_raises(self):
        bad = {**MODULE, "stade": "not-a-real-stade"}
        try:
            build_quiz(bad)
        except KeyError:
            pass
        else:
            raise AssertionError("expected KeyError for unknown stade")


class TestEvaluate:
    def test_all_correct_passes_with_full_score(self):
        quiz = build_quiz(MODULE)
        result = evaluate(quiz, _correct_answers(quiz))
        assert result == {"correct": 8, "total": 8, "score": 1.0, "passed": True}

    def test_all_wrong_fails(self):
        quiz = build_quiz(MODULE)
        wrong = {str(q["n"]): "__none__" for q in quiz}
        result = evaluate(quiz, wrong)
        assert result["correct"] == 0
        assert result["passed"] is False

    def test_threshold_is_80_percent(self):
        quiz = build_quiz(MODULE)
        answers = _correct_answers(quiz)
        # Flip exactly 2 of 8 answers (75%) — must fail the 80% threshold.
        for n in ("1", "2"):
            answers[n] = "__wrong__"
        result = evaluate(quiz, answers)
        assert result["score"] == 0.75
        assert result["passed"] is False

    def test_empty_quiz_scores_zero_without_dividing_by_zero(self):
        result = evaluate([], {})
        assert result == {"correct": 0, "total": 0, "score": 0.0, "passed": False}
