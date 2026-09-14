# FRK-60 — Banque N1 (formatif)

Réserve `FRK60.SKILL.*`.

1. Pourquoi cette formation est-elle qualifiée de « pont conceptuel »
   plutôt que d'intégration réelle FREK↔Intelligence OS/Agent
   Infrastructure ?
2. Que veut dire « les deux côtés sont des stubs génériques » — cite
   les deux artefacts réels concernés (`frek_core.py`,
   `services/integrations/registry.py`) et leur nature exacte.
3. Pourquoi additionner deux stubs (l'un interne, l'autre écosystème
   générique) ne produit-il pas une intégration réelle ?
4. Qu'est-ce qu'une intégration réelle exigerait (schéma d'échange,
   authentification, contrat d'erreur) — pourquoi cette liste reste
   documentée et non construite ?
5. Pourquoi un schéma d'échange à lui seul, sans authentification
   mutuelle ni contrat d'erreur partagé, resterait-il insuffisant pour
   une intégration réelle ?
6. Pourquoi serait-il une erreur éliminatoire d'affirmer qu'un agent
   Intelligence OS peut aujourd'hui consommer un signal FREK ?
7. En quoi `frek_core.py` diffère-t-il d'un connecteur d'agent
   infrastructure réel — précise sa surface exacte (interne, appelé
   en-process, sans route HTTP propre) ?
8. Pourquoi `services/integrations/registry.py` ne constitue-t-il pas,
   à lui seul, un câblage FREK-spécifique ?

## Corrigé indicatif

1. Aucune implémentation fonctionnelle ne relie les deux systèmes — la
   formation enseigne la relation architecturale possible, jamais un
   système qui fonctionne.
2. `frek_core.py` est un client Python interne sans surface externe ;
   `services/integrations/registry.py` est une configuration
   d'intégration écosystème générique, sans câblage FREK-spécifique
   réel — les deux sont des stubs, pas des implémentations.
3. Chaque stub couvre un rôle différent et incomplet (client interne
   d'un côté, configuration générique de l'autre) — aucun des deux
   n'implémente un canal fonctionnel, et leur juxtaposition ne crée
   pas ce canal.
4. Une intégration réelle exigerait un schéma d'échange défini, une
   authentification mutuelle et un contrat d'erreur partagé — documenté
   ici comme exigence future, jamais construit faute de côté
   fonctionnel des deux systèmes.
5. Un schéma d'échange sans authentification mutuelle serait
   usurpable, et sans contrat d'erreur partagé un échec d'un côté
   serait ininterprétable de l'autre — les trois éléments sont
   nécessaires ensemble, pas indépendamment suffisants.
6. Cela affirmerait une capacité d'intégration inexistante des deux
   côtés — contraire à la discipline `CAPABILITY_NOT_IMPLEMENTED`.
7. `frek_core.py` est un `FrekCoreClient` appelé en-process par le
   backend de cette Academy, sans route HTTP ni surface externe — il
   n'expose rien à un système tiers, agent infrastructure inclus.
8. Il définit une configuration générique d'intégration écosystème,
   sans entrée ni logique spécifique à FREK — un registre vide de
   contenu FREK réel, pas un connecteur.
