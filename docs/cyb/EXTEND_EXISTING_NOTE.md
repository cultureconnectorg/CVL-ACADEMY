# CyberSecure — Cross-Domain Security Rows (`EXTEND_EXISTING`, pointer only)

Per the reconciliation's own G8 resolution: per-product security rows
already flagged in other domains resolve as `EXTEND_EXISTING`, pointing
at `CYB-31→42` (specifically `CYB-32`, the one buildable row) — never
re-teaching security fundamentals per product. One security curriculum,
referenced everywhere it is needed, never duplicated per domain (same
reuse discipline as `AF-22` → `AUTHORIZATION_MODEL.md`).

| Row | Domain | Resolution |
|---|---|---|
| `FRK-48/49/50/51/70` | FREK | Point to `CYB-31→42` (`CYB-32` buildable now); until the rest of `CYB-31→42` is unblocked, these stay `BLOCKED` alongside it — not separately re-litigated. See `docs/frk/README.md`. |
| `KLT-17` | Kiltikonet | Same resolution. |
| `WAL-14` | Wallet | Same resolution. See `docs/wal/README.md`'s own CyberSecure boundary note (`G8`, resolved). |

**No new content here** — this note exists only so a reader of any of
these three domains' own docs can trace the security boundary back to
its single source (`docs/cyb/`) rather than finding three independent,
possibly-drifting descriptions of the same fact.
