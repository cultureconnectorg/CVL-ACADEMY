# FRK-03 — Guide Candidat

## Avant de commencer

Prérequis : FRK-01, FRK-58.

## Ce que tu dois savoir faire

Lire un header `FREK_PROOF_MAPPING` réel, opérer les effets de bord
réels d'`emit_signal()`/`mint_frek_id()`, et jamais promouvoir
`READY_FOR_FREK_PROOF` à `TRUE` sans preuve.

## Comment réviser

1. Lis un header réel dans `docs/kor/kor01/modules/`.
2. Lis `docs/kor/kor01/skills/EVIDENCE_MODEL.md`.
3. Fais les 8 questions de `BANQUE_N1.md`, traite les 3 cas de
   `BANQUE_N2.md`.

## Piège le plus fréquent

Confondre "le header existe" avec "une preuve externe vérifiée
existe" — ce sont deux choses différentes.

## Règle absolue

N'invente jamais une ancre externe ou un `READY_FOR_FREK_PROOF =
TRUE` non justifié — élimination automatique.
