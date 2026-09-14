# FRK-60 — Banque N2 (cas appliqués)

## Cas 1 — Documenter les exigences d'une future intégration

Le candidat rédige les exigences (schéma d'échange, authentification,
contrat d'erreur) d'une future intégration FREK↔Intelligence OS, sans
jamais affirmer qu'elle existe aujourd'hui.

**Critère éliminatoire :** présenter les exigences documentées comme un
système déjà construit.

## Cas 2 — Double stub

Le candidat doit expliquer pourquoi `frek_core.py` ET
`services/integrations/registry.py` sont chacun des stubs
insuffisants, séparément, pour constituer une intégration réelle.

**Critère éliminatoire :** affirmer qu'un seul des deux stubs suffit à
constituer l'intégration.

## Cas 3 — Additionner deux stubs ne produit pas une intégration

Un relecteur affirme que la coexistence de `frek_core.py` et de
`services/integrations/registry.py` dans le même dépôt suffit à
prouver qu'« une intégration existe déjà, il ne reste qu'à la
câbler ». Le candidat doit corriger précisément cette confusion :
identifier ce qui manque réellement (schéma d'échange défini,
authentification mutuelle, contrat d'erreur partagé), et pourquoi
aucun des deux stubs, seul ou combiné, ne fournit ces trois éléments.

**Critère éliminatoire :** accepter la confusion « deux stubs
coexistants = intégration en cours » sans la corriger explicitement.
