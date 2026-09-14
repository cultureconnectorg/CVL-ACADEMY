# FRK-17 — Banque N1 (formatif)

Réserve `FRK17.SKILL.*`.

## Modèle de confiance (M1)

1. Qu'apporte un horodatage de confiance (RFC 3161 ou équivalent) qu'un
   simple timestamp local ne peut pas garantir ?
2. Pourquoi une autorité d'horodatage (TSA) doit-elle être tierce et
   vérifiable, et pas simplement « une base de données qui enregistre
   une date » ?

## Structure du jeton (M2)

3. Cite les 4 champs d'un jeton RFC 3161. (Hash de l'artefact,
   horodatage, identité de la TSA, signature sur l'ensemble)
4. Que se passe-t-il si la signature est retirée du jeton ? (Le jeton
   devient une simple affirmation non vérifiable)
5. Décris les étapes de vérification manuelle d'un jeton sans outil.
   (Recalculer le hash de l'artefact, confirmer qu'il correspond au
   hash du jeton, vérifier la signature de la TSA sur le contenu du
   jeton avec sa clé publique connue)

## Vérification vs. confiance de façade (M2)

6. Quelle est la différence entre « vérifier un ancrage temporel » et
   « faire confiance à une date affichée » ?

## Frontière FRK-13 (M3)

7. Explique pourquoi `issue_proof()` (`frek_core.py`) — qui génère un
   simple UUID sans horodatage cryptographique tiers — ne peut jamais
   être présenté comme une implémentation d'ancrage temporel de
   confiance.
8. L'écart entre `issue_proof()` et RFC 3161 est-il une nuance
   d'implémentation ou un écart total ? (Total — aucun lien
   cryptographique à un instant attesté n'existe dans `issue_proof()`)

## Corrigé indicatif

1. Un horodatage de confiance lie cryptographiquement l'artefact à un
   instant attesté par une autorité tierce, vérifiable indépendamment.
2. Sans tiers indépendant, rien n'empêche de falsifier la date a
   posteriori — la garantie vient de la vérifiabilité externe.
3. Hash de l'artefact, horodatage, identité de la TSA, signature.
4. Le jeton devient une affirmation non vérifiable.
5. Recalcul du hash → correspondance avec le hash du jeton →
   vérification de la signature TSA avec sa clé publique.
6. Vérifier suppose de rejouer la preuve cryptographique auprès de la
   TSA (ou de la structure d'ancrage) ; faire confiance à une date
   affichée n'offre aucune garantie.
7. `issue_proof()` ne produit qu'un identifiant opaque sans lien
   cryptographique à un instant attesté — l'écart avec RFC 3161 est
   total, pas une nuance d'implémentation.
8. Total.
