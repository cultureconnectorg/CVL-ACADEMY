# KLT-02 — M08 — Risques et conformité

```
MODULE_ID: KLT02-M08
COMPETENCY_ID: C8 — Identifier et traiter risques et conformité (net-new)
PREREQUISITES: M01-M07
ASSESSMENT_LEVEL: N2
KILTIKONET_DEPENDENCY: Compliance — NOT_IMPLEMENTED comme donnée structurée en Academy (KLT-0001 §4). Le module ne lit aucun système de conformité réel ; il forme le jugement, pas une procédure outillée.
ROLE_BOUNDARIES: Identifier un risque de conformité n'autorise pas à trancher seul une question de gouvernance associative (KLT-04) — le chef de projet signale, il n'arbitre pas la structure
FREK_PROOF_MAPPING: FREK-WORK (mapping proposé — aucun signal legacy n'existait pour ce module, net-new)
ORIGIN: master plan M05 (BUILD_NEW) — KLT-0002 §KLT-02
```

## Situation professionnelle

Ignorer un risque connu jusqu'à ce qu'il survienne est la cause la plus
fréquente d'échec de projet — pas le manque de compétence technique.
Aucun module legacy ne traitait explicitement cette compétence : c'est
la seule addition nette du master plan pour `KLT-02`.

## Objectifs d'apprentissage

- Identifier les risques réels d'un projet (pas une liste générique).
- Distinguer un risque projet (retard, budget) d'un risque de conformité
  (obligation légale ou associative non respectée).
- Construire un registre des risques priorisé, avec réponse prévue pour
  chacun.

## Notions essentielles

Un **risque** a une probabilité et un impact ; un **enjeu de
conformité** est une obligation (légale, associative, contractuelle) qui,
non respectée, expose le projet ou l'association à une conséquence
directe (pas seulement un retard). Les deux se traitent différemment :
un risque s'atténue, un enjeu de conformité se respecte ou s'escalade.

## Méthode

1. Lister les risques réels du projet (probabilité × impact).
2. Distinguer, parmi eux, ce qui relève de la conformité pure (ex. une
   obligation d'accessibilité légale) de ce qui relève du risque
   opérationnel classique (ex. un retard de financement).
3. Prévoir une réponse pour chaque risque prioritaire.
4. Escalader — sans trancher soi-même — tout enjeu de conformité qui
   dépasse le mandat projet.

## Exemples

Le risque "salle non-PMR" est à la fois un risque opérationnel (calendrier)
et un enjeu de conformité accessibilité — le chef de projet le traite
comme risque (chercher une alternative) et le signale comme conformité
(vérifier l'obligation légale réelle, sans la trancher seul si elle
dépasse son mandat).

## Cas

Registre des risques du projet Veillée du Tanbou : tension spectacle/
rituel (risque relationnel), salle non-PMR (risque + conformité),
disponibilité bénévole (risque opérationnel), délai DAC (risque
calendaire).

## Erreurs fréquentes

- Traiter tous les risques avec la même réponse générique ("on verra").
- Confondre un risque opérationnel avec un enjeu de conformité et le
  traiter comme un simple aléa gérable en interne.
- Attendre qu'un risque survienne pour le documenter, au lieu de
  l'anticiper.

## Activité

Classement des 4 risques du cas en risque pur / enjeu de conformité /
les deux, avec justification.

## Exercice

Proposer une réponse concrète et réaliste pour le risque le plus
probable ET le plus impactant du registre.

## Livrable

Registre des risques (gabarit `templates/TEMPLATES.md` — hérité du
gabarit KLT-01, réutilisé tel quel).

## Critères de réussite

- Chaque risque du cas est qualifié (probabilité/impact) et une réponse
  proposée.
- La distinction risque/conformité est appliquée correctement au cas de
  la salle non-PMR.
- Aucun enjeu de conformité n'est tranché seul au-delà du mandat projet.

## Preuve

Registre des risques, conservé dans le registre de preuves (M10) —
signal `FREK-WORK` (mapping proposé).

## Auto-évaluation

*Ai-je traité chaque risque avec une réponse spécifique, ou une réponse
générique répétée ? Ai-je escaladé ce qui dépassait mon mandat ?*

## Passage au module suivant

Les risques anticipés ici informent directement l'évaluation d'impact
(M09) — un risque survenu et documenté ici doit apparaître dans le bilan,
pas être passé sous silence.
