# FRK-69 — Banque N1 (formatif)

Réserve `FRK69.SKILL.*`.

## Extension de FRK-68 (M1/M3)

1. Comment l'audit d'artefacts de preuve/provenance étend-il la
   compétence procédurale générale de FRK-68 (FREK Auditor) ?
2. Rappelle les trois surfaces réelles d'audit citées par FRK-68
   (`db.frek_signals`, `db.frek_outbox`, `db.wallet_outbox`) — pourquoi
   cette formation les réutilise-t-elle par référence plutôt que de
   les redécrire ?

## Audit d'artefact vs. audit procédural (M1)

3. Qu'est-ce qui distingue un audit d'artefact de preuve (ex. vérifier
   qu'un `PROOF-{uuid}` correspond bien à un événement réel dans
   `db.frek_signals`) d'un audit procédural général ?

## Procédure d'audit d'artefact (M2)

4. Que fait un auditeur qui reçoit un artefact `PROOF-{uuid}` sans
   accès à `db.frek_signals` correspondant ? (Il documente
   l'incohérence, jamais il ne l'ignore ni ne suppose que l'événement
   existe)
5. Quel est le schéma d'insertion réel de `db.frek_signals` (hérité de
   FRK-68) ? (`user_id`, `signal`, `meta`, `ts`)

## Discipline des deux formations (M3)

6. Pourquoi une confusion entre FRK-68 et FRK-69 serait-elle
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
4. Il documente l'incohérence, jamais il ne l'ignore.
5. `user_id`, `signal`, `meta`, `ts`.
6. Une confusion des deux ferait perdre la spécialisation propre à
   cette formation et dupliquerait inutilement FRK-68.
