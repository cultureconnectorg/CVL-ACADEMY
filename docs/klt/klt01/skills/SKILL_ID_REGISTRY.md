# KLT-01 — Registre de Skill IDs

```
NAMESPACE: KLT01.SKILL.xxx — distinct du namespace FMS (FMSxx-Ay).
Aucun ID FMS réutilisé, aucune collision de forme (FMS = "FMS01-A1" ;
KLT = "KLT01.SKILL.C01"). Ce registre est un document — il ne crée
aucune donnée en base (NO_DB_MUTATION) et n'est lu par aucun code
aujourd'hui.
```

Chaque Skill ID pointe vers exactement une compétence, un module, un
mode d'évaluation, et une preuve — condition posée par le Founder
(KLT-0004 §11).

| Skill ID | Compétence | Module | Assessment | Evidence |
|---|---|---|---|---|
| `KLT01.SKILL.C01` | Lire et diagnostiquer un territoire/public | M01 | N1 (`Q-N1-01`, `Q-N1-03`) | Note personnelle + carte des rôles |
| `KLT01.SKILL.C02` | Comprendre le patrimoine et les codes culturels | M02 | N1 (`Q-N1-02`) | 5 fiches patrimoine sourcées |
| `KLT01.SKILL.C03` | Identifier, qualifier, catégoriser, relier, prioriser les acteurs | M03 | N1/N2 (`Q-N1-10`, `E-N2-03`) | Cartographie d'acteurs qualifiée |
| `KLT01.SKILL.C04` | Concevoir un dispositif de médiation | M04 | N2 (`E-N2-01`, `E-N2-04`) | Fiche action complète |
| `KLT01.SKILL.C05` | Animer/faciliter un groupe avec posture appropriée | M05 | N2 (`Q-N1-12`, `E-N2-02`) | Grille d'animation + posture |
| `KLT01.SKILL.C06` | Mobiliser des médias et outils de médiation | M06 | N2 (`E-N2-08`) | Support de médiation produit |
| `KLT01.SKILL.C07` | Naviguer l'interculturel avec éthique, arbitrer sans folkloriser | M07 | N2 (`Q-N1-08`, `Q-N1-09`, `E-N2-02`, `E-N2-07`) | Note d'arbitrage |
| `KLT01.SKILL.C08` | Adapter la médiation à un public jeune | M08 | N2 (`Q-N1-06`, `E-N2-01`) | Atelier conduit + retour |
| `KLT01.SKILL.C09` | Adapter la médiation à un public senior / recueil mémoire orale | M09 | N2 (`Q-N1-07`, `E-N2-06`) | Interview transcrite + consentement |
| `KLT01.SKILL.C10` | Documenter et produire une preuve exploitable | M10 | N2/N3 (`Q-N1-11`, `Q-N1-14`, `E-N2-06`) | Registre de preuves |
| `KLT01.SKILL.C11` | Conduire une médiation de bout en bout et la défendre | M11 | N3 (`KLT01-A01`) | Dossier de certification + soutenance |

## Statut

`STATUS = PROPOSED` — ce registre n'existe dans aucune base de données
aujourd'hui (`NO_DB_MUTATION`, `NO_RUNTIME_BINDING`). Il documente la
forme que prendrait un futur registre `db.klt_skills` (ou équivalent),
sur le modèle de l'extraction canonique déjà réelle côté FMS
(`fms_canonical/read_model.py`), sans réutiliser son code ni ses
identifiants.

## Différence explicite avec FMS

FMS utilise `FMSxx-Ay` (une lettre = un bloc de compétence, un chiffre =
un niveau, format court hérité de la certification A01-shaped). KLT
utilise `KLTxx.SKILL.Cnn` (plus long, plus explicite) — un choix
délibéré pour ne jamais risquer une collision visuelle ou une confusion
d'origine avec un ID FMS réel dans les logs ou l'UI future.
