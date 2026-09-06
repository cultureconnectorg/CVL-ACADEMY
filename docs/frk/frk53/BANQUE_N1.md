# FRK-53 — Banque N1 (formatif)

Réserve `FRK53.SKILL.*`.

1. Qu'est-ce qu'un SDK (bibliothèque cliente) et en quoi son ingénierie
   diffère-t-elle de la conception d'API elle-même (FRK-52) ?
2. Pourquoi cette formation hérite-t-elle du même constat que FRK-52 —
   aucun SDK/surface FREK publique n'existe aujourd'hui ?
3. Cite un principe de bonne expérience développeur (DX) pour un SDK
   (ex. types explicites, messages d'erreur actionnables) et explique
   pourquoi son absence dégrade l'adoption.
4. Pourquoi cette formation cite FRK-52 par référence plutôt que de
   redéfinir la conception d'API ?

## Corrigé indicatif

1. Un SDK enveloppe une API dans une interface idiomatique pour un
   langage donné ; FRK-52 conçoit l'API elle-même, FRK-53 conçoit
   comment la rendre facile à consommer.
2. Sans API publique réelle (FRK-52), aucun SDK ne peut exister
   aujourd'hui — le même constat s'applique mécaniquement.
3. Des messages d'erreur actionnables réduisent le temps de débogage
   du développeur intégrateur — leur absence pousse à l'abandon de
   l'intégration.
4. Réutiliser par référence évite la duplication et garde FRK-52
   comme source unique de vérité pour la conception d'API.
