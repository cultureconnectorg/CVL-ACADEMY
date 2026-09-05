# KOR-06 — Banque N1

**Q-N1-01** (C1) — Un DSP est-il un composant unique et indivisible ?
`CORRECT_ANSWER` : non — il combine hébergement, catalogue, flux et
distribution, chacun pouvant tomber en panne indépendamment.
`RATIONALE` : M01. `DIFFICULTY` : facile.

**Q-N1-02** (C2) — Une chaîne ingestion→delivery peut-elle avoir un
seul point de défaillance ?
`CORRECT_ANSWER` : non — chaque étape est un point de défaillance
possible distinct.
`RATIONALE` : M02. `DIFFICULTY` : facile.

**Q-N1-03** (C4) — Une lecture saccadée localisée à une seule région
suggère-t-elle plutôt un problème player ou CDN ?
`CORRECT_ANSWER` : CDN — un problème player affecterait tous les
auditeurs également.
`RATIONALE` : M04. `DIFFICULTY` : moyen.

**Q-N1-04** (C8) — Un créneau de maintenance choisi pour une seule zone
convient-il automatiquement à toutes les autres ?
`CORRECT_ANSWER` : non — les fuseaux horaires doivent être pris en
compte, un compromis est souvent nécessaire.
`RATIONALE` : M08. `DIFFICULTY` : moyen.
