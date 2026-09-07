"""Database indexes — ensured once at startup (rule 13: ready for
thousands of users). Every collection that gets queried by user_id (which
is most of them, at multi-user scale) gets an index on it; unique lookup
keys (email, frek_id, opaque tokens, invite codes) get unique indexes so
duplicates fail fast at the DB layer, not just in application code.

`create_index` is idempotent — safe to call on every startup.
"""

from __future__ import annotations

from db import db


async def ensure_indexes() -> None:
    # Identity / auth
    await db.users.create_index("email", unique=True)
    await db.users.create_index("frek_id", unique=True)
    await db.refresh_tokens.create_index("token_hash", unique=True)
    await db.refresh_tokens.create_index("user_id")
    await db.password_resets.create_index("token_hash", unique=True)
    await db.email_verifications.create_index("token_hash", unique=True)
    await db.invitations.create_index("code", unique=True)

    # Learning progress — queried by user_id on every dashboard/module load
    await db.progress.create_index([("user_id", 1), ("module_code", 1)], unique=True)
    await db.user_badges.create_index([("user_id", 1), ("badge_code", 1)], unique=True)
    await db.user_missions.create_index(
        [("user_id", 1), ("mission_code", 1)], unique=True
    )
    await db.frek_signals.create_index([("user_id", 1), ("ts", -1)])

    # Skill Engine / Certification Engine
    await db.skill_evidence.create_index([("user_id", 1), ("skill_id", 1)])
    await db.user_skills.create_index([("user_id", 1), ("skill_id", 1)], unique=True)
    await db.certification_attempts.create_index([("user_id", 1), ("created_at", -1)])
    await db.certification_attempts.create_index("status")
    await db.certification_rubrics.create_index("certification_code", unique=True)

    # Template Engine
    await db.template_documents.create_index([("user_id", 1), ("updated_at", -1)])
    await db.template_document_versions.create_index(
        [("document_id", 1), ("version", -1)]
    )
    await db.template_definitions.create_index("type", unique=True)

    # Wallet
    await db.wallet_accounts.create_index("user_id", unique=True)
    await db.wallet_transactions.create_index([("user_id", 1), ("created_at", -1)])
    # WAL-01 (Audit Chirurgical 2026-09-07) — the real idempotency
    # guard: every wallet.credit() call now requires a real
    # economic_event_id, so this index is never sparse-vs-null
    # ambiguous (see wallet/service.py's own docstring for why).
    # MIGRATION NOTE: this repo has no live MongoDB in this sandbox and
    # this session never observed a real deployed wallet_transactions
    # collection, so no backfill script exists here. A real production
    # deployment carrying pre-existing rows with no economic_event_id
    # (multiple such rows collide on `null`) must run a one-time
    # backfill (a synthetic unique id per legacy row, e.g. its own `id`
    # field) before this index build — this comment names that
    # requirement rather than silently assuming it away.
    await db.wallet_transactions.create_index(
        [("user_id", 1), ("economic_event_id", 1)], unique=True
    )

    # Assistants / mentor
    await db.mentor_conversations.create_index(
        [("user_id", 1), ("session_id", 1)], unique=True
    )
    await db.assistant_conversations.create_index(
        [("user_id", 1), ("persona", 1), ("session_id", 1)], unique=True
    )

    # Orgs / cohorts
    await db.organisations.create_index("slug", unique=True)
    await db.cohorts.create_index("org_id")

    # Catalogue
    await db.formations.create_index("code", unique=True)
    await db.formations.create_index("content_status")

    # ACA-0005 — Module Lineage (legacy<->canonical FMS mapping, additive
    # only, never touches db.formations/db.progress — see fms_lineage/).
    await db.module_lineage.create_index("lineage_id", unique=True)
    # Refuses an exact duplicate pair (same legacy module, same canonical
    # target, same archive version) while still allowing a legacy module
    # to hold several distinct RELATED records against different
    # canonical modules (they differ on canonical_module_code, so the
    # compound key differs too).
    await db.module_lineage.create_index(
        [
            ("legacy_formation_code", 1),
            ("legacy_module_code", 1),
            ("canonical_formation_code", 1),
            ("canonical_module_code", 1),
            ("canonical_version", 1),
        ],
        unique=True,
        name="module_lineage_pair_unique",
    )
    await db.module_lineage.create_index(
        [("legacy_formation_code", 1), ("legacy_module_code", 1)]
    )
    await db.module_lineage.create_index(
        [("canonical_formation_code", 1), ("canonical_module_code", 1)]
    )
    await db.module_lineage.create_index("status")

    # ACA-0006 — Canonical FMS runtime binding.
    # Canonical progress: a collection *separate* from db.progress by
    # construction, not just by convention — see fms_canonical/progress.py.
    await db.canonical_progress.create_index(
        [("user_id", 1), ("canonical_module_code", 1)], unique=True
    )
    await db.canonical_progress.create_index(
        [("user_id", 1), ("canonical_formation_code", 1)]
    )
    # Source-file provenance ledger (Founder blocking correction,
    # 2026-09-03): one row per real ZIP entry, parsed or not — see
    # fms_canonical/provenance.py.
    await db.fms_resource_provenance.create_index(
        [("original_path", 1), ("canonical_version", 1)], unique=True
    )
    await db.fms_resource_provenance.create_index("sha256")
    await db.fms_resource_provenance.create_index("parsing_status")
    await db.fms_resource_provenance.create_index(
        [("formation_code", 1), ("resource_type", 1)]
    )

    # ACA-0007/ACA-0008 — Physical/hybrid delivery (physical_delivery.py).
    await db.physical_sessions.create_index(
        [("formation_code", 1), ("starts_at", 1)]
    )
    await db.physical_sessions.create_index("status")
    # PHY-01 (Audit Chirurgical 2026-09-07) — real, DB-enforced guard
    # against double-booking: unique per (session_id, user_id), but only
    # across "active" statuses (partialFilterExpression). Scoping it to
    # enrolled/waitlisted — never a plain unique index — is deliberate:
    # a user who cancels and later re-enrolls must be allowed to (a new
    # document, since cancel_enrollment never deletes the cancelled
    # record — see its own docstring), and a bare unique index would
    # reject that legitimate second enrollment as a duplicate of the
    # first, now-cancelled one.
    await db.physical_enrollments.create_index(
        [("session_id", 1), ("user_id", 1)],
        unique=True,
        partialFilterExpression={"status": {"$in": ["enrolled", "waitlisted"]}},
    )
    await db.physical_enrollments.create_index([("user_id", 1), ("status", 1)])
    await db.physical_attendance.create_index([("session_id", 1), ("user_id", 1)])
