"""Referential validation across a batch of parsed FMS resources.

Runs after every file in a ZIP has been parsed, so it can check
cross-references (prerequisites, formation_code) between resources in the
same batch — not just each file in isolation.
"""

from __future__ import annotations

from collections import Counter
from typing import List

from .models import FmsResource, ImportIssue


def validate_batch(resources: List[FmsResource]) -> List[ImportIssue]:
    issues: List[ImportIssue] = []
    codes = {r.code for r in resources}

    # Duplicate codes within the same import — last one wins on upsert,
    # which is surprising enough to always flag.
    counts = Counter(r.code for r in resources)
    for code, n in counts.items():
        if n > 1:
            issues.append(
                ImportIssue(
                    level="warning",
                    file=code,
                    message=f"Code « {code} » présent {n} fois dans ce ZIP — le dernier écrase les précédents.",
                )
            )

    for r in resources:
        # Prerequisites should point at another resource in this batch (a
        # module's prereq will usually be another module in the same ZIP).
        for prereq in r.prerequisites:
            if prereq not in codes:
                issues.append(
                    ImportIssue(
                        level="warning",
                        file=r.source_file,
                        message=(
                            f"Prérequis « {prereq} » introuvable dans ce ZIP "
                            f"(peut-être défini dans un import précédent — non bloquant)."
                        ),
                    )
                )

        if r.type == "module" and not r.formation_code:
            issues.append(
                ImportIssue(
                    level="error",
                    file=r.source_file,
                    message="Un module doit déclarer `formation_code:` en frontmatter.",
                )
            )

        if not r.body_markdown:
            issues.append(
                ImportIssue(
                    level="warning",
                    file=r.source_file,
                    message="Fichier sans contenu après le frontmatter.",
                )
            )

    return issues
