# KLT-0008 — Décision déléguée : contextes de livraison & périmètre buildable KLT-06/07/08

```
WORKSTREAM = KLT
KLT-0001..0007 = FROZEN
KLT-0008 = AUTHORIZED = TRUE (ce ticket) — délégation explicite du
Founder ("Prends la décision tu es autorisé. Avant de prendre la
décision audit pour comprendre l'utilité et les niveaux et les
objets", 2026-09-04) pour résoudre §1.5 (INTERNAL/EXTERNAL/BRIDGE) et
§6 (périmètre buildable) des référentiels KLT-0005/0006/0007.
PORTÉE = DÉCISION DE CLASSIFICATION + DÉCISION DE PÉRIMÈTRE, PAS LE
BUILD DE MODULES LUI-MÊME — voir §5.
DB_MUTATION = FALSE (aucun `db.formations` touché — KLT-06/07/08
n'existent pas encore en base)
STOP_AFTER_DELIVERY = TRUE
```

---

## 1. AUDIT — utilité, niveaux, objets

### 1.1 Cadre mécanique réel (pas inventé pour ce ticket)

La classification `INTERNAL`/`EXTERNAL`/`BRIDGE` n'est **pas** un simple
« public vs privé » — c'est une règle Founder déjà gelée pour FMS
(`ACA-0004`, `backend/fms_canonical/delivery_architecture.py`), appliquée
mécaniquement à tout `Formation.contexts` réel :

```
INTERNAL_DELIVERY = E_LEARNING (canal INTERNAL, AVAILABLE)
EXTERNAL_DELIVERY = E_LEARNING (canal EXTERNAL, AVAILABLE)
                     + PHYSICAL (canal EXTERNAL, ELIGIBLE_PENDING_OFFER —
                       jamais réservable tant qu'aucune offre commerciale
                       réelle n'existe)
BRIDGE = point d'entrée/articulation (is_bridge_entry_point = True)
```

Les trois valeurs ne sont **pas exclusives** — une formation peut cumuler
plusieurs contextes (ex. `KLT-03` legacy = `INTERNAL, EXTERNAL, BRIDGE`).
Ce ticket applique cette même règle, sans l'inventer, à `KLT-06`/`07`/`08`.

Le référentiel réel des **niveaux** (`AudienceLevel`, `backend/
models.py:21-22`) est : `DEBUTANT, INTERMEDIAIRE, AVANCE, PROFESSIONNEL,
INSTITUTIONNEL`. `KLT-0001` §2 donne pour les trois formations le niveau
`Avancé` (= `AVANCE`) — au-dessus de la bande d'entrée
(`DEBUTANT`/`INTERMEDIAIRE`) que porte `KLT-01` (`KLT-0003` §1.5).

### 1.2 KLT-06 — Analyste Observatory

- **Utilité réelle** : produire de l'analyse et de la méthode de lecture
  de données pour appuyer d'autres rôles Kiltikonet (`KLT-02` chef de
  projet, `KLT-04` gouvernance, `KLT-07` déploiement — voir `KLT-0005`
  §2, `C3`/`C6`). 5 des 7 compétences (`C1`-`C4`, `C7`) sont une
  littératie/méthode/éthique de la donnée **transférable hors Kiltikonet**
  (un « Cultural Data Analyst » reste employable dans n'importe quelle
  institution culturelle) — ce n'est pas un rôle purement interne
  d'exécution.
- **Niveau** : `Avancé` (`KLT-0001` §2) — pas `Fondamentaux`.
- **Objets réels manipulés** (compétences buildable uniquement, `KLT-0005`
  §2-3) : méthode de lecture d'un observatoire, grille de provenance/
  fiabilité d'un signal, spécification de besoin de données, grille
  éthique/confidentialité, restitution à un public non spécialiste. Les
  objets *bloqués* (tableau de bord réel, signal territorial réel) restent
  `BLOCKED` et hors périmètre de ce ticket.
- **Signal indirect** : la synthèse chiffrée de `KLT-0001` §2 regroupe
  `KLT-06` parmi les 6 « formations publiques » (avec `KLT-01`→`05`), pas
  parmi les 2 « spécialisations avancées » (`KLT-07`/`08`) — un indice
  réel, même si inféré et non déclaré explicitement dans la source.

### 1.3 KLT-07 — Responsable déploiement territorial culturel

- **Utilité réelle** : exécuter le déploiement du **réseau Kiltikonet
  lui-même** — onboarding d'opérateurs, suivi de couverture territoriale,
  gestion de la relation opérateur (`KLT-0006` §2). C'est un rôle qui
  s'exerce *pour* Kiltikonet, sur le réseau Kiltikonet — pas une
  compétence générique vendable ailleurs de la même façon que `KLT-06`.
- **Niveau** : `Avancé`.
- **Objets réels manipulés** : processus d'onboarding opérateur, méthode
  de gestion de la relation opérateur, méthode d'évaluation de
  faisabilité d'extension territoriale, méthode de remontée d'incident.
  L'objet bloqué (état réel de couverture territoriale/licences) reste
  `BLOCKED`.
- **Signal indirect** : `KLT-0001` §2 regroupe `KLT-07` parmi les 2
  « spécialisations avancées » (avec `KLT-08`), séparément des 6
  « publiques » — signal contraire à `KLT-06`.

### 1.4 KLT-08 — Responsable qualité, conformité & audit réseau

- **Utilité réelle** : auditer et faire monter en conformité le **réseau
  d'opérateurs Kiltikonet** (au-delà d'une association isolée, déjà
  couverte par `KLT-04`/M12-M13) et former les opérateurs aux exigences
  (`KLT-0007` §2). Rôle d'audit/contrôle interne au réseau, pas une
  offre pédagogique généraliste.
- **Niveau** : `Avancé`. Signal le plus net des trois : le libellé du
  master plan porte explicitement **« interne »** (« Spécialisation
  pro/interne », `KLT-0001` §2/§3).
- **Objets réels manipulés** : grille d'audit réseau (héritée de `KLT-04`/
  M13), méthode de consolidation multi-opérateurs, matériel de formation
  opérateurs, discipline de recommandation sans décision (héritée). L'objet
  bloqué (statut de conformité agrégé réel) reste `BLOCKED`.
- **Signal indirect** : regroupé parmi les 2 « spécialisations avancées »,
  comme `KLT-07`.

---

## 2. DÉCISION — contextes de livraison

| Formation | `contexts` (décidé) | Rationale principale |
|---|---|---|
| `KLT-06` | `EXTERNAL` | 5/7 compétences buildable sont une littératie/méthode transférable hors Kiltikonet ; regroupement « publiques » de `KLT-0001` §2. `INTERNAL` **non retenu pour l'instant** — les 2 compétences qui justifieraient un usage interne pur (`C5`/`C6`, lecture Observatory réelle) restent `BLOCKED`, donc hors périmètre buildable de ce ticket. `BRIDGE` **non retenu** — niveau `Avancé`, pas un point d'entrée du parcours (`KILTIKONET_PROFESSIONAL_PATHWAY.md` classe déjà `KLT-01` seul comme `ENTRY_PATH`). |
| `KLT-07` | `INTERNAL` | Rôle exercé *pour* le réseau Kiltikonet lui-même, pas une compétence généraliste ; regroupement « spécialisations avancées » de `KLT-0001` §2. `EXTERNAL` non retenu (pas de signal de transférabilité externe comparable à `KLT-06`). `BRIDGE` non retenu — niveau `Avancé`. |
| `KLT-08` | `INTERNAL` | Signal le plus net des trois (libellé « interne » explicite, `KLT-0001` §2/§3) ; rôle de contrôle interne au réseau. `EXTERNAL` non retenu. `BRIDGE` non retenu — niveau `Avancé`. |

**Application mécanique de la règle `ACA-0004`** (`derive_delivery_
architecture`, appliquée à titre indicatif — aucune écriture `db.
formations` réelle tant que ces formations n'existent pas en base) :

| Formation | `E_LEARNING` | `PHYSICAL` | `is_bridge_entry_point` |
|---|---|---|---|
| `KLT-06` (`EXTERNAL`) | canal `EXTERNAL`, `AVAILABLE` | canal `EXTERNAL`, `ELIGIBLE_PENDING_OFFER` (jamais réservable sans offre réelle) | `False` |
| `KLT-07` (`INTERNAL`) | canal `INTERNAL`, `AVAILABLE` | — (pas de canal `EXTERNAL`) | `False` |
| `KLT-08` (`INTERNAL`) | canal `INTERNAL`, `AVAILABLE` | — | `False` |

**Cette décision reste révisable** — notamment pour `KLT-06`, si les
compétences bloquées (`C5`/`C6`) sont un jour débloquées par un accès
Observatory réel, la question d'ajouter `INTERNAL` (pour un usage staff
sur données réelles) devra être réexaminée, pas assumée dès maintenant.

---

## 3. DÉCISION — périmètre buildable (résout §6 de chaque référentiel)

**Autorisé** : construire les compétences marquées `BUILDABLE` dans
`KLT-0005`/`0006`/`0007` — 5/7 (`KLT-06`), 6/7 (`KLT-07`), 6/7 (`KLT-08`).
**Non autorisé** : les compétences `BLOCKED` (`KLT-06` C5/C6, `KLT-07`
C4, `KLT-08` C4) restent explicitement différées — aucune donnée
Observatory/Network/Compliance simulée pour les débloquer artificiellement.

| Formation | Modules à construire | Modules différés (`BLOCKED`) |
|---|---|---|
| `KLT-06` | M01, M02, M03, M04, M07 (5) | M05, M06 (2) |
| `KLT-07` | M01, M02, M03, M05, M06, M07 (6) | M04 (1) |
| `KLT-08` | M01, M02, M03, M05, M06, M07 (6) | M04 (1) |

Chaque formation aura donc, à l'issue du prochain build, **une structure
à trous explicitement documentée** (5 ou 6 modules réels + 1-2 modules
`À produire ultérieurement`), plutôt qu'un compte artificiellement
complété. C'est le même principe déjà appliqué dans `KLT-01`/M10 (limite
nommée, pas contournée).

---

## 4. Mise à jour des documents (par ce ticket)

- `KLT-0005`/`0006`/`0007` §1.5 et §6 : statut `UNRESOLVED` → `RESOLVED
  par KLT-0008`, avec renvoi vers ce document (la structure de
  compétences et la traçabilité déjà gelées ne changent pas).
- Master Package (`06_KLT06_PLANNED/PLANNED.md`, `07_.../PLANNED.md`,
  `08_.../PLANNED.md`, `00_MASTER/MASTER_INDEX.md`) : statut mis à jour
  pour refléter la décision, sans dupliquer ce document.

## 5. Ce que cette décision N'AUTORISE PAS

Cette décision résout une **classification et un périmètre** — elle
n'est pas, par elle-même, une autorisation de rédiger le contenu
pédagogique des modules. Conformément au rythme déjà appliqué à `KLT-01`
(`KLT-0003` référentiel gelé → **STOP** → `KLT-0004` autorisé séparément
pour le build), le build effectif de ces 17 modules (5+6+6) sur les 3
formations reste un ticket distinct, à autoriser explicitement.

## REVIEW

- `NO_DB_MUTATION` — aucune écriture `db.formations`, ces formations
  n'existent pas encore en base.
- `NO_FAKE_OBSERVATORY` / `NO_FAKE_NETWORK` / `NO_FAKE_COMPLIANCE` —
  décision de classification uniquement, aucune donnée simulée pour
  débloquer les compétences `BLOCKED`.
- Règle `ACA-0004` réutilisée à l'identique, pas réinventée par
  formation.

```bash
git status --short   # expect: only this new doc + 3 referential updates
                      # + 4 Master Package status updates
```

## FREEZE

**`KLT-06/07/08_CONTEXT_AND_SCOPE = FROZEN`.** `contexts` décidés,
périmètre buildable décidé (17/21 modules indicatifs autorisés, 4
explicitement différés). Les référentiels `KLT-0005`/`0006`/`0007`
restent par ailleurs inchangés dans leur structure de compétences.

`STOP = TRUE.` Build effectif des modules non commencé — en attente
d'autorisation explicite pour ce ticket suivant.
