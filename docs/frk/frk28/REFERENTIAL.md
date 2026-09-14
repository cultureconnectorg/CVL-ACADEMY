# FRK-28 — Event Registry & Event-Driven Provenance

## Grounding

Per `FREK_01_75_RECONCILIATION.md` : coverage `NONE (curriculum) /
PARTIAL (repo)`, distinctness `DISTINCT_PROFESSION`, action
`NEW_EXTERNAL`. Contre-exemple réel cité :
`backend/services/events.py` — un bus pub/sub en mémoire, interne à
cette Academy, jamais un registre d'événements de provenance. Ne
jamais confondre les deux.

## Objectives

Un candidat qui complète FRK-28 sait concevoir un vrai registre
d'événements de provenance, en utilisant l'`events.py` réel de cette
Academy comme contre-exemple précis :

- Enseigner l'architecture événementielle de provenance comme
  discipline industrielle réelle (event sourcing, registres
  d'événements de provenance) — patrons marché-général, sans référence
  à un système CVLN spécifique.
- Concevoir un registre append-only : une fois un événement écrit, il
  ne peut plus être modifié ni supprimé — toute correction se fait par
  un nouvel événement compensatoire, jamais par une réécriture.
- Concevoir un chaînage cryptographique ou logique entre événements
  successifs (chaque événement référence le précédent), garantissant
  qu'aucun événement intermédiaire ne peut être inséré ou retiré sans
  briser la chaîne visible.
- Utiliser l'`events.py` réel de cette Academy (un bus pub/sub en
  mémoire alimentant `academy.certification.passed`) comme exemple
  travaillé et *non-provenance* d'architecture événementielle —
  distinguer explicitement et précisément pourquoi un bus pub/sub en
  mémoire ne garantit ni persistance, ni append-only, ni chaînage :
  ses abonnés reçoivent une notification transitoire, sans trace
  durable ni vérifiable après coup.
- Expliquer précisément pourquoi confondre `events.py` avec un
  registre de provenance serait une erreur éliminatoire : cela
  affirmerait qu'une fonctionnalité de provenance existe déjà dans
  cette Academy, alors que `events.py` ne fait que notifier des
  abonnés internes sans laisser aucune trace vérifiable.

## Modules

1. **Fondamentaux de l'architecture événementielle** — event sourcing,
   patrons pub/sub, comme discipline marché-générale.
2. **Conception d'un registre d'événements de provenance** —
   append-only, horodatage, chaînage — les trois garanties qu'un
   pub/sub en mémoire ne fournit pas.
3. **Discipline de frontière vs. `events.py`** — le bus pub/sub réel
   de cette Academy (`academy.certification.passed`), cité comme
   contre-exemple pédagogique précis, jamais comme brique à étendre.

## Assessment

Un exercice de conception d'un registre d'événements de provenance
(append-only, horodaté, chaîné) pour un cas marché-général (ex. chaîne
d'objets culturels), suivi d'une note expliquant précisément pourquoi
`events.py` ne peut pas servir de fondation à ce registre sans
réécriture complète — noté contre la pratique réelle d'architecture
événementielle, avec règle éliminatoire sur tout registre mutable ou
toute confusion avec `events.py`.

## Evidence / mission eligibility

Aucun chemin d'éligibilité mission aujourd'hui.
`FRK28.SKILL.EVENT_PROVENANCE_REGISTRY.L1` réservé une fois
approfondi (voir `EVIDENCE_MODEL.md`).

## Status

`STATUS = PACKAGE_COMPLETE` — référentiel, banques N1/N2, assessment +
rubric, evidence model, 3 guides, cette note d'intégration existent
tous, deepened this pass. `FULLY_COMPLETE` non déclaré — requiert un
passage réel vérifié par un humain.
