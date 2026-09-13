# FRK-23 — Banque N2 (cas appliqués)

## Cas 1 — Conception d'un schéma d'objet culturel

Le candidat modélise un objet culturel (ex. artefact patrimonial) avec
ses entités, attributs et relations, sans référence à un format de
sérialisation.

**Critère éliminatoire :** faire dépendre le modèle d'un détail
d'encodage binaire particulier.

**Critères de notation :** entités, attributs et relations réellement
distincts, réutilisables indépendamment du format choisi pour les
sérialiser.

## Cas 2 — Frontière `.fk`

Le candidat doit expliquer pourquoi son schéma resterait valide même si
`.fk` (FRK-21/22) n'est jamais spécifié — démontrant l'indépendance
réelle des deux sujets.

**Critère éliminatoire :** affirmer que le schéma dépend de `.fk`.

## Cas 3 — Dépendance cachée

Un candidat propose un modèle où l'attribut "provenance" est structuré
comme une liste ordonnée, en justifiant ce choix par "c'est comme ça
que `.fk` l'encoderait probablement". Identifie le problème dans cette
justification.

**Critères de notation :** identifie que cette justification introduit
une dépendance cachée à une supposition sur un format inexistant — la
structure de l'attribut doit être justifiée par la sémantique du
domaine (ex. l'ordre chronologique de la chaîne de provenance
lui-même), jamais par une anticipation d'encodage `.fk`. Élimination
si le candidat ne perçoit pas le problème.
