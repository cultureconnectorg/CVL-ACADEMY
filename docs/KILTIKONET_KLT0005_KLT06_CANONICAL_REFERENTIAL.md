# KLT-0005 — KLT-06 Analyste Observatory / Cultural Data Analyst — Référentiel canonique

```
WORKSTREAM = KLT
KLT-0001..0004 = FROZEN · Kiltikonet Master Package v1 = DELIVERED
KLT-0005 = AUTHORIZED = TRUE (ce ticket) — portée explicitement limitée
au RÉFÉRENTIEL (compétences + structure indicative de modules), PAS aux
modules eux-mêmes ni aux assessments — décision Founder du 2026-09-04
("un seul référentiel canonique d'abord").
KLT-06 MODULE CONTENT BUILD = NOT_AUTHORIZED (hors scope de ce ticket)
METHOD = AUDIT -> COMPETENCY MAP -> STRUCTURE INDICATIVE -> TRAÇABILITÉ
-> REVIEW -> FREEZE (référentiel uniquement)
DB_MUTATION = FALSE / RUNTIME_BINDING = FALSE / SEED_MUTATION = FALSE /
FAKE_OBSERVATORY = FALSE
STOP_AFTER_DELIVERY = TRUE
```

## Avertissement de source — plus mince que KLT-01→05

Contrairement à `KLT-01`→`05`, **`KLT-06` n'a ni legacy** (`KLT-0001` §1 :
"zéro trace nulle part dans le repo") **ni détail de module par module
dans le master plan** — `KLT-0001` §2 ne donne, pour `KLT-06`, qu'un
intitulé, un type, un statut `NEW`, un niveau, une priorité et un domaine
de dépendance ("8 modules planned" est un **chiffre indicatif de la
feuille *Vue d'ensemble*, sans détail module par module disponible dans
ce repo** — contrairement à `KLT-01` où `seed_modules.py` fournissait 9
modules réels et le master plan en nommait explicitement d'autres).

**Conséquence assumée** : la carte de compétences ci-dessous est
**`PROPOSED`** de bout en bout — dérivée par Claude du seul intitulé
métier + domaine de dépendance nommé, croisée avec les frontières déjà
posées par `KLT-01`→`05` pour éviter toute duplication, **jamais
présentée comme extraite d'un détail de master plan que je n'ai pas**.
C'est une différence de nature avec `KLT-0003` (où une majorité de
compétences étaient `OBSERVED` depuis un vrai contenu legacy), à ne pas
perdre.

---

## 1. AUDIT

### 1.1 Métier cible

**Analyste Observatory / Cultural Data Analyst** (`KLT-0001` §2, ligne 6)
— type `Formation / spécialisation`, statut `NEW`, niveau `Avancé`,
priorité `P1`, dépendance nommée : `Observatory / data lineage / signaux`.

### 1.2 État réel d'Observatory dans Academy (`OBSERVED`)

`KLT-0001` §4, reconfirmé ici : **zéro footprint** — aucune collection
`observatory_events`/`signals`/`adapters` dans `backend/`, aucun shim
d'intégration (contrairement à Culture Connect ou Kiltikonet qui ont un
shim réel non configuré). `Observatory` n'existe dans ce repo sous
aucune forme, ni donnée ni interface. `NOT_CONNECTED` en Academy /
`EXTERNAL_EVIDENCE_NOT_AUDITED` à l'extérieur.

### 1.3 Nature du blocage — pourquoi `KLT-06` diffère de `KLT-01`/M10

Dans `KLT-01`/M10, `KLT-02`/M09, `KLT-03`/M10, `KLT-05`/M09, Observatory
est une **dépendance annexe** d'un module parmi 11-14 — le module se
recentre sur ce qui est réel (`frek_signal`) et nomme la limite. Pour
`KLT-06`, Observatory est **l'objet même du métier** : on ne peut pas
"analyser des données Observatory" sans données Observatory. La
`PLANNED.md` déjà livrée dans le Master Package le dit explicitement :
bâtir les modules qui nécessitent une lecture Observatory réelle
simulerait le système, ce qu'aucune discipline de ce corpus n'autorise.

**Ce référentiel distingue donc, compétence par compétence, ce qui est
réellement constructible aujourd'hui (méthode, littératie, éthique,
spécification de besoin) de ce qui reste bloqué (lecture et restitution
de données Observatory réelles)** — plutôt que de déclarer tout le métier
bloqué ou, à l'inverse, de prétendre qu'il ne l'est pas.

### 1.4 Limites du rôle — ce que le métier n'est PAS

Cross-référencé contre `KLT-01`→`05` pour éviter le chevauchement :

- **N'anime pas** d'atelier de médiation ni de dispositif culturel
  terrain — c'est `KLT-01`.
- **Ne gère pas** de budget ni de projet culturel — c'est `KLT-02`.
- **Ne négocie pas** de partenariat institutionnel — c'est `KLT-03`.
- **N'a pas** d'autorité de gouvernance associative ou réseau — c'est
  `KLT-04`.
- **N'opère pas** la plateforme Kiltikonet.fr (modération, support,
  administration) — c'est `KLT-05`.
- **Ne déploie pas** d'opérateurs sur le terrain — c'est `KLT-07`
  (référentiel `KLT-0006`, distinct).
- Livre une **analyse et une recommandation**, jamais une décision
  engageant une structure — la décision reste au rôle qui la porte
  (gouvernance, projet, territoire).

### 1.5 Contexte de la formation (PUBLIC/EXTERNAL/BRIDGE)

`KLT-0001` §3 avait laissé cette question `UNRESOLVED`. **`RESOLVED par
KLT-0008`** (décision déléguée par le Founder, 2026-09-04) :
`contexts = [EXTERNAL]` — voir `docs/KILTIKONET_KLT0008_KLT06_08_
CONTEXT_AND_SCOPE_DECISION.md` §2 pour l'audit et la rationale complète.
`INTERNAL` non retenu pour l'instant (lié aux compétences `BLOCKED`
C5/C6) ; `BRIDGE` non retenu (niveau `Avancé`, pas un point d'entrée).

---

## 2. CARTE DE COMPÉTENCES (`PROPOSED`, voir avertissement de source)

| # | Compétence | Constructible aujourd'hui ? |
|---|---|---|
| C1 | Comprendre l'objet et la méthode d'un observatoire de données culturelles (ce qu'il capte : événements, sessions, territoires, acteurs, signaux) | **Oui** — littératie/méthode, indépendante d'un accès live |
| C2 | Évaluer la provenance et la fiabilité d'un signal ou d'une donnée (traçabilité, biais de méthode) | **Oui** — méthode, illustrable sur des jeux de données proxy/pédagogiques |
| C3 | Formuler une spécification de besoin de données pour un tiers (chef de projet `KLT-02`, gouvernance `KLT-04`, déploiement `KLT-07`) | **Oui** — compétence de spécification, ne requiert pas de données réelles |
| C4 | Éthique et confidentialité des données communautaires/culturelles (consentement, représentation, anti-folklorisation appliquée à la donnée) | **Oui** — prolonge la discipline déjà posée en `KLT-01`/M07, appliquée aux données |
| C5 | Construire un tableau de bord ou un rapport à partir de données Observatory réelles | **Non** — `UNRESOLVED`, requiert un accès Observatory réel |
| C6 | Interpréter des signaux territoriaux réels pour appuyer une décision d'un autre rôle Kiltikonet | **Non** — `UNRESOLVED`, requiert un accès Observatory réel |
| C7 | Restituer une analyse de données à un public non spécialiste (communication de données) | **Oui** — méthode de restitution, illustrable sans données Observatory réelles |

**Synthèse** : 5 compétences sur 7 sont constructibles à un niveau
référentiel/méthode dès aujourd'hui (C1-C4, C7) ; 2 restent bloquées tant
qu'Observatory n'est pas accessible (C5, C6) — précisément celles qui
constituent le cœur analytique du métier. Un `KLT-06` complet sans C5/C6
resterait un métier "de préparation à Observatory", pas l'analyste
Observatory pleinement défini par le master plan.

---

## 3. STRUCTURE INDICATIVE DE MODULES (noms et compétences uniquement — contenu `À produire`, hors scope)

| Module (indicatif) | Compétence(s) | Niveau éval indicatif | Statut de construction |
|---|---|---|---|
| M01 | Qu'est-ce qu'un observatoire de données culturelles ? | C1 | N1 | `BUILDABLE` |
| M02 | Provenance, traçabilité et fiabilité d'un signal | C2 | N1/N2 | `BUILDABLE` |
| M03 | Spécifier un besoin de données pour un tiers | C3 | N2 | `BUILDABLE` |
| M04 | Éthique et confidentialité des données culturelles | C4 | N2 | `BUILDABLE` |
| M05 | Construire un tableau de bord à partir de données réelles | C5 | N2/N3 | `BLOCKED` — Observatory non connecté |
| M06 | Interpréter des signaux territoriaux pour appuyer une décision | C6 | N2/N3 | `BLOCKED` — Observatory non connecté |
| M07 | Restituer une analyse à un public non spécialiste | C7 | N2 | `BUILDABLE` |

Le chiffre indicatif du master plan ("8 modules") n'est **pas confirmé**
par ce référentiel — 7 compétences réelles sont identifiées, pas 8 ; le
chiffre du master plan reste `UNVERIFIED` faute de détail source
disponible dans ce repo (voir avertissement de source).

**Aucun contenu de module n'est écrit ici** — cette table gèle une
structure indicative de compétences et de statuts de constructibilité,
pas un contenu pédagogique.

---

## 4. TRAÇABILITÉ (niveau référentiel)

| Compétence | Module indicatif | Statut |
|---|---|---|
| C1 | M01 | `BUILDABLE` |
| C2 | M02 | `BUILDABLE` |
| C3 | M03 | `BUILDABLE` |
| C4 | M04 | `BUILDABLE` |
| C5 | M05 | `BLOCKED` |
| C6 | M06 | `BLOCKED` |
| C7 | M07 | `BUILDABLE` |

**Couverture** : 7/7 compétences ont un module indicatif nommé — zéro
compétence orpheline. 5/7 sont réellement constructibles aujourd'hui.

## 5. Dépendances Kiltikonet (`KLT-06` scope)

| Dépendance | Modules concernés | Classification |
|---|---|---|
| Observatory | M05, M06 (cœur du métier) | `NOT_CONNECTED` en Academy / `EXTERNAL_EVIDENCE_NOT_AUDITED` externe |
| FREK | Restitution/preuve d'apprentissage (M01-M04, M07) | `ACADEMY_LOCAL_IMPLEMENTATION` — réel, déjà utilisé ailleurs dans le corpus |

## 6. Ce qui devra être fait avant le build des modules

1. ~~Décision Founder sur `PUBLIC/EXTERNAL/BRIDGE`~~ — **`RESOLVED par
   KLT-0008`** : `contexts = [EXTERNAL]`.
2. ~~Décision Founder sur le périmètre~~ — **`RESOLVED par KLT-0008`** :
   M01-M04+M07 (5/7 compétences) autorisées comme premier périmètre ;
   M05/M06 explicitement différés (`BLOCKED`, Observatory non connecté).
3. Le build effectif du contenu de ces 5 modules reste un ticket
   distinct, à autoriser séparément (`KLT-0008` §5).
4. Si le master plan source (fichier Excel) contient un détail
   module-par-module pour `KLT-06` non résumé dans `KLT-0001`, le
   Founder est le seul à pouvoir le fournir — ce référentiel ne l'invente
   pas.

## REVIEW

- `NO_DB_MUTATION` / `NO_RUNTIME_BINDING` / `NO_SEED_MUTATION` — aucun
  code touché.
- `NO_FAKE_OBSERVATORY` — aucune lecture Observatory simulée ; M05/M06
  explicitement `BLOCKED`, pas construits, pas contournés par une
  fausse donnée.
- `NO_KLT06_MODULE_CONTENT_BUILD` — seuls des noms de modules indicatifs
  et une carte de compétences sont produits, aucun contenu pédagogique
  (pas de `## Situation professionnelle`, pas de cas, pas d'évaluation).

```bash
git status --short   # expect: only this new doc
```

## FREEZE

**`KLT-06_CANONICAL_REFERENTIAL = FROZEN` (compétences + structure
indicative uniquement)**. 7/7 compétences ont un module indicatif nommé.
**Les modules eux-mêmes restent `À produire`**, et 2 des 7 (`M05`, `M06`)
restent bloqués sur un accès Observatory réel — ce gel porte sur le
périmètre et la traçabilité, pas sur la rédaction pédagogique.

`STOP = TRUE.` Build de modules `KLT-06` non commencé, en attente
d'autorisation explicite et de décision sur §1.5/§6.
