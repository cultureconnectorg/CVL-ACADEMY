# FRK-17 — Banque N1 (formatif)

Réserve `FRK17.SKILL.*`.

1. Qu'apporte un horodatage de confiance (RFC 3161 ou équivalent) qu'un
   simple timestamp local ne peut pas garantir ?
2. Pourquoi une autorité d'horodatage (TSA) doit-elle être tierce et
   vérifiable, et pas simplement « une base de données qui enregistre
   une date » ?
3. Explique pourquoi `issue_proof()` (`frek_core.py`) — qui génère un
   simple UUID sans horodatage cryptographique tiers — ne peut jamais
   être présenté comme une implémentation d'ancrage temporel de
   confiance.
4. Quelle est la différence entre « vérifier un ancrage temporel » et
   « faire confiance à une date affichée » ?

## Corrigé indicatif

1. Un horodatage de confiance lie cryptographiquement l'artefact à un
   instant attesté par une autorité tierce, vérifiable indépendamment.
2. Sans tiers indépendant, rien n'empêche de falsifier la date a
   posteriori — la garantie vient de la vérifiabilité externe.
3. `issue_proof()` ne produit qu'un identifiant opaque sans lien
   cryptographique à un instant attesté — l'écart avec RFC 3161 est
   total, pas une nuance d'implémentation.
4. Vérifier suppose de rejouer la preuve cryptographique auprès de la
   TSA (ou de la structure d'ancrage) ; faire confiance à une date
   affichée n'offre aucune garantie.
