# KOR-06 — M05 — Définir un SLA/SLO et la qualité de service

```
MODULE_ID: KOR06-M05
COMPETENCY_ID: C5 — Définir un SLA/SLO et la qualité de service
PREREQUISITES: M04
ASSESSMENT_LEVEL: N2
KORA_DEPENDENCY: aucune
ROLE_BOUNDARIES: aucune
FREK_PROOF_MAPPING: FREK-SCORE
ORIGIN: net-new
```

## Situation professionnelle

Anba Tonèl Host n'a jamais formalisé d'engagement de qualité de
service envers ses créateurs hébergés — sans SLA/SLO, aucun seuil
n'existe pour juger si le service est "acceptable" ou non.

## Objectifs d'apprentissage

- Distinguer un SLA (engagement contractuel) d'un SLO (objectif
  interne).
- Fixer des seuils réalistes pour une structure de taille moyenne.

## Notions essentielles

Un **SLO** (objectif de niveau de service) est un objectif interne
("99% de disponibilité"). Un **SLA** (accord de niveau de service) est
un engagement formalisé envers un tiers, avec des conséquences en cas
de non-respect. Fixer un SLA trop ambitieux sans les moyens de le tenir
est pire que ne pas en avoir.

## Méthode

1. Évaluer les moyens réels d'Anba Tonèl Host (infrastructure, équipe).
2. Fixer un SLO réaliste compte tenu de ces moyens.
3. Décider si un SLA formel est tenable, ou si le SLO reste interne
   pour l'instant.

## Exemple

Une disponibilité de 99,5% (environ 3,5h d'indisponibilité par mois)
est réaliste pour une structure moyenne sans infrastructure redondante
complète — promettre 99,99% serait irréaliste sans investissement
majeur.

## Cas

Le SLA/SLO est défini pour Anba Tonèl Host réellement (`case/
CASE.md`), compte tenu de ses moyens réels.

## Erreurs fréquentes

- Fixer un objectif ambitieux sans vérifier les moyens réels de le
  tenir.
- Confondre SLO interne et SLA contractuel.

## Activité

Évaluation des moyens réels d'Anba Tonèl Host.

## Exercice

Rédiger le SLO (et éventuellement un SLA) réaliste.

## Livrable

SLA/SLO documenté.

## Critères de réussite

- Le seuil fixé est cohérent avec les moyens réels évalués.
- La distinction SLA/SLO est correctement appliquée.

## Preuve

SLA/SLO, signal `FREK-SCORE`.

## Auto-évaluation

*Mon seuil est-il réaliste, ou ambitieux au point d'être intenable ?*

## Passage au module suivant

Ce SLA/SLO devient la référence pour juger l'incident géré en M06.
