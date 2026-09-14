# FRK-54 — Event Bus, Webhooks & Integration Contracts

## Grounding

Per `FREK_01_75_RECONCILIATION.md` : coverage `NONE (curriculum) /
PARTIAL (repo, services/events.py)`, distinctness
`DISTINCT_PROFESSION`, action `NEW_EXTERNAL`. Un vrai bus pub/sub
générique en-process existe dans ce dépôt (`events.py`, alimente
`academy.certification.passed`) — utilisable comme exemple travaillé
authentique (petit), mais c'est le bus événementiel propre à cette
Academy, jamais un bus FREK ; la frontière doit être explicite.

## Objectives

Un candidat qui complète FRK-54 sait concevoir un bus d'événements et
des contrats d'intégration webhook réels, en utilisant l'`events.py`
réel de cette Academy comme exemple travaillé précisément borné :

- Enseigner la conception réelle de bus d'événements/webhooks/contrats
  d'intégration comme discipline industrielle marché-générale — sans
  référence à un système CVLN spécifique.
- Distinguer précisément un bus d'événements (diffusion interne,
  souvent en mémoire) d'un webhook (poussée HTTP active vers un
  système externe) — deux mécanismes de diffusion aux garanties
  différentes.
- Concevoir un contrat d'intégration stable : un schéma d'événement
  versionné, documenté, dont l'évolution ne casse jamais
  silencieusement les consommateurs externes existants.
- Utiliser l'`events.py` réel de cette Academy (bus pub/sub en-process,
  alimentant `academy.certification.passed`) comme exemple travaillé
  et petit du patron pub/sub — en précisant explicitement qu'il s'agit
  du bus interne propre à cette Academy, jamais un système
  FREK-branded, et qu'il n'a aucune surface webhook ou d'intégration
  externe aujourd'hui.
- Expliquer précisément pourquoi présenter `events.py` comme une
  infrastructure webhook ou FREK, ou affirmer qu'il notifie déjà des
  systèmes externes, serait une erreur éliminatoire : cela
  affirmerait une capacité d'intégration externe qui n'existe pas —
  `events.py` reste un pub/sub interne, sans aucune route HTTP externe
  ni contrat de webhook.

## Modules

1. **Fondamentaux de conception de bus d'événements** — diffusion
   interne, patrons pub/sub, comme discipline marché-générale.
2. **Patrons webhooks/contrats d'intégration (marché-général)** —
   schéma d'événement versionné, garanties de compatibilité
   ascendante.
3. **Discipline de l'exemple travaillé** — `events.py` comme
   illustration uniquement, jamais présenté comme infrastructure FREK
   ou surface webhook.

## Assessment

Un exercice de conception : un contrat d'intégration webhook versionné
pour un système marché-général, en citant `events.py` comme
illustration du patron pub/sub sous-jacent — noté contre la pratique
réelle de conception de bus d'événements, avec règle éliminatoire sur
toute présentation d'`events.py` comme infrastructure webhook ou FREK.

## Evidence / mission eligibility

Base pour FRK-55 (standards transversaux) — réutilisé par référence.
Aucun chemin d'éligibilité mission aujourd'hui.
`FRK54.SKILL.EVENT_BUS_WEBHOOK_CONTRACTS.L1` réservé une fois
approfondi (voir `EVIDENCE_MODEL.md`).

## Status

`STATUS = PACKAGE_COMPLETE` — référentiel, banques N1/N2, assessment +
rubric, evidence model, 3 guides, cette note d'intégration existent
tous, deepened this pass. `FULLY_COMPLETE` non déclaré — requiert un
passage réel vérifié par un humain.
