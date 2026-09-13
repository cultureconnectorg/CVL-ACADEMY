# BRN-15 — CVLN Brain Touchpoint Operator

## Repo truth this formation is built on

Grounded directly in the one real Brain touchpoint in this Academy :
`backend/certification/service.py:140` émet `academy.certification.
passed` via le pub/sub en-process de `backend/services/events.py`, et
`subscribers.py` le relaie vers `/academy/certification-passed`. Per
`AGENT_FACTORY_IOS_BRAIN_CMD_LAURENTIA_RECONCILIATION.md` : coverage
`PARTIAL (real academy.certification.passed touchpoint)`, action
`NEW_INTERNAL`, « buildable now — reuse the boundary language already
established in `docs/kor/kor12/` and `FREK_01_75_RECONCILIATION.md`
(FRK-58/60) verbatim... converge, don't re-derive ».

**Contexte de marché, jamais le substrat opérant** : le vrai
`/brain/ask` de `metacvln-spec/MetaCVLN` (une vraie route
d'interface Brain, confirmée par grep cette session) est cité comme
preuve qu'un vrai concept de Brain CVLN existe dans l'écosystème —
jamais comme ce à quoi l'événement `academy.certification.passed` de
cette Academy serait câblé.

## Prerequisites

IOS-07 (partage le même mécanisme de bus d'événements).

## Objectives

Un candidat qui complète BRN-15 sait tracer précisément l'unique
touchpoint Brain réel de cette Academy, sans jamais l'inflater en
moteur de raisonnement :

- Opérer l'unique touchpoint Brain réel de cette Academy : un seul
  événement (`academy.certification.passed`) émis à la réussite d'une
  certification, relayé vers une seule route.
- Tracer précisément le chemin réel de cet événement depuis son
  émission jusqu'à sa relève : `backend/certification/service.py:140`
  émet l'événement via `backend/services/events.py` (pub/sub
  en-process), relayé par `subscribers.py` vers la route
  `/academy/certification-passed` — sans inventer d'étape
  intermédiaire (analyse, enrichissement contextuel) absente du code
  réel.
- Ne jamais affirmer que ceci constitue un moteur de
  raisonnement/contexte/mémoire/connaissance — c'est un simple
  abonnement à un événement, rien de plus.
- Citer le vrai `/brain/ask` de `MetaCVLN` comme preuve que le concept
  plus large de « CVLN Brain » est réel ailleurs dans l'écosystème,
  jamais comme une capacité opérante de cette Academy elle-même.
- Expliquer précisément pourquoi cette formation partage son mécanisme
  sous-jacent avec IOS-07, et pourquoi le langage de frontière est
  repris verbatim de `docs/kor/kor12/` plutôt que re-dérivé : IOS-07
  et BRN-15 reposent sur le même bus `events.py` ; reprendre le
  langage déjà établi ailleurs (FRK-58/60) évite de re-dériver une
  frontière déjà posée — converger, pas dupliquer.
- Expliquer précisément pourquoi affirmer un câblage entre cet
  événement et `/brain/ask` serait une erreur éliminatoire : aucune
  intégration observée ne relie les deux — les fusionner inventerait
  un câblage inexistant.

## Modules

1. **Littératie de l'événement `academy.certification.passed`** —
   trace précise émission → bus → relais.
2. **Discipline de touchpoint unique** — ne jamais inflater en moteur
   de raisonnement.
3. **Contexte de marché** — le vrai `/brain/ask` de `MetaCVLN` cité
   honnêtement, jamais comme capacité opérante de cette Academy.

## Assessment

Un exercice de littératie de touchpoint : le candidat trace l'événement
depuis `certification/service.py:140` à travers `events.py` jusqu'à
`subscribers.py` — échec éliminatoire pour toute affirmation qu'un
moteur de raisonnement existe, ou tout câblage inventé vers
`/brain/ask`.

## Evidence / mission eligibility

`BRN15.SKILL.BRAIN_TOUCHPOINT_OPERATOR.L1` réservé une fois approfondi.
Aucun chemin d'éligibilité mission aujourd'hui.

## Status

`STATUS = PACKAGE_COMPLETE` — référentiel, banques N1/N2, assessment +
rubric, evidence model, 3 guides, cette note d'intégration existent
tous, deepened this pass. `FULLY_COMPLETE` non déclaré — requiert un
passage réel vérifié par un humain.
