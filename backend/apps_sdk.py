"""OpenAI Apps SDK augmentation for the existing public Academy MCP server.

The core server remains vendor-neutral MCP. This module only adds an optional
ChatGPT-friendly widget resource and tool result metadata; other MCP clients can
ignore the OpenAI metadata and continue using the same server.
"""

from __future__ import annotations

import json

import mcp.types as types

from mcp_server import academy_capabilities, academy_mcp

TEMPLATE_URI = "ui://cvln-academy/overview.html"


@academy_mcp.tool()
async def academy_overview_widget() -> types.CallToolResult:
    """Render a compact CVLN Academy capability card for Apps SDK hosts."""
    capabilities = await academy_capabilities()
    structured = {
        "name": capabilities["name"],
        "mode": capabilities["mode"],
        "domains": capabilities["domains"],
        "active_experts": capabilities["active_experts"],
        "private_actions_endpoint": "/mcp/private",
    }
    return types.CallToolResult(
        content=[
            types.TextContent(
                type="text",
                text="CVLN Academy est prêt : catalogue public + actions privées OAuth.",
            )
        ],
        structuredContent=structured,
        _meta={
            "openai/outputTemplate": TEMPLATE_URI,
            "openai/toolInvocation/invoking": "Chargement de CVLN Academy",
            "openai/toolInvocation/invoked": "CVLN Academy prêt",
            "openai/widgetAccessible": True,
        },
        isError=False,
    )


@academy_mcp.resource(
    TEMPLATE_URI,
    "CVLN Academy Overview",
    mime_type="text/html+skybridge",
)
async def academy_overview_template() -> str:
    """Inline Apps SDK widget; deliberately dependency-free and CSP-minimal."""
    return """<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>CVLN Academy</title>
  <style>
    body{font-family:system-ui,-apple-system,sans-serif;margin:0;padding:16px;background:transparent;color:var(--color-text-primary,#111)}
    .card{border:1px solid rgba(127,127,127,.25);border-radius:16px;padding:16px}
    h2{margin:0 0 8px;font-size:18px}.muted{opacity:.7;font-size:13px}.chips{display:flex;gap:6px;flex-wrap:wrap;margin-top:12px}
    .chip{border:1px solid rgba(127,127,127,.25);border-radius:999px;padding:5px 9px;font-size:12px}
  </style>
</head>
<body>
  <div class="card">
    <h2>CVLN Academy</h2>
    <div id="mode" class="muted">Catalogue et expertise formation</div>
    <div id="chips" class="chips"></div>
  </div>
  <script>
    const payload = window.openai?.toolOutput || window.openai?.toolResult?.structuredContent || {};
    const domains = payload.domains || [];
    document.getElementById('mode').textContent = payload.mode || 'CVLN Academy';
    document.getElementById('chips').innerHTML = domains.map(x => `<span class="chip">${String(x).replace(/[&<>"']/g, s => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[s]))}</span>`).join('');
  </script>
</body>
</html>"""
