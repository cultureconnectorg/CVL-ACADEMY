"""Canonical Economy 3D line registry.

Generated from CVLN_Academy_Master_Economie_3D_DECIDE_V1.xlsx / Mapping_812
on 2026-09-11. This file is a traceability manifest, not a replacement for
the workbook and not evidence of runtime implementation.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

SOURCE_WORKBOOK = "CVLN_Academy_Master_Economie_3D_DECIDE_V1.xlsx"
SOURCE_SHEET = "Mapping_812"
SOURCE_SHA256 = "be41260e722ac3daa1974ef52fb0f48f8c31536a8be420469b139755bb9c6bc0"
EXPECTED_LINE_COUNT = 812


def _codes(prefix: str, start: int, end: int) -> list[str]:
    return [f"{prefix}-{i:02d}" for i in range(start, end + 1)]


CANONICAL_CODES: tuple[str, ...] = tuple(
    _codes("KLT", 9, 20)
    + _codes("FMS", 7, 18)
    + _codes("FRK", 1, 75)
    + _codes("LOS", 1, 14)
    + _codes("AF", 1, 15)
    + _codes("WAL", 1, 18)
    + _codes("GCF", 1, 18)
    + _codes("GMD", 1, 20)
    + _codes("CYB", 1, 30)
    + _codes("BCI", 1, 30)
    + _codes("GRP", 1, 58)
    + _codes("SAY", 1, 50)
    + ["SAY-LAB"]
    + _codes("KOR-OP", 1, 12)
    + _codes("LOS-OP", 1, 15)
    + _codes("AF", 16, 25)
    + _codes("LAU", 1, 10)
    + _codes("WAL", 19, 28)
    + _codes("GCF", 19, 30)
    + _codes("GMD", 21, 34)
    + _codes("CYB", 31, 42)
    + _codes("BCI", 31, 40)
    + _codes("GRP", 59, 72)
    + _codes("CVE", 1, 15)
    + _codes("TOK", 1, 15)
    + _codes("CEO", 1, 12)
    + _codes("IOS", 1, 25)
    + _codes("BRN", 1, 15)
    + _codes("CMD", 1, 15)
    + _codes("SYS", 1, 10)
    + _codes("FDC", 1, 48)
    + _codes("MEM", 1, 10)
    + _codes("TRN", 1, 7)
    + _codes("HOS", 1, 30)
    + ["HOS-GAP"]
    + _codes("KOR-X", 1, 7)
    + _codes("LOS-X", 1, 8)
    + _codes("AF-X", 1, 9)
    + _codes("WAL-X", 1, 9)
    + _codes("GCF-X", 1, 8)
    + _codes("GMD-X", 1, 9)
    + _codes("BCI-X", 1, 11)
    + _codes("FDC-X", 1, 9)
    + _codes("XCV", 1, 67)
)

NATURE_RUNS: tuple[tuple[int, int, str], ...] = (
    (1, 12, "Interne"),
    (13, 23, "Marché"),
    (24, 24, "Cross-ecosystem"),
    (25, 26, "Marché"),
    (27, 27, "Interne"),
    (28, 29, "Marché"),
    (30, 30, "Interne"),
    (31, 39, "Marché"),
    (40, 40, "Interne"),
    (41, 62, "Marché"),
    (63, 63, "Interne"),
    (64, 79, "Marché"),
    (80, 84, "Cross-ecosystem"),
    (85, 87, "Marché"),
    (88, 88, "Interne"),
    (89, 91, "Marché"),
    (92, 92, "Interne"),
    (93, 352, "Marché"),
    (353, 353, "Bridge"),
    (354, 487, "Interne"),
    (488, 514, "Marché"),
    (515, 554, "Interne restreint"),
    (555, 569, "Interne privilégié"),
    (570, 579, "Cross-ecosystem"),
    (580, 614, "Marché"),
    (615, 627, "Interne restreint"),
    (628, 674, "Marché"),
    (675, 675, "Hold"),
    (676, 812, "Cross-ecosystem"),
)

EXPECTED_NATURE_COUNTS = {
    "Marché": 437,
    "Cross-ecosystem": 153,
    "Interne": 152,
    "Interne restreint": 53,
    "Interne privilégié": 15,
    "Bridge": 1,
    "Hold": 1,
}

TraceStatus = Literal[
    "UNVERIFIED",
    "VERIFIED_RUNTIME",
    "VERIFIED_NON_RUNTIME",
    "BLOCKED",
    "FAILED",
]


@dataclass(frozen=True)
class EconomyTraceLine:
    line_id: str
    source_row: int
    code: str
    nature: str
    status: TraceStatus = "UNVERIFIED"
    implementation_evidence: tuple[str, ...] = ()
    runtime_evidence: tuple[str, ...] = ()
    test_evidence: tuple[str, ...] = ()
    justification: str | None = None


def nature_for_line(line_number: int) -> str:
    if not 1 <= line_number <= EXPECTED_LINE_COUNT:
        raise ValueError(f"Economy line out of range: {line_number}")
    for start, end, nature in NATURE_RUNS:
        if start <= line_number <= end:
            return nature
    raise AssertionError(f"No canonical nature registered for line {line_number}")


def line_id(line_number: int) -> str:
    if not 1 <= line_number <= EXPECTED_LINE_COUNT:
        raise ValueError(f"Economy line out of range: {line_number}")
    return f"ACA-ECO-{line_number:04d}"


TRACEABILITY: tuple[EconomyTraceLine, ...] = tuple(
    EconomyTraceLine(
        line_id=line_id(i),
        source_row=i + 1,
        code=code,
        nature=nature_for_line(i),
    )
    for i, code in enumerate(CANONICAL_CODES, start=1)
)


def validate_verified_line(line: EconomyTraceLine) -> None:
    """Fail closed: a verified claim must carry the required evidence."""
    if line.status == "VERIFIED_RUNTIME":
        missing = [
            name
            for name, evidence in (
                ("implementation", line.implementation_evidence),
                ("runtime", line.runtime_evidence),
                ("tests", line.test_evidence),
            )
            if not evidence
        ]
        if missing:
            raise ValueError(
                f"{line.line_id} cannot be VERIFIED_RUNTIME; missing "
                f"{', '.join(missing)} evidence"
            )
    elif line.status == "VERIFIED_NON_RUNTIME":
        if not line.justification or not line.test_evidence:
            raise ValueError(
                f"{line.line_id} cannot be VERIFIED_NON_RUNTIME without "
                "justification and tests"
            )


def completion_counts() -> dict[str, int]:
    result = {
        "UNVERIFIED": 0,
        "VERIFIED_RUNTIME": 0,
        "VERIFIED_NON_RUNTIME": 0,
        "BLOCKED": 0,
        "FAILED": 0,
    }
    for line in TRACEABILITY:
        result[line.status] += 1
    return result
