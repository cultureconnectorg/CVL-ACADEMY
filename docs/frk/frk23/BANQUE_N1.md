# FRK-23 — Banque N1 (formatif)

Réserve `FRK23.SKILL.*`.

## Distinction modélisation/sérialisation (M1)

1. Qu'est-ce que la modélisation d'un objet culturel (entités,
   attributs, relations) et pourquoi est-ce une discipline distincte
   du format binaire `.fk` (FRK-21/22) ?
2. Pourquoi un schéma de métadonnées bien conçu reste-t-il indépendant
   de tout format de sérialisation particulier ?
3. Si un schéma casse quand on change son format de sérialisation, que
   peut-on en conclure ? (Le schéma n'était jamais vraiment bien conçu
   — une dépendance cachée existait)

## Entités et relations (M2)

4. Donne un exemple de relation entité-entité pertinente pour un objet
   culturel (ex. œuvre ↔ auteur ↔ provenance) sans référence à un
   format CVLN.
5. Cite trois entités typiques d'un modèle d'objet culturel. (Œuvre,
   Créateur, Registre de provenance)

## Frontière `.fk` (M3)

6. Explique pourquoi cette formation reste enseignable et évaluable
   même si `.fk` (FRK-21/22) reste `BLOCKED_PRODUCT_DEPENDENCY` —
   qu'est-ce qui rend les deux sujets réellement indépendants ?
7. Une spécification `.fk` existe-t-elle quelque part dans ce dépôt ?
   (Non — donc un modèle construit ici n'a littéralement rien de réel
   dont dépendre)
8. Un candidat peut-il faire dépendre son modèle d'une supposition sur
   la façon dont `.fk` encoderait éventuellement les données ? (Non —
   élimination automatique, même dépendance cachée)

## Corrigé indicatif

1. La modélisation porte sur la structure conceptuelle (entités,
   attributs, relations) ; `.fk` porterait sur l'encodage binaire —
   deux couches distinctes.
2. Un bon schéma conceptuel se traduit dans n'importe quel format
   (JSON, XML, binaire) sans changer de sens.
3. Le schéma n'était jamais vraiment bien conçu — une dépendance
   cachée existait.
4. Œuvre → créée_par → Auteur ; Œuvre → dérive_de → Œuvre source ; ce
   sont des relations de modélisation générale, indépendantes de tout
   format CVLN.
5. Œuvre, Créateur, Registre de provenance.
6. Aucune spécification `.fk` n'existe dans ce dépôt — la formation ne
   dépend donc d'aucune ressource bloquée, elle enseigne une discipline
   de modélisation générale et réelle.
7. Non.
8. Non — élimination automatique.
