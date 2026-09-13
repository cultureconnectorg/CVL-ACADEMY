# AF-17 — Banque N1 (formatif)

Réserve `AF17.SKILL.*`.

1. Décris l'architecture réelle du client agent de cette Academy : un
   seul client, une seule persona enregistrée. Pourquoi cette
   description doit-elle rester aussi étroite ?
2. Pourquoi serait-il une erreur d'inventer une taxonomie de types
   d'agents (« agent planificateur », « agent critique », « agent
   outil ») pour décrire ce système ?
3. Pourquoi le vrai `CVLNAgentfactory` (types d'agents multiples via
   ADL, étapes de cycle de vie) reste-t-il cité comme contexte de
   marché uniquement, jamais comme la forme réelle de cette Academy ?
4. Pourquoi cette formation cite-t-elle AF-16 comme prérequis plutôt
   que de redéfinir le même grounding ?
5. Si un développeur ajoutait une deuxième persona réelle au code,
   cela validerait-il rétroactivement une taxonomie de types d'agents
   déjà enseignée comme existante ? Pourquoi cette question révèle-
   t-elle un piège de raisonnement ?
6. Pourquoi la simplicité réelle de l'architecture (un client, une
   persona) n'est-elle pas en elle-même une faiblesse à corriger dans
   cette formation, mais un fait à décrire fidèlement ?

## Corrigé indicatif

1. Le code réel (`agent_factory.py`) ne définit qu'un seul client et
   qu'une seule persona — toute description plus riche serait une
   invention.
2. Aucune de ces catégories n'existe dans le code réel — les inventer
   masquerait la simplicité réelle de l'architecture.
3. Aucune intégration observée ne relie `CVLNAgentfactory` à cette
   Academy — le citer comme forme réelle inventerait une capacité.
4. Réutiliser par référence évite la duplication et garde AF-16 comme
   source unique de vérité pour le grounding commun.
5. Non — même avec une deuxième persona réelle ajoutée, cela resterait
   un fait ponctuel du code, jamais une taxonomie structurée de
   « types » d'agents ; le piège serait de sur-généraliser un
   changement futur hypothétique en une classification actuelle
   inexistante.
6. Parce que la discipline de cette formation est de décrire le réel
   fidèlement, pas de l'améliorer ou de l'enrichir artificiellement —
   la simplicité observée est le fait pédagogique central, pas un
   défaut du système à corriger dans la réponse du candidat.
