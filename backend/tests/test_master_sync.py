from services.master_sync import validate_master_sources


def test_all_coded_excel_master_sources_validate_before_sync():
    result = validate_master_sources()

    assert result["valid"] is True
    assert result["catalogue_rows"] == 812
    assert result["economy_rows"] == 812
    assert result["shared_codes"] == 812
    assert result["cartography_2d_rows"] == 1884
    assert result["cartography_2d_sheets"] == 11
    assert result["protocol_rows"] == 227
