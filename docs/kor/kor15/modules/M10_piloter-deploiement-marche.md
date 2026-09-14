# KOR-15 — M10 — Piloter un déploiement marché

```
MODULE_ID: KOR15-M10
COMPETENCY_ID: C10 — Piloter un déploiement marché
PREREQUISITES: M09
ASSESSMENT_LEVEL: N2, E-N2-04
KORA_DEPENDENCY: aucune
ROLE_BOUNDARIES: un playbook qui programme le déploiement sans condition sur la clarification des droits (M05) échoue ce critère
NEEDS_EXPERT_REVIEW: TRUE (réglementation locale réelle)
FREK_PROOF_MAPPING: READY_FOR_FREK_PROOF = FALSE
ORIGIN: net-new
```

## Situation professionnelle

Nadège doit construire le playbook de déploiement test pour le marché
Caraïbe (Rézo Radyo Kreyòl), en intégrant toutes les étapes
précédentes — et en respectant la condition bloquante posée en M05.

## Objectifs d'apprentissage

- Construire un playbook de déploiement intégrant stratégie, analyse,
  localisation, droits et partenariats.
- Respecter la réglementation locale sans s'y substituer.

## Notions essentielles

Un **playbook** structure les conditions préalables (droits clarifiés),
le séquencement, les jalons et les critères d'arrêt/poursuite. Rappel :
`NEEDS_EXPERT_REVIEW = TRUE` — ce module ne remplace aucune expertise
juridique/réglementaire locale réelle.

## Méthode

1. Vérifier que la condition de M05 (clarification des droits) est
   explicitement posée comme jalon.
2. Séquencer les jalons du déploiement.
3. Définir les critères d'arrêt/poursuite.

## Exemples

Un playbook qui inscrit "clarification `KOR-07` obtenue" comme jalon
explicite de type go/no-go avant que le lancement Caraïbe ne procède
respecte la discipline. À l'inverse, un playbook qui séquence le
lancement sur une date calendaire fixe, indépendamment de l'arrivée ou
non de la clarification des droits, ignorerait entièrement la condition
bloquante posée en M05.

## Cas

Épisode E — playbook de déploiement test pour le marché Caraïbe (Rézo
Radyo Kreyòl), conditionné à la clarification des droits (M05)
(`case/CASE.md`).

## Erreurs fréquentes

- Programmer le déploiement sans condition explicite sur la
  clarification des droits (M05).
- Prétendre remplacer une expertise réglementaire locale réelle par le
  contenu de ce module.
- Omettre les critères d'arrêt/poursuite, rendant le playbook
  irréversible en cas de problème.

## Activité

Vérifier l'état de la clarification des droits (M05) avant de
séquencer.

## Exercice

Produire le playbook de déploiement.

## Livrable

Playbook (`EVIDENCE_TYPE = MARKET_DEPLOYMENT_PLAYBOOK`).

## Critères de réussite

- La condition M05 est un jalon explicite go/no-go.
- Le séquencement reste réaliste.
- Les critères d'arrêt/poursuite sont définis.

## Preuve

Playbook, `READY_FOR_FREK_PROOF = FALSE`.

## Auto-évaluation

*Mon playbook conditionne-t-il réellement le déploiement à la
clarification des droits, ou l'ai-je programmé indépendamment ?*

## Passage au module suivant

Le marché Caraïbe n'est qu'un des marchés en parallèle — la
coordination multi-territoire est traitée en M11.
