# CVLN Academy Master — Cross-Ecosystem Map

```
SOURCE: raw/Cross_Ecosystem.csv (153 rows) + raw/Missions_Pipelines.csv
(10 rows: 4 Missions, 6 Pipelines). STATUS: PROPOSED (153), DECIDED
(10 pipelines — adopted as doctrine, not yet implemented).
```

## Les 6 pipelines cross-CVLN (doctrine, §19 mission)

| Pipeline | Chaîne |
|---|---|
| Artist-to-Audience | artiste → FMS → FREK → LabelOS → KORA → public |
| Activity-to-Value | activité → événement → identité → preuve → signal → CVE → allocation → Wallet → ledger → settlement → reconciliation |
| Learning-to-Opportunity | information → apprentissage → simulation → assessment → compétence → preuve → qualification → opportunité → mission → expérience |
| Digital-to-Physical | Academy → Spatial → lieu → mission réelle → preuve terrain |
| Cultural Memory | création → diffusion → expérience → documentation → FREK → Fondation → archive → Academy → transmission |
| Intelligent Operations | humain → Laurentia → IOS → Brain → Agent Factory → application → Proof → Command Center → humain |

## Les 4 missions (cas d'usage bout-en-bout)

| Mission | Chaîne | Règle |
|---|---|---|
| A — Sortir un morceau | FMS → FREK → LabelOS → KORA → Wallet/CVE | Ne perdre ni droits, metadata, provenance, responsabilité |
| B — Produire Good Mood | Kiltikonet → artistes → LabelOS/FMS → Good Mood → Gala → Hospitality → KORA → FREK → Wallet → Fondation | Mission cross-ecosystem live complète |
| C — Former puis employer | Academy → assessment → FREK proof → Kiltikonet opportunity → Good Mood mission → évaluation terrain → Wallet → portfolio Academy | Learning-to-work |
| D — Incident écosystème | KORA + agent autonome + Wallet sensible → autorité → suspension → preuve → reprise | Human authority, incident, recovery |

## 153 compétences cross-écosystème candidates (index)

Réparties principalement entre KOR-X (7), LOS-X (8), WAL-X (9), et le
reste sous "Cross-CVLN" (67) et sous-domaines croisés (Agent
Factory/Laurentia 9, Blockchain/Tokenomics 11, Intelligent Operations
10) — voir `raw/Cross_Ecosystem.csv` pour le détail complet.

## Repo truth vérifié sur ces chaînes

- **Mission B** (Good Mood) : le maillon `FREK` et `Wallet` de cette
  chaîne existe réellement côté Good Mood (`frek_service.py`,
  `wallet_service.py`, outbox pattern) — voir
  `95_GAPS/REPO_TRUTH_AUDIT.md`. Le reste de la chaîne (Kiltikonet,
  LabelOS/FMS, Gala, Hospitality, Fondation) n'a aucun ancrage vérifié.
- **Mission C** (Learning-to-work) : le maillon `Academy → assessment
  → FREK proof` existe partiellement (FREK core réel, mais
  `READY_FOR_FREK_PROOF = FALSE` pour KORA — voir corpus `docs/kor/`).
  Le reste (Kiltikonet opportunity, Good Mood mission, Wallet) reste
  candidat.

`DUPLICATE_CURRICULUM` : aucune compétence cross-écosystème de cette
carte ne doit reconstruire l'enseignement vertical d'un domaine — elle
enseigne le *handoff*, jamais le contenu déjà couvert par le domaine
source (règle §19).
