# KLT-08 — M04 — Suivre l'état réel de conformité réseau agrégé

```
MODULE_ID: KLT08-M04
COMPETENCY_ID: C4 — Suivre l'état réel de conformité réseau agrégé
PREREQUISITES: M01, M03
ASSESSMENT_LEVEL: N2
KILTIKONET_DEPENDENCY: Network/Compliance — PRODUCT_CODE_REAL_VERIFIED (`backend/routes/network.py`, endpoints `/compliance`, `/audits`, collections `network_compliance_records`/`network_audits`, repo `cultureconnectorg/Kiltikonet-Aout2026`, commit `bb64ce7`, vérifié 2026-09-07) ; NOT_CONNECTED_TO_ACADEMY_RUNTIME (Academy n'a aucun client ni credentials appelant cette API) ; toute donnée manipulée dans ce module reste PEDAGOGICAL_ILLUSTRATIVE.
ROLE_BOUNDARIES: Concevoir un suivi de conformité sur le schéma réel vérifié n'équivaut jamais à une requête live sur des données réelles ; le suivi ne remplace jamais la recommandation d'audit (frontière M06)
FREK_PROOF_MAPPING: FREK-WORK (mapping proposé — net-new, re-vérifié 2026-09-07)
ORIGIN: PROPOSED (Claude-derived, re-verified against Kiltikonet-Aout2026 2026-09-07 — voir KLT_09_20_RECONCILIATION.md §Re-vérification)
```

## Situation professionnelle

Après la consolidation (M03), la formation des opérateurs (M05) et les
recommandations (M06), le responsable qualité/conformité doit pouvoir
suivre, dans la durée, un état agrégé de conformité réseau — pas
seulement l'audit ponctuel déjà mené. Ce suivi s'appuie sur un système
réel et vérifié, mais dont les collections peuvent être vides tant
qu'aucune donnée n'y a été insérée, et auquel Academy n'a aucune
connexion live.

## Objectifs d'apprentissage

- Concevoir un suivi de conformité réseau agrégé aligné sur le schéma
  réel vérifié (endpoints, agrégation, lineage).
- Distinguer une conformité "mesurée dans le système" (`OBSERVED`) d'une
  conformité "non encore configurée" (`NOT_CONFIGURED`).
- Ne jamais confondre ce suivi factuel avec une recommandation d'audit
  (frontière M06).

## Notions essentielles

Le système Network réel (`backend/routes/network.py`) expose
`/compliance` (`network_compliance_records`) et `/audits`
(`network_audits`), et son instantané agrégé `/overview` calcule un
score moyen de conformité (`compliance_avg_score`) uniquement quand des
enregistrements existent — sinon `compliance_available = false`. Suivre
la conformité agrégée, c'est produire une vue honnête de ce que ce
système contient réellement aujourd'hui, jamais une estimation.

## Méthode

1. Identifier les endpoints réels pertinents pour le suivi de
   conformité (`/compliance`, `/audits`, `/overview`).
2. Vérifier si l'agrégation (`compliance_avg_score`) est réellement
   disponible ou non (`compliance_available`).
3. Produire une fiche de suivi qui distingue explicitement `OBSERVED`
   de `NOT_CONFIGURED`, sans jamais formuler une recommandation
   d'audit à sa place (cela reste M06).

## Exemples

Une fiche qui note "score de conformité agrégé : non disponible,
`compliance_available = false`, aucun enregistrement à ce jour" est
honnête ; une fiche qui affiche "conformité moyenne : 3,2/4" en
l'absence de toute donnée réelle fabrique un score. À l'inverse, une
fiche qui ajouterait "il est recommandé d'auditer immédiatement
l'opérateur X" dépasserait son rôle de suivi factuel — cette
recommandation relève de M06, pas de ce module.

## Cas

Fiche de suivi de conformité réseau agrégé, dans la continuité de
l'audit déjà mené (`case/CAS_ANGLE_AUDIT_RESEAU.md`).

## Erreurs fréquentes

- Présenter un score de conformité fabriqué en l'absence de données
  réelles insérées.
- Confondre le suivi factuel avec une recommandation d'audit (retour à
  M06).
- Ignorer l'indicateur réel `compliance_available` et présenter une
  agrégation comme si elle existait toujours.

## Activité

Repérage des endpoints réels et de leur logique d'agrégation
(`compliance_available`, `compliance_avg_score`).

## Exercice

Produire la fiche de suivi de conformité réseau agrégé, avec état de
provenance pour chaque donnée citée.

## Livrable

Fiche de suivi de conformité (1-2 pages).

## Critères de réussite

- Chaque donnée citée précise son endpoint réel et son état de
  provenance (`OBSERVED`/`NOT_CONFIGURED`).
- Le suivi reste un constat, jamais une recommandation d'audit.
- Aucun score n'est fabriqué en l'absence de données réelles.

## Preuve

Fiche de suivi, conservée dans le registre de preuves — signal
`FREK-WORK`.

## Auto-évaluation

*Ma fiche cite-t-elle honnêtement l'état réel (souvent
`NOT_CONFIGURED`), ou ai-je fabriqué un score plausible ?*

## Passage au module suivant

M05 aborde la formation des opérateurs aux exigences de conformité —
révélée comme un besoin réel par la consolidation (M03) et le suivi
agrégé (ce module).
