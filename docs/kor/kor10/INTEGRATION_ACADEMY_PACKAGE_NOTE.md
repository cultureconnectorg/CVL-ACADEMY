# KOR-10 — Note d'intégration au Master Package

Ce document pointe vers le corpus KOR-10 sans le dupliquer. Il sera
référencé depuis `docs/kora_master_package/` une fois celui-ci
construit (après KOR-15).

## Ce que KOR-10 fournit au Master Package

- 10 compétences (C1-C10), dont **1 seule** `KORA_CURRENT_CAPABILITY`
  réelle dans tout le corpus KOR à ce stade : C8 (Wallet/JCC).
- Un registre de Skill IDs stable : `KOR10.SKILL.C01`-`C10`.
- Un `KORA_PRODUCT_GAP` explicite pour tout ce qui dépasse Wallet/JCC
  (pas de moteur de tarification dynamique, pas de CRM créateur
  intégré au module économique — cf. `KOR-09`/`KOR-14`).
- Une clarification CVE réutilisable telle quelle par toute autre
  formation qui mentionnerait CVE (`EXTERNAL_PRODUCT_EVIDENCE_NOT_AUDITED`,
  jamais `CVE_DOES_NOT_EXIST`).

## Tensions actives à reporter au Boundary Map global

- #6 (`KOR-07`/`KOR-10` — royalties vs pricing/monétisation).

## Statut d'intégration

`NOT_YET_LINKED` — en attente de `docs/kora_master_package/`.
