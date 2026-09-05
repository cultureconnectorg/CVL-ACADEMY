# KOR-03 — M09 — Encoder pour la livraison

```
MODULE_ID: KOR03-M09
COMPETENCY_ID: C9 — Encoder pour la livraison
PREREQUISITES: M08
ASSESSMENT_LEVEL: N1
KORA_DEPENDENCY: aucune — formats/plateformes du marché, aucune plateforme KORA réelle requise
ROLE_BOUNDARIES: ce module ne couvre pas l'exploitation d'un CDN réel (KOR-06, non construit)
FREK_PROOF_MAPPING: FREK-WORK
ORIGIN: net-new
```

## Situation professionnelle

La vidéo postproduite (M08) doit être livrée dans des formats adaptés
aux plateformes visées (réseaux sociaux de *Dyaspora FM*, hébergement
web) — un fichier mal encodé peut être refusé ou illisible malgré un
montage parfait.

## Objectifs d'apprentissage

- Choisir une résolution et un débit adaptés à la plateforme cible.
- Distinguer les formats verticaux (réseaux sociaux) des formats
  horizontaux (web).
- Vérifier qu'un fichier encodé est conforme avant livraison.

## Notions essentielles

Chaque plateforme du marché a des contraintes réelles (résolution
maximale, ratio, durée) — encoder sans les vérifier risque un refus ou
une dégradation à la publication. Le format vertical (réseaux sociaux)
et horizontal (web classique) ne sont **pas interchangeables** sans
recadrage réfléchi.

## Méthode

1. Identifier les contraintes réelles de chaque plateforme cible
   (résolution, ratio, durée maximale).
2. Encoder une version par format cible, avec recadrage réfléchi si
   nécessaire (pas un simple étirement).
3. Vérifier chaque fichier encodé avant livraison (lecture complète).

## Exemple

Une version verticale pour les réseaux sociaux de *Dyaspora FM*
nécessite un recadrage qui garde Man Rosa centrée, pas un simple
redimensionnement qui la couperait.

## Cas

L'encodage porte sur les plateformes réellement visées par le cas
(`case/CASE.md`), pas des formats hypothétiques.

## Erreurs fréquentes

- Livrer un seul format pour toutes les plateformes sans l'adapter.
- Ne pas vérifier le fichier encodé avant livraison.

## Activité

Identification des contraintes de chaque plateforme cible du cas.

## Exercice

Encoder au moins deux formats (vertical et horizontal) et les vérifier.

## Livrable

Fichiers encodés conformes aux plateformes cibles.

## Critères de réussite

- Au moins deux formats sont produits et adaptés, pas un seul
  redimensionné mécaniquement.
- Chaque fichier est vérifié par lecture complète avant livraison.
- Aucune dépendance à une plateforme KORA réelle n'est introduite.

## Preuve

Fichiers encodés + preuve de vérification, signal `FREK-WORK`.

## Auto-évaluation

*Ai-je vérifié chaque fichier par lecture complète, ou supposé qu'il
fonctionnait ?*

## Passage au module suivant

Les fichiers encodés sont publiés et contrôlés en M10.
