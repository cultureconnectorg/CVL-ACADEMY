# KLT-13 — Modèle de certification

```
Même modèle que les formations KLT précédentes. Formation NEW,
construite complète dès le départ (5/5 compétences).
```

## Couverture

Évaluation Academy **complète** (5/5 compétences, `C1`-`C5`). Niveaux
N1 (banque de questions), N2 (évaluations de décision/application), et
un assessment terminal N2/N3 `KLT13-A01` (module M05).

## Ce que la certification atteste — et ce qu'elle n'atteste pas

Atteste la capacité à concevoir, spécifier et opérer un dispositif
d'accréditation terrain rigoureux, en s'appuyant honnêtement sur un
précédent réel cross-écosystème et en documentant tout ce qui n'est pas
encore implémenté. **N'atteste pas** l'existence ou l'usage d'un système
NFC réel (aucun n'existe), ni d'une connexion à un système Kiltikonet de
contrôle d'accès (aucun n'existe non plus). N'atteste pas la médiation
(`KLT-01`), la gestion budgétaire (`KLT-02`), la représentation
institutionnelle (`KLT-03`), la gouvernance (`KLT-04`), ni le protocole
badge/scan générique de `KLT-05`/M04, qui reste distinct.

## Badge et reconnaissance externe

**Aucun badge existant** pour `KLT-13` — formation nouvelle, sans
équivalent legacy. Ni RNCP, ni équivalence professionnelle externe
établie à ce stade.

## `FULLY_COMPLETE`

`TRUE` — aucune compétence de cette formation ne dépend d'un système
externe non connecté (contrairement à `KLT-06/07/08`), donc ce champ se
calcule honnêtement à `TRUE` dès la construction (même dérivation que
`KLT-01→05`). Ceci ne dit rien de l'import en base `db.formations`, qui
reste `NO_RUNTIME_BINDING_YET` — une question distincte, jamais confondue
avec `fully_complete`. Voir `INTEGRATION_ACADEMY_PACKAGE_NOTE.md`.
