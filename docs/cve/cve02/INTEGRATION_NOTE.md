# CVE-02 — Integration Academy Package Note

## Réel vs. supposé

**Réel (re-vérifié directement cette session) :**
`KORA_CVE_Specification_Mathematique_v1.0.md` §1 (Trust Score, les 5
composantes `S,E,F,C,L`) et §2.1 (transformation de saturation,
statut explicitement non tranché). Tout est cité section par section
dans `REFERENTIAL.md`.

**Supposé :** un lien `CVE02.SKILL.*` réel dans le runtime de cette
Academy — inexistant (`NO_RUNTIME_BINDING`). Également supposé
non-existant, explicitement : toute simulation ou calibration réelle
des paramètres (`τ_fraude`, poids, `ρ_c`) — le document lui-même place
cela au chantier 2, non réalisé.

## Dépendances

- `docs/cvln_academy_master/20_EXTERNAL/WALLET_CVE_RECONCILIATION.md`
  (jamais re-audité ni contredit ici — `FD-CVE-001`), `70_EVIDENCE/
  EVIDENCE_ARCHITECTURE.md`, `100_ECONOMY/ECONOMIC_MODEL.md`
  (`INTERNAL_QUALIFICATION`, `NOT_FOR_SALE`), CVE-01 (prérequis).

## Ce qu'une future intégration exigerait

1. Une entrée `CVE02` dans le registre de certification de cette
   Academy.
2. Une surface candidat réelle (ce corpus est markdown seul).
3. Que le chantier 2 (simulation) de la méthodologie KORA soit
   effectivement réalisé avant qu'un candidat certifié puisse opérer
   un vrai calcul CVE — jamais avant, jamais automatique.

## Status

`STATUS = PACKAGE_COMPLETE_FOR_CVE02` — référentiel, banques N1/N2,
assessment + rubric, evidence model, 3 guides, cette note
d'intégration existent tous. `FULLY_COMPLETE` non déclaré — requiert
un passage réel vérifié par un humain.
