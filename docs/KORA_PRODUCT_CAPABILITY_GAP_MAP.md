# KORA — Product Capability Gap Map

```
SCOPE: docs/kor/kor01/ … docs/kor/kor15/ (corpus pédagogique complet)
NO_PRODUCT_IMPLEMENTATION — ce document n'implémente rien ; il
consolide, capacité par capacité, ce que le corpus pédagogique KORA a
observé et déclaré sur l'état réel du produit KORA dans ce repo.
NO_KORA_PRODUCT_UPGRADE.
```

## Méthode

Chaque capacité évoquée par le contenu principal d'une formation
(`REFERENTIAL.md` §6 de chaque `docs/kor/korXX/`) est classée selon
une seule étiquette :

- `CAPABILITY_ALREADY_REAL` — le code existe et fait ce que le corpus
  enseigne (fichiers cités).
- `CAPABILITY_PARTIAL` — une brique réelle existe mais ne couvre
  qu'une partie de la capacité enseignée.
- `CAPABILITY_NOT_CONNECTED` — une brique réelle existe ailleurs dans
  l'écosystème CVLN mais n'est pas interfacée avec KORA.
- `CAPABILITY_NOT_IMPLEMENTED` — aucun code, aucune collection,
  aucune brique réelle n'existe.
- `CAPABILITY_TARGET_ONLY` — capacité évoquée uniquement comme
  ambition future, jamais confondue avec une capacité actuelle.

## Table consolidée (par formation)

| Formation | Capacité | Statut | Preuve / justification |
|---|---|---|---|
| `KOR-01` | Émission/traitement de signal FREK (`FREK-WORK`, `FREK-SCORE`) | `CAPABILITY_ALREADY_REAL` | `services/frek_core.py`, déjà utilisé par les modules legacy KOR-01/02 |
| `KOR-01`/`KOR-02` | Preuve de certification signée pour KORA (`FREK_PROOF` côté KORA) | `CAPABILITY_NOT_IMPLEMENTED` | `READY_FOR_FREK_PROOF = FALSE` dans tous les Evidence Models du corpus |
| `KOR-03` | Infrastructure de production/montage vidéo réelle | `CAPABILITY_NOT_IMPLEMENTED` | Aucune collection média dans ce repo |
| `KOR-04` | Moteur de programmation/curation éditoriale | `CAPABILITY_NOT_IMPLEMENTED` | Aucune collection programmation |
| `KOR-05` | Outils d'opérations créateur (support, incidents) | `CAPABILITY_NOT_IMPLEMENTED` | Aucune collection ops créateur |
| `KOR-06` | DSP/CDN/monitoring streaming, SLA/SLO | `CAPABILITY_NOT_IMPLEMENTED` | Confirmé zéro footprint (KOR-0001 §4) |
| `KOR-07` | Registre de droits/royalties/territoires | `CAPABILITY_NOT_IMPLEMENTED` | Aucune collection contrats/royalties |
| `KOR-08` | Métadonnées/taxonomies/catalogue d'œuvres | `CAPABILITY_NOT_IMPLEMENTED` (KORA) / `CAPABILITY_NOT_CONNECTED` (LabelOS) | `db.fms_resources`/`db.klt_resources` sont des catalogues pédagogiques, pas des catalogues d'œuvres ; LabelOS (`LOS-02`) réel mais non interfacé à KORA |
| `KOR-09` | CRM/A-B testing d'audience à l'échelle | `CAPABILITY_NOT_IMPLEMENTED` | Aucune collection croissance/marketing |
| `KOR-10` | Wallet/JCC | `CAPABILITY_ALREADY_REAL` | `wallet/models.py:44-46` (`jcc_balance`), `wallet/service.py:49`, `wallet/passes.py` |
| `KOR-10` | CVE | `CAPABILITY_TARGET_ONLY` (statut non audité) | `EXTERNAL_PRODUCT_EVIDENCE_NOT_AUDITED` — jamais affirmé inexistant ni existant |
| `KOR-11` | File de modération, signalement, sanctions, transparence | `CAPABILITY_NOT_IMPLEMENTED` | Aucune collection modération/signalement dans `backend/` |
| `KOR-12` | Événements de lecture réels (plays/completions), dashboards | `CAPABILITY_NOT_IMPLEMENTED` | `db.progress` mesure la progression pédagogique Academy, pas une consommation média KORA — domaines distincts |
| `KOR-12` | Moteur de recommandation | `CAPABILITY_NOT_IMPLEMENTED` | Aucun moteur ni modèle dans ce repo |
| `KOR-12` | CVLN Brain → recommandations KORA | `CAPABILITY_NOT_CONNECTED` | Brain réel (`registry.py`, événement `academy.certification.passed`) mais sert la certification Academy, pas KORA |
| `KOR-13` | CRM partenariats/acquisitions, signature électronique | `CAPABILITY_NOT_IMPLEMENTED` | Aucune collection partenariats |
| `KOR-14` | Recherche produit, recommandation UX, app TV/mobile native, tests utilisateurs outillés, analytics produit | `CAPABILITY_NOT_IMPLEMENTED` | Aucune collection produit/UX KORA |
| `KOR-15` | Infrastructure de distribution multi-territoire, gestion de droits automatisée, localisation outillée | `CAPABILITY_NOT_IMPLEMENTED` | Aucune collection réseau international |

## Synthèse par statut

| Statut | Occurrences |
|---|---|
| `CAPABILITY_ALREADY_REAL` | 2 (FREK émission de signal ; Wallet/JCC) |
| `CAPABILITY_PARTIAL` | 0 |
| `CAPABILITY_NOT_CONNECTED` | 3 (LabelOS↔KORA métadonnées ; CVLN Brain↔KORA recommandation ; FREK proof↔KORA certification) |
| `CAPABILITY_NOT_IMPLEMENTED` | 14 lignes (majorité du tableau) |
| `CAPABILITY_TARGET_ONLY` | 1 (CVE, statut non audité) |

## Portée et limites de ce document

Ce Gap Map reflète l'état du code **au moment de la construction du
corpus pédagogique** (branche `claude/cvln-academy-canonical-fms`). Il
ne constitue ni une roadmap produit, ni un engagement de
développement — `NO_KORA_PRODUCT_UPGRADE`, `NO_RUNTIME_BINDING`,
`NO_DB_MUTATION`, `NO_SEED_MUTATION`. Toute décision d'implémenter une
capacité listée `CAPABILITY_NOT_IMPLEMENTED` relève d'un ticket produit
séparé, hors mandat de ce chantier pédagogique.
