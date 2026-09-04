# 06 — KLT-06 — Analyste Observatory / Cultural Data Analyst

```
STATUS = PLANNED
BUILD_STATUS = NOT_STARTED — NO_KLT06_08_BUILD respecté dans ce ticket.
```

## Position dans l'architecture globale

Nommé dans `KLT_MASTER_MAP_v1` (`docs/KILTIKONET_KLT0001_CANONICAL_
EDUCATION_MAP.md`) comme formation `NEW` (aucun équivalent legacy —
confirmé, zéro trace dans `seed_data.py`/`seed_modules.py`/`catalog_
cartography.py`). Type `Formation / spécialisation`, priorité `P1`,
dépendance nommée : `Observatory / data lineage / signaux`.

## Blocage structurel réel

Contrairement à `KLT-01`→`05`, cette formation dépend d'**Observatory**
comme cœur de son objet métier (pas comme une dépendance annexe qu'on
peut contourner comme dans `KLT-01`/M10, `KLT-02`/M09, `KLT-03`/M10,
`KLT-05`/M09). `Observatory` a un statut `NOT_CONNECTED` en Academy
(`KLT-0001` §4) — bâtir `KLT-06` en respectant `NO_FAKE_OBSERVATORY`
demanderait de construire un métier entier sur des capacités simulées,
ce qu'aucune discipline de ce corpus n'autorise. Un accès Observatory
réel (ou une décision Founder explicite sur comment traiter cette
formation sans lui) est un préalable à toute construction.

## Ce qui devra être fait avant construction

1. Décision Founder : accès Observatory réel, ou périmètre alternatif
   pour `KLT-06` qui ne dépend pas structurellement de données non
   disponibles.
2. Une reconciliation legacy/canonique n'est pas nécessaire (aucun
   legacy à concilier) — mais un référentiel canonique (méthode
   `KLT-0003`) reste requis avant tout module.
