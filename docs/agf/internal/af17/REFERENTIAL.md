# AF-17 — CVLN Agent Factory Client Architecture (internal, narrow)

## Repo truth this formation is built on

Per `AGENT_FACTORY_IOS_BRAIN_CMD_LAURENTIA_RECONCILIATION.md` :
coverage `PARTIAL (la vraie architecture est un seul client + une
seule persona — enseigner cela honnêtement, pas une taxonomie
inventée)`, action `NEW_INTERNAL (narrow)`. Même grounding qu'AF-16 :
`backend/services/agent_factory.py`.

## Prerequisites

AF-16.

## Objectives

Un candidat qui complète AF-17 sait décrire précisément la forme
architecturale réelle du client agent de cette Academy, sans jamais
inventer de taxonomie :

- Enseigner la forme architecturale réelle du client agent de cette
  Academy : **un** client, **une** persona enregistrée — pas une
  taxonomie de types d'agents, de rôles, ni une flotte d'agents
  spécialisés.
- Expliquer précisément pourquoi cette description doit rester aussi
  étroite : le code réel (`agent_factory.py`) ne définit qu'un seul
  client et qu'une seule persona (« Mentor CVLN ») — toute description
  plus riche (« agent planificateur », « agent critique », « agent
  outil ») serait une invention, aucune de ces catégories n'existant
  dans le code réel.
- Refuser explicitement toute taxonomie inventée qui n'existe pas
  dans le code réel — l'architecture honnête est délibérément étroite,
  et l'enrichir masquerait cette simplicité réelle plutôt que de
  l'expliquer.
- Citer le vrai `CVLNAgentfactory` externe (types d'agents multiples
  via ADL, étapes de cycle de vie à 7 stades) comme contexte de marché
  uniquement, hérité de la discipline propre d'AF-16 — jamais comme la
  forme réelle opérée par cette Academy : aucune intégration observée
  ne relie les deux systèmes.
- Expliquer précisément pourquoi cette formation cite AF-16 comme
  prérequis plutôt que de redéfinir le même grounding : réutiliser
  par référence évite la duplication et garde AF-16 comme source
  unique de vérité pour le grounding commun (`agent_factory.py`).
- Expliquer précisément pourquoi affirmer que l'Academy suit un cycle
  de vie ADL (Draft→Prototype→Alpha→Beta→Production→Maintenance→
  Archive) serait une erreur éliminatoire : cela affirmerait une
  capacité de gestion de cycle de vie qui n'existe nulle part dans
  `agent_factory.py`.

## Modules

1. **Littératie de l'architecture client unique/persona unique** —
   ancrée dans le code réel `agent_factory.py`.
2. **Discipline anti-taxonomie** — refus de toute classification de
   types d'agents inventée.
3. **Comparaison de contexte de marché** (héritée d'AF-16) — le vrai
   `CVLNAgentfactory` cité honnêtement comme « ce qui existe dans
   l'écosystème, pas ce que cette Academy opère ».

## Assessment

Un exercice de description architecturale : le candidat décrit
l'architecture agent réelle de cette Academy sans inventer de
taxonomie — échec éliminatoire pour toute description de plusieurs
types/rôles d'agents inexistants dans `agent_factory.py`, ou toute
affirmation d'un cycle de vie ADL opéré par l'Academy.

## Evidence / mission eligibility

Aucun chemin d'éligibilité mission n'existe — aucune intégration
observée à opérer. `AF17.SKILL.CLIENT_ARCHITECTURE.L1` réservé une
fois approfondi.

## Status

`STATUS = PACKAGE_COMPLETE` — référentiel, banques N1/N2, assessment +
rubric, evidence model, 3 guides, cette note d'intégration existent
tous, deepened this pass. `FULLY_COMPLETE` non déclaré — requiert un
passage réel vérifié par un humain.
