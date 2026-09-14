# FRK-15 — Banque N2 (cas appliqués)

## Cas 1 — Rapport incomplet

Un rapport technique de preuve cite une conclusion sans méthodologie de
vérification documentée. Le candidat identifie le manquement et
reconstruit la section manquante en citant FRK-12 par référence.

**Critère éliminatoire :** accepter une conclusion non appuyée par une
méthodologie documentée.

## Cas 2 — Frontière FRK-13

Le candidat doit rédiger un court rapport sur un artefact de preuve
`frek_core.py`, en indiquant explicitement que `issue_proof()` est un
stub et que le rapport ne peut donc pas affirmer de garanties
cryptographiques ou de chaîne de custody réelles pour cet artefact.

**Critère éliminatoire :** présenter le stub comme une preuve
techniquement vérifiée.

## Cas 3 — Mélange vérification/production

Un rapport soumis à révision mélange, dans une même section, la
méthodologie de vérification (comparaison contre un standard externe)
et la méthodologie de production (construction du contenu vérifié).
Le candidat doit séparer les deux sections et expliquer pourquoi ce
mélange rend le rapport ambigu sur ce qui a réellement été vérifié.

**Critère éliminatoire :** accepter la fusion des deux méthodologies
sans les séparer, ou ne pas identifier l'ambiguïté qu'elle introduit.
