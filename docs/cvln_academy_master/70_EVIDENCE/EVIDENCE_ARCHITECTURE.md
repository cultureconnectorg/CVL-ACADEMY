# CVLN Academy Master — Evidence Architecture

```
STATUS: DECIDED (doctrine, reuses proven Academy/FMS/KLT/KOR patterns).
No new evidence types invented without repo grounding.
```

## Chaîne d'évidence (rappel §21 mission)

```
COMPETENCY → MODULE/PATH → ASSESSMENT → EVIDENCE → SKILL_ID → QUALIFICATION
```

Si une habilitation s'applique :

```
QUALIFICATION → HUMAN/POLICY GATE → AUTHORIZATION
```

## Règle FREK

`READY_FOR_FREK_PROOF = FALSE` par défaut pour toute évidence tant que
l'ancrage FREK réel n'est pas câblé pour ce domaine précis. Vérifié
dans ce repo : FREK core (`services/frek_core.py`) et l'événement
`academy.certification.passed` (→ CVLN Brain) sont réels, mais
**aucune** évidence pédagogique KOR/KLT/FMS ne les utilise encore comme
preuve signée — cohérent avec le corpus KOR-01→15 déjà livré (voir
`docs/kor/kora_master_package/MASTER_EVIDENCE_MODEL.md`).

## Skill ID Namespace Map

| Corpus | Namespace | Statut |
|---|---|---|
| KOR-01→15 | `KOR01.SKILL.*` → `KOR15.SKILL.*` | `PROPOSED`, 169 IDs, aucune collision (déjà livré) |
| KLT-01→08 | `KLT01.SKILL.*` → `KLT08.SKILL.*` | `PROPOSED` (déjà livré) |
| FMS-01→06 | espace existant (voir `backend/fms_canonical/`) | Lié au runtime |
| Domaines candidats de cette cartographie (LOS, WAL-interne, CVE, KLT-09→20, FMS-07→18, etc.) | à définir au niveau W6 par domaine | `NOT_STARTED` — aucun Skill ID n'est réservé prématurément par ce document |

## Interdiction

`NO_FAKE_PROOF` : aucune évidence proposée dans ce Master Package
n'affirme un ancrage FREK, Brain, ou Wallet au-delà de ce qui est
vérifié dans `95_GAPS/REPO_TRUTH_AUDIT.md`.
