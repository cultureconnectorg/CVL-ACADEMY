# FRK-27 — Banque N1 (formatif)

Réserve `FRK27.SKILL.*`.

1. Comment l'ingénierie de graphe de connaissances (knowledge graph)
   étend-elle les fondamentaux de FRK-26 (graphe de relations) au-delà
   d'une simple structure de dérivation ?
2. Pourquoi un graphe de connaissances culturel introduit-il des types
   de nœuds/relations sémantiquement riches (ontologies) plutôt que de
   simples paires nœud-arête ?
3. Explique pourquoi cette formation réutilise FRK-26 par référence
   plutôt que de re-décrire ses fondamentaux de modélisation de graphe.
4. Donne un exemple d'application culturelle d'un knowledge graph (ex.
   relier œuvre, période, mouvement artistique, lieu) sans confondre
   avec une simple base de données relationnelle.

## Corrigé indicatif

1. FRK-26 pose la structure orientée-acyclique de dérivation ; FRK-27
   ajoute la sémantique riche (ontologies, inférence) au-delà de la
   simple traçabilité.
2. Une ontologie permet d'exprimer des relations typées et des règles
   d'inférence, impossible avec un simple graphe non typé.
3. Réutiliser par référence évite la duplication et garde une source
   unique de vérité pour les fondamentaux de graphe.
4. Un knowledge graph relie ces entités par des relations sémantiques
   typées, permettant des requêtes d'inférence (ex. « œuvres du même
   mouvement dans la même période ») — pas juste des jointures.
