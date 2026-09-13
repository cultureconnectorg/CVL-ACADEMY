# BRN-15 — Banque N1 (formatif)

Réserve `BRN15.SKILL.BRAIN_TOUCHPOINT_OPERATOR.L1`.

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
5. Qu'est-ce que `backend/services/events.py` fait réellement, et
   qu'est-ce qu'il ne fait pas ? Décris son mécanisme en une phrase
   sans inventer de capacité absente.
6. Un candidat affirme que `subscribers.py` "analyse le contenu de la
   certification avant de la relayer". Que réponds-tu ?
7. Pourquoi le statut `READY_FOR_FREK_PROOF = FALSE` s'applique-t-il à
   ce domaine, alors même que le touchpoint qu'il décrit est réel et
   fonctionnel en production ?
8. Un candidat propose d'étendre l'événement `academy.certification.
   passed` avec un champ `brain_context` rempli par un futur appel à
   `/brain/ask`. Pourquoi cette proposition, même présentée comme une
   évolution future plutôt qu'un état actuel, doit-elle rester
   clairement hors du périmètre certifiable de BRN-15 ?

## Corrigé indicatif

1. `backend/certification/service.py:140` émet l'événement via
   `backend/services/events.py` (pub/sub en-process), relayé par
   `subscribers.py` vers la route `/academy/certification-passed`.
   Aucun autre fichier n'intervient dans ce chemin réel.
2. C'est un simple abonnement à un événement unique — aucune capacité
   de raisonnement, de récupération contextuelle, ou de mémoire n'est
   impliquée. L'événement transporte une notification de réussite, pas
   un contenu à interpréter.
3. Aucune intégration observée ne relie `academy.certification.passed`
   à `/brain/ask` — les fusionner inventerait un câblage inexistant.
   `/brain/ask` prouve seulement qu'un concept de Brain CVLN existe
   ailleurs dans l'écosystème, pas que cette Academy y est connectée.
4. IOS-07 et BRN-15 reposent sur le même bus `events.py` ; reprendre le
   langage déjà établi (`docs/kor/kor12/`, FRK-58/60) évite de
   re-dériver une frontière déjà posée ailleurs — converger, pas
   dupliquer un raisonnement identique sous un nom différent.
5. `events.py` implémente un pub/sub en-process : un émetteur publie un
   événement nommé, des abonnés enregistrés le reçoivent. Il ne fait ni
   file de messages durable, ni bus distribué, ni traitement du
   contenu de l'événement — c'est un simple registre d'abonnements en
   mémoire.
6. Réponse éliminatoire à corriger : `subscribers.py` relaie
   l'événement vers une route HTTP, il ne l'analyse pas. Affirmer une
   analyse invente une étape de traitement absente du code réel.
7. Parce que ce domaine ne produit aucune preuve mission-éligible
   aujourd'hui — la littératie du touchpoint est certifiable, mais
   aucun chemin FREK n'existe pour ce patron tant qu'aucun humain n'a
   vérifié un passage réel.
8. Parce que certifier une évolution hypothétique reviendrait à
   certifier une capacité non observée dans le code réel — la
   discipline de BRN-15 porte strictement sur ce qui existe
   aujourd'hui, jamais sur une roadmap non implémentée.
