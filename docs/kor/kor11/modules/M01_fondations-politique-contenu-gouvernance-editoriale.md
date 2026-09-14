# KOR-11 — M01 — Fondations : politique de contenu et gouvernance éditoriale

```
MODULE_ID: KOR11-M01
COMPETENCY_ID: C1 — Distinguer politique de contenu et gouvernance éditoriale
PREREQUISITES: Aucun
ASSESSMENT_LEVEL: N1
KORA_DEPENDENCY: aucune
ROLE_BOUNDARIES: ce module ne couvre pas la gouvernance FREK (preuve de compétence, `services/frek_core.py`) — tension #13 explicitement écartée
FREK_PROOF_MAPPING: READY_FOR_FREK_PROOF = FALSE — le travail Trust & Safety n'émet aucun signal de preuve créateur
ORIGIN: net-new
```

## Situation professionnelle

Widlène rejoint Anba Tonèl Host comme coordinatrice Trust & Safety,
sans qu'aucune politique de contenu écrite n'existe — chaque décision
de modération s'est faite jusqu'ici au cas par cas, sans règle ni
processus documenté.

## Objectifs d'apprentissage

- Distinguer une politique de contenu (ce qui est publié, interdit,
  restreint) d'une gouvernance éditoriale (qui décide, avec quel
  processus).
- Distinguer les deux de la "gouvernance" FREK (gouvernance de la
  preuve de compétence, sans rapport).

## Notions essentielles

Une **politique de contenu** énonce des règles (interdit, restreint,
autorisé sous condition). Une **gouvernance éditoriale** définit le
processus (qui écrit la politique, qui l'applique, qui l'arbitre en
cas de litige). `services/frek_core.py` gère des preuves de compétence
(`FREK-WORK`, `FREK-SCORE`) — une gouvernance de nature entièrement
différente, jamais à confondre avec la gouvernance éditoriale de
modération.

## Méthode

1. Lister les catégories de contenu (interdit, restreint, autorisé
   sous condition) pertinentes pour Anba Tonèl Host.
2. Définir qui écrit, applique, et arbitre la politique.
3. Vérifier explicitement que la gouvernance éditoriale ainsi définie
   n'est jamais confondue avec la gouvernance FREK.

## Exemples

Une politique interdisant l'incitation à la haine, restreignant le
contenu à caractère violent (avertissement requis), et autorisant sous
condition la nudité artistique (contexte documenté) — trois
traitements distincts pour trois catégories réelles. À l'inverse,
présenter la politique de contenu comme "gérée par le même mécanisme
que les preuves FREK" laisserait croire à un lien qui n'existe pas —
la gouvernance éditoriale (ce module) et la gouvernance FREK
(`services/frek_core.py`) n'ont ni le même objet ni le même mécanisme.

## Cas

La politique porte sur Anba Tonèl Host réellement (`case/CASE.md`) —
module fondation, non encore appliqué à un épisode précis.

## Erreurs fréquentes

- Confondre politique de contenu (les règles) et gouvernance
  éditoriale (le processus de décision).
- Laisser croire que la gouvernance éditoriale de modération est liée
  à la gouvernance FREK.
- Rédiger une politique de contenu sans processus d'arbitrage associé,
  laissant chaque décision au hasard du modérateur du moment.

## Activité

Analyse comparative de politiques de contenu existantes (génériques,
hors CVLN) pour identifier la structure type.

## Exercice

Rédiger une politique de contenu courte (5 règles) pour Anba Tonèl
Host, avec un processus de gouvernance éditoriale associé (qui décide
en cas de doute).

## Livrable

Note de politique (`EVIDENCE_TYPE = POLICY_NOTE`).

## Critères de réussite

- La politique distingue clairement interdit/restreint/autorisé sous
  condition.
- Le processus de gouvernance éditoriale est explicite (qui écrit,
  applique, arbitre).
- Aucune confusion avec la gouvernance FREK n'est introduite.

## Preuve

Note de politique, signal `READY_FOR_FREK_PROOF = FALSE` — aucun
signal FREK n'est émis par ce module.

## Auto-évaluation

*Ma politique et mon processus de gouvernance sont-ils clairement
distincts, ou ai-je laissé planer une confusion avec la gouvernance
FREK ?*

## Passage au module suivant

Cette politique cadre le recueil et le tri des signalements traité en
M02.
