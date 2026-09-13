# AF-16 — Guide Candidat

## Avant de commencer

Aucun prérequis. Apprends le fonctionnement réel de `chat_reply()`
(transport de chat persona-agnostique) et `mentor_reply()` (la seule
persona réellement enregistrée, "Mentor CVLN").

## Ce que tu dois savoir faire

Décrire exactement ce que fait chaque fonction, sans inventer de
logique de routage de persona. Distinguer explicitement ce shim narrow
du vrai `CVLNAgentfactory` externe (225 fichiers, ADL, gates, cycle de
vie à 7 étapes) — cité uniquement comme contexte de marché, jamais
comme ce que cette Academy opère.

## Comment réviser

1. Lis `REFERENTIAL.md` §Objectives et §Modules.
2. Fais les 6 questions de `BANQUE_N1.md`.
3. Traite les 3 cas de `BANQUE_N2.md`.

## Pièges les plus fréquents

1. Inventer un registre d'agents, un système de mission/détachement,
   ou un mécanisme de rollback — élimination automatique.
2. Affirmer une intégration entre `agent_factory.py` et le vrai
   `CVLNAgentfactory` — élimination automatique.
3. Présenter une proposition future comme un développement déjà
   entamé — élimination automatique.

## Règle absolue

`chat_reply()`/`mentor_reply()` sont les deux seules fonctions réelles.
Aucune autre logique n'existe. Le vrai `CVLNAgentfactory` prouve
l'ampleur du concept ailleurs dans l'écosystème — jamais ce que cette
Academy opère.
