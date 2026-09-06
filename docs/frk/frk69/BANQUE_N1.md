# FRK-69 — Banque N1 (formatif)

Réserve `FRK69.SKILL.*`.

1. Comment l'audit d'artefacts de preuve/provenance étend-il la
   compétence procédurale générale de FRK-68 (FREK Auditor) ?
2. Rappelle les trois surfaces réelles d'audit citées par FRK-68
   (`db.frek_signals`, `db.frek_outbox`, `db.wallet_outbox`) — pourquoi
   cette formation les réutilise-t-elle par référence plutôt que de
   les redécrire ?
3. Qu'est-ce qui distingue un audit d'artefact de preuve (ex. vérifier
   qu'un `PROOF-{uuid}` correspond bien à un événement réel dans
   `db.frek_signals`) d'un audit procédural général ?
4. Pourquoi une confusion entre FRK-68 et FRK-69 serait-elle
   éliminatoire ici ?

## Corrigé indicatif

1. FRK-68 pose la discipline procédurale générale d'audit ; FRK-69 la
   spécialise pour l'audit spécifique d'artefacts de preuve et de
   provenance.
2. Réutiliser par référence évite la duplication et garde FRK-68 comme
   source unique de vérité pour la description de ces trois surfaces.
3. L'audit d'artefact de preuve vérifie la cohérence entre un artefact
   (ex. `PROOF-{uuid}`) et son événement source réel — plus spécifique
   qu'un audit procédural général qui vérifie la conformité du
   processus lui-même.
4. Une confusion des deux ferait perdre la spécialisation propre à
   cette formation et dupliquerait inutilement FRK-68.
