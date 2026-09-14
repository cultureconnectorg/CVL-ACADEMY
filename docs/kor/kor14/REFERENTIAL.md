# KOR-14 — Référentiel canonique : Streaming Product & Experience Operations

```
FORMATION: KOR-14
STATUT_LEGACY: NEW
BASELINE: KOR-01/KOR-02
```

## 1. Contenu principal (source : KOR-0001 §3, ligne 14)

Parcours utilisateur · discovery · search · home/feed · bibliothèque ·
player · queue · playlists · recommandations · accessibilité ·
TV/mobile/web · expérience creator · tests utilisateurs · analytics
produit · incidents UX · amélioration continue.

## 2. PROFESSIONAL_ROLE → ACTIVITIES → COMPETENCIES

**Rôle professionnel** : Product manager / UX streaming.

| Activité | Compétence |
|---|---|
| Cartographier | C1 — Cartographier le parcours utilisateur de bout en bout |
| Faire découvrir | C2 — Concevoir discovery, home et feed |
| Faire trouver | C3 — Concevoir une expérience de recherche |
| Organiser | C4 — Concevoir une bibliothèque personnelle |
| Faire écouter | C5 — Concevoir player, file d'attente et playlists |
| Situer la recommandation | C6 — Concevoir le placement UX de recommandations (sans moteur réel) |
| Inclure | C7 — Assurer l'accessibilité de l'expérience |
| Adapter | C8 — Adapter l'expérience à TV/mobile/web |
| Servir le créateur | C9 — Concevoir l'expérience creator in-app (distincte de `KOR-05`) |
| Tester | C10 — Conduire des tests utilisateurs |
| Mesurer le produit | C11 — Analyser des analytics produit (distinct de `KOR-12`) |
| Réagir | C12 — Gérer un incident UX |
| Améliorer | C13 — Piloter une amélioration continue |
| Synthétiser | C14 — Conduire un dossier produit/UX de bout en bout |

`DEPTH_DETERMINES_MODULE_COUNT` : 14 compétences → 14 modules
(`M01`-`M14`).

## 3. Provenance des compétences

Toutes `MARKET_SKILL`. Aucune `KORA_CURRENT_CAPABILITY`.

## 4. Vérification anti-footprint

Aucune collection produit/UX (parcours, tests utilisateurs, analytics
produit) n'existe dans ce repo pour KORA. Toute pratique s'exerce sur
le vehicule fictif Anba Tonèl Host (`KOR-06`), jamais présenté comme
KORA réel.

## 5. Tensions de frontière actives

- **#2 (`KOR-06`/`KOR-14`)** : `KOR-06` = disponibilité, qualité de
  service, infrastructure (vue exploitation). `KOR-14` = parcours,
  ergonomie, expérience perçue (vue utilisateur) — **du même système**
  Anba Tonèl Host, jamais dupliqué : un incident de disponibilité est
  `KOR-06`, un incident d'ergonomie confuse est `KOR-14`.
- **#5 (`KOR-09`/`KOR-14`)** : `KOR-09` = acquisition/rétention/canaux
  externes. `KOR-14` = expérience une fois l'utilisateur dans
  l'application — frontière posée : la première session in-app est
  `KOR-14`, le canal qui l'y a amené est `KOR-09`.
- **C6 (recommandations)** reconfirme, sous l'angle UX cette fois
  (placement, pas modèle de données — voir `KOR-12` pour l'angle
  data), qu'aucun moteur de recommandation KORA n'existe.

## 6. KORA_PRODUCT_GAP

| Capacité évoquée | Statut réel |
|---|---|
| Moteur de recherche produit | `CAPABILITY_NOT_IMPLEMENTED` |
| Système de recommandation en place | `CAPABILITY_NOT_IMPLEMENTED` |
| Application TV/mobile native | `CAPABILITY_NOT_IMPLEMENTED` |
| Outils de test utilisateur intégrés | `CAPABILITY_NOT_IMPLEMENTED` |
| Analytics produit instrumentés | `CAPABILITY_NOT_IMPLEMENTED` |

`NO_KORA_PRODUCT_UPGRADE`.

## 7. Cas fil rouge

**Djems**, product manager/UX à Anba Tonèl Host (`KOR-06`), redessine
le parcours de découverte de *Rasin*, dont l'audience diaspora
(`KOR-09`) peine à naviguer l'application sur mobile avec une faible
littératie numérique.

`STATUS = PROPOSED`.
