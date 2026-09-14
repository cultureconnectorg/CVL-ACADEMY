# FRK-69 — Evidence Model

`READY_FOR_FREK_PROOF = FALSE`.

## Chaîne de preuve

Audit d'artefact annoté (correspondance source, ou incohérence
documentée) → note de référence FRK-68 → correcteur → (jury si
2.0–2.5) → `FRK69.SKILL.EVIDENCE_PROVENANCE_AUDIT.L1` (réservé).

## Ce qui compte comme preuve

Un audit qui vérifie réellement la correspondance artefact/événement
source ; toute incohérence détectée est documentée, jamais ignorée ;
la référence correcte à FRK-68.

## Ce qui NE compte PAS comme preuve

Un audit qui ignore une incohérence détectée ; une redéfinition des
trois surfaces de FRK-68 au lieu d'une référence.

- Réservation d'ID : `FRK69.SKILL.EVIDENCE_PROVENANCE_AUDIT.L1` —
  réservé, non émis.
- Prérequis : FRK-68 (trois surfaces réelles `db.frek_signals`,
  `db.frek_outbox`, `db.wallet_outbox`), réutilisé par référence.
- Mapping `VALID_SIGNALS` : aucun aujourd'hui pour cette formation
  elle-même — l'audit porte sur les signaux déjà émis via ces surfaces.
