"""ACA-0006 — structured extraction from a real Master Module Map body.

Deliberately a **separate** module from `fms_import/module_map.py`
rather than an extension of it: that file is already tested and scoped
narrowly to what `fms_import`'s dependency-graph step needs (module ID +
`Prérequis`, nothing else). This package needs richer fields (title,
bloc, niveau, N1/N2/N3 references) for a learner-facing read model, so it
extracts them itself rather than widening an already-shipped file's
responsibility.

**Two real layouts, confirmed by reading all 6 métiers' own Master
Module Maps this session** (same two layouts `fms_import/module_map.py`'s
own docstring already documents for ID/Prérequis, extended here to the
extra fields actually present):

- FMS-01/FMS-02 ("rich" layout): one field per table row —
  `| **Titre** | ... |`, `| **Bloc de compétence** | ... |`,
  `| **Niveau de progression** | ... |`, plus `| **N1 associé** | ... |`
  / `| **N2 associé** | ... |` / `| **Préparation N3** | ... |` — these
  three assessment-reference fields exist **only** in this layout.
- FMS-03..FMS-06 ("compact" layout): one packed row —
  `| **ID** | FMS03-M02 · **Bloc** : ... · **Niveau** : ... · **Prérequis**
  : ... |` (field labels shortened — "Bloc" not "Bloc de compétence",
  "Niveau" not "Niveau de progression") — and it **has no N1/N2/N3
  fields at all**, using `Hook`/`Compétence visée`/`Exercice`/`Livrable`
  instead. This is a real, structural absence in the source, not a
  parsing gap — reflected here as `None`, never fabricated.

Module titles are extracted uniformly across both layouts from each
section's own `## M<NN> — <title>` heading, which both layouts share
identically — more robust than either layout's own "Titre" field
(compact layout doesn't reliably have one).

Tolerant by the same construction as `fms_import/module_map.py`: a field
missing from a given module's row is simply absent from that module's
result — never a crash, never a fabricated value.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from .models import PrerequisiteStatus

_HEADING_RE = re.compile(r"^##\s*M(\d{2})\s*[—\-–]\s*(.+?)\s*$", re.MULTILINE)
_ID_RE = re.compile(r"\*\*ID\*\*\s*\|\s*FMS\d{2}-(M\d{2})", re.IGNORECASE)
_BLOC_RE = re.compile(
    r"Bloc(?: de comp[ée]tence)?\*\*?\s*[:|]\s*([^|·\n]+)", re.IGNORECASE
)
_NIVEAU_RE = re.compile(
    r"Niveau(?: de progression)?\*\*?\s*[:|]\s*([^|·\n]+)", re.IGNORECASE
)
_N1_RE = re.compile(r"N1 associ[ée]\*\*?\s*[:|]\s*([^|·\n]+)", re.IGNORECASE)
_N2_RE = re.compile(r"N2 associ[ée]\*\*?\s*[:|]\s*([^|·\n]+)", re.IGNORECASE)
_N3_RE = re.compile(r"Pr[ée]paration N3\*\*?\s*[:|]\s*([^|·\n]+)", re.IGNORECASE)
_PREREQ_RE = re.compile(r"Pr[eé]requis\*\*?\s*[:|]\s*([^|·\n]+)", re.IGNORECASE)
_MODULE_TOKEN_RE = re.compile(r"\bM\d{2}\b")


def _clean(raw: Optional[str]) -> Optional[str]:
    if raw is None:
        return None
    raw = raw.strip()
    return raw or None


@dataclass
class ModuleMapEntry:
    module_number: str  # "M01"
    title: Optional[str] = None
    bloc: Optional[str] = None
    niveau: Optional[str] = None
    n1_reference: Optional[str] = None
    n2_reference: Optional[str] = None
    n3_reference: Optional[str] = None
    prerequisite_status: PrerequisiteStatus = "UNSPECIFIED"
    prerequisite_modules: List[str] = field(default_factory=list)


def extract_module_map_entries(body_markdown: str) -> Dict[str, ModuleMapEntry]:
    """One entry per `M<NN>` module section found in a real Master Module
    Map body. Certification sections (`A0<n>`) never match — the heading
    regex only matches `M<NN>`, never `A<NN>`."""
    entries: Dict[str, ModuleMapEntry] = {}

    # Titles: uniform across both layouts, read directly off each
    # section's own heading.
    for m in _HEADING_RE.finditer(body_markdown):
        module_number = f"M{m.group(1)}"
        entries[module_number] = ModuleMapEntry(
            module_number=module_number, title=_clean(m.group(2))
        )

    # Everything else: block-split from one **ID** marker to the next
    # (same technique as fms_import/module_map.py's own extractor).
    id_matches = list(_ID_RE.finditer(body_markdown))
    for i, id_match in enumerate(id_matches):
        module_number = id_match.group(1).upper()
        section_end = (
            id_matches[i + 1].start() if i + 1 < len(id_matches) else len(body_markdown)
        )
        section = body_markdown[id_match.end() : section_end]

        entry = entries.setdefault(
            module_number, ModuleMapEntry(module_number=module_number)
        )

        bloc_m = _BLOC_RE.search(section)
        entry.bloc = _clean(bloc_m.group(1)) if bloc_m else None
        niveau_m = _NIVEAU_RE.search(section)
        entry.niveau = _clean(niveau_m.group(1)) if niveau_m else None
        n1_m = _N1_RE.search(section)
        entry.n1_reference = _clean(n1_m.group(1)) if n1_m else None
        n2_m = _N2_RE.search(section)
        entry.n2_reference = _clean(n2_m.group(1)) if n2_m else None
        n3_m = _N3_RE.search(section)
        entry.n3_reference = _clean(n3_m.group(1)) if n3_m else None

        prereq_m = _PREREQ_RE.search(section)
        if prereq_m:
            cell = prereq_m.group(1)
            if re.search(r"\baucun\b", cell, re.IGNORECASE):
                entry.prerequisite_status = "NONE"
                entry.prerequisite_modules = []
            else:
                tokens = sorted(
                    {
                        t.upper()
                        for t in _MODULE_TOKEN_RE.findall(cell)
                        if t.upper() != module_number
                    }
                )
                if tokens:
                    entry.prerequisite_status = "DEFINED"
                    entry.prerequisite_modules = tokens
                # a Prérequis field present but naming no module and not
                # "Aucun" stays UNSPECIFIED — never guessed.
        # else: no Prérequis marker at all for this module -> stays
        # UNSPECIFIED (the real, documented FMS-04/05/06 gap).

    return entries
