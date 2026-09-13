# FRK-28 — Assessment & Rubric

## Exercice

Le candidat conçoit un registre d'événements de provenance
(append-only, horodaté, chaîné) pour un cas marché-général, puis
rédige une note expliquant précisément pourquoi `events.py`
(`academy.certification.passed`) ne peut pas servir de fondation à ce
registre sans réécriture complète.

## Compétences évaluées

| ID | Compétence |
|---|---|
| C1 | Concevoir un registre append-only et chaîné, techniquement, pas seulement documentairement. |
| C2 | Distinguer précisément un bus pub/sub en mémoire d'un registre de provenance persistant. |
| C3 | Concevoir un mécanisme de correction par événement compensatoire, jamais par réécriture. |

## Grille (0–4)

| Niveau | Critère |
|---|---|
| 0 | Confond `events.py` avec un registre de provenance. |
| 1 | Distingue les deux en théorie, registre non append-only. |
| 2 | Registre append-only, chaînage absent. |
| 3 | Registre append-only et chaîné, correct. |
| 4 | Niveau 3 + frontière `events.py` explicite et correcte + mécanisme de correction par événement compensatoire. |

**Règle éliminatoire :** proposer un registre mutable, présenter
`events.py` comme un registre de provenance existant, ou proposer de
modifier/supprimer un événement erroné directement.

**Seuil de passage :** ≥2.5/4.
