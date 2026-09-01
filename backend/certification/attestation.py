"""Attestation generation (PDF) + FREK-ready proof hashing.

"FREK-ready" (rule 11) here means: every graded attempt carries a SHA-256
hash over its scores + grader identity + timestamp, and the rendered PDF
embeds that same hash — so a printed/downloaded attestation can be
verified against the DB record without trusting the PDF file itself.
Once FrekCore is live, `services/frek_core.issue_proof` is the next link
in that chain (see certification/service.py) — this module doesn't call
FrekCore directly, it only produces what that call will carry.
"""

from __future__ import annotations

import hashlib
import json
from io import BytesIO
from typing import Any, Dict

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

from .models import CertificationAttempt, JurySignature


def compute_jury_signature(
    attempt_id: str, jury_id: str, scores: Dict[str, float], signed_at: str
) -> str:
    canonical = json.dumps(
        {
            "attempt_id": attempt_id,
            "jury_id": jury_id,
            "scores": scores,
            "signed_at": signed_at,
        },
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(canonical.encode()).hexdigest()


def make_jury_signature(
    attempt_id: str, jury_id: str, scores: Dict[str, float], signed_at: str
) -> JurySignature:
    return JurySignature(
        jury_id=jury_id,
        signed_at=signed_at,
        sha256=compute_jury_signature(attempt_id, jury_id, scores, signed_at),
    )


def generate_attestation_pdf(
    attempt: CertificationAttempt,
    user_display_name: str,
    user_frek_id: str,
    formation_name: str,
) -> bytes:
    if not attempt.passed or not attempt.jury_signature:
        raise ValueError("Attestation only generated for a passed, jury-signed attempt")

    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(
        width / 2, height - 40 * mm, "CVLN Academy — Attestation de Certification"
    )

    c.setFont("Helvetica", 12)
    y = height - 60 * mm
    lines = [
        f"Certification : {attempt.certification_code} ({attempt.level})",
        f"Formation : {formation_name}",
        f"Titulaire : {user_display_name} ({user_frek_id})",
        f"Score global : {attempt.score_global}%",
        f"Statut : {'RÉUSSI' if attempt.passed else 'NON RÉUSSI'}",
    ]
    if attempt.mention:
        lines.append(f"Mention : {attempt.mention}")
    lines += [
        f"Version du référentiel : {attempt.rubric_version}",
        f"Délivré le : {attempt.graded_at}",
    ]
    for line in lines:
        c.drawString(30 * mm, y, line)
        y -= 8 * mm

    y -= 6 * mm
    c.setFont("Helvetica-Bold", 12)
    c.drawString(30 * mm, y, "Scores par bloc")
    y -= 7 * mm
    c.setFont("Helvetica", 11)
    for bloc, pct in sorted(attempt.score_by_bloc.items()):
        c.drawString(35 * mm, y, f"{bloc} : {pct}%")
        y -= 6 * mm

    y -= 10 * mm
    c.setFont("Helvetica-Oblique", 9)
    c.drawString(
        30 * mm, y, f"Signature jury (FREK-ready) : {attempt.jury_signature.sha256}"
    )
    y -= 5 * mm
    c.drawString(30 * mm, y, f"Signé par le jury le {attempt.jury_signature.signed_at}")

    c.showPage()
    c.save()
    return buf.getvalue()


def attestation_export_metadata(attempt: CertificationAttempt) -> Dict[str, Any]:
    """What a FrekCore `issue_proof(kind="certification")` call will carry
    once that integration is live — see services/frek_core.py."""
    return {
        "attempt_id": attempt.id,
        "certification_code": attempt.certification_code,
        "score_global": attempt.score_global,
        "mention": attempt.mention,
        "jury_signature_sha256": (
            attempt.jury_signature.sha256 if attempt.jury_signature else None
        ),
        "rubric_version": attempt.rubric_version,
    }
