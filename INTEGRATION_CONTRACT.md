# CVLN Academy OS — Integration Contract

Ce document décrit précisément les endpoints et payloads que **CVLN Academy OS** attend
de la part des deux systèmes externes de l'écosystème CVLN :

1. **FrekCore** — infrastructure d'identité, signaux, badges & preuves.
2. **CVLN Agent Factory** — orchestrateur d'agents IA (Mentor, futurs agents pôles).

## Principe d'identité

Un **FREK-ID est une identité souveraine de l'écosystème CVLN**, pas un rôle Academy.
La même personne conserve le même FREK-ID lorsqu'elle agit dans d'autres plateformes CVLN.
Academy rattache ensuite localement à cette identité ses rôles pédagogiques, memberships,
organisations, permissions, progression et données propres au produit.

Academy ne doit donc jamais devenir une seconde autorité concurrente de FREKCORE en
production.

---

## 1. Variables d'environnement à ajouter dans `backend/.env`

```env
# FrekCore — développement/test local uniquement
FREK_CORE_IDENTITY_AUTHORITY=local_dev

# FrekCore — déploiement intégré / identité souveraine
# FREK_CORE_IDENTITY_AUTHORITY=frekcore
# FREK_CORE_BASE_URL=https://<real-frekcore-host>
# FREK_CORE_API_KEY=xxxx

# CVLN Agent Factory
CVLN_AGENT_FACTORY_URL=https://agents.cvln.io
CVLN_AGENT_FACTORY_API_KEY=xxxx
```

`FREK_CORE_IDENTITY_AUTHORITY` accepte uniquement :

- `local_dev` : Academy peut mint un identifiant séquentiel local pour le développement et les tests.
- `frekcore` : FREKCORE est l'unique autorité d'identité. Si l'URL est absente, si le service est
  indisponible ou si `/mint` ne retourne pas un `frek_id` valide, l'inscription échoue en **HTTP 503**.
  Il n'existe aucun fallback local de mint dans ce mode.

Le endpoint de santé `/api/` expose :

- `frek_core_remote`
- `frek_core_identity_authority`
- `frek_core_sovereign_identity`

Cela permet de vérifier sans ambiguïté si Academy est réellement configurée pour déléguer
l'identité à FREKCORE.

---

## 2. Contrat FrekCore (client HTTP)

Fichier : `backend/services/frek_core.py` — méthodes publiques utilisées par le reste
de l'app :

| Méthode Academy | Endpoint attendu | Payload (JSON) | Réponse attendue |
|---|---|---|---|
| `mint_frek_id()` | `POST {BASE_URL}/mint` | `{}` | `{ "frek_id": "FREK-042" }` |
| `emit_signal(user_id, sig, meta)` | `POST {BASE_URL}/signal` | `{ "user_id": "...", "signal": "FREK-WORK", "meta": {…} }` | `{ "ok": true }` (200) |
| `issue_proof(user_id, kind, meta)` | `POST {BASE_URL}/proof` | `{ "user_id": "...", "kind": "badge", "meta": {…} }` | `{ "proof_id": "PROOF-ABC123" }` |

Signaux FREK valides envoyés depuis Academy :
`FREK-TIME`, `FREK-WORK`, `FREK-SCORE`, `FREK-LINK`, `FREK-CERT`, `FREK-CONTRIB`, `FREK-SHARE`, `FREK-MISSION`.

Headers : `Authorization: Bearer {FREK_CORE_API_KEY}` lorsqu'une clé est configurée.

### Comportement de mint

- En `local_dev`, le mint se fait via `db.counters` pour permettre le développement autonome.
- En `frekcore`, Academy appelle exclusivement `POST {BASE_URL}/mint`.
- En `frekcore`, une panne ou une réponse invalide de FREKCORE **ne déclenche jamais** de mint local.

### Signaux et preuves

Les signaux restent archivés localement puis sont miroirés en best-effort vers FREKCORE afin
qu'une panne de télémétrie ne rende pas Academy inutilisable.

La preuve (`issue_proof`) conserve encore un fallback local temporaire tant que le contrat de
preuve FREKCORE n'a pas été rendu obligatoire. Cette tolérance ne s'applique pas à l'identité.

---

## 3. Contrat CVLN Agent Factory

Fichier : `backend/services/agent_factory.py` — méthodes publiques :

### 3.1 `list_available_agents()`
Endpoint suggéré : `GET {URL}/agents`
Réponse attendue :
```json
[
  {
    "code": "mentor-cvln",
    "name": "Mentor CVLN",
    "description": "Guide de parcours…",
    "model": "claude-sonnet-5",
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

Comportement fallback : si `CVLN_AGENT_FACTORY_URL` est vide → Academy appelle directement
le SDK `anthropic` avec le prompt système Mentor CVLN, selon l'implémentation actuelle.

---

## 4. Frontière stricte Academy / FREKCORE

Academy :

- ✅ conserve le `frek_id` comme clé d'identité portable ;
- ✅ gère ses rôles, organisations, cohortes, memberships et permissions propres ;
- ✅ consomme les capacités FREKCORE par la couche `services/frek_core.py` ;
- ❌ ne définit pas un nouveau FREK-ID selon le rôle métier ;
- ❌ ne crée pas une seconde identité pour une personne lorsqu'elle change de plateforme CVLN ;
- ❌ ne devient pas la source de vérité canonique d'identité en mode `frekcore` ;
- ❌ n'implémente pas la certification blockchain / preuve cryptographique FREKCORE.

Les collections MongoDB locales servent au fonctionnement propre d'Academy et au mode
`local_dev`. Elles ne remplacent pas l'autorité canonique FREKCORE en mode souverain.

---

## 5. Checklist d'intégration FREKCORE

- [ ] FREKCORE expose un `POST /mint` stable et idempotent selon son contrat canonique.
- [ ] FREKCORE expose `POST /signal`.
- [ ] FREKCORE expose `POST /proof` lorsque la preuve distante sera rendue obligatoire.
- [ ] Une vraie `FREK_CORE_BASE_URL` est fournie à Academy.
- [ ] Une vraie `FREK_CORE_API_KEY` est fournie si le service l'exige.
- [ ] `FREK_CORE_IDENTITY_AUTHORITY=frekcore` est activé dans l'environnement intégré.
- [ ] `/api/` retourne `frek_core_sovereign_identity: true`.
- [ ] Un test d'inscription confirme qu'un FREK-ID minté par FREKCORE est conservé tel quel.
- [ ] Un test de panne confirme qu'Academy retourne 503 et ne crée aucun FREK-ID local.

Tant que ces points ne sont pas vérifiés sur une instance FREKCORE réelle, l'état honnête est :
**contrat prêt côté Academy, connexion souveraine non prouvée en runtime**.
