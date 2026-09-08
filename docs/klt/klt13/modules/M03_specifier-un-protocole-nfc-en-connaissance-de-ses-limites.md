# KLT-13 — M03 — Spécifier une extension NFC en connaissance de ses limites actuelles

```
MODULE_ID: KLT13-M03
COMPETENCY_ID: C3 — Spécifier une extension NFC en connaissance de ses limites actuelles (non implémentée)
PREREQUISITES: M01, M02
ASSESSMENT_LEVEL: N2
KILTIKONET_DEPENDENCY: NFC — NOT_IMPLEMENTED, nulle part dans l'écosystème CVLN vérifié (ni Kiltikonet, ni Good Mood — QR uniquement). Ce module conçoit une spécification, jamais un système existant.
ROLE_BOUNDARIES: Spécifier une extension NFC n'autorise jamais à la présenter comme un système déjà disponible
FREK_PROOF_MAPPING: FREK-WORK (mapping proposé — net-new, formation sans legacy)
ORIGIN: PROPOSED (Claude-derived, KLT_09_20_RECONCILIATION.md §KLT-13)
```

## Situation professionnelle

Le métier de Responsable Accréditation Terrain porte, dans son titre, la
mention NFC — une technologie citée dans le secteur événementiel réel
pour son confort d'usage (badge à approcher, pas à scanner). Mais aucun
système NFC réel n'existe nulle part dans l'écosystème CVLN vérifié.
Spécifier une extension NFC sans nommer ce statut, dans un dossier
professionnel ou face à un partenaire, fabriquerait une capacité
technique qui n'existe pas.

## Objectifs d'apprentissage

- Distinguer une spécification technique (ce qu'un système ferait s'il
  existait) d'une affirmation de disponibilité (ce qui existe
  aujourd'hui).
- Rédiger une spécification NFC réaliste, ancrée sur les exigences déjà
  extraites du précédent QR réel (M02).
- Nommer explicitement, à chaque usage de cette spécification, son
  statut `NOT_IMPLEMENTED`.

## Notions essentielles

Une spécification technique est un document de conception — elle décrit
ce qu'un système *ferait* s'il était construit, sur la base d'exigences
réelles déjà identifiées (identifiant unique, point de contrôle,
comptage, établies en M02). Elle ne devient jamais, par elle-même, une
preuve que le système existe. La confusion entre les deux est la faute
professionnelle la plus grave de ce module : présenter un document de
conception comme une fonctionnalité disponible.

## Méthode

1. Reprendre les exigences transposables identifiées en M02 (identifiant
   unique, point de contrôle, comptage).
2. Rédiger une spécification NFC qui reprend ces exigences, en les
   adaptant à la technologie NFC (approche sans contact, pas de scan
   visuel requis).
3. Apposer, sur chaque exemplaire de la spécification, la mention
   explicite `NOT_IMPLEMENTED — spécification, aucun système réel`.

## Exemples

Une spécification qui décrit "badge NFC portant un identifiant unique,
lu à un point de contrôle, avec comptage — `STATUS: NOT_IMPLEMENTED`"
est correcte : elle conçoit sans fabriquer de disponibilité. À
l'inverse, présenter cette même spécification à un partenaire comme
"notre système d'accréditation NFC" sans la mention de statut laisse
croire à une capacité opérationnelle qui n'existe pas — la même
spécification technique, selon qu'elle porte ou non la mention de statut,
passe d'un document honnête à une affirmation trompeuse.

## Cas

Spécification NFC pour la Veillée du Tanbou, reprenant le plan
d'accréditation (M01) et les exigences du précédent QR (M02), avec
mention explicite de son statut non implémenté.

## Erreurs fréquentes

- Omettre la mention de statut sur un exemplaire de la spécification,
  même par oubli.
- Présenter la spécification à un tiers (partenaire, financeur) sans
  rappeler oralement son statut non implémenté.
- Spécifier des fonctionnalités NFC qui dépassent les exigences déjà
  identifiées, sans lien avec un besoin réellement établi.

## Activité

Comparaison de deux versions d'une même spécification (avec et sans
mention de statut) pour identifier le risque de confusion introduit par
l'omission.

## Exercice

Rédiger la spécification NFC complète pour la Veillée du Tanbou, avec
mention de statut sur chaque section.

## Livrable

Spécification NFC (statut explicite).

## Critères de réussite

- La mention `NOT_IMPLEMENTED` est présente sur l'intégralité du
  document, pas seulement en en-tête.
- Les fonctionnalités spécifiées reprennent des exigences réellement
  établies en M02, sans extension non justifiée.

## Preuve

Spécification, conservée dans le registre de preuves — signal
`FREK-WORK`.

## Auto-évaluation

*Un lecteur pressé de ma spécification pourrait-il croire, même un
instant, que ce système existe déjà ?*

## Passage au module suivant

M04 aborde la gestion d'un incident d'accréditation terrain le jour J —
avec le dispositif réel (QR ou manuel), pas la spécification NFC non
implémentée.
