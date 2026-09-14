# GMD-22 — Banque N1 (formative, M1→M3)

```
16 questions, sourced against gmfest972/goodmooddjsayd/backend/server.py
lines 80-98 (VolumeIn/Volume) and lines 219-305 (catalogue routes).
Same discipline as GMD-21/BANQUE_N1.md: no invented field, no invented
route.
```

## M1 — `Volume`/`VolumeIn` field literacy

1. Name the two required fields on `VolumeIn` that have no default
   value. (`number`, `title`)
2. `year`, `plays`, `description`, `cover_url`, `listen_url` are all
   declared `Optional[str] = ""`. What does that mean for a candidate
   who claims "the field is mandatory in the database"? (False — Pydantic
   defaults them to empty string, not required)
3. What type is `sc_track`, and what does its default tell you about
   whether every `Volume` is expected to have a SoundCloud track id?
   (`Optional[int] = None` — not every Volume has one)
4. What field controls display ordering, and what is its default?
   (`order: int = 0`)
5. Which two fields exist on `Volume` but not on `VolumeIn`, and why?
   (`id`, `created_at` — server-generated, never client-supplied)
6. `model_config = ConfigDict(extra="ignore")` — what happens if an
   operator submits an extra field like `"artist_note"` on a create
   call? (Silently ignored, not stored, not an error)

## M2 — CRUD walkthrough (real admin routes)

7. Name the exact HTTP method + path to create a `Volume`.
   (`POST /admin/catalogue`)
8. Name the exact HTTP method + path to list all volumes as an admin
   (not the public view). (`GET /admin/catalogue`)
9. What does `admin_catalogue_list` sort by, and in which direction?
   (`.sort("order", 1)` — ascending)
10. What is the maximum number of records `GET /admin/catalogue`
    returns in one call, per the code? (`to_list(500)`)
11. Compare: what is that same cap for the **public** `GET /catalogue`
    route? (`to_list(200)`) — why might a candidate wrongly assume
    they're identical? (Because both sort by `order` — only the cap
    differs, easy to miss without reading both lines)
12. What HTTP method + path updates an existing volume, and what
    identifies which one? (`PUT /admin/catalogue/{vid}`, `vid` = the
    volume's `id`)
13. What does `admin_catalogue_update` do if `vid` does not match any
    existing document? (It reads `existing` first — a real
    implementation must be checked, not assumed; the honest answer a
    candidate must give is "trace the actual code," not guess)
14. What HTTP method + path deletes a volume, and is deletion soft or
    hard per the route name alone? (`DELETE /admin/catalogue/{vid}` —
    the route is a hard delete call; "soft-retire" in the M2 objective
    is an operator **convention**, not a distinct API mechanism — do
    not invent a `status` field that does not exist on `Volume`)
15. Every admin catalogue route carries `_=Depends(get_current_admin)`.
    What does a candidate need to hold before they can exercise any of
    these four routes? (A valid admin session/auth — same boundary as
    GMD-21/M3)

## M3 — diagnostic

16. A fan reports "my new track isn't showing on the site." Given only
    the model and the public route (`db.catalogue.find({}, {"_id": 0})
    .sort("order", 1)`), what is the FIRST thing to check before
    assuming a bug? (Whether the `POST /admin/catalogue` call actually
    succeeded and the record exists at all — the public route has no
    visibility filter beyond existing-and-sorted, so "not showing"
    usually means "not created," not "hidden by a flag that doesn't
    exist in this model")
