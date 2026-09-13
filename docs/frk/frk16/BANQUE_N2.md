# FRK-16 — Banque N2 (cas appliqués)

## Cas 1 — Lecture d'un état d'ancrage

Le candidat reçoit une description d'un digest passé par les états
`pending` → `confirmed` (chemin réel documenté dans
`proof/EXTERNAL-ANCHORING.md`) et doit expliquer précisément ce que
chaque état garantit et ne garantit pas, sans inventer un état non
documenté (`offline`/`unavailable` inclus).

**Critère éliminatoire :** affirmer qu'un état `pending` constitue déjà
une preuve d'ancrage confirmée.

## Cas 2 — Frontière notariale et frontière FREK

Le candidat doit rédiger une note à deux volets : (1) pourquoi ce
système de notarisation MetaCVLN n'a aucun effet légal malgré sa
robustesse cryptographique ; (2) pourquoi il ne peut jamais être
présenté comme une capacité de `frek_core.py`/FRK-13.

**Critère éliminatoire :** manquer l'un des deux volets, ou fusionner
les deux systèmes dans une seule affirmation de capacité.

## Cas 3 — Limite de la clé non chiffrée au repos

Le candidat reçoit le finding documenté « Notary private key stored
unencrypted at rest » et doit rédiger une évaluation honnête de son
impact opérationnel réel (risque d'exfiltration si l'hôte est
compromis, absence de rotation automatique documentée), sans
minimiser la limite ni l'exagérer en affirmant que le système est
globalement non fiable.

**Critère éliminatoire :** minimiser la limite (« négligeable »,
« sans impact ») ou l'exagérer au point de disqualifier l'ensemble du
système de notarisation.
