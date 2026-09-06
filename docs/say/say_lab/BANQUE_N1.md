# SAY-LAB — Banque N1 (formatif)

Réserve `SAYLAB.SKILL.*`.

1. Pourquoi `SAY-LAB` réutilise-t-il `GMD-22/24/27/28` plutôt que de
   réinventer un backend fictif pour l'artiste DJ Sayd ?
2. Quelle est la frontière entre la compétence "artiste" (DJ Sayd) et
   la compétence "opérateur plateforme" (Good Mood) dans ce capstone ?
3. Pourquoi serait-il une erreur éliminatoire d'inventer une capacité
   (ex. moteur de fidélité, calcul de royalties) absente du vrai repo
   `gmfest972/goodmooddjsayd` ?
4. En quoi ce capstone prouve-t-il que Good Mood et DJ Sayd sont une
   seule histoire racontée des deux côtés, jamais deux Academies
   parallèles ?

## Corrigé indicatif

1. Parce que `gmfest972/goodmooddjsayd` est un repo réel déjà audité
   — utiliser un backend fictif inventerait une capacité, contraire à
   la discipline de ce Master Package.
2. L'artiste (DJ Sayd) raisonne sur son propre parcours créatif/
   commercial ; l'opérateur (Good Mood) lit les routes/modèles réels
   du côté plateforme — les deux compétences sont complémentaires,
   jamais fusionnées en une seule.
3. Cela affirmerait une capacité produit inexistante — contraire à la
   discipline `CAPABILITY_NOT_IMPLEMENTED`/`FAKE_PRODUCT_CAPABILITY`.
4. Parce que le même backend réel (`GMD-22/24/27/28`) sert de preuve
   travaillée aux deux domaines — la réutilisation par référence,
   jamais la duplication, démontre leur cohérence.
