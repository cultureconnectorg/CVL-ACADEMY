"""Best-effort dependency extraction from a Master Module Map document.

The real FMS ZIP's `NN_FMS0<n>_Master_Module_Map.md` is the one document
type explicitly declared authoritative by its own authors ("Aucun module
ne doit être rédigé avant que sa ligne ici soit validée" —
09_FMS01_Master_Module_Map.md). It comes in **two real layouts**,
confirmed by inspecting all 6 métiers' Module Maps:

- FMS-01/FMS-02: one field per table row —
  `| **ID** | FMS01-M07 |` ... `| **Prérequis** | M03 |`.
- FMS-03..FMS-06: one compact row per module, fields separated by "·" —
  `| **ID** | FMS03-M03 · **Bloc** : A · ... · **Prérequis** : M02 · ... |`
  (FMS-04's own Module Map even calls out this compaction as deliberate;
  it is not a formatting mistake to normalize away).

Both encode the same thing: an `**ID**` marker naming the module, and a
`**Prérequis**` marker naming its prerequisite module(s) — just delimited
by `|` in one layout and `·` in the other. This module extracts from
either, and deliberately does **not** interpret the certification row
(`FMS0n-A0n`): that cell mixes a hard prerequisite with merely-recommended
and never-required modules in free prose (FMS-01's A01 row: "M12
(obligatoire) ; M13/M14 recommandés ... ; M15 jamais requis") —
collapsing that into a flat dependency list would misrepresent the
doctrine, so importer.py only ever applies this graph to `module`
resources, never to certification resources.

Tolerant by construction: if a métier's Module Map doesn't follow either
pattern for a given row, that row is simply absent from the result — never
a crash, never a fabricated edge.
"""

from __future__ import annotations

import re
from typing import Dict, List

# One module's ID marker, e.g. "**ID** | FMS01-M07" or "**ID** | FMS03-M03 ·
# ..." -> "M07"/"M03" — deliberately not anchored to what follows, since
# that differs between the two real layouts.
_ID_RE = re.compile(r"\*\*ID\*\*\s*\|\s*FMS\d{2}-(M\d{2})", re.IGNORECASE)
# That module's Prérequis marker, up to the next field delimiter (either
# layout's) or end of line — free prose allowed inside.
_PREREQ_RE = re.compile(r"Pr[eé]requis\*\*?\s*[:|]\s*([^|·\n]+)", re.IGNORECASE)
_MODULE_TOKEN_RE = re.compile(r"\bM\d{2}\b")


def extract_module_prerequisites(body_markdown: str) -> Dict[str, List[str]]:
    """Returns {module_number: [prereq module_numbers]}, e.g.
    {"M02": ["M01"], "M11": ["M07", "M08", "M09", "M10"], "M01": []}.
    Only `M\\d\\d` IDs are considered — the `A0n` certification row is
    intentionally skipped (see module docstring)."""
    result: Dict[str, List[str]] = {}
    # Walk block-by-block: each module's section runs from one ID marker
    # to the next, so pairing the nearest ID with the nearest following
    # Prérequis marker is reliable without a full table parser.
    id_matches = list(_ID_RE.finditer(body_markdown))
    for i, id_match in enumerate(id_matches):
        module_id = id_match.group(1).upper()
        section_end = (
            id_matches[i + 1].start() if i + 1 < len(id_matches) else len(body_markdown)
        )
        section = body_markdown[id_match.end() : section_end]
        prereq_match = _PREREQ_RE.search(section)
        if not prereq_match:
            continue
        cell = prereq_match.group(1)
        if re.search(r"\baucun\b", cell, re.IGNORECASE):
            result[module_id] = []
            continue
        tokens = [
            t.upper() for t in _MODULE_TOKEN_RE.findall(cell) if t.upper() != module_id
        ]
        result[module_id] = sorted(set(tokens))
    return result
