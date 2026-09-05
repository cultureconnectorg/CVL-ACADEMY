# KOR-04 — Référentiel canonique : Editorial Programming & Curation

```
SOURCE = KOR-0001 §2/§4, KOR-0002 §4 tension #8 (KOR-04/KOR-02,
programmation vs storytelling)
DB_MUTATION = FALSE
```

## 1. Métier réel et rôle professionnel

**Programmateur/curateur éditorial diaspora** — décide ce qui est mis
en avant, quand, et pour qui, à travers un catalogue de contenus déjà
produits par d'autres (créateurs, collectifs) — distinct du métier de
créateur (`KOR-01`/`02`/`03`).

## 2. Activités professionnelles réelles

Définir une ligne éditoriale ; connaître les publics visés ;
programmer un calendrier ; curer musique/vidéo en playlists ; gérer des
cycles éditoriaux ; veiller à la diversité culturelle du catalogue mis
en avant ; contextualiser un contenu pour un nouveau public ;
recommander éditorialement (choix humain, pas algorithmique) ;
programmer des événements ; mesurer la performance de la programmation.

## 3. Compétences (provenance)

| # | Compétence | Provenance |
|---|---|---|
| C1 | Diagnostiquer une ligne éditoriale et un contexte de programmation | `MARKET_SKILL` |
| C2 | Connaître et segmenter les publics visés par une programmation | `MARKET_SKILL` |
| C3 | Construire un calendrier et des cycles éditoriaux | `MARKET_SKILL` |
| C4 | Curer musique/vidéo en playlists cohérentes | `MARKET_SKILL` |
| C5 | Garantir la diversité culturelle d'une programmation | `MARKET_SKILL` |
| C6 | Contextualiser un contenu pour un nouveau public | `MARKET_SKILL` |
| C7 | Recommander éditorialement (curation humaine) | `MARKET_SKILL` |
| C8 | Programmer un événement et mesurer sa performance | `MARKET_SKILL` |
| C9 | Conduire une programmation éditoriale de bout en bout et la défendre | `MARKET_SKILL` (synthèse) |

Aucune `PRODUCT_DEPENDENCY` — la programmation éditoriale est un
travail humain de choix, pas un système technique ; elle ne requiert
aucune brique KORA vivante.

## 4. Blocs pédagogiques → modules

Diagnostic (C1) → connaissance publics (C2) → construction du
calendrier (C3) → curation (C4-C5) → contextualisation et
recommandation (C6-C7) → événements et mesure (C8) → synthèse (C9).

## 5. Boundary check

| Formation | Recouvrement | Handoff |
|---|---|---|
| `KOR-02` (storytelling) | Programmer un contenu existant vs créer un contenu original — `KOR-0002` §4 tension #8 | `KOR-02` crée, `KOR-04` met en avant ce qui existe déjà ; `KOR-04` ne réécrit ni ne recadre le contenu (relèverait de `KOR-02`) |
| `KOR-12` (data/intelligence, non construit) | Recommandation éditoriale humaine (`KOR-04`) vs recommandation algorithmique/data (`KOR-12`) | Distinction explicite posée en M07 : la curation ici reste un choix humain assumé, jamais présentée comme pilotée par des données réelles |
| `KOR-09` (audience/growth, non construit) | Mesure de performance de programmation (`KOR-04`) vs croissance d'audience globale (`KOR-09`) | `KOR-04` mesure sa propre programmation, ne construit pas de stratégie d'acquisition |

## 6. Dépendances KORA vérifiées

Aucun système de programmation/CMS éditorial KORA réel dans ce repo —
`ACADEMY_LOCAL_EVIDENCE = NOT_FOUND`. La compétence reste enseignable
sur un catalogue de cas simulé (voir `case/CASE.md`), sans fabriquer de
capacité produit.

## 7. `PUBLIC/EXTERNAL/BRIDGE`

`UNRESOLVED`, non tranché par ce ticket.

## 8. Statut

`CORE_BUILD = COMPLETE` visé, aucune compétence `BLOCKED`.
