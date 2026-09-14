# BRN-15 — Guide Candidat

## Avant de commencer

Prérequis : IOS-07 (partage le même mécanisme de bus d'événements
`events.py`). Lis d'abord son `REFERENTIAL.md` si tu ne l'as pas déjà
fait — la discipline anti-inflation que tu apprends ici s'applique de
la même façon là-bas.

## Ce que tu dois savoir faire

Tracer précisément l'unique touchpoint Brain réel de cette Academy :
l'événement `academy.certification.passed`, émis à
`backend/certification/service.py:140` via le pub/sub en-process de
`backend/services/events.py`, relayé par `subscribers.py` vers la
route `/academy/certification-passed`. Tu dois savoir citer ce chemin
exact, sans inventer d'étape intermédiaire.

Tu dois aussi savoir situer honnêtement le vrai `/brain/ask` de
`metacvln-spec/MetaCVLN` : c'est une preuve qu'un concept de "Brain
CVLN" existe réellement dans l'écosystème — jamais une description de
ce à quoi cette Academy est câblée.

## Comment réviser

1. Lis `REFERENTIAL.md` §Objectives et §Modules.
2. Fais les 8 questions de `BANQUE_N1.md`.
3. Traite les 3 cas de `BANQUE_N2.md`.
4. Relis `EVIDENCE_MODEL.md` pour comprendre pourquoi
   `READY_FOR_FREK_PROOF = FALSE` s'applique ici.

## Pièges les plus fréquents

1. Inventer une étape de traitement (analyse, enrichissement
   contextuel, scoring) entre l'émission et le relais de l'événement —
   élimination automatique.
2. Affirmer que `academy.certification.passed` est câblé à
   `/brain/ask` — élimination automatique. Ce sont deux systèmes non
   reliés ; l'un est réel-interne, l'autre réel-externe, et ils ne se
   touchent pas.
3. Présenter une proposition d'intégration future comme un état actuel
   du système — toujours qualifier explicitement l'hypothétique comme
   tel.

## Règle absolue

Ce touchpoint est un simple abonnement à un événement unique — jamais
un moteur de raisonnement, de contexte, de mémoire, ou de
connaissance. Le langage de frontière que tu emploies est repris
verbatim de `docs/kor/kor12/` et `FREK_01_75_RECONCILIATION.md`
(FRK-58/60) : ne le re-dérive pas, converge vers lui.
