# KOR-09 — M06 — Gérer CRM et notifications

```
MODULE_ID: KOR09-M06
COMPETENCY_ID: C6 — Gérer CRM et notifications
PREREQUISITES: M05
ASSESSMENT_LEVEL: N1
KORA_DEPENDENCY: aucune — outils génériques (tableur) ; un vrai CRM/notifications push à grande échelle = KORA_PRODUCT_GAP, REFERENTIAL.md §6
ROLE_BOUNDARIES: aucune
FREK_PROOF_MAPPING: FREK-WORK
ORIGIN: net-new
```

## Situation professionnelle

Marc-Andy ne garde aucune trace de qui a été contacté, comment, ni
quand — impossible de savoir qui recontacter sans un suivi structuré,
même simple.

## Objectifs d'apprentissage

- Construire un suivi CRM minimal avec des outils génériques.
- Reconnaître la limite d'un CRM manuel à grande échelle sans la
  combler par une fausse capacité.

## Notions essentielles

Un **CRM simplifié** (tableur) suffit à l'échelle actuelle de *Rasin*
(quelques dizaines/centaines de contacts) — au-delà, un vrai système
serait nécessaire, ce qui relève d'un `KORA_PRODUCT_GAP` documenté,
pas d'une solution à fabriquer ici.

## Méthode

1. Construire un tableur de suivi (contact, canal, dernière
   interaction, statut).
2. Définir une règle simple de notification (relance après X jours
   sans interaction).
3. Documenter explicitement la limite d'échelle de cette méthode.

## Exemple

Un tableur avec colonnes (nom, canal, dernière interaction, statut
activé/non activé) suffit pour quelques centaines de contacts — au-delà
de mille, une vraie solution serait nécessaire.

## Cas

Le CRM porte sur les contacts réels du cas (`case/CASE.md`).

## Erreurs fréquentes

- Ne tenir aucun suivi, rendant impossible toute relance ciblée.
- Prétendre qu'un tableur tiendrait à n'importe quelle échelle.

## Activité

Construction du tableur de suivi.

## Exercice

Définir la règle de notification/relance.

## Livrable

CRM simplifié + note de limite d'échelle.

## Critères de réussite

- Le suivi est structuré et actionnable.
- La limite d'échelle est explicitement reconnue.

## Preuve

CRM + note, signal `FREK-WORK`.

## Auto-évaluation

*Mon CRM simplifié tiendrait-il à l'échelle actuelle, et ai-je
reconnu sa limite au-delà ?*

## Passage au module suivant

Ce suivi alimente le travail de rétention traité en M07.
