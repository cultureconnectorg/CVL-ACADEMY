# KOR-06 — Référentiel canonique : Streaming Platform Operations

```
SOURCE = KOR-0001 §2/§4 ("DSP/CDN/streaming... zéro footprint" côté
KORA elle-même), KOR-0002 §4
DB_MUTATION = FALSE
MÉTHODE DE CE TICKET POUR LES COMPÉTENCES "PRODUIT-ADJACENTES" : le
savoir-faire d'exploitation de plateforme (DSP/CDN/monitoring/SLA) est
un savoir de marché réel, enseignable via un véhicule pédagogique
générique explicitement distinct de KORA (ici, "Anba Tonèl Host", un
hébergeur fictif générique) — jamais présenté comme une capacité KORA
réelle. Ce qui reste `PRODUCT_DEPENDENCY = NOT_IMPLEMENTED` est
strictement : l'existence d'une plateforme KORA réelle elle-même
(aucune compétence n'exige de plateforme KORA vivante pour être
prouvée — voir §6).
```

## 1. Métier réel et rôle professionnel

**Ops de plateforme streaming/podcast** — assure le fonctionnement
quotidien d'un service de diffusion (DSP), de l'ingestion à la
livraison, la qualité de service, la gestion d'incidents et la
continuité — chez un hébergeur/DSP du marché réel, pas nécessairement
KORA.

## 2. Activités professionnelles réelles

Comprendre le fonctionnement d'un DSP ; modéliser une chaîne ingestion→
delivery ; exploiter quotidiennement (disponibilité des contenus) ;
comprendre player/CDN ; définir SLA/SLO ; gérer incidents et
escalade ; monitorer et assurer la continuité ; opérer à l'échelle
multi-territoires.

## 3. Compétences (provenance)

| # | Compétence | Provenance |
|---|---|---|
| C1 | Comprendre le fonctionnement d'un DSP | `MARKET_SKILL` |
| C2 | Modéliser une chaîne ingestion→delivery | `MARKET_SKILL` |
| C3 | Exploiter quotidiennement une plateforme (disponibilité) | `MARKET_SKILL` |
| C4 | Comprendre player et CDN (concepts) | `MARKET_SKILL` |
| C5 | Définir un SLA/SLO et la qualité de service | `MARKET_SKILL` |
| C6 | Gérer un incident et l'escalade | `MARKET_SKILL` |
| C7 | Monitorer en continu et assurer la continuité | `MARKET_SKILL` |
| C8 | Opérer à l'échelle multi-territoires | `MARKET_SKILL` |
| C9 | Conduire des opérations de plateforme de bout en bout et les défendre | `MARKET_SKILL` (synthèse) |

Toutes `MARKET_SKILL` — enseignées via un véhicule générique
("Anba Tonèl Host"), jamais présentées comme une capacité KORA réelle.
Aucune compétence n'est `KORA_CURRENT_CAPABILITY` (KORA n'opère aucune
plateforme réelle aujourd'hui).

## 4. Blocs pédagogiques → modules

Compréhension DSP (C1) → modélisation technique (C2, C4) →
exploitation (C3) → qualité de service (C5) → incidents (C6) →
monitoring/continuité (C7) → multi-territoires (C8) → synthèse (C9).

## 5. Boundary check

| Formation/entité | Recouvrement | Handoff |
|---|---|---|
| `KOR-14` (product/experience, non construit) | Exploitation infra (`KOR-06`) vs parcours utilisateur (`KOR-14`) — `KOR-0002` §4 tension #2 | `KOR-06` = vue infra/ops ; `KOR-14` = vue UX du même système |
| `KOR-01` (distribution via outils marché) | `KOR-01`/M10 utilise déjà un hébergeur réel du marché pour publier | `KOR-06` explique en profondeur le métier qui exploite cet hébergeur, ne le réutilise pas comme cas — véhicule distinct (Anba Tonèl Host) pour éviter toute confusion |

## 6. Dépendances KORA vérifiées — `KORA_PRODUCT_GAP`

**Aucune plateforme de streaming/DSP KORA réelle n'existe dans ce
repo** (`ACADEMY_LOCAL_EVIDENCE = NOT_FOUND`, reconfirmé, cohérent avec
`KOR-0001` §4). Ce gap est documenté ici pour alimenter le futur
`KORA_PRODUCT_CAPABILITY_GAP_MAP` :

| Capacité nommée par le contenu principal | Statut réel KORA |
|---|---|
| DSP/plateforme d'écoute | `CAPABILITY_NOT_IMPLEMENTED` |
| CDN | `CAPABILITY_NOT_IMPLEMENTED` |
| Monitoring/dashboards d'exploitation | `CAPABILITY_NOT_IMPLEMENTED` |
| Infrastructure multi-territoires | `CAPABILITY_NOT_IMPLEMENTED` |

Aucune compétence de ce référentiel ne dépend de l'existence de ces
capacités pour être enseignée ou évaluée — toutes sont enseignées via
le véhicule générique `Anba Tonèl Host` (`case/CASE.md`).

## 7. `PUBLIC/EXTERNAL/BRIDGE`

`UNRESOLVED`.

## 8. Statut

`CORE_BUILD = COMPLETE`, `FULL_CURRICULUM = COMPLETE` (aucune
compétence non enseignée), `FULLY_COMPLETE = FALSE` au niveau `KORA`
global — et au niveau produit, `KORA_PRODUCT_GAP` documenté ci-dessus.
