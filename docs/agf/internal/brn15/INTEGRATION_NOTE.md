# BRN-15 — Integration Academy Package Note

## Réel vs. supposé

**Réel :** `backend/certification/service.py:140` émet
`academy.certification.passed` via `backend/services/events.py`
(pub/sub en-process), relayé par `subscribers.py` vers la route
`/academy/certification-passed`. C'est l'unique touchpoint Brain réel
de cette Academy — ni plus, ni moins qu'un abonnement à un événement.

**Réel, mais externe et non câblé :** le vrai `/brain/ask` de
`metacvln-spec/MetaCVLN` (grep-confirmé cette session) — une preuve
que le concept de "Brain CVLN" existe dans l'écosystème, jamais une
description de cette Academy.

**Supposé :** un moteur de raisonnement/contexte/mémoire/connaissance
dans cette Academy, ou un câblage entre `academy.certification.passed`
et `/brain/ask` — ni l'un ni l'autre n'existe dans le code réel
(`NO_RUNTIME_BINDING`).

## Dépendances

`AGENT_FACTORY_IOS_BRAIN_CMD_LAURENTIA_RECONCILIATION.md`,
`docs/agf/internal/ios07/REFERENTIAL.md` (prérequis, même mécanisme de
bus `events.py`), `docs/kor/kor12/REFERENTIAL.md` (langage de
frontière repris verbatim), `docs/frk/frk58/`, `frk60/REFERENTIAL.md`
(convergence documentaire — même discipline de frontière, pas de
re-dérivation).

## Ce qu'une future évolution exigerait

1. Une décision produit explicite avant tout câblage vers un système
   Brain externe — hors périmètre de cette formation aujourd'hui.
2. Une nouvelle formation ou une révision explicite documentant le
   nouvel état, jamais une extension silencieuse de BRN-15.
3. Un correcteur humain réévaluant la formation à la lumière du
   nouveau périmètre, si celui-ci se matérialisait.

## Status

`STATUS = PACKAGE_COMPLETE` — référentiel, banques N1/N2, assessment +
rubric, evidence model, 3 guides, cette note d'intégration existent
tous, deepened this pass. `FULLY_COMPLETE` non déclaré — requiert un
passage réel vérifié par un humain.
