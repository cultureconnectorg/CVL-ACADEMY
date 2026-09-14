# GMD-31 — Banque N1 (formative, M1→M3)

```
Sourced directly against frek_service.py (full file, 127 lines) and
server.py:765-768 (GET /admin/outbox/frek-id).
```

## M1 — outbox payload literacy

1. Name every top-level key in the real emit payload.
   (`source`, `interaction_type`, `identifier`, `event`, `ticket_type`,
   `timestamp`)
2. What is the fixed, literal value of `source`? (`"good-mood-os"` —
   never varies)
3. What are the only two real values `interaction_type` can take, per
   this codebase's own callers? (`"purchase"`, `"entry_scan"` — seen at
   the GMD-24 checkout-issuance call site and GMD-25's `scan_check`
   respectively)
4. What does `identifier` contain? (`email`, `external_id` — the same
   `external_id` convention as the fan record, `gm-fan-{local-part}`)

## M2 — retry-schedule literacy

5. Name the exact 5 backoff delays, in order, and their real-world
   meaning. (`30s, 2m, 10m, 1h, 6h` — `RETRY_BACKOFFS_SEC = [30, 120,
   600, 3600, 21600]`)
6. What real status values can an outbox entry hold? (`"delivered"`,
   `"pending"`, `"failed"`)
7. After how many total attempts is an entry marked `"failed"`, and
   what does that require? (`attempts > len(RETRY_BACKOFFS_SEC)` — i.e.
   the 6th attempt is the one that finally gives up; `attempts` starts
   at 1 on the initial synchronous try)
8. How many pending entries does one `retry_loop` iteration process at
   most, and how often does it run? (`limit(20)` per iteration,
   `asyncio.sleep(30)` between iterations)
9. What real timeout does the initial synchronous POST use?
   (`httpx.AsyncClient(timeout=3.0)` — 3 seconds)

## M3 — boundary discipline (eliminatory)

10. Is `frek_service.py`'s `FREK_ID_URL` the same system as this
    Academy's own `backend/services/frek_core.py`? (**No** — two
    entirely separate systems that happen to follow the same
    architectural pattern: env-gated outbox with local fallback.
    Good Mood's FREK-ID client talks to Good Mood's own configured
    `FREK_ID_URL`; this Academy's `frek_core.py` is a different
    client, in a different repo, pointed at a different (also
    unconfigured-by-default) endpoint. Conflating the two is exactly
    the `CROSS_DOMAIN_CONTAMINATION` failure mode this whole Master
    Package exists to prevent — a candidate who merges them fails this
    formation regardless of any other score.)
