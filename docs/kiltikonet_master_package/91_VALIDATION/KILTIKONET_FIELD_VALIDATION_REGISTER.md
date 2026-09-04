# Kiltikonet Field Validation Register

```
Distingue quatre niveaux de validation qu'aucun élément du corpus n'a
encore atteint au-delà du premier.
```

## Les quatre niveaux

| Niveau | Définition | Qui le fait |
|---|---|---|
| `DOCUMENT_VALIDATED` | Le document est structurellement complet, cohérent avec les quality gates de sa formation | **Atteint pour KLT-01→05** — vérifié par les 5 `QUALITY_GATES.md` locaux |
| `EXPERT_VALIDATED` | Un professionnel du métier (médiateur, chef de projet, chargé de partenariats, dirigeant associatif, opérateur plateforme réel) a relu et confirmé le contenu | **Non atteint** — aucune revue experte n'a eu lieu |
| `FIELD_TESTED` | Le contenu a été utilisé avec de vrais candidats/correcteurs/jurys, en conditions réelles ou proches | **Non atteint** |
| `PRODUCTION_VALIDATED` | Le contenu a servi à une vraie certification, avec de vrais enjeux pour le candidat | **Non atteint** |

## État par formation

| KLT | `DOCUMENT_VALIDATED` | `EXPERT_VALIDATED` | `FIELD_TESTED` | `PRODUCTION_VALIDATED` |
|---|---|---|---|---|
| `KLT-01` | ✅ | ❌ | ❌ | ❌ |
| `KLT-02` | ✅ | ❌ | ❌ | ❌ |
| `KLT-03` | ✅ | ❌ | ❌ | ❌ |
| `KLT-04` | ✅ | ❌ | ❌ | ❌ |
| `KLT-05` | ✅ | ❌ | ❌ | ❌ |

**Aucune formation du corpus n'a dépassé `DOCUMENT_VALIDATED`.** C'est
le point que le Founder a explicitement demandé de ne jamais masquer.

## Ce qui devrait être testé, et avec qui

| Rôle à mobiliser | Ce qu'il devrait valider |
|---|---|
| Professionnels en poste (médiateur culturel, chef de projet culturel, chargé de partenariats, dirigeant associatif, community manager plateforme) | Réalisme des situations professionnelles, exactitude des notions métier propres à chaque formation |
| Formateurs | Applicabilité pédagogique des modules, charge de travail réaliste, clarté des consignes |
| Candidats (pilote) | Compréhension réelle des consignes, faisabilité des livrables dans le temps imparti |
| Correcteurs | Applicabilité des critères de réussite module par module sans interprétation arbitraire (déjà visé par les `CORRECTOR_GUIDE.md` locaux, jamais testé en situation réelle) |
| Jurys | Applicabilité de `RUBRIC.md` en délibération réelle, pertinence des questions type proposées dans `JURY_GUIDE.md` |
| Opérateurs Kiltikonet réels (si accessibles) | Spécifique à `KLT-05` — vérifier que le contenu correspond à une vraie pratique opérationnelle, une fois qu'un système réel existe |

## Priorité recommandée (non un ordre imposé)

1. `KLT-01` et `KLT-05` — les deux formations dont un test pilote léger
   (quelques candidats, un correcteur) serait le plus rapide à organiser
   (pas de dépendance institutionnelle/juridique externe bloquante).
2. `KLT-03` et `KLT-04` — nécessitent une revue experte (voir `EXTERNAL_
   VALIDATION_REGISTER.md`) **avant** tout test candidat, pour ne pas
   faire travailler des candidats sur un contenu factuel non vérifié.
3. `KLT-02` — dépendance la plus faible, testable à tout moment.

## Ce que ce registre ne fait pas

N'organise aucun test réel, ne recrute personne, ne planifie aucune
session — c'est un registre de ce qui reste à faire, pas une exécution.
