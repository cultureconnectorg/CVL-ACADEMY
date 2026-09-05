# KORA Master Package — Product Dependency Map

Chaque dépendance produit KORA déclarée dans le corpus (voir aussi
`KORA_PRODUCT_CAPABILITY_GAP_MAP.md` pour la vue exhaustive
capacité-par-capacité).

| Formation | Dépendance déclarée | Statut |
|---|---|---|
| `KOR-01` | services/frek_core.py (FREK) | `KORA_CURRENT_CAPABILITY` (réel, local, découplé) |
| `KOR-06` | DSP/CDN/monitoring streaming | `CAPABILITY_NOT_IMPLEMENTED` |
| `KOR-07` | Registre de droits/royalties | `CAPABILITY_NOT_IMPLEMENTED` |
| `KOR-08` | LabelOS (métadonnées) | `CAPABILITY_NOT_CONNECTED` (pôle réel, handoff non câblé pour KORA) |
| `KOR-09` | CRM/A-B testing à l'échelle | `CAPABILITY_NOT_IMPLEMENTED` |
| `KOR-10` | **Wallet/JCC** (`wallet/models.py`, `wallet/service.py`, `wallet/passes.py`) | `CAPABILITY_ALREADY_REAL` — **seule capacité réelle du corpus** |
| `KOR-10` | CVE | `EXTERNAL_PRODUCT_EVIDENCE_NOT_AUDITED` (jamais défini par invention) |
| `KOR-11` | File de modération, signalement, sanctions | `CAPABILITY_NOT_IMPLEMENTED` |
| `KOR-12` | Événements de lecture, dashboards, recommandation | `CAPABILITY_NOT_IMPLEMENTED` |
| `KOR-12` | CVLN Brain → recommandations KORA | `CAPABILITY_NOT_CONNECTED` (Brain réel pour `academy.certification.passed`, pas pour KORA) |
| `KOR-13` | CRM partenariats/acquisitions | `CAPABILITY_NOT_IMPLEMENTED` |
| `KOR-14` | Recherche, recommandation, TV/mobile natif, tests, analytics produit | `CAPABILITY_NOT_IMPLEMENTED` |
| `KOR-15` | Infrastructure de distribution multi-territoire, gestion de droits automatisée | `CAPABILITY_NOT_IMPLEMENTED` |

## Règle universelle

`NO_KORA_PRODUCT_UPGRADE` — ce corpus documente des dépendances, il
n'en construit ni n'en modifie aucune. `NO_FAKE_PRODUCT_CAPABILITY = 0`
occurrence sur 15 formations.
