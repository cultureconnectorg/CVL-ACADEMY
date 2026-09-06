# GMD-33 — Banque N1 (formative, M1→M3)

```
Sourced against server.py lines 36-70 (auth utils, get_current_admin)
and 261-278 (auth routes).
```

## M1 — auth lifecycle literacy

1. Exact route to log in, and what two things does it set on success?
   (`POST /auth/login` — returns a JWT `token` in the body, AND sets an
   httpOnly cookie `access_token`, `secure=True`, `samesite="none"`,
   `max_age=60*60*12` — a candidate must name both, not just the body
   token)
2. How long is a token valid, exactly? (12 hours — `exp: now +
   timedelta(hours=12)`)
3. From which two possible sources can `get_current_admin` read the
   token? (`Authorization: Bearer <token>` header, OR the
   `access_token` cookie — checked in that order)
4. What real password hashing scheme is used? (`bcrypt` —
   `bcrypt.hashpw`/`bcrypt.checkpw`, not a home-rolled scheme)
5. Exact route to verify a session and exact route to log out.
   (`GET /auth/me`, `POST /auth/logout` — logout simply deletes the
   cookie, `response.delete_cookie("access_token", path="/")`)

## M2 — route-boundary audit

6. Name the exact condition `get_current_admin` checks on the user
   record beyond a valid signature. (`user.get("role") != "admin"` —
   even a valid, unexpired token for a non-admin user is rejected with
   401 "Not authorized")
7. What are the two distinct JWT failure modes the code separately
   handles, and do they return different messages? (Yes —
   `jwt.ExpiredSignatureError` → "Token expired"; `jwt.InvalidTokenError`
   → "Invalid token" — a candidate should be able to name both, not
   just "invalid token" generically)
8. Name the public (non-admin-gated) routes confirmed in this
   corpus. (`GET /catalogue`, `GET /events`, `GET /merch`, `POST
   /newsletter`, `POST /payments/checkout`, `GET /payments/status/
   {id}`, `POST /stripe/webhook`, `GET /tickets/{tid}`, `GET /tickets/
   {tid}/qr.png` — no `Depends(get_current_admin)` on any of these)
9. Name at least 3 `/admin/*` routes and confirm each carries the
   dependency. (Any 3 of: `/admin/catalogue`, `/admin/events`,
   `/admin/merch`, `/admin/fans`, `/admin/newsletter`, `/admin/orders`,
   `/admin/outbox/frek-id`, `/admin/outbox/wallet` — all gated)

## M3 — incident recognition (not response)

10. If a candidate suspects a leaked admin token, what real revocation
    mechanism exists in this code to invalidate it before its natural
    12-hour expiry? (**None observed** — no token blocklist/revocation
    route exists in the audited code; the only real mitigation is the
    token's own 12h expiry and `POST /auth/logout` clearing the
    cookie client-side, which does not invalidate a copied token used
    elsewhere. A candidate must recognize this gap and escalate to a
    human/JWT_SECRET rotation, never invent a revocation endpoint that
    doesn't exist.)
