"""Canonical CVLN Academy commercial offer catalogue.

Source of truth:
CVLN_Academy_Master_Economie_3D_DECIDE_V1.xlsx

The workbook explicitly separates pedagogical objects from commercial products
(ECO-001). Prices here are offer prices in EUR; they are never inferred as the
price of an individual formation.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict, List

from economy_3d import commercial_class, record_by_code

SOURCE_WORKBOOK = "CVLN_Academy_Master_Economie_3D_DECIDE_V1.xlsx"
SOURCE_STATUS = "DECIDED_V1"

OFFER_CATALOG: List[Dict[str, Any]] = [
    {"id":"FREE_ORIENTATION","name":"Free Orientation","channel":"B2C","commercialization":"public","status":"DECIDED_V1","monthly_eur":0,"annual_or_unit_eur":0,"billing":"free","decision_id":"ECO-003"},
    {"id":"ACADEMY_ACCESS","name":"Academy Access","channel":"B2C","commercialization":"public","status":"DECIDED_V1","monthly_eur":24.90,"annual_or_unit_eur":249,"billing":"subscription","decision_id":"ECO-004"},
    {"id":"ACADEMY_PRO","name":"Academy Pro","channel":"B2C","commercialization":"public","status":"DECIDED_V1","monthly_eur":69,"annual_or_unit_eur":690,"billing":"subscription","decision_id":"ECO-005"},
    {"id":"ACADEMY_CAREER","name":"Academy Career","channel":"B2C Career","commercialization":"public","status":"DECIDED_V1","monthly_eur":129,"annual_or_unit_eur":1290,"billing":"subscription","decision_id":"ECO-006"},
    {"id":"CAREER_PATH","name":"Parcours métier","channel":"B2C/B2B","commercialization":"public","status":"DECIDED_V1","monthly_eur":0,"annual_or_unit_eur":990,"billing":"one_time","decision_id":"ECO-007"},
    {"id":"INTENSIVE_HYBRID_WEEK","name":"Intensive Hybrid Week","channel":"B2C/B2B/B2G","commercialization":"cohort","status":"DECIDED_V1","monthly_eur":0,"annual_or_unit_eur":1400,"billing":"per_learner","decision_id":"ECO-008"},
    {"id":"ASSESSMENT_ONLY","name":"Assessment Only","channel":"Certification","commercialization":"public","status":"DECIDED_V1","monthly_eur":0,"annual_or_unit_eur":250,"billing":"one_time","decision_id":"ECO-009"},
    {"id":"CERTIFICATION_ACADEMY","name":"Certification Academy","channel":"Certification","commercialization":"public","status":"DECIDED_V1","monthly_eur":0,"annual_or_unit_eur":390,"billing":"one_time","decision_id":"ECO-010"},
    {"id":"CERTIFICATION_RENEWAL","name":"Renewal","channel":"Certification","commercialization":"public","status":"DECIDED_V1","monthly_eur":0,"annual_or_unit_eur":190,"billing":"one_time","decision_id":"ECO-011"},
    {"id":"B2B_TEAM","name":"B2B Team","channel":"B2B","commercialization":"contract","status":"DECIDED_V1","annual_or_unit_eur":12000,"billing":"annual_contract","capacity":10,"decision_id":"ECO-012"},
    {"id":"B2B_GROWTH","name":"B2B Growth","channel":"B2B","commercialization":"contract","status":"DECIDED_V1","annual_or_unit_eur":39000,"billing":"annual_contract","capacity":50,"decision_id":"ECO-013"},
    {"id":"B2B_ENTERPRISE","name":"B2B Enterprise","channel":"B2B","commercialization":"contract","status":"DECIDED_V1","annual_or_unit_eur":69000,"billing":"annual_contract","capacity":100,"decision_id":"ECO-014"},
    {"id":"B2G_PILOT","name":"B2G Pilot","channel":"B2G","commercialization":"contract","status":"DECIDED_V1","annual_or_unit_eur":35000,"billing":"program","capacity":25,"decision_id":"ECO-015"},
    {"id":"B2G_TERRITORY","name":"B2G Territory","channel":"B2G","commercialization":"contract","status":"DECIDED_V1","annual_or_unit_eur":120000,"billing":"program","capacity":100,"decision_id":"ECO-016"},
    {"id":"B2G_LARGE","name":"B2G Large","channel":"B2G","commercialization":"contract","status":"DECIDED_V1","annual_or_unit_eur":250000,"billing":"program","capacity":250,"decision_id":"ECO-017"},
    {"id":"LEARNING_TO_WORK_CLIENT","name":"Learning-to-Work","channel":"Mission","commercialization":"contract","status":"DECIDED_V1","annual_or_unit_eur":150,"billing":"12_percent_gmv_minimum","gmv_rate":0.12,"minimum_eur":150,"candidate_fee_eur":0,"decision_id":"ECO-019"},
    {"id":"METHODOLOGY_IP_LICENCE","name":"Methodology/IP Licence","channel":"Platform/IP","commercialization":"b2b_b2g","status":"DECIDED_PHASE_2","annual_or_unit_eur":25000,"billing":"annual_contract","decision_id":"ECO-021"},
    {"id":"ACADEMY_SPATIAL_LICENCE","name":"Academy+Spatial Licence","channel":"Platform/IP","commercialization":"b2b_b2g","status":"DECIDED_PHASE_3","annual_or_unit_eur":60000,"billing":"annual_contract","decision_id":"ECO-022"},
    {"id":"WHITE_LABEL_ENTERPRISE","name":"White-label Enterprise","channel":"Platform/IP","commercialization":"enterprise","status":"DECIDED_PHASE_3","annual_or_unit_eur":120000,"setup_eur":25000,"billing":"annual_contract_plus_setup","decision_id":"ECO-023"},
]

OFFER_BY_ID = {offer["id"]: offer for offer in OFFER_CATALOG}
PUBLIC_OFFER_IDS = {"FREE_ORIENTATION","ACADEMY_ACCESS","ACADEMY_PRO","ACADEMY_CAREER","CAREER_PATH","INTENSIVE_HYBRID_WEEK","ASSESSMENT_ONLY","CERTIFICATION_ACADEMY","CERTIFICATION_RENEWAL"}
MARKET_ELIGIBLE_OFFERS = ["ACADEMY_PRO","CAREER_PATH","INTENSIVE_HYBRID_WEEK","B2B_TEAM","B2B_GROWTH","B2B_ENTERPRISE","B2G_PILOT","B2G_TERRITORY","B2G_LARGE"]
CROSS_CVLN_OFFERS = ["B2B_TEAM","B2B_GROWTH","B2B_ENTERPRISE","B2G_PILOT","B2G_TERRITORY","B2G_LARGE"]
BRIDGE_OFFERS = ["ACADEMY_CAREER", *CROSS_CVLN_OFFERS]


def offers(*, public_only: bool = False) -> List[Dict[str, Any]]:
    items = OFFER_CATALOG
    if public_only:
        items = [offer for offer in items if offer["id"] in PUBLIC_OFFER_IDS]
    return deepcopy(items)


def offer_by_id(offer_id: str) -> Dict[str, Any]:
    try:
        return deepcopy(OFFER_BY_ID[offer_id.strip().upper()])
    except KeyError as exc:
        raise KeyError(offer_id) from exc


def formation_commercialization(formation: Dict[str, Any]) -> Dict[str, Any]:
    """Resolve commercial routes without inventing a per-formation price."""
    code = str(formation.get("code") or "").strip()
    if code:
        try:
            record = record_by_code(code)
            category = commercial_class(record)
            result = {
                "mapping_status": "CANONICAL",
                "mapping_source": "Economy3D/Mapping_812",
                "economic_class": record["class_code"],
                "commercial_class": category,
                "public": record["public"],
                "packaging": record["packaging_v1"],
                "price_policy": record["prix_public_v1"],
                "activation_gate": record["activation_gate"],
                "eligible_offer_ids": [],
            }
            if category == "PUBLIC_MARKET":
                result["eligible_offer_ids"] = MARKET_ELIGIBLE_OFFERS
            elif category == "CROSS_ECOSYSTEM_PROGRAM":
                result["eligible_offer_ids"] = CROSS_CVLN_OFFERS
            elif category == "BUNDLED_BRIDGE":
                result["eligible_offer_ids"] = BRIDGE_OFFERS
            return result
        except KeyError:
            pass

    contexts = {str(v).upper() for v in formation.get("contexts", [])}
    base = {"mapping_status":"NEEDS_CANONICAL_MAPPING","mapping_source":"formation.contexts fallback","economic_class":None,"eligible_offer_ids":[]}
    if "EXTERNAL" in contexts:
        return {**base,"commercial_class":"PUBLIC_MARKET_UNMAPPED","public":"OUI","packaging":"OFFER_BASED_NOT_FORMATION_PRICE","price_policy":"subscription / €990 path / cohort / contract","eligible_offer_ids":MARKET_ELIGIBLE_OFFERS}
    if "BRIDGE" in contexts:
        return {**base,"commercial_class":"BUNDLED_BRIDGE_UNMAPPED","public":"SÉLECTIF","packaging":"BUNDLED_BRIDGE","price_policy":"Pas vendu seul","eligible_offer_ids":BRIDGE_OFFERS}
    return {**base,"commercial_class":"INTERNAL_NOT_FOR_SALE_UNMAPPED","public":"NON","packaging":"INTERNAL","price_policy":"NOT_FOR_SALE"}


def economic_rules() -> Dict[str, Any]:
    return {
        "currency":"EUR",
        "payment_installments":"3x sans frais dès €300; pas de 6x en V1",
        "annual_discount":"16.7% vs mensualisation (intégrée aux prix annuels)",
        "scholarship_rate":0.10,
        "partner_commission_max_rate":0.15,
        "content_rnd_reinvestment_rate":0.10,
        "intensive_target_learners":15,
        "intensive_target_revenue_eur":21000,
        "intensive_direct_cost_eur":3000,
        "price_boundary":"Prix EUR; CVE mesure; Wallet exécute; JCC reste distinct",
        "claims_rule":"Aucun claim RNCP/CPF/financement sans preuve vérifiée",
        "source_workbook":SOURCE_WORKBOOK,
        "status":SOURCE_STATUS,
    }
