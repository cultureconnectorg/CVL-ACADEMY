# FRK-73 — FREK Cryptographic Architecture

## Repo truth this formation is built on

Grounded in `frek_v3/docs/FREK_Cryptographic_Architecture_Review_
v0.1.md` + `reference_verifier/frek_crypto.py` (real P-256/ECDSA
primitives, `PUF → HKDF → DRK → AK/FK/CK` key-derivation chain, raw
`r||s` signatures, canonical-message encoding) — déjà audité cette
session, `REPO_REGISTRY.md`.

Per `FREK_01_75_RECONCILIATION.md` : coverage `PARTIAL — SOURCE_
OBSERVED`, distinctness `DISTINCT_PROFESSION`, action `NEW_EXTERNAL`.
**Toujours `NEEDS_EXPERT_REVIEW`** (cryptographie appliquée, jamais
enseignée comme auditée en production sans revue d'un cryptographe
nommé) — cette réserve tient indépendamment du statut
`ARCHITECTURE_LEVEL_2`.

## Prerequisites

FRK-71.

## Objectives

Un candidat qui travaille sur FRK-73 (formation formative uniquement,
sans voie certifiante tant que la revue experte n'est pas levée) sait
lire précisément la chaîne de dérivation de clés et le schéma de
signature réels, sans jamais affirmer de garantie de sécurité :

- Enseigner la chaîne de dérivation de clés et le schéma de signature
  réels, tels que spécifiés et implémentés dans `frek_crypto.py`.
- Porter la réserve `NEEDS_EXPERT_REVIEW` sur chaque affirmation — ce
  contenu n'est jamais présenté comme audité cryptographiquement sans
  revue d'un expert nommé, quelle que soit la réalité du code.
- Distinguer précisément « code réel et fonctionnel » de « sécurité
  prouvée » : le fait que ce code existe, s'exécute et produise des
  résultats corrects sur des tests ne constitue en rien une preuve de
  sécurité cryptographique — seule une revue par un cryptographe
  qualifié peut établir cette garantie.

## Modules

1. **Littératie de la chaîne de dérivation de clés** (`PUF → HKDF →
   DRK → AK/FK/CK`).
2. **Littératie du schéma de signature ECDSA P-256**.
3. **Discipline `NEEDS_EXPERT_REVIEW`**.

## Assessment

Différé en attente de revue experte pour toute affirmation
certifiante ; examen de littératie sur le code/la spec réels autorisé,
jamais une affirmation d'audit de sécurité.

## Status

`STATUS = MODULE_CONTENT_DRAFTED`, `NEEDS_EXPERT_REVIEW` non résolu.
