# CMD-01→14 — Guide Candidat

## Avant de commencer

Aucun prérequis. Apprends les disciplines réelles SRE/NOC/Incident
Command System (marché-général) : supervision de parc, alerting,
rôles ICS, runbooks d'escalade, conception de tableaux de bord KPI.

## Ce que tu dois savoir faire

Concevoir un tableau de bord KPI réaliste et un runbook ICS complet,
en marché-général — jamais rattachés à un système CVLN précis. Règle
absolue : `fms-os/fms`'s `/os/command-center` (studio ops) ≠
`MetaCVLN`'s vrai Command Center (`/command-center/*`, couvert par
CMD-15, `internal/`) ≠ cette discipline générique — trois choses
distinctes, jamais fusionnées.

## Comment réviser

1. Lis `REFERENTIAL.md` §Objectives et §Modules.
2. Fais les 7 questions de `BANQUE_N1.md`.
3. Traite les 3 cas de `BANQUE_N2.md`.

## Pièges les plus fréquents

1. Confondre `fms-os/fms`'s `/os/command-center` avec le vrai Command
   Center de `MetaCVLN` — élimination automatique.
2. Concevoir un tableau de bord KPI avec des compteurs bruts sans
   distinction de sévérité ni de tendance — plafonne la note.
3. Présenter un runbook ICS comme un processus déjà en place dans cette
   Academy — élimination automatique.

## Règle absolue

Trois systèmes distincts, jamais fusionnés : `fms-os/fms` (produit réel
mais sans rapport), `MetaCVLN` (produit réel mais couvert ailleurs et
jamais opéré par cette Academy), et la discipline générique
enseignée ici.
