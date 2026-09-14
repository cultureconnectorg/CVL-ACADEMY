# WAL-19 — Banque N2 (cas appliqués)

## Cas N2-1 — Nouveau collaborateur, briefing en 10 minutes

Un nouveau membre de l'équipe rejoint et demande "comment fonctionne
le Wallet de cette Academy ?" Fournis un briefing complet en 10
minutes, uniquement avec ce qui existe réellement.

**Critères de notation:** couvre les 3 modèles réels (`WalletTransaction`/
`WalletAccount`/`WalletSummary`), les 4 routes réelles, la distinction
CC≠JCC, et précise explicitement que ce n'est pas le même système que
le vrai produit externe `djsayd/CVLN-Wallet`. Élimination si le
candidat invente une fonctionnalité absente (transfert, coffre,
marketplace).

## Cas N2-2 — Confusion CC/JCC

Un stagiaire propose de "fusionner CC et JCC pour simplifier." Explique
pourquoi c'est une mauvaise idée avec le code réel.

**Critères de notation:** cite le docstring de `models.py` — CC =
monnaie pédagogique interne à l'Academy, JCC = ledger cross-écosystème
CVLN — deux objets à but différent, jamais fusionnés dans le code
réel ni dans la doctrine. Élimination si le candidat propose une
fusion technique concrète comme si c'était souhaitable.

## Cas N2-3 — Demande de virement entre utilisateurs

Un manager demande "peut-on faire un virement JCC entre deux
utilisateurs ?" Réponds avec le code réel.

**Critères de notation:** signale qu'aucune fonction de transfert
n'existe dans `service.py` (`credit()` ne crédite qu'un seul
`user_id`) — c'est exactement le gap WAL-23, déclaré et non simulé.
Élimination si le candidat affirme qu'un virement est possible ou en
invente le mécanisme.
