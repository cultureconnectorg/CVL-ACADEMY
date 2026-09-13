# FRK-12 — Banque N2

## Cas N2-1 — Conception d'artefact de preuve

Un organisme culturel affirme qu'une œuvre numérique a été créée par
un artiste donné, à une date donnée, sans modification depuis. Conçois
un artefact de preuve vérifiable pour cette affirmation, en pratique
réelle d'ingénierie — structure, provenance, mécanisme de détection de
falsification — sans l'attribuer à un système CVLN existant.

**Critères de notation :** l'artefact proposé distingue explicitement
la structure (bien formée) de la vérification (la structure prouve-
t-elle réellement la revendication ?) ; aucune référence à un système
CVLN de preuve fonctionnel n'est faite.

## Cas N2-2 — Frontière FRK-12/FRK-13

Un candidat écrit : "Le `issue_proof()` de CVLN est une implémentation
complète d'ingénierie de la preuve." Explique pourquoi cette phrase
confond FRK-12 et FRK-13, et reformule-la correctement.

**Critères de notation :** identifie que `issue_proof()` est un stub
réel (territoire FRK-13, spécifique), tandis que FRK-12 est la
discipline générale ; la reformulation ne prête aucune capacité
non-implémentée à CVLN.

## Cas N2-3 — Détecter une preuve auto-référentielle

Un système affirme qu'un document est authentique en citant... le
document lui-même comme preuve de son authenticité. Explique pourquoi
c'est un échec d'ingénierie de la preuve et propose une structure
alternative avec vérification indépendante.

**Critères de notation :** identifie la preuve auto-référentielle
comme mode d'échec ; la structure alternative introduit un mécanisme
de vérification tiers réel (horodatage indépendant, chaîne de
provenance externe, ou équivalent).
