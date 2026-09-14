# FRK-27 — Banque N1 (formatif)

Réserve `FRK27.SKILL.*`.

## Extension de FRK-26 (M1/M3)

1. Comment l'ingénierie de graphe de connaissances (knowledge graph)
   étend-elle les fondamentaux de FRK-26 (graphe de relations) au-delà
   d'une simple structure de dérivation ?
2. Explique pourquoi cette formation réutilise FRK-26 par référence
   plutôt que de re-décrire ses fondamentaux de modélisation de graphe.

## Ontologie et sémantique (M1)

3. Pourquoi un graphe de connaissances culturel introduit-il des types
   de nœuds/relations sémantiquement riches (ontologies) plutôt que de
   simples paires nœud-arête ?
4. Que permet une relation typée (ex. "influencedBy") qu'une arête
   générique ne permet pas ? (Porter un sens précis, et supporter des
   règles d'inférence)

## Application culturelle (M2)

5. Donne un exemple de types de nœuds pour un domaine culturel. (ex.
   Œuvre, Mouvement, Période, Lieu, Créateur)
6. Donne un exemple d'application culturelle d'un knowledge graph (ex.
   relier œuvre, période, mouvement artistique, lieu) sans confondre
   avec une simple base de données relationnelle.

## Frontière avec le modèle relationnel (M2)

7. Pourquoi une requête d'inférence (« œuvres influencées indirectement
   par X ») est-elle naturelle sur un knowledge graph mais difficile en
   SQL relationnel classique ?
8. À quelle limitation déjà identifiée dans FRK-26 cette difficulté
   SQL fait-elle écho ? (La limitation du modèle relationnel pour les
   chaînes de profondeur variable, qui resurgit au niveau des requêtes
   sémantiques)

## Corrigé indicatif

1. FRK-26 pose la structure orientée-acyclique de dérivation ; FRK-27
   ajoute la sémantique riche (ontologies, inférence) au-delà de la
   simple traçabilité.
2. Réutiliser par référence évite la duplication et garde une source
   unique de vérité pour les fondamentaux de graphe.
3. Une ontologie permet d'exprimer des relations typées et des règles
   d'inférence, impossible avec un simple graphe non typé.
4. Porter un sens précis et supporter l'inférence.
5. Œuvre, Mouvement, Période, Lieu, Créateur.
6. Un knowledge graph relie ces entités par des relations sémantiques
   typées, permettant des requêtes d'inférence — pas juste des
   jointures.
7. Le graphe traverse des relations typées de façon transitive
   (opération native) ; l'équivalent SQL exige des self-joins
   récursifs de profondeur inconnue.
8. La limitation des tables relationnelles pour les chaînes de
   profondeur variable, identifiée dans FRK-26.
