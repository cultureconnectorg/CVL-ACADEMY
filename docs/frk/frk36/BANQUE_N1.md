# FRK-36 — Banque N1 (formatif)

Réserve `FRK36.SKILL.*`.

1. Qu'est-ce que la capture authentique de média (preuve d'intégrité
   dès l'origine, avant tout traitement) au sens marché-général ?
2. Pourquoi cette formation enseigne-t-elle ce concept indépendamment
   de FREKRAW, alors que FREKRAW est le nom cité dans
   `FREK_01_75_RECONCILIATION.md` ?
3. Qu'est-ce que `NEEDS_REPO_AUDIT` signifie concrètement ici (recherche
   exhaustive par grep dans `backend/`, `docs/`, `frekcoreAout2026`,
   `fms-os/fms`, `gmfest972/goodmooddjsayd` — zéro résultat) ?
4. Pourquoi serait-il une erreur éliminatoire d'affirmer que FREKRAW
   « fonctionne de telle manière » dans une copie ?

## Corrigé indicatif

1. La capture authentique intègre des preuves d'intégrité (hash,
   signature, horodatage) au moment même de la capture, pas après
   coup — rendant toute altération ultérieure détectable.
2. Le concept est réel et enseignable indépendamment de toute
   implémentation particulière ; FREKRAW resterait un nom sans
   substance vérifiable dans ce dépôt.
3. Une recherche exhaustive n'a trouvé aucune trace de FREKRAW dans les
   dépôts accessibles — son existence, son architecture et son
   fonctionnement réel restent non vérifiés tant qu'un audit dépôt
   dédié n'a pas eu lieu.
4. Cela affirmerait une fonctionnalité vérifiée alors qu'aucune preuve
   n'existe — exactement le type d'invention de capacité que la
   discipline `NEEDS_REPO_AUDIT` interdit.
