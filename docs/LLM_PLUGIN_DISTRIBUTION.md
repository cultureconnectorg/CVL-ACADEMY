# CVLN Academy — LLM Plugin Distribution

Status: implementation in progress. This document distinguishes implemented runtime from provider publication steps.

## Implemented runtime

- FastAPI mounts a public Streamable HTTP MCP endpoint at `/mcp`.
- The MCP server exposes only published catalogue data and public Expert Directory metadata.
- Expert Directory entries are explicit about `active` versus `planned` status.
- One provider-neutral MCP contract is used for all compatible assistants.

## Expert Directory V1

Active discovery/orchestration experts:

- Orientation
- Formation
- Career
- Music
- Cinema & Audiovisuel
- Tech & AI
- Caribbean / Overseas
- Laurentia orchestration

Planned expert contracts are already registered but MUST NOT be represented as implemented:

- Funding
- Tutor
- Assessment
- Certification
- Institution
- Trainer
- Support

## MCP tools

Current public tools:

- `academy_capabilities`
- `list_experts`
- `get_expert`
- `route_expert`
- `list_poles`
- `search_formations`
- `get_formation`

Resources:

- `academy://about`
- `academy://experts`
- `academy://formations/{code}`

Prompts:

- `recommend_training`
- `academy_expert_assist`

## Distribution architecture

```text
ChatGPT / Claude / Gemini / MCP clients
                |
          provider adapter
                |
        CVLN Academy MCP
                |
       Expert Directory
                |
      Academy business logic
                |
             MongoDB
```

Provider adapters MUST NOT fork business rules. Authentication, learner data and write actions will be introduced as separate authenticated scopes after the public read-only surface is stable.

## ChatGPT

OpenAI publication is a provider-side step after the runtime is reachable over HTTPS and passes review. The codebase prepares the MCP app surface; public Plugin Directory availability is not considered complete until the app/plugin is submitted and approved by OpenAI.

Required release gates before submission:

1. production HTTPS MCP endpoint reachable;
2. MCP CI green on the exact deployment commit;
3. privacy policy and terms URLs point to real production documents;
4. provider-facing app metadata and branding are final;
5. no private learner/admin data exposed by anonymous tools;
6. authentication/scopes added before any personalized or write action;
7. provider Developer Mode smoke test completed against production-like deployment;
8. submission/review completed in the provider console.

## Other LLMs

Claude or other MCP-native clients can consume the same MCP contract when their product/workspace permits remote MCP connections. Gemini and other providers should use an adapter only where their native connector contract differs. The adapter must map to the same CVLN Academy tools rather than duplicate domain logic.

## Evidence First

Compatibility is not publication. A provider name in `academy_capabilities.compatible_targets` means the protocol can be adapted/consumed there; it does not claim that CVLN Academy is already listed, approved or generally available in that provider's directory.
