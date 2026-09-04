# KLT-05 — M09 — Data lineage et reporting

```
MODULE_ID: KLT05-M09
COMPETENCY_ID: C9 — Lire des signaux d'engagement et rendre compte sans fabriquer
PREREQUISITES: M03, M05
ASSESSMENT_LEVEL: N2
KILTIKONET_DEPENDENCY: Observatory — NOT_CONNECTED en Academy (KLT-0001 §4). Ce module ne simule aucune lecture Observatory ; il s'appuie sur les analytics réels déjà pratiqués en legacy (M05), qui restent autoritaires jusqu'à ce qu'un accès Observatory réel existe.
ROLE_BOUNDARIES: Lire des signaux d'engagement n'autorise pas à en tirer des conclusions non fondées sur les données réellement disponibles
FREK_PROOF_MAPPING: FREK-SCORE (signal réel, hérité de seed_modules.py:926-928)
ORIGIN: legacy M05 + master plan M07 (MERGE, legacy reste autoritaire — KLT-0002 §KLT-05)
```

## Situation professionnelle

Rendre compte sans donnée fiable fabrique une fausse impression de
maîtrise — un rapport d'engagement sur la page de l'événement doit
s'appuyer sur ce qui est réellement mesurable aujourd'hui, pas sur une
lecture Observatory qui n'existe pas encore.

## Objectifs d'apprentissage

- Lire des indicateurs d'engagement réels (vues, réactions, partages,
  questions de support déjà journalisées en M07).
- Distinguer donnée observée et interprétation.
- Nommer honnêtement l'absence d'une donnée Observatory, sans la
  simuler.

## Notions essentielles

`KLT-0002` a établi que l'analytics legacy (M05, réel et déjà pratiqué)
reste **autoritaire** tant qu'un accès Observatory réel n'existe pas —
ce module n'est pas un remplacement du legacy par une promesse
Observatory non tenue, c'est le même travail d'analyse honnête, avec une
mention explicite de ce qui manque.

## Méthode

1. Rassembler les données réellement disponibles (portée, réactions,
   support déjà journalisé en M07).
2. Produire une lecture qui distingue observé et interprété.
3. Nommer explicitement ce qu'un accès Observatory apporterait à
   l'avenir, sans le simuler.

## Exemples

"15 réactions et 3 questions de support sur la publication de l'annonce"
est une donnée observée ; "l'événement suscite un engouement fort" est
une interprétation qui doit être nuancée par l'échelle réelle des
chiffres.

## Cas

Rapport d'engagement de la page de la Veillée du Tanbou, s'appuyant sur
les données réelles du cas (portée, support M07).

## Erreurs fréquentes

- Interpréter des chiffres modestes comme un succès disproportionné.
- Simuler une donnée Observatory absente — **interdit** (même discipline
  que dans les 4 formations précédentes).

## Activité

Analyse critique d'un rapport fourni, identification des interprétations
non fondées sur les chiffres réels.

## Exercice

Rédiger la mention explicite de ce qu'un accès Observatory apporterait à
l'avenir, sans l'affirmer comme disponible aujourd'hui.

## Livrable

Rapport sourcé (1 mois) + recommandations.

## Critères de réussite

- Observé et interprété sont distingués.
- Aucune donnée Observatory n'est simulée.

## Preuve

Rapport, conservé dans le registre de preuves (M11) — signal
`FREK-SCORE`.

## Auto-évaluation

*Mes conclusions sont-elles proportionnées aux chiffres réels dont je
dispose ?*

## Passage au module suivant

M10 aborde la gestion d'incident — que faire quand les données révèlent
ou accompagnent un problème réel.
