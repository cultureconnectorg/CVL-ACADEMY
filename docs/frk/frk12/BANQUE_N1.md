# FRK-12 — Banque N1 (formative, M1→M3)

## M1 — evidence-artifact design principles

1. Cite the 2 real disciplines of evidence engineering covered here.
   (Evidence-artifact design, validation & verification methodology)
2. What makes an artifact "verifiable" rather than merely asserted?
   (A third party can check it without trusting the issuer's word
   alone — structure, provenance, tamper-evidence)
3. What is the difference between a claim and a proof? (A claim is an
   assertion; a proof is an artifact structured so the claim can be
   independently checked)

## M2 — validation & verification methodology

4. What is the difference between validating an artifact's structure
   and verifying it supports its claim? (Structural validation checks
   the artifact is well-formed; verification checks it actually
   supports the specific claim attached to it — an artifact can be
   perfectly well-formed and still not prove the claim)
5. Name one common evidence-engineering failure mode. (Self-referential
   proof — an artifact that only "proves" itself using its own
   assertions, with no independent check possible)
6. Why is an unfalsifiable claim a problem for evidence engineering?
   (If no possible check could disprove it, it cannot be verified
   either — verifiability requires the claim be checkable both ways)

## M3 — boundary discipline vs. FRK-13

7. What is the frontier with FRK-13? (FRK-12 = the general discipline
   of evidence engineering; FRK-13 = the narrow, specific question of
   CVLN's own "FREK Proof Engine," including its real stub state)
8. Does a real CVLN system implement full evidence engineering today?
   (No — `CAPABILITY_NOT_IMPLEMENTED`; this formation teaches the
   discipline, it never claims CVLN already runs it)
9. FRK-12 is a prerequisite (with FRK-14) of which formation? (FRK-15)
10. If a candidate's answer implies CVLN's `issue_proof()` stub is a
    working evidence-engineering implementation, what is the correct
    grading response? (Automatic 0 — this is exactly the FRK-12/FRK-13
    confusion the eliminatory rule exists to catch)
