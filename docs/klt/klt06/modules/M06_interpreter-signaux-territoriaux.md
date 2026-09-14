# KLT-06 — M06 — Interpréter des signaux territoriaux réels pour appuyer une décision

```
MODULE_ID: KLT06-M06
COMPETENCY_ID: C6 — Interpréter des signaux territoriaux réels pour appuyer une décision
PREREQUISITES: M05
ASSESSMENT_LEVEL: N2
KILTIKONET_DEPENDENCY: Observatory — PRODUCT_CODE_REAL_VERIFIED (`/api/observatory/signals`, `alerts_adapter`, surfaced from Smart Engine `team_notifications`, repo `cultureconnectorg/Kiltikonet-Aout2026`, commit `bb64ce7`) ; NOT_CONNECTED_TO_ACADEMY_RUNTIME ; tout signal utilisé dans ce module est PEDAGOGICAL_ILLUSTRATIVE, jamais un signal réellement observé aujourd'hui.
ROLE_BOUNDARIES: Interpréter un signal illustratif n'autorise jamais à présenter cette interprétation comme fondée sur un signal réellement observé
FREK_PROOF_MAPPING: FREK-SCORE (mapping proposé — net-new, re-vérifié 2026-09-07)
ORIGIN: PROPOSED (Claude-derived, re-verified against Kiltikonet-Aout2026 2026-09-07 — voir KLT_09_20_RECONCILIATION.md §Re-vérification)
```

## Situation professionnelle

L'endpoint réel `/api/observatory/signals` restitue des "signaux
historiques" remontés par le Smart Engine. Un(e) analyste Observatory
doit savoir interpréter un tel signal pour appuyer une décision d'un
autre rôle (le Founder, un DG Network) — sans jamais décider à sa
place, et sans jamais confondre un signal illustratif d'entraînement
avec un signal réellement observé.

## Objectifs d'apprentissage

- Interpréter la structure réelle d'un signal (type, gravité,
  territoire, horodatage, lineage) pour en tirer une lecture utile à la
  décision.
- Formuler une recommandation d'attention, jamais une décision à la
  place d'un autre rôle.
- Ne jamais confondre un signal d'entraînement illustratif avec un
  signal réellement observé aujourd'hui.

## Notions essentielles

Un signal Observatory réel porte un type, une gravité, un territoire,
un horodatage et une lineage (provenance `team_notifications` du Smart
Engine). L'**interpréter**, c'est en tirer une lecture qui appuie une
décision — pas décider à la place du rôle qui la prend (Founder, DG
Network, etc., selon `NETWORK_GLOBAL_READ_ROLES`, voir `KLT-07`).

## Méthode

1. Lire la structure réelle d'un signal (type, gravité, territoire,
   lineage) telle qu'exposée par `/api/observatory/signals`.
2. Interpréter ce que le signal indique réellement, sans extrapoler
   au-delà de ce qu'il dit.
3. Formuler une note d'attention à destination du rôle décisionnaire,
   sans trancher à sa place.

## Exemples

Interpréter un signal illustratif "hausse inhabituelle des candidatures
d'opérateurs sur un territoire donné, gravité modérée" comme "ce signal
appelle une vérification de capacité d'onboarding, pas une décision
immédiate d'expansion" reste dans le rôle d'interprétation. À l'inverse,
écrire "ce signal montre que Mémoire Vive doit être acceptée comme
opérateur relais dès maintenant" déciderait à la place du rôle réseau
(`KLT-07`), et confondrait en plus un signal d'entraînement illustratif
avec une preuve réelle sur le dossier de Mémoire Vive.

## Cas

Interprétation d'un signal territorial illustratif dans l'hypothèse où
Mémoire Vive serait candidate opérateur (`case/CAS_ANGLE_OBSERVATORY.md`).

## Erreurs fréquentes

- Décider à la place du rôle réseau au lieu de formuler une
  recommandation d'attention.
- Extrapoler au-delà de ce que le signal indique réellement.
- Présenter un signal d'entraînement illustratif comme un signal
  réellement observé sur un dossier réel.

## Activité

Lecture guidée de la structure réelle d'un signal (type, gravité,
territoire, lineage).

## Exercice

Produire la note d'interprétation du signal illustratif fourni, avec
recommandation d'attention.

## Livrable

Note d'interprétation de signal (1-2 pages).

## Critères de réussite

- L'interprétation reste fidèle à ce que le signal indique réellement.
- La note recommande, elle ne décide pas à la place du rôle réseau.
- Le caractère illustratif du signal est explicitement rappelé.

## Preuve

Note d'interprétation, conservée dans le registre de preuves — signal
`FREK-SCORE`.

## Auto-évaluation

*Ma note recommande-t-elle une attention, ou ai-je pris une décision qui
revient à un autre rôle ?*

## Passage au module suivant

M07 aborde la restitution de l'ensemble de l'analyse (M01-M06) à un
public non spécialiste — dernier module de `KLT-06`, désormais complet
(7/7).
