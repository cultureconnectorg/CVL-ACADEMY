# FRK-73 — Integration Academy Package Note

**Réel :** `frek_v3/docs/FREK_Cryptographic_Architecture_Review_v0.1.md`
+ `reference_verifier/frek_crypto.py` — code P-256/ECDSA réel et
fonctionnel, chaîne `PUF→HKDF→DRK→AK/FK/CK`, signatures `r||s`
canoniques.
**Supposé :** `FRK73.SKILL.*` réel — inexistant.

## Dépendances

`FREK_01_75_RECONCILIATION.md`, `docs/frk/frk71/REFERENTIAL.md`
(prérequis), `frek_v3/reference_verifier/frek_crypto.py` (grounding
réel cité), `docs/frk/frk75/REFERENTIAL.md` (couverture par tests
fonctionnels, jamais confondue avec un audit de sécurité).

## Ce que ce package couvre

Les 8 fichiers de support (`BANQUE_N1`, `BANQUE_N2`,
`ASSESSMENT_AND_RUBRIC`, `EVIDENCE_MODEL`, `GUIDE_CANDIDAT`,
`GUIDE_CORRECTEUR`, `GUIDE_JURY`, ce fichier) sont écrits cette passe,
au même niveau de rigueur que les formations promues `PACKAGE_
COMPLETE` de ce corpus.

## Pourquoi le statut reste `MODULE_CONTENT_DRAFTED`

`FRK-73` porte un flag `NEEDS_EXPERT_REVIEW` (cryptographie appliquée)
depuis `FREK_01_75_RECONCILIATION.md`. Ceci reste délibérément en
dessous du niveau des autres formations de cette passe : **aucun
contenu de cryptographie appliquée n'est promu `PACKAGE_COMPLETE` sans
revue réelle par un cryptographe nommé** — même un code réel et
fonctionnel ne constitue pas une preuve de sécurité sans cette revue.
Ce même principe a déjà été appliqué à FRK-10 (EUDI/eIDAS2) et FRK-14
(chaîne de custody) dans les passes précédentes — FRK-73 clôt les
trois exceptions `NEEDS_EXPERT_REVIEW` identifiées dans le corpus
FREK complet (75/75).

## Ce qu'une levée du statut exigerait

1. Un cryptographe réel, nommé, avec ses qualifications déclarées.
2. Une revue documentée de la chaîne de dérivation, du schéma de
   signature, et de la résistance aux classes d'attaques pertinentes.
3. Une distinction explicite, dans cette revue, entre « ce que les 16
   tests fonctionnels de FRK-75 prouvent » et « ce que la revue de
   sécurité elle-même établit » — les deux ne se substituent jamais
   l'un à l'autre.
4. Une mise à jour explicite de ce fichier et de `REFERENTIAL.md`
   confirmant la levée — jamais une promotion silencieuse.

## Status

`STATUS = MODULE_CONTENT_DRAFTED` — package de support complet (8/8
fichiers), mais `REFERENTIAL.md` reste inchangé : `NEEDS_EXPERT_REVIEW`
non levé. Ne jamais promouvoir en `PACKAGE_COMPLETE` sans revue
humaine réelle documentée par un cryptographe nommé.
