# FRK-68 — Banque N2 (cas appliqués)

## Cas N2-1 — Rapport d'audit trimestriel

Un rapport doit couvrir "l'activité FREK" du trimestre. Que dois-tu
inclure, et comment structurer le rapport pour ne pas induire en
erreur ?

**Critères de notation :** structure le rapport en 3 sections
séparées (activité `db.frek_signals` de cette Academy ; statut
`db.frek_outbox` de Good Mood ; statut `db.wallet_outbox` de Good
Mood), jamais fusionnées en une seule métrique "FREK." Élimination si
le candidat produit un chiffre unique agrégeant les trois.

## Cas N2-2 — Entrée bloquée en `failed`

Une entrée `db.wallet_outbox` est `failed`. Explique ce qui a dû se
passer et ce qu'il faut faire.

**Critères de notation :** explique que les 5 tentatives du schedule
ont toutes échoué, et qu'aucun mécanisme de retry automatique
supplémentaire n'existe au-delà — nécessite une intervention manuelle
ou l'acceptation de la perte de livraison. Élimination si le candidat
invente un mécanisme de retry infini.

## Cas N2-3 — Confusion des trois tables

Un stagiaire audite `db.frek_signals` et conclut sur l'état de
`db.frek_outbox` de Good Mood. Corrige-le.

**Critères de notation :** explique que ce sont deux tables
distinctes, dans deux systèmes distincts (cette Academy vs. Good
Mood) — l'état de l'une ne dit rien sur l'état de l'autre. Élimination
si le candidat confirme la conclusion croisée erronée.
