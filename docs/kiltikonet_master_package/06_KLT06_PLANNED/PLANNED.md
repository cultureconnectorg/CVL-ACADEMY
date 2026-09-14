# 06 — KLT-06 — Analyste Observatory / Cultural Data Analyst

```
STATUS = BUILT_PARTIAL (dossier conservé sous son nom historique
"06_KLT06_PLANNED" pour ne pas casser les liens déjà livrés — le
contenu réel n'est plus "planned", voir mise à jour ci-dessous).
REFERENTIAL_STATUS = FROZEN (KLT-0005)
CONTEXT_STATUS = DECIDED (KLT-0008) — contexts = [EXTERNAL]
BUILD_STATUS = PARTIAL — 5/7 modules construits (M01-M04, M07), 2/7
BLOCKED (M05/M06, Observatory non connecté).
FULLY_COMPLETE = FALSE — verrouillé tant que M05/M06 (C5/C6) ne sont
pas réellement connectées à Observatory, pas seulement rédigées.
```

## Mise à jour — contenu pédagogique construit (`KLT-0009`)

Sur autorisation explicite du Founder ("Autorisation de rédigé le
contenu"), le contenu pédagogique complet du périmètre buildable a été
construit : `docs/klt/klt06/` (22 documents). Référentiel :
`docs/KILTIKONET_KLT0005_KLT06_CANONICAL_REFERENTIAL.md`. Décision de
contexte et de périmètre : `docs/KILTIKONET_KLT0008_KLT06_08_CONTEXT_
AND_SCOPE_DECISION.md`.

**5/7 compétences construites** (`C1`-`C4`, `C7`) avec modules, N1, N2,
`KLT06-A01` (certification **partielle**), skills, guides, templates,
certification model, quality gates. **2/7 bloquées** (`C5`, `C6`) —
non construites, non simulées (`NO_FAKE_OBSERVATORY`), voir `docs/klt/
klt06/modules/MODULES_STATUS.md`. **Aucun badge** — formation `NEW`.

## Position dans l'architecture globale

Nommé dans `KLT_MASTER_MAP_v1` (`docs/KILTIKONET_KLT0001_CANONICAL_
EDUCATION_MAP.md`) comme formation `NEW` (aucun équivalent legacy —
confirmé, zéro trace dans `seed_data.py`/`seed_modules.py`/`catalog_
cartography.py`). Type `Formation / spécialisation`, priorité `P1`,
dépendance nommée : `Observatory / data lineage / signaux`.

## Blocage structurel réel (toujours d'actualité pour `M05`/`M06`)

`Observatory` reste `NOT_CONNECTED` en Academy (`KLT-0001` §4) —
`M05`/`M06` restent non construits, sans date. Un accès Observatory réel
(ou une décision Founder explicite alternative) reste un préalable à
leur construction.
