from pricing_catalog import economic_rules, formation_commercialization, offer_by_id, offers


def test_decided_v1_prices_match_workbook():
    assert offer_by_id("ACADEMY_ACCESS")["monthly_eur"] == 24.90
    assert offer_by_id("ACADEMY_ACCESS")["annual_or_unit_eur"] == 249
    assert offer_by_id("ACADEMY_PRO")["monthly_eur"] == 69
    assert offer_by_id("ACADEMY_CAREER")["annual_or_unit_eur"] == 1290
    assert offer_by_id("CAREER_PATH")["annual_or_unit_eur"] == 990
    assert offer_by_id("INTENSIVE_HYBRID_WEEK")["annual_or_unit_eur"] == 1400
    assert offer_by_id("CERTIFICATION_ACADEMY")["annual_or_unit_eur"] == 390
    assert offer_by_id("B2B_TEAM")["annual_or_unit_eur"] == 12000
    assert offer_by_id("B2G_LARGE")["annual_or_unit_eur"] == 250000


def test_white_label_setup_and_learning_to_work_rules():
    white_label = offer_by_id("WHITE_LABEL_ENTERPRISE")
    assert white_label["annual_or_unit_eur"] == 120000
    assert white_label["setup_eur"] == 25000
    ltw = offer_by_id("LEARNING_TO_WORK_CLIENT")
    assert ltw["gmv_rate"] == 0.12
    assert ltw["minimum_eur"] == 150
    assert ltw["candidate_fee_eur"] == 0


def test_public_offer_filter_excludes_contract_only_offers():
    ids = {item["id"] for item in offers(public_only=True)}
    assert "ACADEMY_PRO" in ids
    assert "CAREER_PATH" in ids
    assert "B2B_TEAM" not in ids
    assert "WHITE_LABEL_ENTERPRISE" not in ids


def test_formation_price_is_offer_based_not_legacy_seed_price():
    formation = {
        "code": "UNMAPPED-EXTERNAL",
        "contexts": ["EXTERNAL", "BRIDGE"],
        "economics": {"public_price_eur": 1400},
    }
    result = formation_commercialization(formation)
    assert result["mapping_status"] == "NEEDS_CANONICAL_MAPPING"
    assert result["price_policy"] != 1400
    assert result["packaging"] == "OFFER_BASED_NOT_FORMATION_PRICE"
    assert "ACADEMY_PRO" in result["eligible_offer_ids"]
    assert "INTENSIVE_HYBRID_WEEK" in result["eligible_offer_ids"]


def test_internal_fallback_is_not_for_sale():
    result = formation_commercialization(
        {"code": "UNMAPPED-INTERNAL", "contexts": ["INTERNAL"]}
    )
    assert result["public"] == "NON"
    assert result["price_policy"] == "NOT_FOR_SALE"
    assert result["eligible_offer_ids"] == []


def test_founder_economic_rules_are_exposed():
    rules = economic_rules()
    assert rules["partner_commission_max_rate"] == 0.15
    assert rules["content_rnd_reinvestment_rate"] == 0.10
    assert rules["intensive_target_learners"] == 15
    assert rules["intensive_target_revenue_eur"] == 21000
    assert rules["intensive_direct_cost_eur"] == 3000
