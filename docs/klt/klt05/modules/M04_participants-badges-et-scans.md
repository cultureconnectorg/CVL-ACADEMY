# KLT-05 — M04 — Participants, badges et scans

```
MODULE_ID: KLT05-M04
COMPETENCY_ID: C4 — Gérer participants, badges et preuves de participation (net-new)
PREREQUISITES: M02
ASSESSMENT_LEVEL: N2
KILTIKONET_DEPENDENCY: Badges/NFC — INTEGRATION_CONTRACT, non configuré (KLT-0001 §4). Aucun système de badge/scan réel n'est utilisé — ce module conçoit un protocole simulé.
ROLE_BOUNDARIES: Concevoir un protocole de preuve simulé n'en fait jamais une preuve opposable réelle — OPERATOR_AUTHORIZATION = NOT_IMPLEMENTED/NOT_GRANTED s'applique aussi ici
FREK_PROOF_MAPPING: FREK-WORK (mapping proposé — aucun signal legacy n'existait, net-new)
ORIGIN: master plan M04 (BUILD_NEW) — thème explicitement demandé par le Founder (KLT-0002)
```

## Situation professionnelle

Une preuve de participation mal gérée compromet toute la chaîne de
confiance qu'un système FREK est censé garantir — même dans un cas
pédagogique, ce module enseigne la rigueur que cette chaîne exigerait en
production.

## Objectifs d'apprentissage

- Concevoir un protocole de preuve de participation (badge, scan) simple
  et rigoureux.
- Distinguer une preuve simulée pédagogique d'une preuve réelle
  opposable.
- Documenter le protocole pour qu'il soit reproductible.

## Notions essentielles

Une **preuve de participation** doit répondre à trois exigences : qui a
participé (identité, même minimale), quand (horodatage), et comment la
preuve peut être vérifiée a posteriori. Un protocole non documenté n'est
pas reproductible, et une preuve non vérifiable n'a pas de valeur, réelle
ou pédagogique.

## Méthode

1. Concevoir un protocole simple (ex. un scan fictif à l'entrée/sortie
   de l'événement).
2. Documenter précisément ce qui est enregistré et comment.
3. Marquer explicitement le protocole comme simulé/pédagogique — jamais
   comme une preuve réellement opposable en dehors de ce cas.

## Exemples

Un "scan" simulé qui enregistre simplement "présence confirmée, horaire,
nom" dans un tableau pédagogique est suffisant pour ce module — il ne
prétend jamais être une preuve cryptographiquement vérifiable ni
connectée à un système FREK réel.

## Cas

Runbook badge/scan pour les participants de la Veillée du Tanbou —
protocole simulé, clairement marqué comme tel.

## Erreurs fréquentes

- Présenter le protocole simulé comme une preuve réelle et vérifiable.
- Concevoir un protocole trop complexe pour être réellement suivi le jour
  de l'événement.

## Activité

Conception collective du protocole à partir des contraintes réelles du
cas (petit événement, ressources limitées).

## Exercice

Rédiger la mention explicite marquant le protocole comme simulé/
pédagogique, non opposable en dehors de ce cas.

## Livrable

Runbook badge/scan (mention explicite du caractère simulé).

## Critères de réussite

- Le protocole répond aux 3 exigences (qui/quand/vérifiable).
- La mention "simulé, non opposable" est présente et claire.

## Preuve

Runbook, conservé dans le registre de preuves (M11) — signal
`FREK-WORK` (mapping proposé).

## Auto-évaluation

*Ai-je conçu un protocole réellement suivable, ou trop complexe pour
l'événement réel ? Ai-je été clair sur son caractère simulé ?*

## Passage au module suivant

M05 revient à l'animation de communauté, une compétence issue du legacy.
