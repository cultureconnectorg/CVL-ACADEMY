# FRK-55 — Banque N1 (formatif)

Réserve `FRK55.SKILL.*`.

1. Comment cette formation synthétise-t-elle les compétences plus
   spécifiques de FRK-52 (API) et FRK-54 (event bus/webhooks) en
   standards transversaux ?
2. Qu'est-ce qu'une taxonomie d'erreur cohérente à l'échelle d'un
   système (pas seulement d'une API isolée) et pourquoi est-elle plus
   difficile à maintenir que celle d'une seule API ?
3. Pourquoi le versionnage doit-il être cohérent entre API et
   événements (ex. un même schéma de version) plutôt que traité
   séparément ?
4. Pourquoi cette formation réutilise FRK-52/54 par référence plutôt
   que de les redéfinir ?

## Corrigé indicatif

1. FRK-52 et FRK-54 couvrent chacun un mécanisme (API, événements) ;
   FRK-55 unifie les standards transversaux (erreurs, versions) qui
   doivent rester cohérents à travers tous les mécanismes.
2. Une taxonomie transversale doit rester cohérente à travers des
   dizaines d'endpoints et de types d'événements, alors qu'une
   taxonomie locale ne concerne qu'une seule surface.
3. Un client qui consomme à la fois l'API et les événements a besoin
   d'un seul modèle mental de version — deux schémas divergents
   créeraient une confusion et des bugs d'intégration.
4. Réutiliser par référence évite la duplication et garde chaque
   formation source comme unique référence pour son mécanisme
   spécifique.
