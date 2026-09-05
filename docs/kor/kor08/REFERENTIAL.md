# KOR-08 — Référentiel canonique : Metadata & Cultural Catalog Operations

```
SOURCE = KOR-0001 §2/§4, KOR-0002 §4 tension #10 (KOR-08 vs LabelOS —
recouvrement le plus fort de toute la carte, LOS-02 "Metadata & Catalog
Management", ISRC/ISWC/DDEX)
DB_MUTATION = FALSE
RÈGLE D'APPLICATION KORA (mandat Founder) : LabelOS = spécialiste
profond des standards de métadonnées de l'industrie musicale (ISRC/
ISWC/DDEX, récupération de royalties) ; KORA = application
streaming-spécifique (découvrabilité, crédits affichés à l'auditeur,
enrichissement culturel). Ce référentiel ne réenseigne PAS ISRC/ISWC/
DDEX depuis zéro — il les présuppose et les cite comme prérequis/pont
vers LabelOS (`LOS-02`).
```

## 1. Métier réel et rôle professionnel

**Spécialiste métadonnées et catalogue culturel** — structure les
métadonnées d'un contenu média pour l'exploitation (découvrabilité,
crédits, contexte culturel), en s'appuyant sur les standards détenus
par LabelOS plutôt qu'en les redéfinissant.

## 2. Activités professionnelles réelles

Diagnostiquer un besoin de métadonnées ; utiliser IDs/taxonomies
existants ; gérer crédits et contributeurs ; normaliser genres/langues/
territoires ; modéliser œuvres/enregistrements pour l'exploitation ;
enrichir culturellement (provenance, contexte) ; contrôler la qualité
de la donnée ; optimiser recherche et découvrabilité.

## 3. Compétences (provenance)

| # | Compétence | Provenance |
|---|---|---|
| C1 | Diagnostiquer un besoin de métadonnées et son périmètre (vs LabelOS) | `MARKET_SKILL` |
| C2 | Utiliser IDs et taxonomies existants (pont LabelOS, pas réinvention) | `MARKET_SKILL` |
| C3 | Gérer crédits et contributeurs | `MARKET_SKILL` |
| C4 | Normaliser genres, langues, territoires | `MARKET_SKILL` |
| C5 | Modéliser œuvres/enregistrements pour l'exploitation streaming | `MARKET_SKILL` |
| C6 | Enrichir culturellement une métadonnée (provenance, contexte, FREK) | `MARKET_SKILL` |
| C7 | Contrôler la qualité de la donnée | `MARKET_SKILL` |
| C8 | Optimiser recherche et découvrabilité | `MARKET_SKILL` |
| C9 | Conduire une opération de métadonnées de bout en bout et la défendre | `MARKET_SKILL` (synthèse) |

Aucune `PRODUCT_DEPENDENCY` de blocage — enseignable sur le catalogue
réel de *Rasin* sans système de métadonnées KORA (qui n'existe pas).

## 4. Blocs pédagogiques → modules

Diagnostic et périmètre (C1) → standards existants (C2) → crédits/
normalisation (C3-C4) → modélisation (C5) → enrichissement culturel/
FREK (C6) → qualité (C7) → découvrabilité (C8) → synthèse (C9).

## 5. Boundary check — tension #10, la plus forte de la carte

| Formation/entité | Recouvrement | KORA application rule |
|---|---|---|
| **LabelOS** (`LOS-02` Metadata & Catalog Management, réel — `seed_data.py:807-819`) | Le plus fort recouvrement de toute la carte KORA (`KOR-0002` §4 #10) : les deux domaines manipulent des métadonnées d'œuvres | **LabelOS possède la profondeur** (ISRC/ISWC/DDEX, récupération de royalties, structuration catalogue label) ; **KORA-08 possède l'application streaming** (découvrabilité, crédits affichés à l'auditeur final, enrichissement culturel). Le point de passage : un label structure son catalogue avec les standards LabelOS **en amont** ; `KOR-08` consomme/normalise ces métadonnées pour l'exploitation KORA **en aval**. |
| `KOR-12` (data/intelligence, non construit) | Catalogue descriptif (`KOR-08`) vs mesure d'usage (`KOR-12`) — `KOR-0002` §4 tension #4 | `KOR-08` décrit l'œuvre, `KOR-12` mesurerait son usage |

## 6. Dépendances KORA vérifiées

Aucun système de métadonnées KORA réel — `ACADEMY_LOCAL_EVIDENCE =
NOT_FOUND`. FREK (`frek_core.py`) est réel et local, réutilisé pour
l'enrichissement/provenance (C6) — pas fabriqué.

## 7. `PUBLIC/EXTERNAL/BRIDGE`

`UNRESOLVED`.

## 8. Statut

`CORE_BUILD = COMPLETE` visé. Tension #10 explicitement traitée par la
règle d'application KORA ci-dessus — jamais un doublon d'ISRC/ISWC/
DDEX construit dans ce corpus.
