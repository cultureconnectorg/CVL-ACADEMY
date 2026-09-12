from corpus_learning_contract import (
    CorpusObjectType,
    LearningCompleteness,
    ReconciliationRecord,
    ReconciliationStatus,
    classify_corpus_type,
)


def test_corpus_type_classification():
    assert classify_corpus_type("Formation") == CorpusObjectType.FORMATION
    assert (
        classify_corpus_type("Internal skill / operator")
        == CorpusObjectType.INTERNAL_SKILL_OPERATOR
    )
    assert (
        classify_corpus_type("Cross-ecosystem competency")
        == CorpusObjectType.CROSS_ECOSYSTEM_COMPETENCY
    )
    assert classify_corpus_type("Transversal") == CorpusObjectType.TRANSVERSAL
    assert classify_corpus_type("Case Lab") == CorpusObjectType.CASE_LAB
    assert classify_corpus_type("Coverage gap") == CorpusObjectType.GAP_TO_RECONCILE


def test_complete_requires_every_gate():
    completeness = LearningCompleteness(
        canonical_identity=True,
        pedagogical_design=True,
        learning_content=True,
        assessment=True,
        commercialization_access=True,
        runtime=True,
        verification=True,
    )
    assert completeness.complete is True
    assert completeness.missing_gates() == []


def test_published_formation_without_modules_is_invalid():
    record = ReconciliationRecord(
        canonical_code="BCI-01",
        canonical_title="Blockchain Foundations",
        source_workbook="CVLN_Academy_Cartographie_2D_Master.xlsx",
        source_sheet="Master_Catalogue",
        source_row=216,
        classification=CorpusObjectType.FORMATION,
        status=ReconciliationStatus.PUBLISHED,
        module_count_implemented=0,
    )
    errors = record.validate()
    assert "implemented formation has no real module" in errors
    assert "published formation does not pass every completeness gate" in errors


def test_verified_complete_formation_is_publishable():
    completeness = LearningCompleteness(
        canonical_identity=True,
        pedagogical_design=True,
        learning_content=True,
        assessment=True,
        commercialization_access=True,
        runtime=True,
        verification=True,
    )
    record = ReconciliationRecord(
        canonical_code="KLT-01",
        canonical_title="Médiateur culturel",
        source_workbook="CVLN_Academy_Kiltikonet_Formation_Master_Plan.xlsx",
        source_sheet="Plan modules",
        source_row=3,
        classification=CorpusObjectType.FORMATION,
        status=ReconciliationStatus.VERIFIED,
        module_count_expected=8,
        module_count_implemented=8,
        completeness=completeness,
    )
    assert record.publishable is True
    assert record.validate() == []
