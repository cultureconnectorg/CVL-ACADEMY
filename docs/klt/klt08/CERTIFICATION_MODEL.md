# KLT-08 — Modèle pédagogique de certification

```
Même distinction que les formations précédentes : ACADEMY_CERTIFICATION
!= RNCP_OR_STATE_CERTIFICATION. Mise à jour 2026-09-07 : COUVERTURE =
COMPLÈTE (7/7 compétences, C4 reclassifiée BUILT_UNCONNECTED). Aucun
badge n'existe — KLT-08 est une formation NEW, sans legacy.
```

| | `ACADEMY_CERTIFICATION` | `RNCP_OR_STATE_CERTIFICATION` |
|---|---|---|
| Statut aujourd'hui | Réelle et **complète** (7/7), dès `KLT08-A01` mené | Inexistante — aucune calibration RNCP disponible pour ce métier `NEW` dans ce repo |
| Ce qu'elle prouve | `C1`-`C7` | N/A |
| Ce qu'elle ne prouve pas | Une connexion **live** Academy↔Network réel (`FULLY_COMPLETE` reste `FALSE`, voir `QUALITY_GATES.md`) | N/A |

## Badge

**Aucun badge n'existe pour `KLT-08`.** Contrairement à `KLT-01`→`05`,
`KLT-08` n'a aucun équivalent legacy (`KLT-0001` §1, confirmé zéro trace
dans `seed_data.py`). Un badge éventuel resterait à créer dans un futur
ticket — non anticipé ici.

## Ce que la certification prouve — et ce qu'elle ne prouve pas

Elle certifie le métier complet de Responsable qualité, conformité &
audit réseau tel que buildable dans Academy (7/7 compétences, y compris
`C4` sur la base du schéma réel vérifié du Network Kiltikonet). Elle
**ne prouve pas** que le candidat a interrogé une donnée de conformité
réelle en direct — aucun client Academy↔Kiltikonet-Aout2026 n'existe
aujourd'hui ; tout exercice `C4` reste `PEDAGOGICAL_ILLUSTRATIVE`. Elle
ne prouve pas non plus de savoir auditer une association isolée sans
référence à la méthode `KLT-04`/M13.

## Historique — ce qui a changé le 2026-09-07

Avant cette date, `C4` était `BLOCKED` (`Compliance NOT_IMPLEMENTED`) —
la classification d'origine estimait qu'aucun système externe de
conformité n'était identifié. Une re-vérification, explicitement
autorisée par le Founder, a trouvé que le Network Kiltikonet réel porte
en fait des collections de conformité réelles
(`network_compliance_records`, `network_audits`) — voir
`KLT_09_20_RECONCILIATION.md` §Re-vérification (2026-09-07). `C4` a
alors été construite sur ce schéma réel vérifié, sans jamais fabriquer
une connexion live qui n'existe pas.
