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
