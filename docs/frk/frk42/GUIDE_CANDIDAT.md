# FRK-42 — Guide Candidat

## Avant de commencer

Aucun prérequis. Apprends la conception de transport de preuve
hors-ligne (discipline générale, distincte de la vérification offline
de FRK-20) — jamais attribuée à un système CVLN.

## Ce que tu dois savoir faire

Concevoir un artefact de preuve auto-vérifiable (signature embarquée
ou détachée) destiné à transiter par un support physique déconnecté,
traiter les défis d'intégrité en transit et d'ordre/gap pour des
séquences multi-artefacts, et distinguer précisément transport
(FRK-42) et vérification (FRK-20).

## Comment réviser

1. Lis `REFERENTIAL.md` §Objectives et §Modules.
2. Fais les 10 questions de `BANQUE_N1.md`.
3. Traite les 3 cas de `BANQUE_N2.md`.

## Piège le plus fréquent

Concevoir un artefact qui perd sa vérifiabilité une fois hors réseau —
élimination automatique. Second piège : affirmer qu'un système CVLN
implémente ce transport aujourd'hui.

## Règle absolue

Aucun système CVLN ne transporte de preuve hors-ligne aujourd'hui —
cette discipline est enseignée comme conception marché-générale.
