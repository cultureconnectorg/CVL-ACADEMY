# CVE-08 — Banque N2 (cas appliqués)

## Cas N2-1 — Formule VCF inventée présentée comme spec

Un candidat écrit une équation définissant `VCF_i(t)` en fonction de
`S,E,F,C,N` et l'attribue au document. Corrige.

**Critères de notation:** cite les deux seules apparitions réelles de
VCF (§3.3, §6), toutes deux comme entrée assumée, jamais dérivée — et
confirme qu'aucune équation définissant VCF n'existe dans le document.
**Élimination automatique** — présenter une formule inventée comme
spec réelle est le même mode d'échec que CVE-06/M2.

## Cas N2-2 — Hypothèse de travail non labellisée

Un stagiaire écrit "`VCF_i(t) = CVI_i,c`" dans sa copie sans préciser
qu'il s'agit d'une hypothèse. Corrige.

**Critères de notation:** le contenu de l'hypothèse est défendable
(CVI est la quantité de valeur la plus proche pleinement définie),
mais l'absence de label `HYPOTHESIS, NOT SPEC` est une erreur — exige
la correction du label, pas une réécriture du contenu. Pas
d'élimination si le contenu est correct mais mal labellisé ; note
réduite. Élimination si le candidat maintient que c'est une équation
du document après correction.

## Cas N2-3 — VCF confondu avec CVI

Un collègue affirme que VCF et CVI sont "la même chose sous deux
noms" dans le document. Corrige.

**Critères de notation:** rappelle que CVI (§3.1, Layer 2) est
pleinement défini par une formule CES réelle, tandis que VCF (§3.3,
§6) n'est jamais défini — les traiter comme identiques est une
affirmation non vérifiable qui dépasse ce que le document dit. Le
candidat peut proposer CVI comme proxy hypothétique de VCF (M3), mais
jamais affirmer leur identité comme un fait du spec.
