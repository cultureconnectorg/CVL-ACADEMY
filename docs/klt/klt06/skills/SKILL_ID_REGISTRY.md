# KLT-06 — Registre de Skill IDs

```
NAMESPACE: KLT06.SKILL.xxx. STATUS = PROPOSED, aucune donnée en base.
Mise à jour 2026-09-07 : C5/C6 reclassifiées `BUILT_UNCONNECTED` après
re-vérification du système Observatory réel (Kiltikonet-Aout2026) et
autorisation Founder scopée — un module et un contenu réels existent,
mais Academy n'a aucune connexion live vers ce système externe. 7/7
compétences désormais construites (structurellement complètes) ; voir
`klt_canonical/models.py` (backend) pour la distinction exacte entre
`BUILT`, `BUILT_UNCONNECTED` et `BLOCKED`.
```

| Skill ID | Compétence | Module | Assessment | Evidence | Statut |
|---|---|---|---|---|---|
| `KLT06.SKILL.C01` | Comprendre l'objet et la méthode d'un observatoire | M01 | N1 (`Q-N1-01`, `Q-N1-02`) | Note de cadrage méthode | `BUILT` |
| `KLT06.SKILL.C02` | Évaluer la provenance et la fiabilité d'un signal | M02 | N1 (`Q-N1-03`, `Q-N1-04`), N2 (`E-N2-01`) | Grille de provenance | `BUILT` |
| `KLT06.SKILL.C03` | Formuler une spécification de besoin de données | M03 | N1 (`Q-N1-05`, `Q-N1-06`), N2 (`E-N2-02`) | Fiche de spécification | `BUILT` |
| `KLT06.SKILL.C04` | Éthique et confidentialité des données communautaires | M04 | N1 (`Q-N1-07`, `Q-N1-08`), N2 (`E-N2-03`) | Grille éthique/confidentialité | `BUILT` |
| `KLT06.SKILL.C05` | Construire un tableau de bord sur données Observatory réelles | M05 | N1 (`Q-N1-11`, `Q-N1-12`), N2 (`E-N2-05`) | Maquette de tableau de bord | `BUILT_UNCONNECTED` |
| `KLT06.SKILL.C06` | Interpréter des signaux territoriaux réels | M06 | N1 (`Q-N1-13`), N2 (`E-N2-06`) | Note d'interprétation de signal | `BUILT_UNCONNECTED` |
| `KLT06.SKILL.C07` | Restituer une analyse à un public non spécialiste | M07 | N1 (`Q-N1-09`, `Q-N1-10`), N2 (`E-N2-04`), N2/N3 (`KLT06-A01`) | Support de restitution | `BUILT` |

Namespace distinct de FMS et des autres formations KLT — vérifié sans
collision.

## Note sur `C5`/`C6` — `BUILT_UNCONNECTED`, schéma réel, jamais une connexion live

`KLT06.SKILL.C05` et `KLT06.SKILL.C06` sont construites sur le schéma
réel vérifié de l'Observatory Kiltikonet (`backend/routes/
observatory.py`, `services/observatory_adapters/*`, repo
`cultureconnectorg/Kiltikonet-Aout2026`) — jamais présentées comme une
requête live sur des données réelles qu'Academy ne peut pas interroger
aujourd'hui (`NOT_CONNECTED_TO_ACADEMY_RUNTIME`). Le statut
`BUILT_UNCONNECTED` (distinct de `BUILT` et de `BLOCKED`) porte
précisément cette nuance dans le runtime canonique : un module et un
contenu réels existent (compte comme construit, `structural_status =
COMPLETE`), mais `fully_complete` reste `FALSE` tant qu'aucune connexion
live n'existe.
