"""ACA-0004 — Delivery Architecture Truth (Founder decision, 2026-09-04).

Resolves the `ACA-0004` blocker (`docs/ACADEMY_FMS_CANONICAL_RUNTIME_
BINDING_REPORT.md` never covered this; the canonical archive itself was
grep-confirmed to contain **zero** real delivery-mode signal anywhere —
see the chat record of this session) with the Founder's own explicit
rule, verbatim:

```
CURRICULUM_TRUTH = FMS ZIP 223 DOCS

DELIVERY_ARCHITECTURE_TRUTH = INTERNAL / EXTERNAL / BRIDGE

INTERNAL_DELIVERY = E_LEARNING
EXTERNAL_DELIVERY = E_LEARNING + PHYSICAL/PRESENTIEL
                     (as configured by the external offer)
BRIDGE = ENTRY / ARTICULATION LAYER

CURRICULUM != DELIVERY
DELIVERY != COMMERCIAL_OFFER
```

**This is not extracted from the FMS ZIP** — deliberately: `CURRICULUM
!= DELIVERY` means delivery architecture is not a pedagogical fact the
archive is expected to state (and, confirmed this session, doesn't).
It is derived from `db.formations`'s existing, real `contexts` field
(`Formation.contexts: List[AcademyContext]`, `AcademyContext =
Literal["INTERNAL","EXTERNAL","BRIDGE"]` — `backend/models.py`), applied
by `catalog_cartography.py` to every formation including all 6 FMS
métiers already. This module is the **one deliberate exception** to
`fms_canonical`'s general "never touches `db.formations`" posture
(every other module in this package): reading `contexts` here is a
read-only lookup of an already-real, already-served field — never a
write, and never a read of `modules`/`content_status`/anything else on
that document.

**`DELIVERY != COMMERCIAL_OFFER`** is enforced by never marking `PHYSICAL`
`AVAILABLE` — only `ELIGIBLE_PENDING_OFFER`. Mission `PHYSICAL_SESSION_
AVAILABILITY = REAL_DATA_ONLY` (the original delivery-mode mission) and
`ACA-0007` (physical domain model, not yet built) both still apply: no
code here, or anywhere in this package, claims a real bookable physical
session exists.

This also formally resolves the `AMBIGUOUS` classification of
`catalog_cartography.DELIVERY_FORMATS` from
`docs/ACADEMY_DELIVERY_MODE_AUDIT.md` (headline finding): that field
(a shared `PRO_FORMAT`/`DEFAULT_FORMAT` constant, identical across most
formations) is **not** the source of delivery truth going forward —
`contexts` is, per this Founder decision. `delivery_formats` is left
exactly as-is (untouched, per `DB_FORMATIONS_MUTATION = FORBIDDEN`) —
simply superseded as an input to this derivation.
"""

from __future__ import annotations

from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

from db import db

DeliveryChannel = Literal["INTERNAL", "EXTERNAL"]
DeliveryMode = Literal["E_LEARNING", "PHYSICAL"]
DeliveryStatus = Literal["AVAILABLE", "ELIGIBLE_PENDING_OFFER"]


class DeliveryModeEntry(BaseModel):
    model_config = ConfigDict(extra="ignore")

    mode: DeliveryMode
    channel: DeliveryChannel
    status: DeliveryStatus


class DeliveryArchitecture(BaseModel):
    """One formation's delivery architecture — a distinct truth from its
    curriculum (`CanonicalFormation`, sourced from the FMS ZIP) and from
    any future commercial offer (not built — `ACA-0007`/`ACA-0025`)."""

    model_config = ConfigDict(extra="ignore")

    formation_code: str
    contexts: List[
        str
    ]  # raw INTERNAL/EXTERNAL/BRIDGE, exactly as db.formations has them
    delivery_modes: List[DeliveryModeEntry] = Field(default_factory=list)
    is_bridge_entry_point: bool = False

    curriculum_source: Literal["FMS_ZIP"] = "FMS_ZIP"
    delivery_source: Literal["ACADEMY_CARTOGRAPHY_CONTEXTS"] = (
        "ACADEMY_CARTOGRAPHY_CONTEXTS"
    )


def derive_delivery_architecture(
    formation_code: str, contexts: List[str]
) -> DeliveryArchitecture:
    """Pure — the Founder's rule, applied mechanically to a real
    `contexts` list. No formation-specific judgment is made here; the
    same rule applies identically to every formation, canonical or not."""
    modes: List[DeliveryModeEntry] = []
    if "INTERNAL" in contexts:
        modes.append(
            DeliveryModeEntry(mode="E_LEARNING", channel="INTERNAL", status="AVAILABLE")
        )
    if "EXTERNAL" in contexts:
        modes.append(
            DeliveryModeEntry(mode="E_LEARNING", channel="EXTERNAL", status="AVAILABLE")
        )
        modes.append(
            DeliveryModeEntry(
                mode="PHYSICAL", channel="EXTERNAL", status="ELIGIBLE_PENDING_OFFER"
            )
        )
    return DeliveryArchitecture(
        formation_code=formation_code,
        contexts=list(contexts),
        delivery_modes=modes,
        is_bridge_entry_point="BRIDGE" in contexts,
    )


async def get_delivery_architecture(
    formation_code: str,
) -> Optional[DeliveryArchitecture]:
    """The one read of `db.formations` in this package — read-only,
    `contexts` field only. Returns `None` if the formation doesn't exist
    — never a fabricated default."""
    doc = await db.formations.find_one(
        {"code": formation_code}, {"_id": 0, "contexts": 1}
    )
    if not doc:
        return None
    return derive_delivery_architecture(formation_code, doc.get("contexts", []))
