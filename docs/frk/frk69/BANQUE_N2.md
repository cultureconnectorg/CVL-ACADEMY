# FRK-69 — Banque N2 (cas appliqués)

## Cas 1 — Audit d'un artefact de preuve

Le candidat audite un artefact `PROOF-{uuid}` en vérifiant sa
correspondance avec un événement réel dans `db.frek_signals`, en citant
FRK-68 par référence pour la discipline procédurale des trois
surfaces.

**Critère éliminatoire :** redéfinir les trois surfaces de FRK-68 au
lieu de les citer.

**Critères de notation :** vérifie réellement la correspondance
artefact/événement, pas seulement la présence de l'artefact.

## Cas 2 — Incohérence détectée

Le candidat identifie un cas où un artefact de preuve n'a aucun
événement source correspondant, et documente l'anomalie selon la
discipline d'audit.

**Critère éliminatoire :** ignorer une incohérence détectée sans la
documenter.

## Cas 3 — Artefact valide mais outbox en échec

Un artefact `PROOF-{uuid}` correspond correctement à un événement réel
dans `db.frek_signals`, mais l'entrée correspondante dans
`db.wallet_outbox` est en statut `failed` après ses 5 tentatives de
retry. L'artefact reste-t-il valide au sens de l'audit de provenance ?
Explique en respectant la discipline des trois systèmes séparés.

**Critères de notation :** identifie que l'artefact reste valide au
sens de la provenance (source event réel confirmé) — l'échec de
livraison outbox est un problème distinct, dans un système séparé
(Good Mood→Wallet), jamais fusionné dans le même récit d'audit.
Élimination si le candidat fusionne les deux systèmes en une seule
conclusion de validité.
