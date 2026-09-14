"""Shared primitives reused by every canonical runtime binding
(`fms_canonical`, `klt_canonical`, `master_canonical`).

Rail 2 (Master -> Runtime Academy) finding: `fms_canonical/models.py` and
`klt_canonical/models.py` each independently defined their own copy of
the exact same `Audience` Literal and the exact same
`resource_audience()`/`is_learner_facing()` logic, parametrized only by
a domain-specific `RESOURCE_AUDIENCE` dict. Two copies of the same
enum + the same fail-safe-default logic is exactly the kind of
docs/runtime duplication this rail is meant to eliminate — so this
package is the single canonical source for both, going forward.

This is a pure extraction, not a behavior change: each existing
domain's `resource_audience()`/`is_learner_facing()` public function
still exists under the same name, same signature, same fail-safe
default (`["ADMIN", "INTERNAL"]` for an unrecognized type) — they now
delegate to the generic functions here instead of duplicating the
body. No caller of `fms_canonical`/`klt_canonical` needs to change.
"""

from __future__ import annotations

from .audience import (
    Audience,
    is_learner_facing,
    learner_facing_types,
    resource_audience,
    staff_only_types,
)

__all__ = [
    "Audience",
    "resource_audience",
    "is_learner_facing",
    "learner_facing_types",
    "staff_only_types",
]
