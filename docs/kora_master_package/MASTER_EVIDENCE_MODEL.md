# KORA Master Package — Master Evidence Model

## Typologie d'évidence consolidée (cf. `EVIDENCE_MODEL.md` par formation)

| Type | Formations principales | Forme |
|---|---|---|
| `MEDIA_MASTER` | KOR-01, KOR-03 | Fichier audio/vidéo produit |
| `QC_REPORT` | KOR-03, KOR-06 | Rapport de contrôle qualité |
| `RIGHTS_RECORD` | KOR-07 | Dossier de droits |
| `METADATA_PACKAGE` | KOR-08 | Paquet de métadonnées |
| `EDITORIAL_PLAN` | KOR-02, KOR-04 | Plan éditorial |
| `AUDIENCE_REPORT` | KOR-09, KOR-12 | Rapport d'audience |
| `ECONOMIC_MODEL` | KOR-10 | Modèle économique chiffré |
| `INCIDENT_REPORT` | KOR-05, KOR-06, KOR-11, KOR-14 | Rapport d'incident |
| `DATA_ANALYSIS` | KOR-12 | Analyse de données |
| `PARTNERSHIP_DOSSIER` | KOR-13, KOR-15 | Dossier de partenariat |
| `PRODUCT_REVIEW` | KOR-14 | Revue produit/UX |
| `TERRITORY_PLAN` | KOR-15 | Plan territorial |

## Règle universelle

`READY_FOR_FREK_PROOF = FALSE` sur 100% des évidences du corpus — y
compris `KOR10.SKILL.C08` (Wallet/JCC réel), faute d'ancrage FREK
câblé aujourd'hui. `FAKE_FREK_PROOF = 0`.

## Sensibilité

Toute évidence citant des montants réels, des personnes réelles
identifiables, ou des cas de harcèlement/mineurs est marquée
`PRIVACY_LEVEL = sensible` dans son fichier `EVIDENCE_MODEL.md`
d'origine (voir en particulier KOR-10, KOR-11).
