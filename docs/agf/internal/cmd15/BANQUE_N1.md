# CMD-15 — Banque N1 (formative, M1→M4)

```
Sourced against metacvln-spec/MetaCVLN, commit b36a893049576ce9cf00
da778efd4724fb469670, backend/server.py (already directly grep-
confirmed this session — REPO_REGISTRY.md), never re-cited from
memory.
```

## M1 — `/command-center/overview`

1. À quelle ligne du fichier `backend/server.py` la route
   `/command-center/overview` a-t-elle été confirmée par grep direct
   cette session ? (Ligne 184)
2. Cette route fait-elle partie d'un mockup ou d'un backend FastAPI
   réel ? (Un backend FastAPI réel, 1,611 lignes, ~50 routes au
   total)
3. Le contenu exact du payload retourné par cette route a-t-il été lu
   ligne par ligne cette session, ou seulement la présence de la route
   confirmée ? (Seulement la présence de la route et le contexte
   général du backend confirmés — le détail exact du payload n'a pas
   été cité verbatim, ne jamais l'inventer)

## M2 — `/command-center/timeline`

4. À quelle ligne cette route a-t-elle été confirmée ? (Ligne 221)
5. Sur quel mécanisme réel du même backend cette timeline s'appuie-
   t-elle vraisemblablement ? (Le bus d'événements réel signé
   Ed25519, et le suivi d'état runtime `normal`/`degraded`/`critical`
   — tous deux réels dans le même backend)

## M3 — frontière de maturité

6. Quel était le verdict *avant* la correction Wave 2 de cette
   session pour CMD-15 ? (`BLOCKED_PRODUCT_DEPENDENCY` — "aucun
   Command Center CVLN réel n'existe à opérer")
7. Quel est le verdict *après* correction ? (`NEW_INTERNAL`, maturité
   `PARTIAL` — les routes réelles existent, mais restent
   `PRODUCT_DEPENDENCY`, jamais `BLOCKED` sur "rien n'existe")
8. `MetaCVLN` est-il déclaré `DEPLOYED_RUNTIME` par son propre audit ?
   (Non — son propre `IMPLEMENTATION-STATUS.md` déclare qu'aucun
   composant v1.0 n'est affirmé `DEPLOYED_RUNTIME`, et que "rien
   d'audité ne dépend de lui")
9. Cette Academy a-t-elle un accès opérationnel réel à `MetaCVLN` ?
   (Non — aucune intégration observée, aucun accès réel)

## M4 — discipline des trois systèmes

10. Nomme les trois systèmes distincts qui partagent le terme
    "command center" ou une discipline proche dans ce chantier, et
    explique en une phrase chacun. (1. `fms-os/fms`'s `/os/command-
    center` — tableau de bord opérationnel de studio, sans rapport ;
    2. `MetaCVLN`'s `/command-center/overview`/`/timeline` — le vrai
    Command Center CVLN, réel mais non opérable par cette Academy ;
    3. `external/cmd01_14` — discipline SRE/ICS marché-générale,
    indépendante de l'existence de l'un ou l'autre)
