# GMD-05 — Guide Candidat

## Avant de commencer

Aucun prérequis.

## Ce que tu dois savoir faire

Concevoir une structure de tiers de billetterie, expliquer la nuance
réelle d'intégrité de quota (check non-atomique au checkout, `$inc`
atomique au webhook), et distinguer les pratiques de marché
(tarification dynamique, revente) des capacités réelles de la
plateforme Good Mood.

## Comment réviser

1. Lis `docs/gmd/gmd24/REFERENTIAL.md` toi-même — c'est l'exemple
   travaillé réel de cette formation.
2. Fais les 6 questions de `BANQUE_N1.md`.
3. Traite les 3 cas de `BANQUE_N2.md`.

## Piège le plus fréquent

Affirmer que la plateforme "réserve" un billet au clic — la vraie
garantie anti-survente est l'incrément atomique au moment du webhook,
jamais un verrou au moment du checkout.

## Règle absolue

Ne présente jamais une pratique de marché-général comme une capacité
réelle de la plateforme Good Mood — élimination automatique.
