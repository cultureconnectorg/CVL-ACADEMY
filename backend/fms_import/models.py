"""FMS resource schema — the shape every parsed Markdown file becomes.

**Reconciled against the real FMS ZIP** (`FMS_Chantier_Complet_20260822.zip`,
225 files, all 6 métiers, received after the initial build — see
docs/AUDIT_REPORT.md §8 and docs/DEVELOPER_GUIDE.md §3 for the story).

The convention documented before that ZIP arrived (YAML frontmatter) turned
out not to match reality: every real file is plain Markdown prose with
Markdown tables for structured fields — **no frontmatter block anywhere**.
What the real ZIP does have, consistently across all 6 métiers, is a
locked numbered-filename convention (see `00_GABARIT_Construction_Metier.md`
in the source archive — Academy's authors call it exactly that: a
"gabarit", a locked skeleton extracted from FMS-01 and applied identically
to FMS-02..FMS-06):

    NN_FMS0<métier>_<TypeMarker>[...].md      — e.g. 13_FMS01_M01_Blueprint.md
    NN_FMS-<Lettre>_Referentiel_<Nom>.md      — e.g. 01_FMS-A_Referentiel_Artist_Development.md
    00_INDEX.md / 00_GABARIT_Construction_Metier.md — cross-métier, no formation

The parser (parser.py) now classifies every file from its filename alone
(FILENAME_TYPE_HINTS below), the same way a human skimming the archive
would — frontmatter parsing is kept only as an optional, no-op-if-absent
affordance for any future file that happens to carry one.

Naming normalization applied on import (all directly sourced from the
gabarit's own "Convention de nommage" table — not invented):
  - métier référentiel letter -> formation:  FMS-A -> FMS-01, ... FMS-F -> FMS-06
  - formation code:   FMS01 (as it appears in filenames) -> FMS-01 (dashed —
    matches both the gabarit's own documented convention and this
    platform's existing `db.formations` codes)
  - module code:      FMS01_M07 -> FMS-01-M07 (dashed, gabarit table)
  - Skill ID:          left exactly as its own registry states it —
    FMS01-A1 (no dash after the métier number) — see
    `27_FMS01_Skill_IDs_Registry.md`: "FMS01-A1 est l'identifiant canonique"
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field

FmsResourceType = Literal[
    # Cross-métier, no formation_code
    "index",
    "gabarit",
    "matrice_pedagogique",
    # Métier foundation (one per métier, before any module content)
    "referentiel",
    "learning_map",
    "module_map",
    "cas_fil_rouge",
    "competency_matrix",
    "matrice_tracabilite",
    "infrastructure",
    "evidence_registry",
    "skill_ids_registry",
    "rubric_master",
    # Module content
    "blueprint",
    "module",
    # Certification (A0x)
    "cas_inedit",
    "sujet_officiel",
    "grille_certificative",
    "guide_jury",
    # Industrialisation
    "banque_n1",
    "banque_n2",
    "templates_etudiants",
    "guide_formateur",
    "guide_correcteur",
    "guide_candidat",
    "note_harmonisation",
    # Fallback for a genuine guide that doesn't match a more specific hint
    "guide",
]

RESOURCE_TYPE_LABELS: Dict[str, str] = {
    "index": "Index d'archive",
    "gabarit": "Gabarit de construction",
    "matrice_pedagogique": "Matrice pédagogique",
    "referentiel": "Référentiel métier",
    "learning_map": "Master Learning Map",
    "module_map": "Master Module Map",
    "cas_fil_rouge": "Cas fil rouge",
    "competency_matrix": "Case Competency Matrix",
    "matrice_tracabilite": "Matrice de traçabilité",
    "infrastructure": "Infrastructure (evidence/skills/rubric)",
    "evidence_registry": "Evidence Registry",
    "skill_ids_registry": "Skill IDs Registry",
    "rubric_master": "Rubric Master",
    "blueprint": "Blueprint pédagogique",
    "module": "Module — contenu complet",
    "cas_inedit": "Cas inédit (certification)",
    "sujet_officiel": "Sujet officiel (certification)",
    "grille_certificative": "Grille certificative",
    "guide_jury": "Guide jury / protocole",
    "banque_n1": "Banque N1 consolidée",
    "banque_n2": "Banque N2 consolidée",
    "templates_etudiants": "Templates étudiants",
    "guide_formateur": "Guide formateur",
    "guide_correcteur": "Guide correcteur",
    "guide_candidat": "Guide candidat",
    "note_harmonisation": "Note d'harmonisation des grilles",
    "guide": "Guide",
}

# Métier référentiel letter -> formation code — the gabarit's own mapping
# table (§2 "Convention de nommage"): "Métier (référentiel) FMS-[Lettre]" /
# "Métier (produit/formation) FMS-0[n]", A<->01 in order through F<->06.
METIER_LETTER_TO_FORMATION: Dict[str, str] = {
    "A": "FMS-01",
    "B": "FMS-02",
    "C": "FMS-03",
    "D": "FMS-04",
    "E": "FMS-05",
    "F": "FMS-06",
}

# Filename fragments used to classify a real FMS resource file — matched
# in this order (most specific first) against the filename lowercased with
# every run of non-alphanumeric characters collapsed to a single "_", so
# "13_FMS01_M01_Blueprint.md" and "13-fms01-m01-blueprint.md" match
# identically. A frontmatter `type:` (if present) still wins over this —
# see parser.py — but no real file in the reconciled ZIP carries one.
FILENAME_TYPE_HINTS: List[tuple] = [
    ("index", "index"),
    ("gabarit", "gabarit"),
    ("matrice_pedagogique", "matrice_pedagogique"),
    ("referentiel", "referentiel"),
    ("master_learning_map", "learning_map"),
    ("master_module_map", "module_map"),
    ("cas_fil_rouge", "cas_fil_rouge"),
    ("case_competency_matrix", "competency_matrix"),
    ("matrice_tracabilite", "matrice_tracabilite"),
    ("evidence_registry", "evidence_registry"),
    ("skill_ids_registry", "skill_ids_registry"),
    ("rubric_master", "rubric_master"),
    ("infrastructure", "infrastructure"),
    ("cas_inedit", "cas_inedit"),
    ("sujet_officiel", "sujet_officiel"),
    ("grille_certificative", "grille_certificative"),
    ("guide_jury", "guide_jury"),
    ("banque_n1", "banque_n1"),
    ("banque_n2", "banque_n2"),
    ("templates_etudiants", "templates_etudiants"),
    ("guide_formateur", "guide_formateur"),
    ("guide_correcteur", "guide_correcteur"),
    ("guide_candidat", "guide_candidat"),
    ("note_harmonisation", "note_harmonisation"),
    ("blueprint", "blueprint"),
    ("contenu_complet", "module"),
    ("_complet", "module"),
    ("guide", "guide"),
]


def _uid() -> str:
    return str(uuid.uuid4())


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


class ImportIssue(BaseModel):
    level: Literal["error", "warning"]
    file: str
    message: str


class FmsResource(BaseModel):
    """One parsed FMS artifact, ready to persist to db.fms_resources."""

    id: str = Field(default_factory=_uid)
    import_id: str
    source_file: str
    type: FmsResourceType
    code: str
    formation_code: Optional[str] = None
    title: str
    prerequisites: List[str] = Field(default_factory=list)
    skill_ids: List[str] = Field(default_factory=list)
    version: str = "1.0"
    frontmatter: Dict[str, Any] = Field(default_factory=dict)
    body_markdown: str = ""
    imported_at: str = Field(default_factory=_now)


class ImportReport(BaseModel):
    id: str = Field(default_factory=_uid)
    filename: str
    status: Literal["success", "partial", "failed"]
    resources_created: int = 0
    resources_by_type: Dict[str, int] = Field(default_factory=dict)
    issues: List[ImportIssue] = Field(default_factory=list)
    created_by: Optional[str] = None
    created_at: str = Field(default_factory=_now)
