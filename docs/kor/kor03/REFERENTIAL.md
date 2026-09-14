# KOR-03 — Référentiel canonique : Video & Streaming Production

```
WORKSTREAM = KOR (KORA)
AUTORISATION = GO GLOBAL, "KORA ACADEMY — FULL 15 FORMATIONS CONTINUOUS
BUILD" (Founder, 2026-09-05), CONTINUOUS_BUILD = TRUE
SOURCE = KOR-0001 §2 (contenu principal verbatim), KOR-0001 §4 (aucune
mention KOR-03 dans les dépendances vérifiées — territoire neuf),
KOR-0002 §4 tension #1 (KOR-01 audio vs KOR-03 vidéo)
DB_MUTATION = FALSE — livrable entièrement documentaire
DEPTH_DETERMINES_MODULE_COUNT — le nombre de modules ci-dessous résulte
de l'analyse des compétences, pas d'un objectif de volume.
```

## 1. Métier réel et rôle professionnel

**Producteur/réalisateur vidéo & streaming caribéen** — conçoit, tourne,
monte et livre des contenus vidéo courts et moyens formats pour des
plateformes de streaming diaspora, seul ou en petite équipe, souvent
sans moyens de production broadcast traditionnels.

## 2. Activités professionnelles réelles

Préparer un tournage (repérage, script visuel, plan lumière/son) ;
tourner en single-cam ou multicam ; diriger une régie légère en direct
ou en léger différé ; monter ; postproduire (étalonnage, effets, sound
design vidéo) ; encoder aux formats de livraison du marché ; publier et
contrôler la qualité technique avant mise en ligne.

## 3. Compétences et sous-compétences (provenance classée)

| # | Compétence | Provenance | Sous-compétences |
|---|---|---|---|
| C1 | Diagnostiquer une opportunité vidéo/streaming | `MARKET_SKILL` | analyse de contenus référence, positionnement |
| C2 | Préproduire et écrire pour l'image | `MARKET_SKILL` | script visuel, repérage, plan lumière/son prévisionnel |
| C3 | Éclairer et sonoriser un plateau | `MARKET_SKILL` | lumière naturelle/artificielle, prise de son synchrone |
| C4 | Tourner en single-cam | `MARKET_SKILL` | cadrage, mouvement, continuité |
| C5 | Tourner et réaliser en multicam/direct | `MARKET_SKILL` | coordination caméras, direction en direct |
| C6 | Diriger une régie | `MARKET_SKILL` | commutation, communication équipe, décision en direct |
| C7 | Monter une vidéo | `MARKET_SKILL` | montage narratif, rythme, raccords |
| C8 | Postproduire (étalonnage, effets, son) | `MARKET_SKILL` | correction colorimétrique, habillage, mixage vidéo |
| C9 | Encoder pour la livraison | `MARKET_SKILL` | formats, résolutions, débits selon plateforme cible |
| C10 | Publier et contrôler la qualité | `MARKET_SKILL` | vérification technique pré-mise en ligne |
| C11 | Conduire une production vidéo de bout en bout et la défendre | `MARKET_SKILL` (synthèse) | — |

Aucune compétence `PRODUCT_DEPENDENCY` — la production vidéo elle-même
ne requiert aucune brique KORA vivante (cohérent avec le constat déjà
posé pour `KOR-01`/`KOR-02`, `KOR-0002` §2.5/§3).

## 4. Blocs pédagogiques → modules

Concept/diagnostic (C1) → préproduction (C2) → captation technique
(C3-C6) → post (C7-C8) → livraison (C9-C10) → synthèse (C11). Détail
module par module : `00_BLUEPRINTS.md`.

## 5. Boundary check

| Formation/entité | Nature du recouvrement | Handoff |
|---|---|---|
| `KOR-01` (audio) | Techniques de captation/montage proches, médium différent (`KOR-0002` §4 tension #1) | `KOR-01` possède l'audio ; `KOR-03` possède l'image et le son synchrone à l'image — un module son (C3) reste nécessaire côté vidéo car synchronisé à l'image, pas un doublon de `KOR-01` |
| FMS (Factory Maker Studio, musique) | Aucun recouvrement direct — FMS ne couvre pas la vidéo | Aucun handoff nécessaire |
| Kiltikonet | Aucun recouvrement — métiers de médiation culturelle, pas de production technique | Aucun |

## 6. Dépendances KORA vérifiées

Aucune brique technique KORA (encodeur, CDN, plateforme de diffusion
vidéo) n'existe dans ce repo — reconfirmé (`KOR-0001` §4, "DSP/CDN/
streaming... zéro footprint"). La production elle-même (tournage,
montage) ne dépend d'aucune de ces briques : seule la **diffusion
finale sur une vraie plateforme KORA** serait `PRODUCT_DEPENDENCY` —
non requise pour valider les compétences C1-C11, cohérent avec le
traitement déjà posé pour `KOR-01`/M10 (distribution via outils marché
réels, pas une plateforme KORA).

## 7. `PUBLIC/EXTERNAL/BRIDGE`

`UNRESOLVED` — non tranché par ce ticket (`KOR-0001` §3, décision
formation par formation non encore posée pour `KOR-03`). Cela ne bloque
pas la construction pédagogique, qui n'en dépend pas.

## 8. Statut

`CORE_BUILD = COMPLETE` visé, `FULL_CURRICULUM` visé, `FULLY_COMPLETE
= FALSE` au niveau `KORA` global (rappel permanent, `docs/kor/
README.md`).
