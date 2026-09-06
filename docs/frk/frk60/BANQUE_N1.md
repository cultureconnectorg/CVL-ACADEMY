# FRK-60 — Banque N1 (formatif)

Réserve `FRK60.SKILL.*`.

1. Pourquoi cette formation est-elle qualifiée de « pont conceptuel »
   plutôt que d'intégration réelle FREK↔Intelligence OS/Agent
   Infrastructure ?
2. Que veut dire « les deux côtés sont des stubs génériques » — cite
   les deux artefacts réels concernés (`frek_core.py`,
   `services/integrations/registry.py`) et leur nature exacte.
3. Qu'est-ce qu'une intégration réelle exigerait (schéma d'échange,
   authentification, contrat d'erreur) — pourquoi cette liste reste
   documentée et non construite ?
4. Pourquoi serait-il une erreur éliminatoire d'affirmer qu'un agent
   Intelligence OS peut aujourd'hui consommer un signal FREK ?

## Corrigé indicatif

1. Aucune implémentation fonctionnelle ne relie les deux systèmes — la
   formation enseigne la relation architecturale possible, jamais un
   système qui fonctionne.
2. `frek_core.py` est un client Python interne sans surface externe ;
   `services/integrations/registry.py` est une configuration
   d'intégration écosystème générique, sans câblage FREK-spécifique
   réel — les deux sont des stubs, pas des implémentations.
3. Une intégration réelle exigerait un schéma d'échange défini, une
   authentification mutuelle et un contrat d'erreur partagé — documenté
   ici comme exigence future, jamais construit faute de côté
   fonctionnel des deux systèmes.
4. Cela affirmerait une capacité d'intégration inexistante des deux
   côtés — contraire à la discipline `CAPABILITY_NOT_IMPLEMENTED`.
