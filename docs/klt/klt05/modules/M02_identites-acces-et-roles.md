# KLT-05 — M02 — Identités, accès et rôles

```
MODULE_ID: KLT05-M02
COMPETENCY_ID: C2 — Opérer dans les limites de ses identités, accès et rôles (net-new)
PREREQUISITES: M01
ASSESSMENT_LEVEL: N1/N2
KILTIKONET_DEPENDENCY: Auth/RBAC — INTEGRATION_CONTRACT, non configuré (KLT-0001 §4)
ROLE_BOUNDARIES: Ce module ne confère aucun droit réel — il forme à reconnaître les droits qu'un rôle donné accorderait, dans un environnement pédagogique simulé. OPERATOR_AUTHORIZATION = NOT_IMPLEMENTED/NOT_GRANTED.
FREK_PROOF_MAPPING: FREK-WORK (mapping proposé — aucun signal legacy n'existait, net-new)
ORIGIN: master plan M02 (BUILD_NEW) — thème explicitement demandé par le Founder (KLT-0002)
```

## Situation professionnelle

Un opérateur qui ne connaît pas ses propres droits dépasse son mandat
sans le savoir — un rôle "éditeur de contenu" n'est pas un rôle
"administrateur", et confondre les deux est le risque opérationnel le
plus fréquent chez un opérateur débutant.

## Objectifs d'apprentissage

- Comprendre le principe du contrôle d'accès par rôle (RBAC) appliqué à
  une plateforme culturelle.
- Distinguer les rôles typiques (éditeur, modérateur, support,
  administrateur) et leurs périmètres respectifs.
- Vérifier ses propres droits avant d'agir, plutôt que de les supposer.

## Notions essentielles

Le **RBAC** (Role-Based Access Control) attribue des droits précis à un
rôle, pas à une personne directement — un opérateur change de droits
s'il change de rôle. Un rôle "éditeur" permet typiquement de créer/
modifier du contenu, pas de gérer les accès d'autres utilisateurs ou de
modifier la configuration de la plateforme — ces actions relèvent d'un
rôle "administrateur", généralement hors de portée d'un opérateur
bénévole débutant.

## Méthode

1. Identifier son rôle réel (dans ce cas pédagogique : "éditeur de
   contenu limité").
2. Lister ce que ce rôle permet et ne permet pas.
3. Avant toute action, vérifier qu'elle relève bien du périmètre du
   rôle détenu.

## Exemples

Le candidat, avec un rôle "éditeur", peut publier l'annonce de la
Veillée (M03) mais ne peut pas modifier les rôles d'un autre membre de
l'équipe — cette dernière action, si nécessaire, doit être escaladée à
un rôle administrateur réel.

## Cas

Access checklist pour le rôle "éditeur de contenu limité" attribué au
candidat sur la page de la Veillée du Tanbou.

## Erreurs fréquentes

- Supposer qu'un accès à une fonctionnalité implique l'autorisation de
  l'utiliser dans n'importe quel contexte.
- Confondre "je peux techniquement" et "je suis autorisé à".

## Activité

Classement d'actions possibles (publier, modérer, gérer les accès,
configurer) selon qu'elles relèvent du rôle "éditeur" ou non.

## Exercice

Identifier une action que le candidat serait techniquement capable de
faire mais qui dépasse son rôle réel, et proposer l'escalade appropriée.

## Livrable

Access checklist.

## Critères de réussite

- La checklist distingue clairement ce que le rôle permet et ne permet
  pas.
- Au moins une action hors périmètre est identifiée avec son escalade.

## Preuve

Checklist, conservée dans le registre de preuves (M11) — signal
`FREK-WORK` (mapping proposé).

## Auto-évaluation

*Ai-je vérifié mes droits avant d'agir, ou les ai-je supposés ?*

## Passage au module suivant

M03 applique cette discipline à l'administration concrète de contenus.
