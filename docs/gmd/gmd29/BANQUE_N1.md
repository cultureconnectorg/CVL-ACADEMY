# GMD-29 — Banque N1 (formative, M1→M3)

```
Sourced against server.py lines 241-252 (POST /newsletter, GET
/admin/newsletter, GET /admin/newsletter/export) and
email_service.py lines 64-82 (send_newsletter_welcome).
```

## M1 — send/export walkthrough

1. Exact route a fan uses to subscribe. (`POST /newsletter`)
2. What happens if the email is already subscribed? (`{"ok": true,
   "already": true}` — no duplicate document created, no error raised)
3. Exact route to export the subscriber list, and in what format?
   (`GET /admin/newsletter/export` — CSV, columns `email, lang,
   subscribed_at`)
4. What real cap does the export apply, per the code? (`to_list(50000)`
   — five times the admin list route's own `to_list(5000)` cap)

## M2 — bilingual copy literacy

5. Name the exact four `lang` keys that actually exist in
   `send_newsletter_welcome`'s `copy` dict. (`fr`, `en`, `es`, `kr`)
6. What happens if `send_newsletter_welcome` is called with a `lang`
   not in that dict (e.g. `"de"`)? (`copy.get(lang, copy["fr"])` —
   silently falls back to French, never raises an error)
7. **Real repo-truth finding, verify this yourself, don't take it on
   faith:** what language does the `"kr"` key's copy actually contain?
   (Haitian Creole — "Byenveni nan Good Mood," "Ou nan boukl la" — NOT
   Korean, despite the key name. A candidate must notice and report
   this mislabeling rather than assume `"kr"` means Korean; never
   silently "correct" it in a way that isn't reflected in the real
   code, and never claim Korean is supported)

## M3 — campaign-to-fan-base linkage

8. Which formation's `upsert_fan` logic determines who ends up in
   `db.newsletter`/`db.fans` in the first place? (GMD-26 — a purchase
   triggers fan upsert; newsletter subscription itself is a separate,
   direct `POST /newsletter` call, not derived from a purchase)
9. Are `db.newsletter` subscribers and `db.fans` records the same
   collection? (No — two distinct collections; a person can be in one,
   both, or neither. Never assume every fan is a newsletter subscriber
   or vice versa.)
