# BRN-15 — Banque N1 (formatif)

Réserve `BRN15.SKILL.*`.

1. Trace le chemin réel de l'événement `academy.certification.passed`
   depuis son émission jusqu'à sa relève : quels fichiers/lignes sont
   impliqués ?
2. Pourquoi cet unique événement ne constitue-t-il jamais un moteur de
   raisonnement, de contexte, de mémoire, ou de connaissance ?
3. Le vrai `/brain/ask` de `MetaCVLN` est cité comme preuve qu'un
   concept de "Brain CVLN" existe réellement dans l'écosystème —
   pourquoi ne doit-il jamais être présenté comme ce à quoi cet
   événement est câblé ?
4. Pourquoi cette formation partage-t-elle son mécanisme sous-jacent
   avec IOS-07, et pourquoi le langage de frontière est-il repris
   verbatim de `docs/kor/kor12/` plutôt que re-dérivé ?

## Corrigé indicatif

1. `backend/certification/service.py:140` émet l'événement via
   `backend/services/events.py` (pub/sub en-process), relayé par
   `subscribers.py` vers la route `/academy/certification-passed`.
2. C'est un simple abonnement à un événement unique — aucune capacité
   de raisonnement, de récupération contextuelle, ou de mémoire n'est
   impliquée.
3. Aucune intégration observée ne relie `academy.certification.passed`
   à `/brain/ask` — les fusionner inventerait un câblage inexistant.
4. IOS-07 et BRN-15 reposent sur le même bus `events.py` ; reprendre le
   langage déjà établi (`docs/kor/kor12/`, FRK-58/60) évite de
   re-dériver une frontière déjà posée ailleurs — converger, pas
   dupliquer.
