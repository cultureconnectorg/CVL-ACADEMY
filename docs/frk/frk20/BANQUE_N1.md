# FRK-20 — Banque N1 (formatif)

Réserve `FRK20.SKILL.*`.

1. Qu'est-ce que la vérification « offline-first » et pourquoi
   diffère-t-elle d'une simple mise en cache locale de résultat serveur ?
2. Explique le patron « store-and-forward » : pourquoi une preuve peut
   être vérifiée localement puis synchronisée plus tard sans perte de
   garantie ?
3. Pourquoi une vérification cryptographique locale (signature,
   hash-chain) doit-elle rester possible sans connexion réseau pour
   qu'un système soit réellement offline-first ?
4. Pourquoi ni `frek_core.py` ni aucun système CVLN n'implémente
   aujourd'hui la vérification offline — quelle discipline
   « CVLN-gap » s'applique ici ?

## Corrigé indicatif

1. La vérification offline-first repose sur des garanties
   cryptographiques locales, pas sur une copie temporaire d'un résultat
   déjà validé ailleurs.
2. Le store-and-forward sépare la validation locale immédiate de la
   synchronisation différée — la garantie de preuve ne dépend pas du
   moment de la synchronisation.
3. Sans vérification cryptographique locale, le système dépend
   silencieusement du réseau — ce qui contredit la promesse
   « offline-first ».
4. `frek_core.py` est remote-first avec fallback local simple
   (compteur atomique) — aucune vérification cryptographique locale
   n'existe ; le sujet reste enseigné comme discipline de conception
   marché-générale.
