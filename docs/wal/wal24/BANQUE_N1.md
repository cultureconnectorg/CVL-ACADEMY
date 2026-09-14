# WAL-24 — Banque N1 (formative, M1→M3)

```
Sourced directly against backend/wallet/passes.py and
backend/api/wallet.py (both re-read in full this session).
```

## M1 — payload structure literacy

1. Name the two real payload-building functions in `passes.py`.
   (`build_apple_pass_payload()`, `build_google_pass_payload()`)
2. What real wallet fields appear in the Apple payload's
   `secondaryFields`? (`name` — display name, `jcc` — the account's
   `jcc_balance`)
3. What barcode format does the Apple payload use? (`PKBarcodeFormatQR`,
   encoding the user's `frek_id`)

## M2 — real HTTP behavior correction

4. What does `passes.py`'s own module docstring claim about signing?
   ("signing is explicitly left as a 501")
5. Does any route in `backend/wallet/`/`backend/api/wallet.py` actually
   raise `HTTPException(status_code=501)`? (No — confirmed by direct
   `grep`, none exists)
6. What does `GET /wallet/pass/apple` actually return? (A normal
   HTTP 200 with a JSON body: `{"status": "unsigned", "note": "...",
   "payload": {...}}`)
7. Is the underlying intent of the docstring ("never claim a signed,
   installable pass exists") honored despite the wrong "501" wording?
   (Yes — the real 200-plus-status-field behavior achieves the same
   honest outcome, just not via an HTTP 501)

## M3 — signing-gap literacy

8. What specifically is missing for a real installable Apple pass?
   (An Apple Developer WWDR certificate + a real Pass Type ID — the
   payload uses a placeholder `"pass.io.cvln.academy"`)
9. What specifically is missing for a real Google Wallet save link?
   (A Google Wallet Issuer account to sign the JWT the payload would
   normally be wrapped in)
