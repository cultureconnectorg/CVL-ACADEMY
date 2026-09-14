# FRK-08 — Guide Correcteur

## Avant de noter

Relis `REFERENTIAL.md` §Objectives et §Modules — en particulier la
distinction document DID / modèle VC, et le gap CVLN précis
(`mint_frek_id()` n'a ni document DID, ni méthode de vérification).

## Ce que tu vérifies en priorité

1. Le candidat restitue-t-il correctement le modèle de document DID
   (identifiant, méthodes de vérification, points de service) ?
2. Distingue-t-il émission et présentation dans le modèle VC ?
3. Affirme-t-il, explicitement ou implicitement, une conformité W3C
   DID/VC pour `frek_core.py` ? Applique la règle éliminatoire sans
   exception si oui.

## Ce que tu ne fais pas

Tu ne notes jamais sur une intuition personnelle des standards
d'identité — seulement sur le modèle W3C réel (DID/VC) et sur
l'exactitude du gap CVLN articulé.
