# FRK-14 — Integration Academy Package Note

**Réel :** aucune chaîne de custody CVLN réelle observée ; `issue_proof()`
(`frek_core.py`) est un stub (`PROOF-{uuid.uuid4().hex[:10].upper()}`),
sans chaîne de custody ni horodatage cryptographique.
**Supposé :** `FRK14.SKILL.*` réel — inexistant.

## Dépendances

`FREK_01_75_RECONCILIATION.md`, `docs/frk/frk12/REFERENTIAL.md`
(base commune), `docs/frk/frk15/REFERENTIAL.md` (formation avale,
sequencée après FRK-12/FRK-14).

## Ce que ce package couvre

Les 8 fichiers de support (`BANQUE_N1`, `BANQUE_N2`,
`ASSESSMENT_AND_RUBRIC`, `EVIDENCE_MODEL`, `GUIDE_CANDIDAT`,
`GUIDE_CORRECTEUR`, `GUIDE_JURY`, ce fichier) sont écrits cette passe,
au même niveau de rigueur que les formations promues `PACKAGE_
COMPLETE` de ce corpus.

## Pourquoi le statut reste `MODULE_CONTENT_DRAFTED`

`FRK-14` porte un flag `NEEDS_EXPERT_REVIEW` (forensic/légal-adjacent)
depuis `FREK_01_75_RECONCILIATION.md`. Ceci reste délibérément en
dessous du niveau des autres formations de cette passe : **aucun
contenu de chaîne de custody n'est promu `PACKAGE_COMPLETE` sans revue
réelle par un expert forensic/légal nommé** — le droit de la preuve
varie par juridiction et un gabarit générique ne peut jamais s'y
substituer. Ce même principe a déjà été appliqué à FRK-10 (EUDI/eIDAS2)
dans la passe précédente, et sera appliqué à FRK-73 (cryptographie
appliquée) plus loin dans cette passe.

## Status

`STATUS = MODULE_CONTENT_DRAFTED` — package de support complet (8/8
fichiers), mais `REFERENTIAL.md` reste inchangé : `NEEDS_EXPERT_REVIEW`
non levé. Ne jamais promouvoir en `PACKAGE_COMPLETE` sans revue
humaine réelle documentée.
