from services.cartography_2d_runtime import (
    CLASSIFICATION_EXCEPTIONS,
    SHEET_ROW_COUNTS,
    SOURCE_WORKBOOK_SHA256,
    TOTAL_NONEMPTY_ROWS,
    load_cartography_2d,
)


def test_cartography_2d_source_contract_is_exact():
    assert SOURCE_WORKBOOK_SHA256 == "43a0885dff4177249fa83fb1e7754d48c871df150309d931349c381954fa6bf2"
    assert SHEET_ROW_COUNTS == {
        "Master_Catalogue": 812,
        "External_Market": 437,
        "Internal_CVLN": 220,
        "Cross_Ecosystem": 153,
        "Operator_Roles": 130,
        "Habilitations": 71,
        "Access_Levels": 7,
        "Missions_Pipelines": 10,
        "Coverage_Gaps": 6,
        "Taxonomy": 9,
        "Dashboard": 29,
    }
    assert TOTAL_NONEMPTY_ROWS == 1884


def test_every_nonempty_excel_row_is_runtime_addressable_and_hashed():
    workbook = load_cartography_2d()
    assert set(workbook) == set(SHEET_ROW_COUNTS)
    assert sum(len(rows) for rows in workbook.values()) == 1884
    for sheet, expected in SHEET_ROW_COUNTS.items():
        assert len(workbook[sheet]) == expected
        assert len({row["row_id"] for row in workbook[sheet]}) == expected
        assert all(row["source_hash"] for row in workbook[sheet])
        assert all(row["source"]["sheet"] == sheet for row in workbook[sheet])
        assert all(row["source"]["excel_row"] == row["excel_row"] for row in workbook[sheet])


def test_master_catalogue_is_812_unique_codes():
    workbook = load_cartography_2d()
    codes = [row["normalized"]["code"] for row in workbook["Master_Catalogue"]]
    assert len(codes) == 812
    assert len(set(codes)) == 812


def test_external_internal_cross_are_exact_disjoint_master_views():
    workbook = load_cartography_2d()
    master = {row["normalized"]["code"] for row in workbook["Master_Catalogue"]}
    external = {row["normalized"]["code"] for row in workbook["External_Market"]}
    internal = {row["normalized"]["code"] for row in workbook["Internal_CVLN"]}
    cross = {row["normalized"]["code"] for row in workbook["Cross_Ecosystem"]}
    assert len(external) == 437
    assert len(internal) == 220
    assert len(cross) == 153
    assert not external & internal
    assert not external & cross
    assert not internal & cross
    assert master - (external | internal | cross) == CLASSIFICATION_EXCEPTIONS


def test_operator_roles_are_130_unique_master_codes():
    workbook = load_cartography_2d()
    master = {row["normalized"]["code"] for row in workbook["Master_Catalogue"]}
    roles = [row["normalized"]["code"] for row in workbook["Operator_Roles"]]
    assert len(roles) == 130
    assert len(set(roles)) == 130
    assert set(roles) <= master


def test_habilitations_preserve_human_authority_boundary():
    workbook = load_cartography_2d()
    rows = workbook["Habilitations"]
    assert len(rows) == 71
    pairs = {(row["normalized"]["domain"], row["normalized"]["habilitation"]) for row in rows}
    assert len(pairs) == 71
    assert all("Certification ≠ pouvoir" in row["normalized"]["principle"] for row in rows)
    assert all(row["normalized"]["status"] == "CANDIDATE" for row in rows)


def test_access_levels_do_not_auto_confer_executive_authority():
    workbook = load_cartography_2d()
    levels = {row["normalized"]["level"]: row["normalized"] for row in workbook["Access_Levels"]}
    assert list(levels) == ["L0", "L1", "L2", "L3", "L4", "L5", "L6"]
    assert "jamais attribuée automatiquement par Academy" in levels["L6"]["definition"]


def test_supporting_sheets_are_complete():
    workbook = load_cartography_2d()
    assert len(workbook["Missions_Pipelines"]) == 10
    assert len(workbook["Coverage_Gaps"]) == 6
    assert len(workbook["Taxonomy"]) == 9
    assert len(workbook["Dashboard"]) == 29
