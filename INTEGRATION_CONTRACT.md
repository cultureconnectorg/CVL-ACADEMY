# CVLN Academy OS — Integration Contract

Ce document décrit les intégrations externes consommées par **CVLN Academy OS**.

1. **FREKCORE** — autorité du FREK-ID et capacités transversales de confiance.
2. **CVLN Agent Factory** — orchestrateur d'agents IA.

## Principe d'identité

Un **FREK-ID est une identité persistante de l'écosystème CVLN**, pas un rôle Academy.
Academy conserve localement les rôles pédagogiques, organisations, cohortes, memberships,
permissions, progression et données produit autour de ce même identifiant.

Dans le périmètre actuel, Academy **ne reconstruit pas le portail d'identité FREKCORE et
n'implémente pas de SSO FREK**. Lors d'une inscription Academy, le backend Academy agit comme
client applicatif FREKCORE, demande le FREK-ID canonique, puis enregistre ce FREK-ID dans sa
projection utilisateur locale.

---

## 1. Configuration

```env
# Développement/test autonome uniquement
FREK_CORE_IDENTITY_AUTHORITY=local_dev

# Déploiement intégré
# FREK_CORE_IDENTITY_AUTHORITY=frekcore
# FREK_CORE_BASE_URL=https://<real-frekcore-host>
# FREK_CORE_CLIENT_ID=cvln-academy
# FREK_CORE_CLIENT_SECRET=<secret-client-frekcore>

# Intégrations non-identity historiques, tant que leurs contrats ne sont pas réconciliés
# FREK_CORE_API_KEY=<optional-legacy-service-key>

# CVLN Agent Factory
CVLN_AGENT_FACTORY_URL=https://agents.cvln.io
CVLN_AGENT_FACTORY_API_KEY=xxxx
```

`FREK_CORE_IDENTITY_AUTHORITY` accepte :

- `local_dev` : Academy peut générer un FREK-ID local uniquement pour développement/test.
- `frekcore` : FREKCORE est l'autorité d'émission. Academy utilise le contrat v1 existant et
  **ne génère jamais de FREK-ID local de secours** si FREKCORE est indisponible ou mal configuré.

Le endpoint de santé `/api/` expose notamment :

- `frek_core_remote`
- `frek_core_identity_authority`
- `frek_core_sovereign_identity`

---

## 2. Contrat FREK-ID réellement utilisé

Source vérifiée : branche FREKCORE `claude/frekcore-v1-production-b9h2q0`.

### 2.1 Authentifier CVLN Academy auprès de FREKCORE

`POST {FREK_CORE_BASE_URL}/api/v1/auth/token`

```json
{
  "client_id": "cvln-academy",
  "client_secret": "<secret>",
  "grant_type": "client_credentials"
}
```

Réponse attendue :

```json
{
  "access_token": "...",
  "token_type": "Bearer",
  "expires_in": 86400
}
```

Le client FREKCORE configuré pour Academy doit être actif et posséder la permission `emit`.

### 2.2 Obtenir/créer le FREK-ID lors d'une inscription Academy

`POST {FREK_CORE_BASE_URL}/api/v1/identity/emit`

Header :

```text
Authorization: Bearer <client_access_token>
```

Payload Academy :

```json
{
  "email": "maya@example.com",
  "source": "cvln_academy",
  "metadata": {
    "application": "cvln_academy",
    "lang": "fr"
  }
}
```

Réponse attendue :

```json
{
  "frek_id": "FREK-...",
  "created": true,
  "stage": "GENESIS",
  "message": "..."
}
```

FREKCORE hache l'email avant persistance. Le endpoint est idempotent dans le contexte du
`client_id` FREKCORE : une identité déjà connue pour le même email et le même client retourne
le FREK-ID existant avec `created: false`.

### 2.3 Projection Academy

Après réception du FREK-ID, Academy :

- stocke le `frek_id` tel quel ;
- crée son compte/session Academy ;
- applique éventuellement invitation, rôle, organisation et cohorte ;
- conserve progression et données pédagogiques dans Academy ;
- refuse qu'un même FREK-ID soit projeté sur deux comptes Academy distincts.

Academy ne modifie jamais la syntaxe du FREK-ID reçu et ne crée pas un identifiant différent
selon le rôle ou l'organisation.

### Limite connue du contrat FREKCORE v1

L'idempotence actuellement observée dans FREKCORE v1 est basée sur `email_hash + client_id`.
Cela sécurise l'émission pour un client Academy stable, mais **ne prouve pas encore à lui seul
l'unicité globale du même individu entre plusieurs clients CVLN différents**. Ce sujet relève de
l'évolution canonique FREKCORE et n'est pas reconstruit dans CVLN Academy dans cette PR.

---

## 3. Signaux et preuves FREKCORE

`backend/services/frek_core.py` contient encore des miroirs best-effort historiques pour les
signaux et les preuves. Leurs anciens chemins `/signal` et `/proof` ne sont **pas déclarés comme
contrat FREKCORE v1 vérifié** dans cette livraison.

Ils doivent être réconciliés séparément avec les capacités réelles de FREKCORE avant d'être
considérés comme intégration distante de production. Cette incertitude n'affecte pas le contrat
FREK-ID décrit en section 2.

---

## 4. Contrat CVLN Agent Factory

Fichier : `backend/services/agent_factory.py`.

### `list_available_agents()`

Endpoint cible : `GET {URL}/agents`

### `mentor_reply(...)`

Endpoint cible : `POST {URL}/agents/mentor-cvln/chat`

Le payload transporte notamment le `frek_id` de l'utilisateur afin que les agents puissent
travailler dans le bon contexte sans devenir propriétaires de son identité.

---

## 5. Frontière stricte Academy / FREKCORE

Academy :

- ✅ conserve le FREK-ID canonique retourné par FREKCORE ;
- ✅ utilise un client FREKCORE dédié avec permission minimale `emit` ;
- ✅ gère authentification/session Academy, rôles, organisations, cohortes et progression ;
- ✅ échoue en 503 en mode `frekcore` si l'identité distante ne peut pas être obtenue ;
- ❌ ne génère pas un autre FREK-ID en production ;
- ❌ ne transforme pas rôle/organisation en identité ;
- ❌ ne reconstruit pas FREKCORE, son Identity Engine, ses Passkeys, DID/VC ou son portail ;
- ❌ ne prétend pas fournir aujourd'hui un SSO « Sign in with FREK » qui n'est pas le sujet de cette PR.

---

## 6. Checklist de mise en service Academy

- [ ] Créer/configurer dans FREKCORE un client applicatif stable `cvln-academy` avec permission `emit`.
- [ ] Renseigner `FREK_CORE_BASE_URL`, `FREK_CORE_CLIENT_ID`, `FREK_CORE_CLIENT_SECRET` dans le runtime Academy.
- [ ] Activer `FREK_CORE_IDENTITY_AUTHORITY=frekcore`.
- [ ] Vérifier `POST /api/v1/auth/token` avec le client Academy.
- [ ] Vérifier une inscription Academy → `/api/v1/identity/emit` → FREK-ID reçu → même valeur en base Academy.
- [ ] Vérifier une nouvelle tentative cohérente : pas de second FREK-ID Academy.
- [ ] Vérifier panne FREKCORE : inscription Academy = 503, aucun mint local.
- [ ] Réconcilier séparément les anciens FREK-ID Academy avant bascule production, sans écrasement automatique.

État attendu avant runtime réel : **contrat FREK-ID Academy aligné sur FREKCORE v1 ; connexion de
production non prouvée tant que les credentials et le déploiement réel n'ont pas été testés.**
