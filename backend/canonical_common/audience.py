"""The one `Audience` type + generic resource-audience lookup, shared by
every canonical runtime binding.

`Audience` is CVLN Academy's runtime representation of the docs corpus's
own access-level vocabulary (`docs/cvln_academy_master/00_GOVERNANCE/
AUTHORIZATION_MODEL.md`'s LEARNER/TRAINER/CORRECTOR/JURY/ADMIN/INTERNAL
tiers) — a resource's `RESOURCE_AUDIENCE` mapping is a domain-specific
fact (which file types a given canonical corpus produces), but the type
itself and the fail-safe lookup behavior are not domain-specific, so
they live here once.
"""

from __future__ import annotations

from typing import Dict, List, Literal

Audience = Literal["LEARNER", "TRAINER", "CORRECTOR", "JURY", "ADMIN", "INTERNAL"]

#: The conservative fail-safe default for a resource type a domain's own
#: mapping doesn't recognize — never `LEARNER`, so an unclassified file
#: is never accidentally leaked to a candidate.
_DEFAULT_AUDIENCE: List[Audience] = ["ADMIN", "INTERNAL"]


def resource_audience(
    mapping: Dict[str, List[Audience]], resource_type: str
) -> List[Audience]:
    """Fail-safe: an unrecognized type gets `_DEFAULT_AUDIENCE`, never
    `LEARNER`."""
    return mapping.get(resource_type, _DEFAULT_AUDIENCE)


def is_learner_facing(mapping: Dict[str, List[Audience]], resource_type: str) -> bool:
    """Fail-safe: an unrecognized type is treated as staff-only, never
    leaked by default."""
    return "LEARNER" in resource_audience(mapping, resource_type)


def learner_facing_types(mapping: Dict[str, List[Audience]]) -> frozenset:
    """Backward-compatible derived set, computed from `mapping`, never
    maintained separately so the two can't drift apart."""
    return frozenset(t for t, aud in mapping.items() if "LEARNER" in aud)


def staff_only_types(mapping: Dict[str, List[Audience]]) -> frozenset:
    return frozenset(t for t, aud in mapping.items() if "LEARNER" not in aud)
