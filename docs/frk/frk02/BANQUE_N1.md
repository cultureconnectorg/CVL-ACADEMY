# FRK-02 — Banque N1 (formatif)

Réserve `FRK02.SKILL.*`.

1. Cite la phrase du docstring de `frek_core.py` qui définit son rôle
   architectural. ("the sole boundary through which the app talks to
   FrekCore")
2. FRK-02 peut-il enseigner une architecture DID/VC/provenance-graphe
   comme si elle était construite dans ce repo ?
3. Quelle est la différence d'altitude entre FRK-01 et FRK-02 ?
4. `frek_core.py` mentionne-t-il explicitement Wallet, KORA ou Agent
   Factory comme systèmes connectés ?
5. Que doit faire un candidat qui ne trouve aucune preuve d'une
   architecture demandée ?
6. Pourquoi le docstring de `frek_core.py` utilise-t-il le mot
   « boundary » (frontière) plutôt que « network » (réseau) — quelle
   différence architecturale précise cela implique-t-il ?
7. Un candidat affirme que FREKCORE « se connecte » à Wallet via une
   API partagée. Pourquoi cette affirmation serait-elle éliminatoire
   même si elle semble plausible ?
8. En quoi le positionnement conceptuel enseigné en FRK-02 (« systèmes
   distincts du même écosystème CVLN ») diffère-t-il d'une affirmation
   de wiring technique observé ?

## Corrigé indicatif

1. « the sole boundary through which the app talks to FrekCore »
2. Non — ces concepts n'existent nulle part dans ce repo, seulement
   dans le candidat map Master 2D.
3. FRK-01 = system map opérationnel des 5 méthodes ; FRK-02 =
   positionnement architectural conceptuel de FREKCORE parmi les
   autres systèmes CVLN.
4. Non — aucune mention de connexion réelle observée.
5. Déclarer `CAPABILITY_NOT_IMPLEMENTED`, jamais inventer.
6. « Boundary » signale une frontière unique et mince par laquelle
   passe toute communication, pas un maillage de nœuds interconnectés
   — l'architecture reste un client simple, pas un réseau distribué.
7. Parce qu'aucun câblage réel n'est observé dans le code — affirmer
   une connexion plausible mais non vérifiée introduit une capacité
   inventée, contraire à la discipline de portée de cette formation.
8. Le positionnement conceptuel décrit une relation d'appartenance au
   même écosystème sans prétendre à un lien technique fonctionnel ;
   affirmer un wiring observé prétendrait à une preuve technique qui
   n'existe pas dans le code — deux affirmations de nature très
   différente.
