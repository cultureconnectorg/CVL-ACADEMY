# KLT-07 — Registre de Skill IDs

```
NAMESPACE: KLT07.SKILL.xxx. STATUS = PROPOSED, aucune donnée en base.
Mise à jour 2026-09-07 : C4 reclassifiée `BUILT_UNCONNECTED` après
re-vérification du système Network réel (Kiltikonet-Aout2026) et
autorisation Founder scopée — un module et un contenu réels existent,
mais Academy n'a aucune connexion live vers ce système externe. 7/7
compétences désormais construites (structurellement complètes) ; voir
`klt_canonical/models.py` (backend) pour la distinction exacte entre
`BUILT`, `BUILT_UNCONNECTED` et `BLOCKED`.
```

| Skill ID | Compétence | Module | Assessment | Evidence | Statut |
|---|---|---|---|---|---|
| `KLT07.SKILL.C01` | Comprendre l'écosystème territorial Kiltikonet | M01 | N1 (`Q-N1-01`, `Q-N1-02`) | Note de cadrage écosystème | `BUILT` |
| `KLT07.SKILL.C02` | Distinguer déploiement réseau et gouvernance associative | M02 | N1 (`Q-N1-03`), N2 (`E-N2-01`) | Note de frontière | `BUILT` |
| `KLT07.SKILL.C03` | Structurer l'onboarding d'un opérateur territorial | M03 | N1 (`Q-N1-04`, `Q-N1-05`), N2 (`E-N2-02`) | Dossier d'onboarding | `BUILT` |
| `KLT07.SKILL.C04` | Suivre l'état réel de couverture territoriale | M04 | N1 (`Q-N1-11`, `Q-N1-12`), N2 (`E-N2-06`) | Fiche de suivi de couverture | `BUILT_UNCONNECTED` |
| `KLT07.SKILL.C05` | Gérer une relation opérateur au quotidien | M05 | N1 (`Q-N1-06`, `Q-N1-07`), N2 (`E-N2-03`) | Journal de relation opérateur | `BUILT` |
| `KLT07.SKILL.C06` | Évaluer la faisabilité d'une extension territoriale | M06 | N1 (`Q-N1-08`, `Q-N1-09`), N2 (`E-N2-04`) | Note de faisabilité | `BUILT` |
| `KLT07.SKILL.C07` | Documenter et remonter un incident de déploiement | M07 | N1 (`Q-N1-10`), N2 (`E-N2-05`), N2/N3 (`KLT07-A01`) | Rapport d'incident réseau | `BUILT` |

Namespace distinct de FMS et des autres formations KLT — vérifié sans
collision.

## Note sur `C4` — `BUILT_UNCONNECTED`, schéma réel, jamais une connexion live

`KLT07.SKILL.C04` est construite sur le schéma réel vérifié du Network
Kiltikonet (`backend/routes/network.py`, repo
`cultureconnectorg/Kiltikonet-Aout2026`) — jamais présentée comme une
requête live sur des données réelles qu'Academy ne peut pas interroger
aujourd'hui (`NOT_CONNECTED_TO_ACADEMY_RUNTIME`). Le statut
`BUILT_UNCONNECTED` (distinct de `BUILT` et de `BLOCKED`) porte
précisément cette nuance dans le runtime canonique.
