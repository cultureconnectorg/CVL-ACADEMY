# KLT-06 — Modèle pédagogique de certification

```
Même distinction que les formations précédentes : ACADEMY_CERTIFICATION
!= RNCP_OR_STATE_CERTIFICATION. Mise à jour 2026-09-07 : COUVERTURE =
COMPLÈTE (7/7 compétences, C5/C6 reclassifiées BUILT). Aucun badge
n'existe — KLT-06 est une formation NEW, sans legacy, contrairement à
KLT-01→05.
```

| | `ACADEMY_CERTIFICATION` | `RNCP_OR_STATE_CERTIFICATION` |
|---|---|---|
| Statut aujourd'hui | Réelle et **complète** (7/7), dès `KLT06-A01` mené | Inexistante — aucune calibration RNCP disponible pour ce métier `NEW` dans ce repo |
| Ce qu'elle prouve | `C1`-`C7` | N/A |
| Ce qu'elle ne prouve pas | Une connexion **live** Academy↔Observatory réel (`FULLY_COMPLETE` reste `FALSE`, voir `QUALITY_GATES.md`) | N/A |

## Badge

**Aucun badge n'existe pour `KLT-06`.** Contrairement à `KLT-01`→`05`,
qui héritent chacune d'un `badge_name` legacy maintenu en `DISPLAY_ONLY_
LEGACY`, `KLT-06` n'a aucun équivalent legacy (`KLT-0001` §1, confirmé
zéro trace dans `seed_data.py`). Un badge éventuel resterait à créer
dans un futur ticket — non anticipé ici.

## Ce que la certification prouve — et ce qu'elle ne prouve pas

Elle certifie le métier complet d'Analyste Observatory tel que
buildable dans Academy (7/7 compétences, y compris `C5`/`C6` sur la
base du schéma réel vérifié de l'Observatory Kiltikonet). Elle **ne
prouve pas** que le candidat a interrogé une donnée Observatory réelle
en direct — aucun client Academy↔Kiltikonet-Aout2026 n'existe
aujourd'hui ; tout exercice `C5`/`C6` reste `PEDAGOGICAL_ILLUSTRATIVE`.

## Historique — ce qui a changé le 2026-09-07

Avant cette date, `C5`/`C6` étaient `BLOCKED` (`Observatory
NOT_CONNECTED`) faute de savoir si un tel système existait. Une
re-vérification, explicitement autorisée par le Founder, a confirmé
l'existence d'un système Observatory réel dans
`cultureconnectorg/Kiltikonet-Aout2026` — voir
`KLT_09_20_RECONCILIATION.md` §Re-vérification (2026-09-07). `C5`/`C6`
ont alors été construites sur ce schéma réel vérifié, sans jamais
fabriquer une connexion live qui n'existe pas.
