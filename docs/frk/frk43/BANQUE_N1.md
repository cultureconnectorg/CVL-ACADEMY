# FRK-43 — Banque N1 (formatif)

Réserve `FRK43.SKILL.*`.

1. Qu'est-ce que le patron « store-and-forward » (persistance +
   retry-on-failure) et pourquoi est-il indispensable pour une
   livraison fiable dans un système distribué ?
2. Le vrai `frek_id_outbox`/`frek_outbox` de Good Mood (documenté dans
   `docs/gmd/gmd31`/`gmd32`) utilise un calendrier de retry réel
   `[30s, 2m, 10m, 1h, 6h]` — pourquoi ce calendrier progressif
   (backoff) est-il préférable à des tentatives à intervalle fixe ?
3. Pourquoi cet exemple réel (Good Mood) est-il cité comme illustration
   du patron, et non comme une infrastructure « FREK »-brandée ?
4. Que se passe-t-il si toutes les tentatives de retry échouent — quel
   principe de conception doit couvrir ce cas ?
5. Pourquoi la persistance locale du message doit-elle précéder toute
   tentative d'envoi, plutôt que de retenter directement depuis la
   mémoire ?
6. Quelle est la différence de comportement entre un backoff fixe (ex.
   retenter toutes les 30 secondes indéfiniment) et un backoff
   progressif face à une panne de 4 heures du destinataire ?
7. Pourquoi FRK-44 (récupération/synchronisation) peut-il réutiliser
   le mécanisme store-and-forward de FRK-43 par référence plutôt que
   d'en reconcevoir un ?
8. En quoi le ledger `WalletTransaction` de CVL-ACADEMY, cité dans le
   grounding, illustre-t-il aussi ce patron sans être davantage une
   infrastructure FREK que l'outbox de Good Mood ?

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
5. Sans persistance locale préalable, un crash du processus entre deux
   tentatives ferait perdre le message définitivement — la persistance
   garantit la survie du message indépendamment de l'état du
   processus émetteur.
6. Un backoff fixe continuerait à solliciter un service en panne
   toutes les 30 secondes pendant 4 heures (480 tentatives inutiles) ;
   un backoff progressif espace rapidement les tentatives, réduisant
   la charge tout en couvrant la même durée.
7. Parce que le mécanisme est générique (persistance + retry +
   dead-letter), indépendant du contenu spécifique synchronisé — la
   réutilisation par référence évite la duplication.
8. Le ledger `WalletTransaction` applique le même patron générique
   (persistance avant traitement) dans un contexte différent — sa
   présence dans ce dépôt ne le rend pas davantage FREK-brandé que
   l'outbox de Good Mood.
