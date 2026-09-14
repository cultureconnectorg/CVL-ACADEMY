# FRK-47 — Banque N1 (formatif)

Réserve `FRK47.SKILL.*`.

## Frontière FRK-68 (M3)

1. Qu'est-ce qu'une piste d'audit institutionnelle et pourquoi
   diffère-t-elle du rôle opérateur FREK Auditor (FRK-68) ?
2. Pourquoi FRK-68 est-il grounded sur `db.frek_signals`/l'outbox réel,
   tandis que FRK-47 reste une discipline professionnelle générale ?
3. Pourquoi cette formation cite FRK-68 par référence plutôt que de
   redéfinir son fonctionnement opérateur ?

## Principes de responsabilité institutionnelle (M2)

4. Cite un principe fondamental de responsabilité institutionnelle
   (ex. séparation des rôles) et explique pourquoi il est nécessaire
   au-delà de tout système technique particulier.
5. Qu'est-ce que la séparation des rôles empêche exactement ? (Qu'une
   seule personne contrôle à la fois l'action et son audit)
6. Cite un deuxième principe fondamental. (Traçabilité non répudiable
   — un enregistrement d'audit doit être attribuable de façon
   crédiblement non déniable)
7. Comment obtient-on typiquement une traçabilité non répudiable ?
   (Journalisation append-only + liaison d'identité réelle au moment
   de l'écriture)

## Indépendance du schéma (M1/M3)

8. Un schéma générique de piste d'audit resterait-il valide si FRK-68
   n'existait pas ? (Oui — c'est la preuve de son indépendance réelle)

## Corrigé indicatif

1. La piste d'audit institutionnelle est la discipline générale de
   conception (que consigner, comment, pourquoi) ; FRK-68 est
   l'application opérateur concrète de cette discipline dans le
   contexte FREK réel.
2. FRK-68 est ancré sur des artefacts réels et vérifiables
   (`db.frek_signals`, outbox) ; FRK-47 reste indépendant de toute
   implémentation précise, enseignable dans n'importe quel contexte
   institutionnel.
3. Réutiliser par référence évite la duplication et garde FRK-68 comme
   source unique de vérité pour l'application opérateur réelle.
4. La séparation des rôles empêche qu'une seule personne contrôle à la
   fois l'action et son audit — nécessaire quel que soit le système
   technique utilisé.
5. Qu'une seule personne contrôle à la fois l'action et son audit.
6. Traçabilité non répudiable.
7. Journalisation append-only + liaison d'identité réelle au moment de
   l'écriture.
8. Oui.
