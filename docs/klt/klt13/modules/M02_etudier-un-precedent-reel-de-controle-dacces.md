# KLT-13 — M02 — Étudier un précédent réel de contrôle d'accès électronique

```
MODULE_ID: KLT13-M02
COMPETENCY_ID: C2 — Étudier un précédent réel de contrôle d'accès électronique (cross-écosystème)
PREREQUISITES: M01
ASSESSMENT_LEVEL: N1/N2
KILTIKONET_DEPENDENCY: aucune côté Kiltikonet (aucun système réel n'existe chez Kiltikonet). Précédent réel étudié : Good Mood door-scan/QR (`GMD-25`, `gmfest972/goodmooddjsayd`, réel et vérifié — `/scan/check`, `/scan/counter/{eid}`) — un système d'un autre produit CVLN, cité comme étude de cas cross-écosystème, jamais présenté comme un système Kiltikonet.
ROLE_BOUNDARIES: Étudier un précédent réel d'un autre produit ne donne pas mandat pour prétendre que Kiltikonet dispose du même système
FREK_PROOF_MAPPING: FREK-WORK (mapping proposé — net-new, formation sans legacy)
ORIGIN: PROPOSED (Claude-derived, KLT_09_20_RECONCILIATION.md §KLT-13 — précédent Good Mood cité explicitement)
```

## Situation professionnelle

Concevoir un protocole d'accréditation rigoureux sans avoir jamais étudié
un dispositif réel revient à réinventer, souvent mal, des exigences déjà
connues du secteur événementiel — un dispositif électronique réel et
vérifié existe dans l'écosystème CVLN (Good Mood), et l'étudier
honnêtement, sans en travestir l'origine, enrichit la conception du plan
d'accréditation terrain de la Veillée du Tanbou.

## Objectifs d'apprentissage

- Identifier les exigences réelles d'un dispositif de contrôle d'accès
  électronique à partir d'un précédent vérifié (Good Mood).
- Distinguer un précédent cross-écosystème (un autre produit CVLN) d'un
  système propre à Kiltikonet, qui n'existe pas.
- Extraire de ce précédent des exigences transposables à un dispositif
  terrain, sans copier un système que Kiltikonet n'a pas.

## Notions essentielles

Good Mood (plateforme événementielle réelle du même écosystème CVLN)
opère un contrôle d'accès électronique réel et vérifié : un QR code
généré par billet (`/tickets/{tid}/qr.png`), scanné à l'entrée
(`/scan/check`), avec un compteur d'entrées par événement
(`/scan/counter/{eid}`). Ce n'est **pas** un système NFC, et ce n'est
**pas** un système Kiltikonet — c'est un précédent réel d'un autre
produit du même écosystème, utilisable comme étude de cas pour en
extraire des exigences (identifiant unique par accréditation, point de
scan unique, compteur en temps réel), jamais comme preuve que Kiltikonet
dispose du même système.

## Méthode

1. Lire les capacités réelles du précédent (génération d'un identifiant
   unique, scan à un point de contrôle, comptage).
2. Extraire les exigences transposables (identifiant unique par
   accréditation, traçabilité du passage, comptage par zone).
3. Nommer explicitement, dans toute note produite, que ce précédent
   appartient à un autre produit CVLN — jamais à Kiltikonet.

## Exemples

"Le précédent Good Mood montre qu'un identifiant unique par
accréditation, scanné à un point de contrôle unique, permet un comptage
fiable — exigence transposable au plan terrain de la Veillée" est une
étude de cas correcte, qui nomme sa source réelle. "Kiltikonet dispose
d'un système de scan comme Good Mood" serait une erreur factuelle
directe — aucun système de ce type n'existe chez Kiltikonet, et
l'affirmer, même par raccourci de langage, fabrique une capacité qui
n'existe pas.

## Cas

Fiche d'analyse du précédent Good Mood (`/scan/check`,
`/scan/counter/{eid}`), avec extraction des exigences transposables au
plan d'accréditation terrain de la Veillée du Tanbou construit en M01.

## Erreurs fréquentes

- Présenter le précédent Good Mood comme un système Kiltikonet, même par
  raccourci de langage.
- Copier littéralement un dispositif technique réel (QR, scan) sans
  vérifier qu'il est adapté à l'échelle réelle du petit événement étudié.
- Confondre "identifiant unique" (exigence transposable) et "système NFC"
  (technologie non implémentée nulle part, traitée en M03).

## Activité

Lecture guidée du tableau des routes réelles de Good Mood
(`GOOD_MOOD_DJ_SAYD_RECONCILIATION.md`), identification collective des
exigences transposables et de celles propres à l'échelle de Good Mood
(festivals) non pertinentes pour un petit événement communautaire.

## Exercice

Rédiger la fiche d'analyse du précédent, avec attribution correcte de
sa source (Good Mood, pas Kiltikonet) et extraction des exigences
transposables au plan terrain de la Veillée.

## Livrable

Fiche d'analyse du précédent réel.

## Critères de réussite

- La source du précédent (Good Mood, produit CVLN distinct de
  Kiltikonet) est nommée explicitement, sans confusion.
- Les exigences extraites sont réellement transposables à l'échelle du
  petit événement étudié, pas copiées telles quelles.

## Preuve

Fiche d'analyse, conservée dans le registre de preuves — signal
`FREK-WORK`.

## Auto-évaluation

*Ma fiche laisse-t-elle entendre, même implicitement, que Kiltikonet
dispose du système que j'étudie ?*

## Passage au module suivant

M03 spécifie une extension NFC en connaissance de ses limites actuelles
— la technologie nommée dans le titre du métier, mais non implémentée
nulle part.
