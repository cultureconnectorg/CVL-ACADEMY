# FRK-60 — Guide Correcteur

## Avant de noter

Relis `REFERENTIAL.md` §Objectives et §Modules — en particulier la
nature réelle et distincte de `frek_core.py` et de
`services/integrations/registry.py`.

## Ce que tu vérifies en priorité

1. La copie affirme-t-elle, explicitement ou implicitement, qu'une
   intégration fonctionnelle existe déjà côté FREK ou côté
   Intelligence OS/Agent Infrastructure ? Applique la règle
   éliminatoire sans exception si oui.
2. Le candidat confond-il la coexistence des deux artefacts dans le
   dépôt avec un câblage en cours ? Applique la règle éliminatoire
   sans exception si oui.
3. Les exigences documentées (schéma d'échange, authentification
   mutuelle, contrat d'erreur partagé) sont-elles complètes et jamais
   présentées comme construites ?

## Ce que tu ne fais pas

Tu ne notes jamais sur une intuition personnelle d'architecture
d'agents — seulement sur la précision de la distinction entre les deux
stubs réels et l'absence de toute affirmation de câblage fonctionnel.
