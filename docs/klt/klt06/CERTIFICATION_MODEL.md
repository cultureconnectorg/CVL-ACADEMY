# KLT-06 — Modèle pédagogique de certification (partiel)

```
Même distinction que les formations précédentes : ACADEMY_CERTIFICATION
!= RNCP_OR_STATE_CERTIFICATION. Discipline propre à KLT-06 :
COUVERTURE = PARTIELLE (5/7 compétences). Aucun badge n'existe — KLT-06
est une formation NEW, sans legacy, contrairement à KLT-01→05.
```

| | `ACADEMY_CERTIFICATION` (partielle) | `RNCP_OR_STATE_CERTIFICATION` |
|---|---|---|
| Statut aujourd'hui | Réelle mais **partielle**, dès `KLT06-A01` mené | Inexistante — aucune calibration RNCP disponible pour ce métier `NEW` dans ce repo |
| Ce qu'elle prouve | `C1`-`C4`, `C7` uniquement | N/A |
| Ce qu'elle ne prouve pas | `C5`, `C6` (`BLOCKED`, Observatory non connecté) | N/A |

## Badge

**Aucun badge n'existe pour `KLT-06`.** Contrairement à `KLT-01`→`05`,
qui héritent chacune d'un `badge_name` legacy maintenu en `DISPLAY_ONLY_
LEGACY`, `KLT-06` n'a aucun équivalent legacy (`KLT-0001` §1, confirmé
zéro trace dans `seed_data.py`). Un badge éventuel resterait à créer
dans un futur ticket, une fois la formation complète (`C5`/`C6`
débloquées) — non anticipé ici.

## Ce que la certification partielle ne fait pas

Elle ne prétend pas certifier le métier complet d'Analyste Observatory —
seulement les 5 compétences réellement construites. Un candidat certifié
`KLT06-A01` ne peut pas se prévaloir de savoir construire un tableau de
bord sur des données Observatory réelles ni interpréter des signaux
territoriaux réels.

## Préparation future — ce qui n'existe pas encore

`SKILL_PROOF` (le registre `skills/SKILL_ID_REGISTRY.md` pose la
structure des 7 compétences, `STATUS = PROPOSED`, mais seules 5 ont une
évaluation réelle), `CERTIFICATION` complète (ce document, actuellement
partiel), un badge (aucun n'existe). Rien de tout cela n'est construit
au-delà de sa documentation dans ce ticket.
