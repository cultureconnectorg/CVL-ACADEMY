# Operator Authorization Architecture (future — non implémentée)

```
OPERATOR_AUTHORIZATION = NOT_IMPLEMENTED / NOT_GRANTED aujourd'hui, pour
toutes les formations, sans exception. Ce document décrit l'architecture
FUTURE que le Founder demande de préparer — il ne construit rien.
NO_RUNTIME_BINDING.
```

## Pourquoi ce document existe

`KLT-05` (Opérateur Kiltikonet) est la seule formation dont le métier
cible, à terme, pourrait légitimement conditionner de vrais droits sur
un système Kiltikonet réel — contrairement aux quatre autres formations,
dont aucune n'a de rapport direct avec un accès système. Le Founder
demande de documenter cette architecture future **sans l'implémenter et
sans la simuler**.

## Ce qui existe réellement aujourd'hui

- Un système RBAC est **enseigné** (`KLT-05`/M02) — pas opéré.
- Un protocole de preuve de participation est **conçu** (`KLT-05`/M04) —
  marqué explicitement simulé, non opposable.
- Un badge `Kiltikonet Platform Operator` est **affiché** — jamais
  délivré comme un droit réel (`badge_name = DISPLAY_ONLY_LEGACY`).
- Un critère éliminatoire de `RUBRIC.md` (`KLT-05`, critère 10) **exige**
  que chaque dossier certifié rappelle explicitement l'absence
  d'autorisation réelle.

**Rien de tout cela ne constitue, même partiellement, un mécanisme
d'autorisation.**

## Ce qu'un vrai contrat produit/permissions devrait un jour définir (non construit)

Nommé ici comme architecture cible, pas comme spécification à
implémenter :

| Composant futur | Ce qu'il devrait faire | Dépendance produit réelle requise |
|---|---|---|
| Contrat de rôle Kiltikonet réel | Définir formellement ce qu'un "opérateur certifié KLT-05" peut faire sur un système Kiltikonet réel | `Auth/RBAC` (`INTEGRATION_CONTRACT`, non configuré aujourd'hui) |
| Lien certification → habilitation | Décider si `KLT05-A01` réussi déclenche, ou non, une demande d'habilitation (jamais automatique) | Décision Founder explicite, non prise à ce jour |
| Registre d'habilitations réelles | Distinguer "certifié Academy" de "habilité opérateur" comme deux états séparés et traçables | Une collection dédiée (non `db.user_badges`, qui ne fait pas ça) |
| Révocation | Toute habilitation réelle doit pouvoir être retirée — non pertinent tant qu'aucune n'existe | — |

## Condition de sortie de `NOT_IMPLEMENTED`

Cette architecture ne passe à `IMPLEMENTED` que lorsque **les trois**
conditions suivantes sont réunies, jamais une seule :
1. Un accès réel à `Auth/RBAC` Kiltikonet existe et est configuré.
2. Le Founder prend une décision explicite sur le lien certification →
   habilitation (jamais automatique par défaut).
3. Un ticket dédié construit le registre d'habilitations réel — jamais
   comme sous-produit silencieux d'un ticket de contenu pédagogique.

Tant qu'une seule de ces conditions manque,
`OPERATOR_AUTHORIZATION = NOT_IMPLEMENTED / NOT_GRANTED` reste la seule
affirmation vraie, pour `KLT-05` comme pour les quatre autres
formations.
