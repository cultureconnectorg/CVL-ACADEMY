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
5. Pourquoi une preuve d'intégrité ajoutée après la capture (plutôt
   qu'à l'origine) ne protège-t-elle pas contre une altération
   survenue entre la capture et l'ajout de cette preuve ?
6. En quoi `NEEDS_REPO_AUDIT` diffère-t-il de `NEEDS_EXPERT_REVIEW`
   (utilisé pour FRK-10/14/73) ?
7. Si un futur audit dépôt trouvait effectivement FREKRAW, cela
   changerait-il la nature du concept marché-général enseigné ici ?
8. Pourquoi la discipline `CVLN-gap` exige-t-elle de citer FREKRAW
   uniquement comme nom sans substance vérifiée, plutôt que de
   l'omettre complètement du référentiel ?

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
5. Une altération survenue entre la capture et l'ajout tardif de la
   preuve resterait indétectable — seule une preuve intégrée dès
   l'origine couvre l'intégralité du cycle de vie du média depuis sa
   création.
6. `NEEDS_EXPERT_REVIEW` porte sur un contenu déjà construit
   nécessitant une revue humaine experte (juridique/forensic/
   cryptographique) avant certification ; `NEEDS_REPO_AUDIT` porte sur
   la vérification de l'existence même d'un produit nommé (FREKRAW)
   dans le code, un statut différent et antérieur.
7. Non — le concept marché-général de capture authentique reste réel
   et enseignable quelle que soit l'issue d'un futur audit ; seule
   l'affirmation FREKRAW-spécifique deviendrait alors possible.
8. Citer FREKRAW par son nom, sans substance vérifiée, respecte la
   transparence du référentiel envers le candidat tout en maintenant
   la discipline de gap — l'omettre effacerait une trace utile de ce
   qui reste à vérifier, sans bénéfice pédagogique.
