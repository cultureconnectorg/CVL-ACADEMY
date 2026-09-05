# KOR-08 — M05 — Modéliser œuvres/enregistrements pour l'exploitation

```
MODULE_ID: KOR08-M05
COMPETENCY_ID: C5 — Modéliser œuvres/enregistrements pour l'exploitation streaming
PREREQUISITES: M04
ASSESSMENT_LEVEL: N2
KORA_DEPENDENCY: aucune
ROLE_BOUNDARIES: distinct de la structuration catalogue label (LabelOS) — voir REFERENTIAL.md §5
FREK_PROOF_MAPPING: FREK-WORK
ORIGIN: net-new
```

## Situation professionnelle

Après crédits (M03) et normalisation (M04), l'entrée catalogue de
*Rasin* doit être structurée pour l'exploitation — un modèle qui
manquerait un champ essentiel dégraderait la découvrabilité future.

## Objectifs d'apprentissage

- Structurer une entrée catalogue avec tous les champs nécessaires à
  l'exploitation (pas à la gestion de droits, distincte de LabelOS).
- Distinguer les champs d'exploitation (titre, description, crédits,
  genre) des champs de gestion de droits (ISRC, royalties).

## Notions essentielles

Le **modèle d'exploitation** (`KOR-08`) contient les champs qui servent
la découverte et l'affichage (titre, description, crédits, genre,
langue) — distinct du **modèle de gestion label** (LabelOS) qui contient
les champs de droits et de royalties. Les deux modèles se référencent
mutuellement (un même contenu, deux vues) sans se dupliquer.

## Méthode

1. Lister les champs nécessaires à l'exploitation streaming.
2. Exclure les champs de gestion de droits (hors mandat, LabelOS).
3. Structurer l'entrée catalogue complète.

## Exemple

Champs d'exploitation : titre, description, crédits (M03), genre/
langue (M04), durée, date. Champs hors mandat : taux de royalties,
statut ISRC — renvoyés à LabelOS.

## Cas

Le modèle porte sur *Rasin* réellement (`case/CASE.md`).

## Erreurs fréquentes

- Inclure des champs de gestion de droits dans le modèle
  d'exploitation, dupliquant le rôle de LabelOS.
- Omettre un champ essentiel à la découvrabilité.

## Activité

Liste des champs nécessaires à l'exploitation.

## Exercice

Structurer l'entrée catalogue complète.

## Livrable

Modèle d'entrée catalogue.

## Critères de réussite

- Tous les champs d'exploitation nécessaires sont présents.
- Aucun champ de gestion de droits (hors mandat) n'est dupliqué.

## Preuve

Modèle, signal `FREK-WORK`.

## Auto-évaluation

*Mon modèle mélange-t-il des champs qui relèvent de LabelOS avec ceux
de l'exploitation KORA ?*

## Passage au module suivant

Cette entrée catalogue est enrichie culturellement en M06.
