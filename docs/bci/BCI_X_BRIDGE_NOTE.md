# BCI-X-01→11 — Blockchain Cross-Ecosystem Bridges

Per the reconciliation: coverage `NONE`/`PARTIAL`, action
`NEW_CROSS_ECOSYSTEM`, mostly `BLOCKED_PRODUCT_DEPENDENCY` — with a
subset that can at least cite each real side even while the bridge
itself stays conceptual.

| Row | Bridge | Resolution |
|---|---|---|
| BCI-X-01 | × Kiltikonet | `BLOCKED_PRODUCT_DEPENDENCY` — Kiltikonet side inherits its own domain's block status where applicable. |
| BCI-X-02 | × CVE | **Unblocked** since `FD-CVE-001` (CVE now `FORMALIZED_METHODOLOGY`) — cites `docs/cve/` for the methodology side, never fabricates a wired blockchain↔CVE pipeline. |
| BCI-X-03 | × FREK | `BLOCKED_PRODUCT_DEPENDENCY` — inherits FREK's own block status for this bridge. |
| BCI-X-04 | × Wallet | `PARTIAL` — cites the real Wallet ledger (`docs/wal/`) and the real `djsayd/CVLN-Wallet` product grounding, bridge itself stays conceptual (no wired blockchain↔Wallet integration exists). |
| BCI-X-05 | × GMD | `BLOCKED_PRODUCT_DEPENDENCY`. |
| BCI-X-06 | × LabelOS | `PARTIAL` — cites `docs/los/` and the real `labelos_bridge.py` interface contract observed in `Laurent.ia`, bridge itself stays conceptual. |
| BCI-X-07 | × KORA | `PARTIAL` — cites `docs/kor/kor10/` (Wallet/JCC, the one confirmed KORA capability), bridge itself stays conceptual. |
| BCI-X-08 | × Gala Cook & Food | `BLOCKED_PRODUCT_DEPENDENCY`. |
| BCI-X-09 | × Academy (evidence/credentials) | `PARTIAL` — cites `AUTHORIZATION_MODEL.md`'s skill-registry doctrine, bridge itself stays conceptual (no credential is anchored on-chain in this repo). |
| BCI-X-10 | × Agent Factory | `BLOCKED_PRODUCT_DEPENDENCY` — inherits Agent Factory's own near-total block status for this bridge. |
| BCI-X-11 | × Intelligence OS | `BLOCKED_PRODUCT_DEPENDENCY` — same inheritance as BCI-X-10. |

**No new formation built for any of these 11 rows** — 4 (BCI-X-02/04/
06/07/09 — five, corrected count below) get a citation-only bridge
note; the rest are declared `BLOCKED_PRODUCT_DEPENDENCY` and folded
into `docs/bci/BLOCKED_CANDIDATES.md`'s count. Never claims a wired
blockchain integration with any of these systems — every bridge here
stays conceptual pending real infrastructure on the blockchain side
itself (which does not exist beyond `BCH-01`'s pedagogical testnet).

**Correction:** 5 rows carry a citation (BCI-X-02, 04, 06, 07, 09); 6
rows are pure `BLOCKED_PRODUCT_DEPENDENCY` (BCI-X-01, 03, 05, 08, 10,
11). 5 + 6 = 11.
