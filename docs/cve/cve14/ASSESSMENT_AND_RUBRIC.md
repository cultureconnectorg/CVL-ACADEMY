# CVE-14 — Assessment & Rubric

Structure identique à `../cve02/ASSESSMENT_AND_RUBRIC.md` (N1 40% /
N2 30% / livrable 30%, même `../CERTIFICATION_MODEL.md`).

## Compétences évaluées

| Compétence | Description |
|---|---|
| C1 | H0 et principe de clôture, avec exemple concret d'exclusion |
| C2 | C6 comme mécanisme d'application de H0, jamais une exigence séparée |
| C3 | Vérification honnête des écarts d'auditabilité (CVE-06, CVE-08) |

## Rubric (0–4 par compétence)

| Niveau | Description |
|---|---|
| 0 | Valide une quantité non reproductible, traite C6 comme indépendant de H0, ou invente une méthode d'audit pour une quantité non formalisée |
| 1 | Formulation approximative |
| 2 | H0/C6 corrects mais lien entre eux ou vérification d'écarts absente |
| 3 | Complet et vérifié, imprécision mineure tolérée |
| 4 | Cite H0/§6 C6 précisément, lien explicite, écarts CVE-06/08 correctement identifiés |

## Règle éliminatoire

Toute validation d'une quantité non reproductible, ou toute méthode
d'audit inventée pour une quantité non formalisée, entraîne un 0
automatique.

## Seuil de passage

Moyenne ≥ 2.5/4, aucune compétence à 0 par élimination.
