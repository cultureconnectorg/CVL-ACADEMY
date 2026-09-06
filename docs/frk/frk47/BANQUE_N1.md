# FRK-47 — Banque N1 (formatif)

Réserve `FRK47.SKILL.*`.

1. Qu'est-ce qu'une piste d'audit institutionnelle et pourquoi
   diffère-t-elle du rôle opérateur FREK Auditor (FRK-68) ?
2. Pourquoi FRK-68 est-il grounded sur `db.frek_signals`/l'outbox réel,
   tandis que FRK-47 reste une discipline professionnelle générale ?
3. Cite un principe fondamental de responsabilité institutionnelle
   (ex. séparation des rôles, traçabilité non répudiable) et explique
   pourquoi il est nécessaire au-delà de tout système technique
   particulier.
4. Pourquoi cette formation cite FRK-68 par référence plutôt que de
   redéfinir son fonctionnement opérateur ?

## Corrigé indicatif

1. La piste d'audit institutionnelle est la discipline générale de
   conception (que consigner, comment, pourquoi) ; FRK-68 est
   l'application opérateur concrète de cette discipline dans le
   contexte FREK réel.
2. FRK-68 est ancré sur des artefacts réels et vérifiables
   (`db.frek_signals`, outbox) ; FRK-47 reste indépendant de toute
   implémentation précise, enseignable dans n'importe quel contexte
   institutionnel.
3. La séparation des rôles empêche qu'une seule personne contrôle à la
   fois l'action et son audit — nécessaire quel que soit le système
   technique utilisé.
4. Réutiliser par référence évite la duplication et garde FRK-68 comme
   source unique de vérité pour l'application opérateur réelle.
