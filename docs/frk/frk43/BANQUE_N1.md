# FRK-43 — Banque N1 (formatif)

Réserve `FRK43.SKILL.*`.

1. Qu'est-ce que le patron « store-and-forward » (persistance +
   retry-on-failure) et pourquoi est-il indispensable pour une
   livraison fiable dans un système distribué ?
2. Le vrai `frek_id_outbox`/`frek_outbox` de Good Mood (documenté dans
   `docs/gmd/gmd31`/`gmd32`) utilise un calendrier de retry réel
   `[30s, 2m, 10m, 1h, 6h]` — pourquoi ce calendrier progressif
   (backoff) est-il préférable à des tentatives à intervalle fixe ?
2. Pourquoi cet exemple réel (Good Mood) est-il cité comme illustration
   du patron, et non comme une infrastructure « FREK »-brandée ?
4. Que se passe-t-il si toutes les tentatives de retry échouent — quel
   principe de conception doit couvrir ce cas ?

## Corrigé indicatif

1. Le store-and-forward persiste le message localement avant envoi et
   retente en cas d'échec — sans cela, une panne réseau transitoire
   causerait une perte de données définitive.
2. Un backoff progressif espace les tentatives pour éviter de saturer
   un service déjà en difficulté, tout en couvrant les pannes de
   durées variées.
3. Good Mood est un système réel documenté, mais son outbox n'est pas
   une infrastructure FREK — il sert uniquement d'exemple concret et
   vérifié du patron, jamais présenté comme appartenant à FREK.
4. Un principe de dead-letter (mise de côté après épuisement des
   tentatives, pour intervention manuelle) doit couvrir l'échec
   persistant.
