# Kiltikonet Professional Pathway

```
Logique de progression entre métiers, fondée sur les prérequis réels
déjà déclarés (seed_data.py) et les frontières de rôle posées dans
chaque référentiel — pas une progression linéaire imposée a priori.
```

## Ce que les prérequis réels disent (et ne disent pas)

| Relation déclarée | Nature |
|---|---|
| `KLT-01` → `KLT-02` (recommandé) | `PROGRESSION` faible — utile, non bloquante |
| `KLT-01` + `KLT-02` → `KLT-03` (requis) | `PREREQUISITE` fort |
| `KLT-01` → `KLT-05` (recommandé, avec `FRK-01`) | `PROGRESSION` faible |
| — → `KLT-04` | Aucun prérequis KLT déclaré — `ENTRY_PATH` indépendant |

**Aucune chaîne linéaire unique n'est déclarée entre les 5 métiers.**
Forcer une lecture "KLT-01 → KLT-02 → KLT-03 → KLT-04 → KLT-05" serait
une invention — les données réelles montrent une structure plus proche
d'un **hub** (`KLT-01` comme entrée la plus fréquemment recommandée) que
d'une chaîne.

## Classification par relation

### `ENTRY_PATH` — points d'entrée sans prérequis

- **`KLT-01` (Médiateur culturel)** — aucun prérequis, niveau
  Fondamentaux. C'est le point d'entrée le plus naturel du corpus : trois
  autres formations le recommandent ou l'exigent en amont.
- **`KLT-04` (Gouvernance)** — aucun prérequis KLT déclaré. Entrée
  indépendante, cohérente avec son objet (une association a besoin d'une
  gouvernance dès sa création, pas après un parcours de médiation).

### `PROGRESSION` — enchaînements réels, non bloquants

- `KLT-01` → `KLT-02` : un médiateur qui a pratiqué le terrain comprend
  mieux ce qu'un projet doit livrer. Recommandé, pas requis.
- `KLT-01` → `KLT-05` : la même logique — comprendre la médiation avant
  d'opérer la présence numérique qui la sert.

### `PREREQUISITE` — enchaînement bloquant réel

- `KLT-01` + `KLT-02` → `KLT-03` : seul enchaînement à prérequis
  **multiple et requis** du corpus. Cohérent avec la compétence
  démontrée : négocier des partenariats institutionnels suppose d'avoir
  déjà mené une action (`KLT-01`) et piloté un projet (`KLT-02`).

### `SPECIALIZATION` — formations qui approfondissent un axe plutôt qu'elles ne progressent

- **`KLT-04` (Gouvernance)** peut être suivie en parallèle de n'importe
  quelle autre formation KLT — elle porte sur la structure elle-même
  (l'association), pas sur une action que l'association mène. Un
  médiateur (`KLT-01`) qui devient aussi trésorier de son association a
  besoin de `KLT-04` sans que cela dépende de `KLT-02`/`03`/`05`.
- **`KLT-05` (Opérateur plateforme)** est également largement autonome —
  son seul lien déclaré est `KLT-01` (recommandé), pas `KLT-02`/`03`/`04`.

### `CROSSOVER` — points de bascule entre métiers, identifiés dans le contenu lui-même

| Depuis | Vers | Point de bascule réel (cité dans les modules) |
|---|---|---|
| `KLT-01` | `KLT-03` | L'arbitrage éthique posé en `KLT-01`/M07 (tension spectacle/rituel) est repris tel quel par `KLT-03`/M07 (diplomatie culturelle) — un médiateur qui doit représenter Kiltikonet en instance bascule vers ce rôle. |
| `KLT-02` | `KLT-03` | `KLT-02`/M04 (recherche de financement DAC/CTM/OIF) est le premier contact avec des institutions que `KLT-03` professionnalise entièrement. |
| `KLT-03` | `KLT-04` | `KLT-03`/M06 (négocier une convention) s'arrête explicitement à la préparation — la validation reste `KLT-04` (gouvernance/CA). |
| `KLT-04` | `KLT-07` (`PLANNED`) | `KLT-04`/M11 (gouvernance territoriale, réseau multi-opérateurs) esquisse, sans `Network` réel, ce que `KLT-07` couvrirait avec un accès réel — signalé aussi dans `06_KLT06_PLANNED`/`07_KLT07_PLANNED`. |
| `KLT-05` | `KLT-06` (`PLANNED`) | `KLT-05`/M09 (data lineage, legacy analytics) est le socle réel sur lequel `KLT-06` (Analyste Observatory) se construirait avec un accès Observatory réel. |

## Vue synthétique

```
                     ┌────────── KLT-04 (Gouvernance) ── indépendante ──┐
                     │                                                  │
   ENTRY ── KLT-01 ──┼── (recommandé) ── KLT-02 ──(requis avec KLT-01)──┼── KLT-03
                     │                                                  │
                     └── (recommandé) ── KLT-05 ── (data réelle) ──> [KLT-06 PLANNED]
                                                                          
   KLT-04 ── (gouvernance réseau esquissée) ──> [KLT-07 PLANNED]
   KLT-04 ── (audit association déjà couvert) ──> [KLT-08 PLANNED, frontière à clarifier]
```

## Ce que ce document ne fait pas

Ne force aucune progression linéaire non justifiée par les compétences
réelles (rappel de l'instruction : "ne pas forcer une progression
linéaire si les compétences ne la justifient pas"). Ne construit aucun
mécanisme d'orientation ou de recommandation runtime — c'est une carte de
lecture, pas un moteur.
