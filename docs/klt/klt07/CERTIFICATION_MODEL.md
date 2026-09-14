# KLT-07 — Modèle pédagogique de certification

```
Même distinction que les formations précédentes : ACADEMY_CERTIFICATION
!= RNCP_OR_STATE_CERTIFICATION. Mise à jour 2026-09-07 : COUVERTURE =
COMPLÈTE (7/7 compétences, C4 reclassifiée BUILT_UNCONNECTED). Aucun
badge n'existe — KLT-07 est une formation NEW, sans legacy.
```

| | `ACADEMY_CERTIFICATION` | `RNCP_OR_STATE_CERTIFICATION` |
|---|---|---|
| Statut aujourd'hui | Réelle et **complète** (7/7), dès `KLT07-A01` mené | Inexistante — aucune calibration RNCP disponible pour ce métier `NEW` dans ce repo |
| Ce qu'elle prouve | `C1`-`C7` | N/A |
| Ce qu'elle ne prouve pas | Une connexion **live** Academy↔Network réel (`FULLY_COMPLETE` reste `FALSE`, voir `QUALITY_GATES.md`) | N/A |

## Badge

**Aucun badge n'existe pour `KLT-07`.** Contrairement à `KLT-01`→`05`,
`KLT-07` n'a aucun équivalent legacy (`KLT-0001` §1, confirmé zéro trace
dans `seed_data.py`). Un badge éventuel resterait à créer dans un futur
ticket — non anticipé ici.

## Ce que la certification prouve — et ce qu'elle ne prouve pas

Elle certifie le métier complet de Responsable déploiement territorial
tel que buildable dans Academy (7/7 compétences, y compris `C4` sur la
base du schéma réel vérifié du Network Kiltikonet). Elle **ne prouve
pas** que le candidat a interrogé une donnée Network réelle en direct —
aucun client Academy↔Kiltikonet-Aout2026 n'existe aujourd'hui ; tout
exercice `C4` reste `PEDAGOGICAL_ILLUSTRATIVE`. Elle ne prouve pas non
plus de savoir concevoir à la place d'une association son propre modèle
de gouvernance (`KLT-04`/M11 reste distinct, voir §Frontière).

## Historique — ce qui a changé le 2026-09-07

Avant cette date, `C4` était `BLOCKED` (`Network NOT_CONNECTED`) faute
de savoir si un tel système existait. Une re-vérification,
explicitement autorisée par le Founder, a confirmé l'existence d'un
système Network réel dans `cultureconnectorg/Kiltikonet-Aout2026` — voir
`KLT_09_20_RECONCILIATION.md` §Re-vérification (2026-09-07). `C4` a
alors été construite sur ce schéma réel vérifié, sans jamais fabriquer
une connexion live qui n'existe pas.
