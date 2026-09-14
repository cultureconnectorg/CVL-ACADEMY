# FRK-53 — Banque N1 (formatif)

Réserve `FRK53.SKILL.*`.

## Frontière FRK-52/FRK-53 (M1)

1. Qu'est-ce qu'un SDK (bibliothèque cliente) et en quoi son
   ingénierie diffère-t-elle de la conception d'API elle-même
   (FRK-52) ?
2. Pourquoi cette formation cite FRK-52 par référence plutôt que de
   redéfinir la conception d'API ?

## Design de SDK (M1)

3. Que gagne un consommateur avec des modèles de requête/réponse
   typés plutôt que du JSON brut ? (Un retour d'erreur au moment de la
   compilation/édition plutôt qu'à l'exécution)
4. Quelle est la différence entre "400 Bad Request" et
   "InvalidFieldError: `email` must be a valid address" du point de
   vue DX ? (La seconde traduit l'erreur brute en exception typée avec
   contexte actionnable, sans obliger le développeur à consulter la
   doc API brute)

## Retry et idempotence (M2)

5. Quelles erreurs sont sûres à retenter automatiquement au niveau
   SDK ? (Timeouts réseau, erreurs 5xx)
6. Quelles erreurs ne sont jamais sûres à retenter aveuglément ? (Une
   écriture non-idempotente qui a peut-être déjà réussi)
7. Comment un SDK doit-il exposer cette distinction à l'appelant ?
   (Explicitement — jamais en la masquant derrière un retry
   automatique silencieux et risqué)

## DX et adoption (M2)

8. Cite un principe de bonne expérience développeur (DX) pour un SDK
   et explique pourquoi son absence dégrade l'adoption. (Types
   explicites, messages d'erreur actionnables — leur absence pousse
   à l'abandon de l'intégration)

## Discipline de gap héritée (M3)

9. Pourquoi cette formation hérite-t-elle du même constat que FRK-52 —
   aucun SDK/surface FREK publique n'existe aujourd'hui ?

## Corrigé indicatif

1. Un SDK enveloppe une API dans une interface idiomatique pour un
   langage donné ; FRK-52 conçoit l'API elle-même, FRK-53 conçoit
   comment la rendre facile à consommer.
2. Réutiliser par référence évite la duplication et garde FRK-52
   comme source unique de vérité pour la conception d'API.
3. Un retour d'erreur au moment de la compilation/édition plutôt qu'à
   l'exécution.
4. La seconde traduit l'erreur en exception typée avec contexte
   actionnable, sans obliger à consulter la doc API brute.
5. Timeouts réseau, erreurs 5xx.
6. Une écriture non-idempotente qui a peut-être déjà réussi.
7. Explicitement — jamais masqué derrière un retry silencieux.
8. Des messages d'erreur actionnables réduisent le temps de débogage
   du développeur intégrateur — leur absence pousse à l'abandon de
   l'intégration.
9. Sans API publique réelle (FRK-52), aucun SDK ne peut exister
   aujourd'hui — le même constat s'applique mécaniquement.
