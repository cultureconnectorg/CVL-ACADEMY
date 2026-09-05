# KOR-07 — Référentiel canonique : Media Rights, Licensing & Distribution

```
SOURCE = KOR-0001 §2/§4, KOR-0002 §4 tensions #3 (KOR-07/KOR-13),
#6 (KOR-07/KOR-10), #9 (KOR-07/KOR-15)
DB_MUTATION = FALSE
NEEDS_EXPERT_REVIEW = TRUE pour l'ensemble de ce référentiel — matière
juridique réelle (droit d'auteur, contrats). Ce package enseigne une
méthode et une vigilance professionnelle, jamais un avis juridique
qualifié. Toute application réelle doit être validée par un juriste
spécialisé (`NEEDS_EXPERT_REVIEW`, règle 16 du mandat Founder).
```

## 1. Métier réel et rôle professionnel

**Chargé(e) de droits et licences média** — analyse et sécurise les
droits d'exploitation d'un contenu (copyright, droits voisins,
licences), négocie/lit des contrats de distribution, gère takedowns et
royalties — **niveau de sensibilisation professionnelle**, pas
qualification d'avocat.

## 2. Activités professionnelles réelles

Diagnostiquer une situation de droits ; comprendre licences/masters/
publishing ; gérer territoires et fenêtres d'exploitation ;
comprendre exclusivités et clearances ; lire/analyser un contrat de
distribution ; traiter un takedown ; comprendre royalties et
reporting ; appréhender le cadre de la distribution internationale.

## 3. Compétences (provenance)

| # | Compétence | Provenance |
|---|---|---|
| C1 | Diagnostiquer une situation de droits média | `MARKET_SKILL` |
| C2 | Comprendre licences, masters, publishing | `MARKET_SKILL` |
| C3 | Comprendre territoires et fenêtres d'exploitation | `MARKET_SKILL` |
| C4 | Comprendre exclusivités et clearances | `MARKET_SKILL` |
| C5 | Lire et analyser un contrat de distribution | `MARKET_SKILL` |
| C6 | Gérer un takedown | `MARKET_SKILL` |
| C7 | Comprendre royalties et reporting | `MARKET_SKILL` |
| C8 | Appréhender le cadre de la distribution internationale | `MARKET_SKILL` |
| C9 | Conduire une analyse de droits de bout en bout et la défendre | `MARKET_SKILL` (synthèse) |

Aucune `PRODUCT_DEPENDENCY` de blocage — enseignable sans registre de
droits KORA réel (qui n'existe pas, `ACADEMY_LOCAL_EVIDENCE = NOT_
FOUND`). **Chaque module rappelle explicitement `NEEDS_EXPERT_REVIEW`**
avant toute application réelle.

## 4. Blocs pédagogiques → modules

Diagnostic (C1) → notions fondamentales (C2-C4) → analyse contractuelle
(C5) → gestion opérationnelle (C6-C7) → international (C8) → synthèse
(C9).

## 5. Boundary check

| Formation | Recouvrement | Handoff |
|---|---|---|
| `KOR-13` (partenariats créateurs, non construit) | Cadre juridique (`KOR-07`) vs relation business de négociation de partenariat (`KOR-13`) — `KOR-0002` §4 tension #3 | `KOR-07` analyse le cadre légal, `KOR-13` construit la relation |
| `KOR-10` (monétisation, non construit) | Royalties apparaissent des deux côtés — `KOR-0002` §4 tension #6 | `KOR-07` = cadre contractuel du calcul ; `KOR-10` = application au modèle économique |
| `KOR-15` (réseau international, non construit) | Droits territoriaux (`KOR-07`) vs stratégie de déploiement (`KOR-15`) — `KOR-0002` §4 tension #9 | `KOR-07` pose le cadre légal, `KOR-15` la stratégie de marché |
| `KOR-08` (metadata, non construit) | Les métadonnées de droits (ayants droit) recoupent le catalogue métadonnées | `KOR-07` = statut légal du droit ; `KOR-08` = métadonnée descriptive |

## 6. Dépendances KORA vérifiées

Aucun registre de droits/royalties KORA réel — `ACADEMY_LOCAL_EVIDENCE
= NOT_FOUND`. `CVE` (cité par le Founder pour `KOR-10`, potentiellement
lié aux royalties) reste `EXTERNAL_PRODUCT_EVIDENCE_NOT_AUDITED` —
jamais conclu inexistant.

## 7. `PUBLIC/EXTERNAL/BRIDGE`

`UNRESOLVED`.

## 8. Statut

`CORE_BUILD = COMPLETE` visé. `NEEDS_EXPERT_REVIEW = TRUE` en
permanence sur l'ensemble du corpus — voir chaque `A01`/`RUBRIC`.
