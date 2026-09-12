"""Outbound AI data-minimisation policy for CVLN Academy.

Every foundation-model transport must apply this module before data leaves the
Academy trust boundary. The policy is intentionally provider-neutral: Anthropic,
NVIDIA Dynamo and future providers receive the same minimized payload.

The canonical CVLN identity remains inside CVLN. Provider calls use a deterministic
pseudonym for operational correlation and redact obvious identifiers/secrets from
text payloads. This is defence in depth, not a replacement for user-facing privacy
controls or contractual data-processing terms.
"""

from __future__ import annotations

import hashlib
import hmac
import os
import re
from typing import Any, Dict, List, Mapping, Tuple

OUTBOUND_HISTORY_LIMIT = 12

_EMAIL_RE = re.compile(r"(?<![\w.+-])[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}(?![\w.-])", re.I)
_FREK_ID_RE = re.compile(r"\bFREK-[A-Z0-9][A-Z0-9._:/-]{2,}\b", re.I)
_BEARER_RE = re.compile(r"\bBearer\s+[A-Z0-9._~+/=-]{12,}", re.I)
_API_KEY_RE = re.compile(r"\bsk-[A-Z0-9_-]{16,}\b", re.I)


def _pseudonym_key() -> Tuple[bytes, str]:
    explicit = os.environ.get("AI_PSEUDONYMIZATION_KEY")
    if explicit:
        return explicit.encode("utf-8"), "AI_PSEUDONYMIZATION_KEY"

    jwt_secret = os.environ.get("JWT_SECRET")
    if jwt_secret:
        return jwt_secret.encode("utf-8"), "JWT_SECRET"

    # Development/test fallback only. Production status makes this visible so the
    # deployment can fail its own readiness policy without leaking any secret.
    return b"cvln-academy-development-pseudonym-key", "development-fallback"


def pseudonymise_session(session_id: str) -> str:
    """Return a stable non-reversible correlation id, never the raw session id."""
    key, _source = _pseudonym_key()
    digest = hmac.new(key, session_id.encode("utf-8"), hashlib.sha256).hexdigest()
    return f"ai_{digest[:24]}"


def redact_text(value: str) -> str:
    """Remove identifiers/secrets that model providers do not need for inference."""
    text = str(value or "")
    text = _EMAIL_RE.sub("[redacted-email]", text)
    text = _FREK_ID_RE.sub("[redacted-frek-id]", text)
    text = _BEARER_RE.sub("Bearer [redacted-token]", text)
    text = _API_KEY_RE.sub("[redacted-api-key]", text)
    return text


def sanitise_history(history: List[Mapping[str, Any]]) -> List[Dict[str, str]]:
    """Keep only the recent role/content window needed by a chat model."""
    clean: List[Dict[str, str]] = []
    for item in history[-OUTBOUND_HISTORY_LIMIT:]:
        role = item.get("role")
        content = item.get("content")
        if role not in {"user", "assistant"} or not isinstance(content, str) or not content:
            continue
        clean.append({"role": str(role), "content": redact_text(content)})
    return clean


def prepare_outbound_conversation(
    system_prompt: str,
    message: str,
    history: List[Mapping[str, Any]],
) -> Tuple[str, str, List[Dict[str, str]]]:
    """Return the provider-safe system prompt, message and history."""
    return (
        redact_text(system_prompt),
        redact_text(message),
        sanitise_history(history),
    )


def policy_status() -> Dict[str, Any]:
    """Non-secret observability for health/admin diagnostics."""
    _key, key_source = _pseudonym_key()
    environment = os.environ.get("ACADEMY_ENV", "development").strip().lower()
    strong_key_configured = key_source != "development-fallback"
    return {
        "enabled": True,
        "history_limit": OUTBOUND_HISTORY_LIMIT,
        "canonical_identity_exported": False,
        "session_ids_pseudonymised": True,
        "text_redaction": ["email", "frek_id", "bearer_token", "api_key"],
        "pseudonym_key_source": key_source,
        "production_key_ready": environment != "production" or strong_key_configured,
    }
