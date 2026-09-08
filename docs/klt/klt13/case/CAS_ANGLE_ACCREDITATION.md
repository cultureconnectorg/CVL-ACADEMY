# KLT-13 — Cas fil rouge : La Veillée du Tanbou, angle accréditation terrain

```
CASE_STATUS = PEDAGOGICAL_SIMULATION
Même univers que KLT-01→08. Angle métier : concevoir et opérer un
dispositif d'accréditation terrain rigoureux pour un petit événement
physique, sans jamais fabriquer de système NFC ou de connexion live
qui n'existent nulle part.
```

## Rappel du socle commun

Territoire *Baie-Mahault-sur-Mer*, association *Mémoire Vive*, action
*la Veillée du Tanbou*. Voir `klt01/case/CAS_FIL_ROUGE.md`.

## Ce que l'angle "accréditation terrain" ajoute

**Le lieu** : la salle municipale pressentie pour la Veillée accueille
plusieurs publics aux besoins d'accès distincts — le public général, les
Doyens (dont deux à mobilité réduite, contrainte déjà nommée en
`KLT-01`), le groupe de jeunes, les artistes du collectif Tanbou Rasin,
et l'espace de rangement des instruments (patrimoine matériel sans
inventaire).

**Le plan d'accréditation** (matière de M01) : croiser ces rôles avec les
zones du lieu (salle publique, espace réservé aux Doyens, rangement,
entrée/sortie) pour produire un plan qui n'ouvre à chaque rôle que
l'accès réellement nécessaire à sa mission.

**Le précédent réel étudié** (matière de M02) : le dispositif QR de Good
Mood (`GMD-25`, `gmfest972/goodmooddjsayd`) — un système réel d'un autre
produit CVLN, jamais présenté comme un système Kiltikonet, étudié pour
en extraire des exigences transposables (identifiant unique, point de
contrôle, comptage).

**La spécification NFC** (matière de M03) : le titre du métier nomme la
NFC, technologie non implémentée nulle part dans l'écosystème vérifié —
le candidat spécifie une extension NFC pour la Veillée en connaissance
de ce statut, jamais comme un système disponible.

**L'incident terrain** (matière de M04) : le jour J, une tentative
d'accès non autorisé à l'espace réservé aux Doyens doit être gérée sans
céder à la pression sociale, documentée, et escaladée si nécessaire.

**Le bilan** (matière de M05) : restituer à Mémoire Vive un bilan
d'accréditation fondé exclusivement sur ce qui a été réellement mesuré
pendant l'événement (petit événement, ressources limitées, comptage
souvent manuel et partiel).

## Limites explicites du cas (angle accréditation terrain)

Le candidat conçoit, spécifie et opère un dispositif d'accréditation
terrain (`C1`-`C5`), en étudiant honnêtement un précédent réel
cross-écosystème (Good Mood, jamais Kiltikonet) — mais **ne construit
jamais** de système NFC réel (`NFC_NOT_IMPLEMENTED`, nulle part), ne
prétend jamais que Kiltikonet dispose d'un système de scan comme Good
Mood, et ne fabrique jamais de donnée de bilan non mesurée. Le candidat
**ne conduit pas** l'action de médiation (`KLT-01`), **ne gère pas** le
budget (`KLT-02`), **ne négocie pas** avec des institutions (`KLT-03`),
**n'a pas** d'autorité de gouvernance (`KLT-04`), et ne rouvre ni ne
remplace le protocole badge/scan générique de `KLT-05`/M04.
