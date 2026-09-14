# KORA Master Package — Academy Integration Map

## Statut

`NOT_INTEGRATED` — ce corpus est **documentaire uniquement**. Aucun
fichier de code, seed, ou runtime n'a été créé ni modifié pour produire
KOR-01→15 ou ce Master Package (`NO_RUNTIME_BINDING`, `NO_DB_MUTATION`,
`NO_SEED_MUTATION`).

## Ce qu'une intégration future impliquerait (hors mandat de ce chantier)

- Import des référentiels/modules dans le moteur FMS existant
  (`backend/fms_import/`, déjà construit pour les corpus FMS/
  Kiltikonet) — même mécanique réutilisable, jamais un nouveau moteur.
- Génération de Skill IDs runtime à partir de
  `MASTER_SKILL_REGISTRY.md` — nécessiterait une revue humaine
  préalable (les 169 Skill IDs sont `STATUS = PROPOSED`, pas
  `ACTIVE`).
- Aucune intégration Wallet/JCC supplémentaire n'est nécessaire pour
  `KOR-10`/C8 — le mécanisme réel existe déjà indépendamment de ce
  corpus.

## Interdiction explicite

`NO_KORA_PRODUCT_UPGRADE` — ce document ne mandate aucune intégration,
il documente seulement ce qu'une intégration future demanderait.
