# FRK-20 — Banque N1 (formatif)

Réserve `FRK20.SKILL.*`.

## Offline-first vs. mise en cache (M1)

1. Qu'est-ce que la vérification « offline-first » et pourquoi
   diffère-t-elle d'une simple mise en cache locale de résultat serveur ?
2. Pourquoi une copie en cache d'un résultat serveur n'offre-t-elle
   aucune garantie une fois périmée ? (Elle ne repose sur aucune
   vérification cryptographique locale, seulement sur une copie
   temporaire)

## Store-and-forward (M1)

3. Explique le patron « store-and-forward » : pourquoi une preuve peut
   être vérifiée localement puis synchronisée plus tard sans perte de
   garantie ?
4. La synchronisation différée affecte-t-elle la garantie de la
   vérification locale ? (Non — la vérification locale est complète et
   autosuffisante, la synchronisation est un souci séparé et non
   bloquant)

## Vérification cryptographique locale (M2)

5. Pourquoi une vérification cryptographique locale (signature,
   hash-chain) doit-elle rester possible sans connexion réseau pour
   qu'un système soit réellement offline-first ?

## Discipline CVLN-gap sur `is_remote_enabled()` (M3)

6. Que fait exactement `is_remote_enabled()` dans `frek_core.py` ?
   (Un simple booléen de disponibilité réseau,
   `bool(FREK_CORE_BASE_URL)`, faux par défaut)
7. `is_remote_enabled()` prouve-t-il quoi que ce soit sur la validité
   d'un artefact ? (Non — il décide seulement si un appel distant est
   tenté)
8. Pourquoi ni `frek_core.py` ni aucun système CVLN n'implémente
   aujourd'hui la vérification offline — quelle discipline
   « CVLN-gap » s'applique ici ?

## Corrigé indicatif

1. La vérification offline-first repose sur des garanties
   cryptographiques locales, pas sur une copie temporaire d'un résultat
   déjà validé ailleurs.
2. Elle ne repose sur aucune vérification cryptographique locale.
3. Le store-and-forward sépare la validation locale immédiate de la
   synchronisation différée — la garantie de preuve ne dépend pas du
   moment de la synchronisation.
4. Non — la vérification locale est autosuffisante.
5. Sans vérification cryptographique locale, le système dépend
   silencieusement du réseau — ce qui contredit la promesse
   « offline-first ».
6. Un booléen de disponibilité réseau, `bool(FREK_CORE_BASE_URL)`,
   faux par défaut.
7. Non — il décide seulement si un appel distant est tenté.
8. `frek_core.py` est remote-first avec fallback local simple
   (compteur atomique) — aucune vérification cryptographique locale
   n'existe ; le sujet reste enseigné comme discipline de conception
   marché-générale.
