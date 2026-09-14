# FRK-03 — Guide Correcteur

## Avant de noter

Ouvre un header `FREK_PROOF_MAPPING` réel (`docs/kor/kor01/modules/`)
et `frek_core.py` à côté de la copie.

## Ce que tu vérifies en priorité

1. Le candidat distingue-t-il intention de signal et preuve vérifiée ?
2. Décrit-il correctement les effets de bord réels ?
3. Affirme-t-il à tort `READY_FOR_FREK_PROOF = TRUE` ?
4. Affirme-t-il qu'un échec de mirroring distant invalide l'écriture
   locale `db.frek_signals` ?

## Ce que tu ne fais pas

Tu ne notes pas sur intuition générique — seulement sur les headers et
le code réels.
