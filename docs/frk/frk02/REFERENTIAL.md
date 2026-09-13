# FRK-02 — FREKCORE Architecture & Ecosystem

## Grounding

Per `FREK_01_75_RECONCILIATION.md` : coverage `NONE`, distinctness
`DISTINCT_PROFESSION`, action `NEW_EXTERNAL`. Contrainte explicite de
vérité-dépôt : le contenu doit rester borné à ce que `frek_core.py`
fait réellement (mint/signal/proof-stub/stade) — **jamais** inventer
une architecture DID/VC/provenance-graphe comme si elle était
construite, même si ces concepts apparaissent dans la carte candidate
Master 2D plus large.

## Prerequisites

FRK-01, FRK-58.

## Objectives

Un candidat qui complète FRK-02 sait décrire précisément le
positionnement architectural réel de FREKCORE tel que vu par cette
Academy, sans jamais inventer de capacité inexistante :

- Expliquer l'architecture réelle de FREKCORE *telle que la voit le
  client de cette Academy* : une frontière de service mince,
  remote-first/local-fallback, pas un réseau d'identité distribué
  complet.
- Distinguer la vue côté client (territoire de FRK-01/58) de la
  question architecturale au niveau écosystème que cette formation
  traite réellement : comment FREKCORE se positionne conceptuellement
  parmi les autres systèmes CVLN (Wallet, KORA, Agent Factory) — sans
  jamais affirmer de câblage entre eux qui ne serait pas observé.
- Citer précisément la phrase du docstring de `frek_core.py` qui
  définit son rôle architectural : « the sole boundary through which
  the app talks to FrekCore » — l'unique frontière par laquelle
  l'application parle à FrekCore, pas un réseau distribué.
- Ne jamais affirmer que DID/VC, graphes de provenance, ou le format
  d'objet `.fk` sont implémentés où que ce soit dans ce dépôt — ce
  sont de vrais concepts candidats de la carte Master 2D, pas une
  architecture livrée.
- Expliquer précisément la différence d'altitude entre FRK-01 et
  FRK-02 : FRK-01 couvre le system map opérationnel des 5 méthodes ;
  FRK-02 couvre le positionnement architectural conceptuel de FREKCORE
  parmi les autres systèmes CVLN — deux niveaux d'analyse distincts et
  complémentaires, jamais confondus.
- Expliquer précisément pourquoi affirmer une architecture inventée
  (DID/VC/provenance-graphe construits, ou un câblage observé avec
  Wallet/KORA/Agent Factory) serait une erreur éliminatoire : cela
  affirmerait une capacité qui n'existe nulle part dans ce dépôt.

## Modules

1. **Architecture de frontière client** (ancrée dans le docstring
   propre de `frek_core.py` : « the sole boundary through which the
   app talks to FrekCore »).
2. **Positionnement écosystème** — comment FREKCORE-en-tant-que-client
   se rapporte conceptuellement à Wallet/KORA/Agent Factory, en citant
   uniquement le (non-)câblage observé.
3. **Discipline de portée** — liste explicite de ce qui n'est PAS
   implémenté où que ce soit dans ce dépôt (DID/VC, graphes de
   provenance, format `.fk`).

## Assessment

Un brief de positionnement : le candidat explique l'architecture
réelle de FREKCORE à un nouvel employé sans surestimer la portée —
échec éliminatoire pour toute affirmation d'une capacité non
implémentée comme réelle.

## Evidence / mission eligibility

Aucun chemin d'éligibilité mission aujourd'hui. `FRK02.SKILL.
ARCHITECTURE_POSITIONING` réservé une fois approfondi.

## Status

`STATUS = PACKAGE_COMPLETE` — référentiel, banques N1/N2, assessment +
rubric, evidence model, 3 guides, cette note d'intégration existent
tous, deepened this pass. `FULLY_COMPLETE` non déclaré — requiert un
passage réel vérifié par un humain.
