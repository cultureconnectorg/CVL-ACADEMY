# FRK-43 — Store-and-Forward Cultural Infrastructure

## Grounding

Per `FREK_01_75_RECONCILIATION.md` : coverage `NONE`, distinctness
`DISTINCT_SPECIALIZATION`, action `NEW_EXTERNAL`. Proche conceptuellement
du vrai patron outbox (`frek_id_outbox`/`frek_outbox` de Good Mood,
ledger `WalletTransaction` de CVL-ACADEMY) — **réutilisés comme vrais
exemples travaillés de « store-and-forward »**, même si aucun des deux
n'est FREK-brandé.

## Objectives

Un candidat qui complète FRK-43 sait concevoir une infrastructure
store-and-forward réelle, en utilisant l'exemple réel de Good Mood
comme illustration précisément bornée :

- Enseigner la conception réelle d'infrastructure store-and-forward
  (livraison persistante avec retry sur échec) comme discipline
  industrielle marché-générale.
- Concevoir un mécanisme de persistance locale avant envoi : sans
  cette persistance, une panne réseau transitoire causerait une perte
  de données définitive — le message doit survivre à l'indisponibilité
  temporaire du destinataire.
- Concevoir un calendrier de retry à backoff progressif (espacement
  croissant entre tentatives), en s'appuyant sur le vrai calendrier de
  Good Mood (`frek_id_outbox`/`frek_outbox`, documenté dans
  `docs/gmd/gmd31`/`gmd32`) — `[30s, 2m, 10m, 1h, 6h]` — et expliquer
  précisément pourquoi ce calendrier progressif est préférable à des
  tentatives à intervalle fixe : il évite de saturer un service déjà
  en difficulté tout en couvrant des pannes de durées variées.
- Concevoir un mécanisme de dead-letter : que faire lorsque toutes les
  tentatives du calendrier de retry sont épuisées — mise de côté du
  message pour intervention manuelle, jamais une perte silencieuse.
- Utiliser l'exemple réel de Good Mood (`frek_id_outbox`/
  `frek_outbox`) comme illustration travaillée et vérifiée du patron
  — en précisant explicitement qu'il s'agit d'un système réel mais
  jamais FREK-brandé ni une infrastructure FREK : citer ce calendrier
  précis comme preuve du patron, jamais comme une brique FREK à
  étendre.
- Expliquer précisément pourquoi présenter l'outbox de Good Mood comme
  une infrastructure FREK serait une erreur éliminatoire : cela
  affirmerait une appartenance ou un branding qui n'existe pas — Good
  Mood reste un système tiers documenté, cité par référence
  uniquement.

## Modules

1. **Fondamentaux de conception store-and-forward** — persistance
   locale avant envoi, retry sur échec, comme discipline
   marché-générale.
2. **Littératie retry/backoff** — ancrée dans le vrai calendrier
   `[30s, 2m, 10m, 1h, 6h]` de Good Mood, comme preuve concrète du
   patron backoff progressif.
3. **Discipline de l'exemple travaillé** — utiliser un système réel
   mais non-FREK-brandé comme illustration, sans jamais impliquer
   qu'il s'agit d'infrastructure FREK.

## Assessment

Un exercice de conception d'un mécanisme de livraison persistante avec
backoff progressif et dead-letter, en citant le calendrier réel de
Good Mood comme exemple travaillé — noté contre la pratique réelle de
store-and-forward, avec règle éliminatoire sur toute présentation de
l'outbox de Good Mood comme infrastructure FREK, ou toute absence de
mécanisme d'échec persistant.

## Evidence / mission eligibility

Base pour FRK-44 (récupération/synchronisation) — réutilisé par
référence. Aucun chemin d'éligibilité mission aujourd'hui.
`FRK43.SKILL.STORE_AND_FORWARD.L1` réservé une fois approfondi (voir
`EVIDENCE_MODEL.md`).

## Status

`STATUS = PACKAGE_COMPLETE` — référentiel, banques N1/N2, assessment +
rubric, evidence model, 3 guides, cette note d'intégration existent
tous, deepened this pass. `FULLY_COMPLETE` non déclaré — requiert un
passage réel vérifié par un humain.
