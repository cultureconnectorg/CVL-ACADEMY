# KLT-02 — M03 — Budget culturel prévisionnel

```
MODULE_ID: KLT02-M03
COMPETENCY_ID: C3 — Construire un budget culturel prévisionnel
PREREQUISITES: M01, M02
ASSESSMENT_LEVEL: N2
KILTIKONET_DEPENDENCY: Admin finance (concept, aucun système requis)
ROLE_BOUNDARIES: Construire un budget projet n'est pas arbitrer la comptabilité globale de l'association (KLT-04)
FREK_PROOF_MAPPING: FREK-SCORE (signal réel, hérité de seed_modules.py:660-662)
ORIGIN: legacy M03 + master plan M04 (MERGE)
```

## Situation professionnelle

500€ ne couvrent pas un événement avec matériel technique, communication
et défraiement. Sans budget chiffré, le chef de projet découvre le
manque le jour J plutôt qu'en amont, quand il est encore temps d'agir.

## Objectifs d'apprentissage

- Chiffrer un budget prévisionnel réaliste à partir de postes réels.
- Distinguer ce que la subvention couvre de ce qui reste à financer.
- Construire une trésorerie prévisionnelle simple, pas seulement un
  total.

## Notions essentielles

Un budget prévisionnel liste des **postes de dépense réels** (matériel,
communication, défraiement, imprévu) en face de **sources de
financement réelles** (subvention confirmée, financement à obtenir,
apport en nature). Un budget qui ne distingue pas "confirmé" de "à
obtenir" masque le risque réel du projet.

## Méthode

1. Lister les postes de dépense réels du projet.
2. Chiffrer chaque poste à partir d'estimations réalistes (pas de
   round numbers arbitraires).
3. Faire face à chaque poste sa source de financement, en distinguant
   confirmé/à obtenir.
4. Calculer l'écart de financement à couvrir — c'est l'intrant direct de
   M04.

## Exemples

Poste "matériel audio" : coût nul si prêté par la médiathèque (déjà
identifié en `KLT-01`) — mais le transport et l'assurance du matériel
prêté restent un coût réel à ne pas oublier.

## Cas

Budget prévisionnel complet de la Veillée du Tanbou, avec les 500€
confirmés et l'écart à financer identifié.

## Erreurs fréquentes

- Oublier des postes réels (transport, assurance, imprévu) pour
  présenter un budget artificiellement équilibré.
- Confondre financement confirmé et financement espéré.

## Activité

Revue croisée : chaque candidat identifie, dans le budget d'un pair, un
poste manquant ou une source de financement présentée comme confirmée
sans preuve.

## Exercice

Calculer précisément l'écart entre les 500€ confirmés et le coût total
réaliste du projet — c'est ce chiffre que M04 doit combler.

## Livrable

Budget prévisionnel complet + trésorerie simple.

## Critères de réussite

- Chaque poste de dépense a une source de financement identifiée
  (confirmée ou à obtenir).
- L'écart de financement est chiffré explicitement.
- Aucun poste réel connu du cas n'est omis (transport, assurance,
  imprévu).

## Preuve

Budget chiffré, conservé dans le registre de preuves (M10) — signal
`FREK-SCORE`.

## Auto-évaluation

*Mon budget résisterait-il à une question du CA sur un poste précis ?
Ai-je confondu financement confirmé et financement espéré ?*

## Passage au module suivant

L'écart de financement calculé ici est ce que M04 (recherche de
financement) doit combler.
