# KOR-10 — Référentiel canonique : Content Monetization & Media Economics

```
SOURCE = KOR-0001 §2/§4, KOR-0002 §4 tension #6 (KOR-10/KOR-07)
DB_MUTATION = FALSE
Wallet/JCC = réel et local (wallet/models.py, wallet/service.py,
wallet/passes.py) — seul domaine du tableau Founder avec une
implémentation locale réelle (KOR-0001 §4). CVE reste
EXTERNAL_PRODUCT_EVIDENCE_NOT_AUDITED, jamais conclu inexistant
(KOR-0002 §1.3).
```

## 1. Métier réel et rôle professionnel

**Spécialiste économie des médias/streaming** — conçoit un modèle
économique soutenable pour un contenu diaspora (abonnement, publicité,
sponsoring, partage de valeur créateur), avec des moyens réels
limités.

## 2. Activités professionnelles réelles

Diagnostiquer un modèle économique ; comprendre free/premium et
abonnement ; comprendre publicité/sponsoring ; calculer ARPU/LTV et
unit economics ; comprendre le partage de valeur créateur/royalties ;
comprendre coûts, pricing, bundles ; appliquer Wallet/JCC ; traiter la
question CVE avec la vigilance appropriée.

## 3. Compétences (provenance)

| # | Compétence | Provenance |
|---|---|---|
| C1 | Diagnostiquer un modèle économique de streaming | `MARKET_SKILL` |
| C2 | Comprendre free/premium et abonnement | `MARKET_SKILL` |
| C3 | Comprendre publicité et sponsoring | `MARKET_SKILL` |
| C4 | Comprendre ARPU/LTV et unit economics | `MARKET_SKILL` |
| C5 | Comprendre revenus créateurs et partage de valeur | `MARKET_SKILL` |
| C6 | Comprendre royalties — modèles de calcul | `MARKET_SKILL` |
| C7 | Comprendre coûts streaming, pricing et bundles | `MARKET_SKILL` |
| C8 | Appliquer Wallet/JCC au modèle économique | `KORA_CURRENT_CAPABILITY` (réel, local) |
| C9 | Clarifier le statut de CVE avant toute application | `MARKET_SKILL` (méthode de vigilance) |
| C10 | Conduire une analyse économique de bout en bout et la défendre | `MARKET_SKILL` (synthèse) |

**C8 est la seule compétence `KORA_CURRENT_CAPABILITY`** de tout le
corpus KOR construit à ce jour — `wallet/models.py:44-46`
(`jcc_balance`), `wallet/service.py:49`, `wallet/passes.py` sont réels
et locaux. Aucune autre `PRODUCT_DEPENDENCY` bloquante.

## 4. Blocs pédagogiques → modules

Diagnostic (C1) → modèles de revenu (C2-C3) → mesures économiques
(C4) → partage créateur (C5-C6) → coûts/pricing (C7) → Wallet/JCC
(C8) → CVE (C9) → synthèse (C10).

## 5. Boundary check

| Formation | Recouvrement | Handoff |
|---|---|---|
| `KOR-07` (droits/licensing) | Royalties apparaissent des deux côtés — `KOR-0002` §4 tension #6 | `KOR-07` = cadre contractuel du calcul, `KOR-10` = application au modèle économique global |

## 6. Dépendances KORA vérifiées

Wallet/JCC réel — voir en-tête. CVE reste `EXTERNAL_PRODUCT_EVIDENCE_
NOT_AUDITED` — le module C9 traite spécifiquement cette vigilance,
jamais une définition inventée.

## 7. `PUBLIC/EXTERNAL/BRIDGE`

`UNRESOLVED`.

## 8. Statut

`CORE_BUILD = COMPLETE` visé.
