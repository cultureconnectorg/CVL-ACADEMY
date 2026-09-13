# FRK-60 — FREK × Intelligence OS & Agent Infrastructure

## Grounding

Per `FREK_01_75_RECONCILIATION.md` : coverage `NONE`, distinctness
`CROSS_ECOSYSTEM_ROLE`, action `NEW_CROSS_ECOSYSTEM`. Les deux côtés
de ce pont sont des stubs génériques (`services/integrations/
registry.py` côté écosystème, `frek_core.py` côté FREK) — construit
comme un pont conceptuel seulement, explicitement signalé
`CAPABILITY_NOT_IMPLEMENTED` des deux côtés.

## Objectives

Un candidat qui complète FRK-60 sait expliquer précisément pourquoi
cette formation enseigne une relation architecturale possible, jamais
un système qui fonctionne aujourd'hui :

- Expliquer avec précision pourquoi ce sujet est un « pont
  conceptuel » et non une intégration réelle : aucune ligne de code ne
  relie fonctionnellement FREK et une infrastructure d'agents/OS
  d'intelligence — la formation documente une architecture possible,
  jamais un flux exécutable.
- Décrire séparément et précisément la nature réelle de chacun des
  deux artefacts cités : `frek_core.py` est un client Python interne,
  appelé en-process par le backend de cette Academy, sans surface
  HTTP ou externe propre ; `services/integrations/registry.py` est une
  configuration d'intégration écosystème générique, sans câblage
  FREK-spécifique réel — un stub de registre, pas un connecteur
  fonctionnel.
- Confirmer que ces deux stubs sont insuffisants **individuellement et
  ensemble** pour constituer une intégration : la présence des deux
  artefacts dans le code ne rapproche pas plus une intégration réelle
  que la présence d'un seul — additionner deux stubs ne produit pas un
  système qui fonctionne.
- Documenter précisément ce qu'une intégration réelle exigerait, sans
  jamais la construire dans le cadre de cette formation : (1) un
  schéma d'échange défini entre FREK et l'infrastructure d'agents
  (format de message, champs obligatoires, versionnage) ; (2) une
  authentification mutuelle (chaque côté doit pouvoir vérifier
  l'identité de l'autre, pas une simple clé partagée statique) ; (3)
  un contrat d'erreur partagé (codes d'erreur et sémantique communs
  aux deux systèmes, pour qu'un échec côté FREK soit interprétable
  côté agent, et réciproquement).
- Expliquer pourquoi affirmer qu'un agent Intelligence OS peut
  aujourd'hui consommer un signal FREK, ou que `frek_core.py` expose
  une interface prête pour l'infrastructure d'agents, est une erreur
  éliminatoire : cela affirmerait une capacité côté FREK ET côté
  écosystème qui n'existe ni dans l'un ni dans l'autre.

## Modules

1. **Architecture du pont conceptuel** — ce que signifie « relation
   architecturale documentée mais non construite » ; pourquoi les deux
   côtés stub-level ne se substituent jamais à une intégration réelle.
2. **Nature réelle des deux stubs, séparément** — `frek_core.py`
   (client interne, aucune surface externe) et
   `services/integrations/registry.py` (configuration générique, sans
   câblage FREK) décrits chacun avec précision, jamais fusionnés en un
   seul artefact flou.
3. **Discipline `CAPABILITY_NOT_IMPLEMENTED` des deux côtés** —
   pourquoi la règle éliminatoire s'applique à toute affirmation de
   câblage fonctionnel, côté FREK comme côté écosystème.
4. **Exigences d'une future intégration (documentées, non construites)**
   — schéma d'échange, authentification mutuelle, contrat d'erreur
   partagé : rédigés comme spécification, jamais présentés comme
   livrés.

## Assessment

Un exercice de documentation architecturale : le candidat rédige les
exigences d'une future intégration FREK↔Intelligence OS (schéma
d'échange, authentification, contrat d'erreur) sans jamais l'affirmer
construite, puis explique séparément pourquoi chacun des deux stubs
cités est, à lui seul, insuffisant — noté avec règle éliminatoire sur
toute affirmation de câblage fonctionnel existant, d'un côté ou de
l'autre.

## Evidence / mission eligibility

Aucun chemin d'éligibilité mission aujourd'hui.
`FRK60.SKILL.FREK_INTELLIGENCE_OS_BRIDGE.L1` réservé une fois
approfondi (voir `EVIDENCE_MODEL.md`).

## Status

`STATUS = PACKAGE_COMPLETE` — référentiel, banques N1/N2, assessment +
rubric, evidence model, 3 guides, cette note d'intégration existent
tous, deepened this pass. `FULLY_COMPLETE` non déclaré — requiert un
passage réel vérifié par un humain.
