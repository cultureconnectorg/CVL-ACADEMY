# CVLN Academy OS — Integration Contract

Ce document décrit précisément les endpoints et payloads que **CVLN Academy OS** attend
de la part des deux systèmes externes du écosystème CVLN :

1. **FrekCore** — infrastructure d'identité, signaux, badges & preuves.
2. **CVLN Agent Factory** — orchestrateur d'agents IA (Mentor, futurs agents pôles).

> Tant que les vrais services ne sont pas branchés, Academy fonctionne en mode
> **LOCAL FALLBACK** (voir `backend/services/frek_core.py` & `backend/services/agent_factory.py`).
>
> Le jour où vous fournissez les URLs & clés, **aucun autre fichier du code
> n'a besoin d'être modifié** — seule cette couche d'abstraction est reconfigurée.

---

## 1. Variables d'environnement à ajouter dans `backend/.env`

```env
# FrekCore
FREK_CORE_BASE_URL=https://frekcore.cvln.io       # optionnel : si vide → fallback local
FREK_CORE_API_KEY=xxxx

# CVLN Agent Factory
CVLN_AGENT_FACTORY_URL=https://agents.cvln.io     # optionnel : si vide → fallback Emergent LLM
CVLN_AGENT_FACTORY_API_KEY=xxxx
```

Après modification de `.env` → `sudo supervisorctl restart backend`.

---

## 2. Contrat FrekCore (client HTTP)

Fichier : `/app/backend/services/frek_core.py` — méthodes publiques utilisées par le reste
de l'app :

| Méthode Academy               | Endpoint attendu                   | Payload (JSON)                                              | Réponse attendue                    |
|-------------------------------|------------------------------------|-------------------------------------------------------------|-------------------------------------|
| `mint_frek_id()`              | `POST {BASE_URL}/mint`             | `{}` (ou méta utilisateur si nécessaire)                    | `{ "frek_id": "FREK-042" }`         |
| `emit_signal(user_id, sig, meta)` | `POST {BASE_URL}/signal`       | `{ "user_id": "...", "signal": "FREK-WORK", "meta": {…} }`  | `{ "ok": true }` (200)              |
| `issue_proof(user_id, kind, meta)` | `POST {BASE_URL}/proof`       | `{ "user_id": "...", "kind": "badge", "meta": {…} }`        | `{ "proof_id": "PROOF-ABC123" }`    |

Signaux FREK valides envoyés depuis Academy :
`FREK-TIME`, `FREK-WORK`, `FREK-SCORE`, `FREK-LINK`, `FREK-CERT`, `FREK-CONTRIB`, `FREK-SHARE`, `FREK-MISSION`.

Headers : `Authorization: Bearer {FREK_CORE_API_KEY}`.

Comportement fallback local :
- Si `FREK_CORE_BASE_URL` est vide OU si le remote répond en erreur → Academy utilise
  MongoDB (`db.counters`, `db.frek_signals`) et génère des FREK-IDs séquentiels.

---

## 3. Contrat CVLN Agent Factory

Fichier : `/app/backend/services/agent_factory.py` — méthodes publiques :

### 3.1 `list_available_agents()`
Endpoint suggéré : `GET {URL}/agents`
Réponse attendue :
```json
[
  {
    "code": "mentor-cvln",
    "name": "Mentor CVLN",
    "description": "Guide de parcours…",
    "model": "anthropic/claude-sonnet-4-6",
    "status": "active"
  }
]
```

### 3.2 `mentor_reply(user_frek_id, display_name, session_id, message, history, lang)`
Endpoint suggéré : `POST {URL}/agents/mentor-cvln/chat`

Payload envoyé :
```json
{
  "session_id": "mentor-<user_id>",
  "user": {
    "frek_id": "FREK-042",
    "display_name": "Ali",
    "lang": "fr"
  },
  "message": "Comment débuter FMS-01 ?",
  "history": [
    { "role": "user", "content": "…" },
    { "role": "assistant", "content": "…" }
  ]
}
```

Réponse attendue :
```json
{ "reply": "Kouman ou yé ? Commence par le module FMS-01-M01 …" }
```

Comportement fallback : si `CVLN_AGENT_FACTORY_URL` vide → Academy appelle directement
Claude Sonnet 4.6 via `emergentintegrations` avec le prompt système Mentor CVLN.

---

## 4. Ce que Academy NE fait PAS (frontière stricte)

- ❌ Academy n'implémente pas la logique d'orchestration multi-agent.
- ❌ Academy n'implémente pas la certification blockchain / preuve cryptographique.
- ❌ Academy ne stocke pas les états canoniques d'identité (source de vérité = FrekCore).

Les collections MongoDB `frek_signals`, `user_badges`, `counters` sont uniquement
un **cache local** et un **fallback** en attendant les vraies APIs.

---

## 5. Checklist d'intégration côté vous (FrekCore / Agent Factory)

- [ ] Ouvrir `POST /mint`, `POST /signal`, `POST /proof` côté FrekCore.
- [ ] Ouvrir `POST /agents/mentor-cvln/chat` côté Agent Factory.
- [ ] Fournir `FREK_CORE_BASE_URL`, `FREK_CORE_API_KEY`, `CVLN_AGENT_FACTORY_URL`,
      `CVLN_AGENT_FACTORY_API_KEY`.
- [ ] Notifier Academy → un simple restart backend suffit pour switcher.

Contact technique Academy : voir `/app/memory/PRD.md`.
