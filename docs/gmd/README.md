# Good Mood Internal Operator Corpus (GMD-21 → GMD-34)

```
WORKSTREAM = GMD (Good Mood internal operator layer), W6 Wave 1 of the
CVLN Academy Master 2D reconciliation (docs/cvln_academy_master/).
SOURCE OF TRUTH: docs/cvln_academy_master/20_EXTERNAL/
GOOD_MOOD_DJ_SAYD_RECONCILIATION.md — this corpus builds exactly what
that document already verdicted (NEW_INTERNAL, buildable now on real
code), it does not re-audit or re-classify.
STATUT = 1/14 formation à package canonique complet (GMD-21 :
référentiel + banque N1 + banque N2 + assessment + rubric + evidence
model + 3 guides + integration note — niveau KOR/KLT), 12/14
(GMD-22→33) au niveau MODULE_CONTENT_DRAFTED (référentiel + modules
seulement, approfondissement en cours vague par vague — ce n'est PAS
un état final, voir Founder directive 2026-09-06), 1/14
(GMD-34) BLOCKED_PRODUCT_DEPENDENCY (aucun mécanisme d'incident/
rollback réel n'existe dans gmfest972/goodmooddjsayd ; non simulé,
voir gmd34/GAP.md). Aucune formation n'est FULLY_COMPLETE — même
GMD-21 attend un premier passage réel vérifié par un humain avant ce
statut.
```

## Pourquoi ce corpus existe

`GOOD_MOOD_DJ_SAYD_RECONCILIATION.md` a identifié GMD-21→33 comme le
cluster interne-opérateur le mieux ancré de tout le chantier de
réconciliation (13/14 lignes constructibles immédiatement sur du code
réel — `gmfest972/goodmooddjsayd`, repo public cloné et audité). Ce
corpus est le premier construit du W6 ("construire les référentiels
pédagogiques réels par vagues", instruction Founder du 2026-09-06),
choisi en premier précisément parce qu'il est le mieux grounded.

## Ce que contient ce corpus

| Formation | Dossier | Ancrage repo réel | Modules |
|---|---|---|---|
| GMD-21 — Good Mood OS Operator (ombrelle) | `gmd21/` | `backend/server.py` (874 lignes, vue d'ensemble) | 4 |
| GMD-22 — Catalogue Operator | `gmd22/` | `Volume` model, `/catalogue`, `/admin/catalogue` | 3 |
| GMD-23 — Event Operator | `gmd23/` | `Event` model, `/events`, `/admin/events/*` | 3 |
| GMD-24 — Ticket Type & Sales Operator | `gmd24/` | `TicketType`, `/tickets/{tid}`, `/tickets/{tid}/qr.png` | 3 |
| GMD-25 — Door Scan & Access Operator | `gmd25/` | `/scan/check`, `/scan/counter/{eid}` | 3 |
| GMD-26 — Fan CRM Operator | `gmd26/` | `/admin/fans`, `/newsletter` | 3 |
| GMD-27 — Merch & Store Operator | `gmd27/` | `Product`, `/merch`, `/admin/merch/*` | 3 |
| GMD-28 — Orders & Payment Operations | `gmd28/` | Stripe: `/payments/checkout`, `/stripe/webhook` | 4 |
| GMD-29 — Newsletter & Campaign Operator | `gmd29/` | `/admin/newsletter`, `email_service.py` (bilingue) | 3 |
| GMD-30 — Event Reporting Operator | `gmd30/` | `/admin/events/{eid}/report`, `/admin/events/{eid}/tickets` | 3 |
| GMD-31 — FREK Outbox Operator | `gmd31/` | `frek_service.py`, `/admin/outbox/frek-id` | 3 |
| GMD-32 — Wallet Ticket Integration Operator | `gmd32/` | `wallet_service.py`, `/admin/outbox/wallet` | 3 |
| GMD-33 — Good Mood Admin & Security Operations | `gmd33/` | `/auth/login`, `/auth/me`, `/auth/logout` | 3 |
| GMD-34 — Incident & Recovery Operations | `gmd34/` | **aucun** | 0 (`GAP.md` seulement) |

**41 modules construits** across 13 formations, plus 1 gap explicitement
non construit.

## Doctrine partagée (évite la duplication de contenu, règle §26)

- `CERTIFICATION_MODEL.md` — un seul modèle de certification pour les
  13 formations (elles partagent le même backend, le même
  Acheteur/Contexte — `INTERNAL_QUALIFICATION`, jamais vendu, per
  `100_ECONOMY/ECONOMIC_MODEL.md`).
- `QUALITY_GATES.md` — un seul passage de gates pour tout le corpus.
- Chaque `REFERENTIAL.md` cite le code réel avec chemin de fichier —
  jamais de capacité "probablement présente".

## Ce que ce corpus NE fait PAS

Ne modifie aucun fichier du repo `gmfest972/goodmooddjsayd` (lecture
seule, cloné publiquement). Ne prétend à aucune capacité au-delà de ce
qui est vérifié dans `GOOD_MOOD_DJ_SAYD_RECONCILIATION.md` — GMD-34
reste un gap déclaré, jamais simulé. Aucune certification n'a été
délivrée à un candidat réel — `FULLY_COMPLETE = FALSE` pour
l'ensemble du corpus tant qu'un premier passage réel n'est pas
vérifié par un humain.
