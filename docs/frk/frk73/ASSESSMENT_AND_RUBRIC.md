# FRK-73 — Assessment & Rubric

**Statut d'évaluation : formatif seul.** Aucune certification ne peut
être délivrée sur cette formation tant que `NEEDS_EXPERT_REVIEW` n'est
pas levé par un cryptographe réel et nommé.

## Exercice formatif

Le candidat trace la chaîne de dérivation `PUF → HKDF → DRK →
AK/FK/CK` réelle documentée dans `frek_crypto.py`, décrit le format de
signature `r||s`, puis corrige la confusion d'un relecteur qui
prendrait des tests fonctionnels passants pour une preuve de sécurité.

## Compétences formatives évaluées (non certifiantes)

| ID | Compétence |
|---|---|
| C1 | Lire et tracer fidèlement la chaîne de dérivation réelle. |
| C2 | Articuler la discipline de revue experte. |
| C3 | Distinguer conformité fonctionnelle (tests passants) et sécurité cryptographique prouvée. |

## Grille indicative (0–4, usage formatif)

| Niveau | Critère |
|---|---|
| 0 | Invente une étape de dérivation non présente dans le code réel. |
| 1 | Lecture correcte du code, revue experte non mentionnée. |
| 2 | Lecture correcte + mention générale de la nécessité de revue. |
| 3 | Lecture correcte + discipline de revue experte bien articulée. |
| 4 | Niveau 3 + distinction claire entre « code réel » et « sécurité prouvée » + correction de la confusion tests/audit. |

**Règle éliminatoire :** présenter le schéma comme audité/sécurisé
sans réserve, ou inventer une étape de dérivation.

Seuil de passage (si/quand la formation devient certifiante) : ≥2.5/4
— **inapplicable aujourd'hui**, cette formation reste `MODULE_CONTENT_
DRAFTED`.
