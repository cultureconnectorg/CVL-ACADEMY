# FRK-52 — Banque N1 (formatif)

Réserve `FRK52.SKILL.*`.

## Grounding réel de `frek_core.py` (M3)

1. Confirme précisément : `frek_core.py` expose-t-il aujourd'hui une
   API HTTP publique ? Justifie en citant sa vraie nature (client
   Python interne, appelé en-process).
2. Comment s'appelle la classe réelle qui constitue `frek_core.py` ?
   (`FrekCoreClient`)

## Versionnage (M2)

3. Qu'est-ce que le versionnage d'API (ex. `/v1/`, en-tête de version)
   et pourquoi est-il indispensable dès la première mise en production
   d'une API réelle ?
4. Que se passe-t-il sans stratégie de versionnage ? (Tout changement
   d'interface casse silencieusement les intégrateurs existants)

## Gestion d'erreur (M2)

5. Cite un principe réel de gestion d'erreur d'API (ex. codes HTTP
   sémantiques, structure d'erreur cohérente) et explique pourquoi son
   absence casse l'expérience développeur.
6. Les codes 404 et 409 sont-ils interchangeables ? (Non — chaque code
   doit être choisi de façon sémantiquement précise)

## Discipline de gap (M3)

7. Pourquoi serait-il une erreur éliminatoire d'affirmer que
   `frek_core.py` « expose une API REST » dans une copie ?

## Corrigé indicatif

1. Non — `frek_core.py` est un `FrekCoreClient`, un client Python
   interne appelé en-process par le backend de l'Academy ; il n'a
   aucune route HTTP propre.
2. `FrekCoreClient`.
3. Le versionnage protège les clients existants d'un changement
   d'interface — sans lui, toute évolution casserait silencieusement
   les intégrateurs.
4. Tout changement d'interface casse silencieusement les intégrateurs.
5. Des codes HTTP sémantiques et une structure d'erreur cohérente
   permettent au développeur intégrateur de traiter les erreurs
   automatiquement plutôt que de deviner leur cause.
6. Non — chaque code doit être choisi de façon sémantiquement précise.
7. Cela affirmerait une capacité technique inexistante — la discipline
   `CVLN-gap` interdit explicitement ce type d'invention.
