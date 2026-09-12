from __future__ import annotations

from corpus_812 import (
    EXPECTED_CORPUS_COUNT,
    EXPECTED_FORMATION_COUNT,
    formation_codes,
    formation_learning_evidence,
    legacy_mapping_report,
    module_has_authored_content,
    module_has_structure,
    runtime_coverage,
)


def test_canonical_formation_projection_is_complete_and_unique():
    codes = formation_codes()
    assert EXPECTED_CORPUS_COUNT == 812
    assert len(codes) == EXPECTED_FORMATION_COUNT == 554
    assert len(set(codes)) == 554
    assert "BCI-01" in codes
    assert "BCI-30" in codes
    assert "KLT-09" in codes
    assert "KLT-20" in codes


def test_legacy_mapping_report_keeps_noncanonical_history_visible():
    report = legacy_mapping_report()
    assert report["runtime_count"] == 30
    assert report["direct_canonical_count"] == 14
    assert report["legacy_only_count"] == 16
    assert "BCH-01" in report["legacy_only_codes"]
    assert "KLT-01" in report["legacy_only_codes"]
    assert "GMD-01" in report["direct_canonical_codes"]


def test_module_structure_is_not_authored_content():
    module = {
        "code": "KLT-01-M01",
        "name": "Comprendre la médiation culturelle",
        "deliverable": "Diagnostic de territoire",
        "hook": "Cas terrain",
    }
    assert module_has_structure(module) is True
    assert module_has_authored_content(module) is False


def test_generic_fallback_does_not_pass_learning_content_gate():
    formation = {
        "code": "BCH-01",
        "modules": [
            {
                "code": "BCH-01-M01",
                "name": "Blockchain culturelle",
                "deliverable": "Note de cadrage",
                "hook": "Cas culturel",
            }
        ],
    }
    evidence = formation_learning_evidence(formation)
    assert evidence["module_structure_complete"] is True
    assert evidence["authored_learning_content_complete"] is False
    assert evidence["uses_only_fallback_content"] is True


def test_substantial_authored_content_can_pass_content_gate():
    authored_body = "A" * 600
    formation = {
        "code": "BCI-01",
        "modules": [
            {
                "code": "BCI-01-M01",
                "name": "Blockchain Foundations",
                "deliverable": "Architecture commentée",
                "authored_content_md": authored_body,
            }
        ],
    }
    evidence = formation_learning_evidence(formation)
    assert evidence["module_structure_complete"] is True
    assert evidence["authored_learning_content_complete"] is True
    assert evidence["uses_only_fallback_content"] is False


def test_runtime_coverage_reports_canonical_and_legacy_separately():
    runtime = [
        {
            "code": "GMD-01",
            "modules": [
                {
                    "code": "GMD-01-M01",
                    "name": "Event foundations",
                    "deliverable": "Production brief",
                }
            ],
        },
        {
            "code": "BCH-01",
            "modules": [
                {
                    "code": "BCH-01-M01",
                    "name": "Blockchain culturelle",
                    "deliverable": "Note",
                }
            ],
        },
    ]
    report = runtime_coverage(runtime)
    assert report["runtime_formations"] == 2
    assert report["runtime_direct_canonical"] == 1
    assert report["runtime_legacy_only"] == 1
    assert report["runtime_with_complete_module_structure"] == 2
    assert report["runtime_with_complete_authored_content"] == 0
    assert report["runtime_fallback_only"] == 2
