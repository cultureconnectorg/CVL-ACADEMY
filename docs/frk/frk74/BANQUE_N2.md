# FRK-74 — Banque N2 (cas appliqués)

## Cas 1 — Statut de spécification

Le candidat reçoit des extraits de la spécification DSP Fingerprint et
doit identifier correctement lesquels sont verrouillés et lesquels
restent des décisions ouvertes selon `CE_QUI_MANQUE.md`.

**Critère éliminatoire :** présenter un paramètre explicitement ouvert
(taille FFT, hop size, nombre de bandes, algorithme) comme verrouillé.

## Cas 2 — Frontière FRK-29/30

Le candidat doit expliquer pourquoi son analyse de la spécification DSP
ne s'appliquerait pas telle quelle à une empreinte culturelle générale
non-audio (FRK-29/30).

**Critère éliminatoire :** fusionner les deux domaines techniques.

## Cas 3 — Compromis fenêtre/hop size

Le candidat doit expliquer, pour deux scénarios distincts (analyse
temps réel à faible latence vs. analyse hors-ligne haute précision),
quel compromis de fenêtre FFT et de hop size serait raisonnable à
envisager — en précisant explicitement qu'il s'agit d'une proposition
d'ingénierie, jamais d'une valeur déjà verrouillée par la spécification.

**Critère éliminatoire :** présenter une valeur proposée comme la
décision officielle déjà prise par le corpus FREK v3.
