# KLT-18 — Modèle de certification

```
Même modèle que les formations KLT précédentes. Formation NEW,
construite complète dès le départ (5/5 compétences).
```

## Couverture

Évaluation Academy **complète** (5/5 compétences, `C1`-`C5`). Niveaux
N1 (banque de questions), N2 (évaluations de décision/application), et
un assessment terminal N2/N3 `KLT18-A01` (module M05).

## Ce que la certification atteste — et ce qu'elle n'atteste pas

Atteste la capacité à concevoir, décliner, piloter en situation de
crise, mesurer honnêtement et restituer stratégiquement une campagne de
communication. **N'atteste pas** l'animation quotidienne d'une
communauté, le traitement de support individuel, ni la lecture de
signaux d'engagement au quotidien — ces compétences restent celles de
`KLT-05`, non dupliquées ici. N'atteste pas la médiation (`KLT-01`), la
gestion budgétaire (`KLT-02`), la représentation institutionnelle
(`KLT-03`), ni la gouvernance (`KLT-04`).

## Badge et reconnaissance externe

**Aucun badge existant** pour `KLT-18` — formation nouvelle, sans
équivalent legacy. Ni RNCP, ni équivalence professionnelle externe
établie à ce stade.

## `FULLY_COMPLETE`

`TRUE` — aucune compétence de cette formation ne dépend d'un système
externe non connecté, donc ce champ se calcule honnêtement à `TRUE` dès
la construction (même dérivation que `KLT-01→05`). Ceci ne dit rien de
l'import en base `db.formations`, qui reste `NO_RUNTIME_BINDING_YET` —
une question distincte, jamais confondue avec `fully_complete`. Voir
`INTEGRATION_ACADEMY_PACKAGE_NOTE.md`.
