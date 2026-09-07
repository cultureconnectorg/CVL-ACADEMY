# KOR-12 — M09 — Comprendre les systèmes de recommandation (concept)

```
MODULE_ID: KOR12-M09
COMPETENCY_ID: C9 — Comprendre les systèmes de recommandation sans en fabriquer un réel pour KORA
PREREQUISITES: M08
ASSESSMENT_LEVEL: N1
KORA_DEPENDENCY: aucune ; CVLN Brain (`registry.py`, événement `academy.certification.passed`) existe pour la certification Academy, jamais pour la recommandation KORA — `CAPABILITY_NOT_CONNECTED`
ROLE_BOUNDARIES: toute affirmation qu'un moteur de recommandation KORA existe aujourd'hui, ou que Brain l'alimente, est éliminatoire à ce niveau de formation
FREK_PROOF_MAPPING: READY_FOR_FREK_PROOF = FALSE
ORIGIN: net-new
```

## Situation professionnelle

Naïma demande si un système de recommandation aiderait *Rasin* à
trouver un public plus large — Fabiola doit répondre au niveau des
principes, sans jamais laisser croire qu'un tel système existe déjà
côté KORA.

## Objectifs d'apprentissage

- Comprendre les principes d'un système de recommandation (filtrage
  par contenu vs collaboratif).
- Confirmer explicitement qu'aucun système de ce type n'existe dans ce
  repo pour KORA.

## Notions essentielles

Les **principes** couvrent le filtrage collaboratif, le filtrage par
contenu, et les approches hybrides — à un niveau conceptuel, de
marché. Le pôle réel `CVLN Brain` (`registry.py`, événement
`academy.certification.passed`) existe pour la **certification
Academy**, jamais comme moteur de recommandation KORA —
`CAPABILITY_NOT_CONNECTED`, une distinction à ne jamais brouiller.

## Méthode

1. Présenter les principes des systèmes de recommandation au niveau
   conceptuel.
2. Vérifier explicitement l'absence de tout système réel côté KORA
   dans ce repo.
3. Distinguer clairement Brain (certification) de tout moteur de
   recommandation KORA (inexistant).

## Exemples

Une note explique le filtrage par contenu (recommander des épisodes
aux thèmes similaires) et le filtrage collaboratif (recommander ce que
des auditeurs similaires ont aimé), tout en confirmant qu'aucun des
deux n'est implémenté pour KORA aujourd'hui. À l'inverse, affirmer que
"Brain alimente déjà des recommandations pour *Rasin*" parce que Brain
existe dans le repo confondrait un événement de certification Academy
avec un moteur de recommandation KORA — une capacité qui n'existe pas.

## Cas

Épisode D — Naïma demande si un système de recommandation aiderait
*Rasin* à trouver un public plus large (`case/CASE.md`).

## Erreurs fréquentes

- Affirmer qu'un moteur de recommandation KORA existe aujourd'hui.
- Affirmer que Brain alimente des recommandations KORA en temps réel.
- Présenter les principes de recommandation sans jamais confirmer
  l'absence de système réel.

## Activité

Présentation conceptuelle des principes de recommandation (contenu,
collaboratif, hybride).

## Exercice

Rédiger une note expliquant ce qu'un système de recommandation
pourrait apporter en principe, et confirmant qu'aucun n'existe
aujourd'hui côté KORA.

## Livrable

Note conceptuelle (`EVIDENCE_TYPE = RECOMMENDATION_CONCEPT_NOTE`).

## Critères de réussite

- Les principes sont présentés correctement à un niveau conceptuel.
- L'absence de système réel côté KORA est confirmée explicitement.
- Brain n'est jamais présenté comme un moteur de recommandation KORA.

## Preuve

Note conceptuelle, `READY_FOR_FREK_PROOF = FALSE`.

## Auto-évaluation

*Ma note confirme-t-elle explicitement qu'aucun système de
recommandation KORA n'existe, ou ai-je laissé planer une ambiguïté ?*

## Passage au module suivant

Si un tel système existait un jour, ses biais potentiels devraient
être anticipés — traité en M10.
