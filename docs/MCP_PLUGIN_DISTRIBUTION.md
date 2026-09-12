# CVLN Academy — MCP / Plugin distribution

## Surfaces

- `POST /mcp` — public, read-only MCP catalogue and expert discovery.
- `POST /mcp/private` — OAuth-protected MCP actions for the connected Academy user.
- `GET /.well-known/oauth-authorization-server` — OAuth authorization-server metadata.
- `GET /.well-known/oauth-protected-resource/mcp/private` — RFC 9728 protected-resource metadata.
- `/oauth/authorize` — Authorization Code + PKCE S256 user consent/login.
- `/oauth/token` — authorization-code and refresh-token grants.
- `/oauth/revoke` — refresh-token revocation.
- `/oauth/register` — optional dynamic client registration, disabled by default.

## OAuth scopes

- `academy:profile.read`
- `academy:funding.read`
- `academy:funding.write`
- `academy:enrollment.read`
- `academy:enrollment.write`

The private MCP transport always requires `academy:profile.read`. Individual tools enforce their additional scopes.

## Funding guarantees

Afdas and France Travail remain evidence-based `PORTAL_ASSISTED` connectors until CVLN has a verified contractual machine interface. MCP tools create real Academy dossier records and can mark them `READY`, but never fabricate external submission, approval or eligibility. This deliberately reuses the Institutional Bridge policy.

## ChatGPT Apps SDK

`backend/apps_sdk.py` augments the vendor-neutral public MCP server with an Apps SDK-compatible widget resource (`text/html+skybridge`) and `openai/*` tool-result metadata. Other MCP clients may ignore this metadata.

The app can therefore be tested in ChatGPT Developer Mode against the deployed `/mcp` endpoint. Connected-user actions live on `/mcp/private` and use OAuth discovery.

## Render production configuration

Set these variables on the existing CVLN Academy backend service. Do not put secrets in GitHub:

```text
ACADEMY_ENV=production
JWT_SECRET=<long random production secret>
MONGO_URL=<production MongoDB connection>
DB_NAME=<production database>
MCP_OAUTH_ISSUER=https://<public-backend-host>
MCP_PRIVATE_RESOURCE=https://<public-backend-host>/mcp/private
MCP_OAUTH_ALLOW_DYNAMIC_REGISTRATION=true
MCP_ALLOWED_HOSTS=<public-backend-host>,<public-backend-host>:*
CORS_ORIGINS=<approved frontend origins>
```

Keep `MCP_OAUTH_ALLOW_DYNAMIC_REGISTRATION=false` until the public production host and redirect policy have been reviewed. Static clients can instead be supplied through `MCP_OAUTH_CLIENTS_JSON`.

After deployment run:

```bash
python scripts/verify_mcp_distribution.py https://<public-backend-host>
```

Expected result: public MCP reachable, OAuth metadata aligned with the public host, and private MCP returning `401/403` without a token.

## ChatGPT / Plugin Directory release gate

Code completion is not the same as directory publication. Publication requires an external OpenAI submission/review and cannot be completed by a Git commit. Before submission, verify:

1. Production `/mcp` and `/mcp/private` over HTTPS.
2. OAuth authorization flow from a fresh account using PKCE.
3. Privacy policy and terms URLs on the Academy public site.
4. Tool descriptions and action semantics match runtime behavior.
5. Funding actions clearly state preparation vs external submission.
6. Write actions require user authorization and appropriate scopes.
7. Developer Mode smoke test in ChatGPT.
8. Submit the app/plugin through the current OpenAI submission flow.

OpenAI currently recommends Apps SDK for packaging/publishing MCP-backed app experiences; Plugins Directory publication is a separate reviewed distribution step.
