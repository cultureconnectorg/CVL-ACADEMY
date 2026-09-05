# KOR-06 — Cas : Anba Tonèl Host — exploiter une plateforme de podcast

```
CASE_STATUS = PEDAGOGICAL_SIMULATION
VÉHICULE GÉNÉRIQUE — "Anba Tonèl Host" est un hébergeur/DSP fictif
générique, explicitement DISTINCT de KORA. Aucune capacité KORA n'est
simulée ici ; ce cas enseigne un métier de marché réel (exploitation
de plateforme), transférable, pas une capacité KORA.
```

## Continuité

*Rasin* (Lanbi Collective, `KOR-01`/`02`) est hébergé chez *Anba Tonèl
Host*, aux côtés de centaines d'autres podcasts diaspora — c'est
l'hébergeur choisi en `KOR-01`/M10. Le candidat rejoint l'équipe
d'exploitation d'*Anba Tonèl Host* (pas le collectif créateur) pour ce
cas.

## Rôle et acteurs

| Acteur | Nature |
|---|---|
| Anba Tonèl Host | hébergeur/DSP générique du marché, employeur du candidat |
| Lanbi Collective | un des créateurs hébergés, dont *Rasin* |
| Centaines d'autres créateurs hébergés | trafic agrégé à gérer |

## Tension centrale

Un pic de trafic inattendu (une republication virale d'un épisode
concurrent) sature temporairement les serveurs d'*Anba Tonèl Host* —
*Rasin* devient indisponible quelques minutes pendant une publication
importante. Le candidat doit gérer l'incident, communiquer, et
proposer une amélioration de continuité.

## Contraintes réelles

*Anba Tonèl Host* est une structure de taille moyenne (pas un géant du
secteur) avec une infrastructure limitée ; aucun SLA formel n'existait
avant ce cas ; l'équipe d'exploitation est réduite (3 personnes).

## Action à concevoir

Comprendre et documenter le fonctionnement de la plateforme,
définir un SLA/SLO réaliste, gérer l'incident de saturation touchant
*Rasin*, améliorer le monitoring et la continuité, et documenter les
enjeux d'opérer à l'échelle de plusieurs territoires (audience
diaspora dispersée).

## Limites explicites

Le cas ne prétend jamais qu'*Anba Tonèl Host* est KORA, ni qu'une
plateforme KORA réelle existe. Il ne demande jamais de construire un
parcours utilisateur (`KOR-14`, non construit) ni de négocier des
droits de diffusion (`KOR-07`, non construit).
