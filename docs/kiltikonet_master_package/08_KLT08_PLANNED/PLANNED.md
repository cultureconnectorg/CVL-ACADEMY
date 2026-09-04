# 08 — KLT-08 — Responsable qualité, conformité & audit réseau

```
STATUS = PLANNED
REFERENTIAL_STATUS = FROZEN (KLT-0007) — compétences + structure
indicative de modules uniquement, aucun contenu de module.
BUILD_STATUS = NOT_STARTED — aucun module écrit.
```

## Mise à jour — référentiel canonique livré (`KLT-0007`)

Sur autorisation explicite du Founder, un référentiel canonique a été
construit et gelé : `docs/KILTIKONET_KLT0007_KLT08_CANONICAL_
REFERENTIAL.md`. Il examine et résout la frontière avec `KLT-04`/M12-M13
(audit/conformité à l'échelle d'une association vs échelle réseau —
méthode héritée par référence, jamais dupliquée, unité d'analyse et
compétence "formation opérateurs" distinctes) et identifie 7 compétences
(`PROPOSED`), dont **6/7 constructibles dès aujourd'hui** et **1/7
bloquée** (`C4` — suivi de conformité réseau agrégée réelle, `Compliance`
`NOT_IMPLEMENTED`).

**Mise à jour (`KLT-0008`)** : `contexts = [INTERNAL]` décidé — signal
le plus net des trois formations (libellé "pro/interne", voir
`docs/KILTIKONET_KLT0008_KLT06_08_CONTEXT_AND_SCOPE_DECISION.md`) ;
périmètre buildable confirmé = 6/7 compétences (M01-M03, M05-M07). Aucun
module n'est écrit — le build de contenu reste un ticket distinct,
`NOT_AUTHORIZED`.

## Position dans l'architecture globale

Nommé dans `KLT_MASTER_MAP_v1` comme spécialisation pro/interne `NEW`,
priorité `P2`, dépendance nommée : `Compliance / audits / formation
opérateurs`. Seule des trois formations planifiées dont le libellé type
porte explicitement la mention "interne" (`KLT-0001` §3, signal réel
retenu à l'époque).

## Recouvrement à examiner avant construction

Cette formation recouvre potentiellement une compétence déjà construite
dans `KLT-04`/`M13` (Auditer un dispositif de gouvernance — audit
d'association) et `KLT-04`/`M12` (conformité). `KLT-08` porte
vraisemblablement sur un audit à l'échelle **réseau** (plusieurs
opérateurs), pas une seule association — un niveau distinct, mais le
recouvrement de méthode (comment auditer, quelles preuves) est réel et
devra être traité explicitement pour éviter que `KLT-08` ne réécrive
`KLT-04`/`M13` sous un autre nom.

## Ce qui devra être fait avant construction

1. Décision Founder sur le périmètre exact (audit réseau vs audit
   association — déjà couvert par `KLT-04`).
2. Vérifier l'accès aux dépendances `Compliance`/`audits` (statut
   `NOT_IMPLEMENTED` comme donnée structurée en Academy, `KLT-0001` §4).
3. Cadrer explicitement la frontière avec `KLT-04`/`M12`-`M13` avant
   tout référentiel.
