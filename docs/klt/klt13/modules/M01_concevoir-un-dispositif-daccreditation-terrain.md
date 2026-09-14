# KLT-13 — M01 — Concevoir un dispositif d'accréditation terrain

```
MODULE_ID: KLT13-M01
COMPETENCY_ID: C1 — Concevoir un dispositif d'accréditation terrain pour un événement physique
PREREQUISITES: aucun
ASSESSMENT_LEVEL: N1/N2
KILTIKONET_DEPENDENCY: Accréditation/NFC — NOT_CONNECTED (KLT-05/M04 : aucun système de badge/scan réel n'est utilisé chez Kiltikonet). Ce module ne présuppose aucun système Kiltikonet réel ; il enseigne la méthode de conception, transposable à tout événement physique.
ROLE_BOUNDARIES: Concevoir un dispositif d'accréditation ne donne pas mandat pour décider seul de la jauge globale de l'événement, qui reste une décision d'organisation (KLT-02/KLT-05)
FREK_PROOF_MAPPING: FREK-WORK (mapping proposé — net-new, formation sans legacy)
ORIGIN: PROPOSED (Claude-derived, KLT_09_20_RECONCILIATION.md §KLT-13 — SPECIALIZE_EXISTING sur KLT-05/C4)
```

## Situation professionnelle

La Veillée du Tanbou se tient dans une salle municipale : le public
général, les Doyens (dont deux à mobilité réduite), le groupe de jeunes,
les artistes du collectif Tanbou Rasin, et l'espace de rangement des
instruments (patrimoine matériel sans inventaire, `KLT-01`) ne partagent
pas le même niveau d'accès. Sans dispositif d'accréditation pensé par
zone et par rôle, n'importe qui pourrait accéder à l'espace de rangement
ou perturber l'espace réservé aux Doyens avant leur intervention.

## Objectifs d'apprentissage

- Distinguer les rôles présents à un événement physique (public,
  bénévoles, artistes, personnes à mobilité réduite, presse éventuelle).
- Cartographier les zones d'un lieu selon leur niveau de sensibilité
  (accès libre, accès restreint, accès interdit au public).
- Concevoir un plan d'accréditation qui associe rôle × zone × niveau
  d'accès, sans complexité inutile pour un petit événement.

## Notions essentielles

Un dispositif d'accréditation terrain repose sur trois éléments
distincts qu'il ne faut jamais confondre : le **rôle** (qui est la
personne, à quel titre), la **zone** (quel espace physique), et le
**niveau d'accès** (ce que ce rôle est autorisé à faire dans cette zone,
à quel moment). Une accréditation qui ne nomme que le rôle sans la zone
("badge bénévole") est incomplète — elle ne dit rien de ce que le
bénévole peut réellement faire une fois sur place.

## Méthode

1. Lister tous les rôles réellement présents à l'événement (public,
   Doyens, jeunes, bénévoles, artistes, organisation).
2. Cartographier les zones du lieu et leur sensibilité (salle publique,
   espace réservé aux Doyens, rangement des instruments).
3. Croiser rôle × zone pour produire un plan d'accréditation, en
   vérifiant qu'aucune zone sensible n'est accessible sans rôle
   explicitement autorisé.

## Exemples

Un plan qui accorde à "bénévole accueil" un accès uniquement à la salle
publique et à l'entrée, mais pas au rangement des instruments, est
correctement scoped — le rôle ne peut agir que là où sa mission
l'exige. À l'inverse, un plan qui accorde à tous les bénévoles un accès
identique "backstage complet" par simplicité administrative expose le
rangement des instruments et l'espace réservé aux Doyens à des passages
non maîtrisés — la simplicité de gestion ne justifie jamais d'ouvrir un
accès au-delà du rôle réellement exercé.

## Cas

Plan d'accréditation terrain pour la Veillée du Tanbou : rôles (public,
Doyens, jeunes, bénévoles, Tanbou Rasin, organisation), zones (salle
publique, espace réservé aux Doyens, rangement des instruments, entrée/
sortie), niveaux d'accès associés.

## Erreurs fréquentes

- Accorder un accès identique à tous les bénévoles par simplicité,
  au-delà de leur rôle réellement exercé.
- Nommer un rôle sans nommer la zone associée, rendant le plan
  inexploitable le jour J.
- Oublier de traiter l'accès des personnes à mobilité réduite comme une
  contrainte d'accréditation à part entière (parcours, pas seulement
  présence).

## Activité

Cartographie collective des zones du lieu à partir d'un plan simplifié,
puis attribution des niveaux d'accès par rôle.

## Exercice

Rédiger le plan d'accréditation terrain complet pour la Veillée du
Tanbou, incluant le parcours d'accès des Doyens à mobilité réduite.

## Livrable

Plan d'accréditation terrain (rôles × zones × niveaux d'accès).

## Critères de réussite

- Chaque rôle a un accès explicitement scoped à ce que sa mission exige,
  jamais plus.
- Le parcours d'accès des personnes à mobilité réduite est traité
  explicitement, pas seulement leur présence.

## Preuve

Plan d'accréditation, conservé dans le registre de preuves — signal
`FREK-WORK`.

## Auto-évaluation

*Mon plan accorde-t-il à chaque rôle un accès réellement nécessaire à sa
mission, ou ai-je simplifié en accordant plus large que nécessaire ?*

## Passage au module suivant

M02 étudie un précédent réel de contrôle d'accès électronique, pour
enrichir ce plan des exigences d'un dispositif rigoureux.
