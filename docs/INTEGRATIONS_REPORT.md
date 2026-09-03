# CVLN Academy — Rapport des intégrations écosystème

Statut réel de chaque connexion à l'écosystème CVLN, au 30 août 2026. La
même donnée est exposée programmatiquement via `GET /api/integrations`
(rôle admin) — ce rapport ne peut donc pas dériver de ce qui est
effectivement câblé : les deux lisent `services/integrations/registry.py`.

**Principe directeur (règle 9)** : chaque système ci-dessous est une
interface réelle et typée, activée par variables d'environnement, jamais un
faux "connecté". Sans les identifiants du système cible, Academy tourne en
mode local/fallback — documenté au cas par cas.

---

## Statut par système

| Système | Fichier | État aujourd'hui | Pour l'activer |
|---|---|---|---|
| **FrekCore** | `services/frek_core.py` | Fallback local complet et fonctionnel : FREK-ID séquentiel généré via `db.counters`, signaux archivés dans `db.frek_signals`, stades calculés localement. Pas juste un stub — c'est le comportement réel de production tant que FrekCore n'est pas branché. | `FREK_CORE_BASE_URL` + `FREK_CORE_API_KEY` — voir `INTEGRATION_CONTRACT.md` pour le contrat REST exact attendu (`/mint`, `/signal`, `/proof`) |
| **CVLN Agent Factory** | `services/agent_factory.py` | Fallback local complet : appelle directement Claude Sonnet 5 via le SDK Anthropic officiel (`chat_reply()`, transport générique partagé par tous les assistants — règle 12). Remplace l'ancien `emergentintegrations`, qui n'était même pas installable hors du sandbox Emergent. | `CVLN_AGENT_FACTORY_URL` + `CVLN_AGENT_FACTORY_API_KEY` |
| **CVLN Intelligence OS** | `services/integrations/registry.py` (`intelligence_os`) | Interface générique prête (`EcosystemIntegration`), non configurée — aucun appel n'est fait tant que l'URL n'est pas définie. | `CVLN_INTELLIGENCE_OS_URL` + `_API_KEY` |
| **CVLN Brain** | idem (`brain`) | Interface prête **et déjà câblée à un événement réel** : `academy.certification.passed` (émis par `certification/service.py` à chaque certification réussie) tente de le notifier en best-effort dès qu'il sera configuré — voir `services/integrations/subscribers.py`. | `CVLN_BRAIN_URL` + `_API_KEY` |
| **CVLN Command Center** | idem (`command_center`) | Même chose que Brain — reçoit le même événement `academy.certification.passed`. | `CVLN_COMMAND_CENTER_URL` + `_API_KEY` |
| **CVLN Agent Factory** | *(voir plus haut)* | | |
| **Laurent.ia** | idem (`laurentia`) | Interface prête, non configurée. | `LAURENTIA_URL` + `_API_KEY` |
| **FREKCORE** | *(voir FrekCore plus haut)* | | |
| **KORA** | idem (`kora`) | Interface prête, non configurée. | `KORA_URL` + `_API_KEY` |
| **Factory Maker Studio** | idem (`factory_maker_studio`) | Interface prête, non configurée. | `FACTORY_MAKER_STUDIO_URL` + `_API_KEY` |
| **CVLN Wallet** (interne) | `wallet/` | **Implémenté et actif**, pas seulement une interface : grand livre JCC/tokens (`wallet_transactions`, append-only), soldes cachés (`wallet_accounts`), déjà crédité par les badges (+10 JCC) et les certifications réussies (+50 JCC). Voir la section Wallet ci-dessous pour ce qui reste externe (Apple/Google réels). | Rien à activer côté interne — fonctionne dès le premier déploiement |
| **Good Mood** | `services/integrations/registry.py` (`good_mood`) | Interface prête, non configurée. | `GOOD_MOOD_URL` + `_API_KEY` |
| **Culture Connect** | idem (`culture_connect`) | Interface prête, non configurée. | `CULTURE_CONNECT_URL` + `_API_KEY` |
| **Kiltikonet** | idem (`kiltikonet`) | Interface prête, non configurée. | `KILTIKONET_URL` + `_API_KEY` |

---

## CVLN Wallet — détail (règle 10)

- **Ce qui fonctionne aujourd'hui, réellement** : solde JCC/tokens par
  utilisateur, historique de transactions, crédit automatique sur badge
  obtenu et certification réussie, endpoints `GET /api/wallet/me` et
  `GET /api/wallet/transactions`.
- **Apple Wallet / Google Wallet** (`wallet/passes.py`) : la *donnée* du pass
  est produite dans le format documenté de chaque plateforme
  (`GET /api/wallet/pass/apple`, `.../google`) — mais **non signée**. Un vrai
  fichier `.pkpass` installable nécessite un certificat Apple Developer WWDR
  + un Pass Type ID ; un vrai lien "Ajouter à Google Wallet" nécessite un
  compte Google Wallet Issuer pour signer le JWT. Ni l'un ni l'autre
  n'existe pour CVLN à ce jour — les endpoints le disent explicitement
  (`"status": "unsigned"`) plutôt que de produire un fichier qui a l'air
  installable et ne l'est pas.

## FREKCORE-ready — détail (règle 11)

"FREK-ready" est implémenté comme : chaque preuve de compétence
(`skills/EvidenceEntry`) et chaque signature de jury
(`certification/JurySignature`) porte un hash SHA-256 canonique sur son
propre contenu — vérifiable indépendamment de la base de données. C'est
exactement ce qu'un futur appel `frek_core.issue_proof(kind="certification")`
transportera (voir `certification/attestation.py::attestation_export_metadata`)
une fois FrekCore réellement branché — cette mission construit ce que cet
appel transportera, pas l'appel lui-même (qui suppose un FrekCore actif).

## Assistant IA commun — détail (règle 12)

`services/ai_assistant.py` définit 4 personas (student/trainer/jury/
corrector) **entièrement comme des données** (prompt système + rôles
autorisés) au-dessus d'un seul transport générique
(`agent_factory.chat_reply`). Ajouter un 5ᵉ persona = une entrée de
dictionnaire, jamais une branche de code. `GET /api/assistants` (filtré par
rôle) + `POST /api/assistants/{persona}/chat`.

---

## Checklist d'activation (côté CVLN, quand les systèmes existent)

Pour chaque système listé "non configuré" ci-dessus :

1. Fournir l'URL de base + la clé API de service à l'équipe Academy.
2. Renseigner les deux variables d'environnement correspondantes dans
   `backend/.env` (voir `backend/.env.example` pour la liste complète).
3. Redémarrer le backend — `GET /api/integrations` doit passer à
   `"configured": true` pour ce système, sans aucune modification de code.
4. Pour Brain/Command Center spécifiquement : rien d'autre à faire, l'appel
   `academy.certification.passed` partira automatiquement dès la
   configuration détectée.
