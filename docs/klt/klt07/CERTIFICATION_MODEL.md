# KLT-07 — Modèle pédagogique de certification (partiel)

```
Même distinction que les formations précédentes : ACADEMY_CERTIFICATION
!= RNCP_OR_STATE_CERTIFICATION. Discipline propre à KLT-07 : COUVERTURE
= PARTIELLE (6/7 compétences). Aucun badge n'existe — KLT-07 est une
formation NEW, sans legacy.
```

| | `ACADEMY_CERTIFICATION` (partielle) | `RNCP_OR_STATE_CERTIFICATION` |
|---|---|---|
| Statut aujourd'hui | Réelle mais **partielle**, dès `KLT07-A01` mené | Inexistante — aucune calibration RNCP disponible pour ce métier `NEW` dans ce repo |
| Ce qu'elle prouve | `C1`-`C3`, `C5`-`C7` uniquement | N/A |
| Ce qu'elle ne prouve pas | `C4` (`BLOCKED`, Network non connecté) | N/A |

## Badge

**Aucun badge n'existe pour `KLT-07`.** Contrairement à `KLT-01`→`05`,
`KLT-07` n'a aucun équivalent legacy (`KLT-0001` §1, confirmé zéro trace
dans `seed_data.py`). Un badge éventuel resterait à créer dans un futur
ticket, une fois la formation complète (`C4` débloquée) — non anticipé
ici.

## Ce que la certification partielle ne fait pas

Elle ne prétend pas certifier le métier complet de Responsable
déploiement territorial — seulement les 6 compétences réellement
construites. Un candidat certifié `KLT07-A01` ne peut pas se prévaloir
de savoir suivre l'état réel de couverture territoriale du réseau, ni
concevoir à la place d'une association son propre modèle de gouvernance.

## Préparation future — ce qui n'existe pas encore

`SKILL_PROOF` (le registre `skills/SKILL_ID_REGISTRY.md` pose la
structure des 7 compétences, `STATUS = PROPOSED`, mais seules 6 ont une
évaluation réelle), `CERTIFICATION` complète (ce document, actuellement
partiel), un badge (aucun n'existe). Rien de tout cela n'est construit
au-delà de sa documentation dans ce ticket.
