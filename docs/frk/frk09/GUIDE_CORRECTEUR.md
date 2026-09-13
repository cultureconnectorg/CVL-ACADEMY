# FRK-09 — Guide Correcteur

## Avant de noter

Relis `REFERENTIAL.md` §Objectives et §Modules — en particulier les
trois stades du cycle de vie, le modèle de récupération/réconciliation,
et le gap FREK-ID précis pour chacun des trois mécanismes.

## Ce que tu vérifies en priorité

1. Le candidat restitue-t-il correctement les trois stades (émission,
   rotation, révocation), sans les confondre ?
2. Décrit-il un schéma de récupération réel et son compromis de
   sécurité, et un scénario de réconciliation cohérent ?
3. Affirme-t-il, explicitement ou implicitement, qu'un FREK-ID peut
   être rotationné, révoqué, ou récupéré ? Applique la règle
   éliminatoire sans exception si oui, pour chacun des trois
   mécanismes séparément.

## Ce que tu ne fais pas

Tu ne notes jamais sur une intuition personnelle du cycle de vie
d'identité — seulement sur la pratique IAM réelle et sur l'exactitude
du gap FREK-ID articulé pour chaque mécanisme.
