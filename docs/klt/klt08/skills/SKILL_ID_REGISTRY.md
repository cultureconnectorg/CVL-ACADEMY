# KLT-08 — Registre de Skill IDs

```
NAMESPACE: KLT08.SKILL.xxx. STATUS = PROPOSED, aucune donnée en base.
Mise à jour 2026-09-07 : C4 reclassifiée `BUILT_UNCONNECTED` après
re-vérification — le Network Kiltikonet réel porte des collections de
conformité réelles, et autorisation Founder scopée. 7/7 compétences
désormais construites (structurellement complètes) ; voir
`klt_canonical/models.py` (backend) pour la distinction exacte entre
`BUILT`, `BUILT_UNCONNECTED` et `BLOCKED`.
```

| Skill ID | Compétence | Module | Assessment | Evidence | Statut |
|---|---|---|---|---|---|
| `KLT08.SKILL.C01` | Distinguer audit d'association et audit réseau | M01 | N1 (`Q-N1-01`, `Q-N1-02`) | Note de cadrage échelle | `BUILT` |
| `KLT08.SKILL.C02` | Concevoir une grille d'audit réseau héritée de `KLT-04`/M13 | M02 | N1 (`Q-N1-03`), N2 (`E-N2-01`) | Grille d'audit réseau | `BUILT` |
| `KLT08.SKILL.C03` | Consolider des audits individuels en une vue réseau | M03 | N1 (`Q-N1-04`, `Q-N1-05`), N2 (`E-N2-02`) | Vue consolidée réseau | `BUILT` |
| `KLT08.SKILL.C04` | Suivre l'état réel de conformité réseau agrégé | M04 | N1 (`Q-N1-11`, `Q-N1-12`), N2 (`E-N2-06`) | Fiche de suivi de conformité | `BUILT_UNCONNECTED` |
| `KLT08.SKILL.C05` | Former des opérateurs aux exigences de conformité | M05 | N1 (`Q-N1-06`), N2 (`E-N2-03`) | Support de formation opérateurs | `BUILT` |
| `KLT08.SKILL.C06` | Recommander sans décider — discipline d'audit réseau | M06 | N1 (`Q-N1-07`, `Q-N1-08`), N2 (`E-N2-04`) | Note de recommandations | `BUILT` |
| `KLT08.SKILL.C07` | Documenter et escalader une non-conformité réseau | M07 | N1 (`Q-N1-09`, `Q-N1-10`), N2 (`E-N2-05`), N2/N3 (`KLT08-A01`) | Rapport de non-conformité réseau | `BUILT` |

Namespace distinct de FMS et des autres formations KLT — vérifié sans
collision.

## Note sur `C4` — `BUILT_UNCONNECTED`, schéma réel, jamais une connexion live

`KLT08.SKILL.C04` est construite sur le schéma réel vérifié du Network
Kiltikonet (`backend/routes/network.py`, endpoints `/compliance`,
`/audits`, repo `cultureconnectorg/Kiltikonet-Aout2026`) — jamais
présentée comme une requête live sur des données réelles qu'Academy ne
peut pas interroger aujourd'hui (`NOT_CONNECTED_TO_ACADEMY_RUNTIME`). Le
statut `BUILT_UNCONNECTED` (distinct de `BUILT` et de `BLOCKED`) porte
précisément cette nuance dans le runtime canonique.
