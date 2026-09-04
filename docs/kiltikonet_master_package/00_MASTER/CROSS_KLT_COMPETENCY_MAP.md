# Cross-KLT Competency Map

```
Les 59 compétences réelles du corpus (extraites des 5 SKILL_ID_REGISTRY.md,
pas recréées), classées par famille pour éviter que KLT-01→05 ne
deviennent cinq silos.
```

## Méthode

Chaque ligne trace `KLT → COMPETENCY → SKILL → MODULE → ASSESSMENT →
EVIDENCE`. Le détail complet (assessment/evidence exacts) vit déjà dans
chaque `skills/SKILL_ID_REGISTRY.md` — cette carte ajoute la couche que
ces registres locaux n'ont pas : la comparaison **entre** formations.

## Familles de compétences transversales

### Famille 1 — Lecture de contexte / diagnostic initial (`SHARED_COMPETENCY`, forme partagée, portée différente)

| KLT | Skill ID | Compétence | Portée |
|---|---|---|---|
| `KLT-01` | `C1` | Lire et diagnostiquer un territoire/public | Terrain, un public |
| `KLT-02` | `C1` | Cadrer un projet culturel | Mandat projet |
| `KLT-03` | `C1` | Cartographier l'écosystème institutionnel | Institutions |
| `KLT-04` | `C1` | Fonder et faire vivre une association | Structure juridique |
| `KLT-05` | `C1` | Comprendre l'architecture Kiltikonet | Plateforme technique |

**Verdict** : `SHARED_COMPETENCY` au niveau de la *méthode* ("comprendre
avant d'agir"), `ROLE_SPECIFIC_COMPETENCY` au niveau de l'objet. Pas de
`DUPLICATION_RISK` — chaque module explicite déjà, dans son propre texte,
en quoi il diffère des `C1` voisins (ex. `KLT-02`/M01 distingue
explicitement cadrage projet et diagnostic `KLT-01`).

### Famille 2 — Cartographie d'acteurs/parties prenantes (`OVERLAP` réel, résolu dans le texte source)

| KLT | Skill ID | Compétence | Portée |
|---|---|---|---|
| `KLT-01` | `C3` | Identifier, qualifier, catégoriser, relier, prioriser les acteurs | Acteurs de **terrain** |
| `KLT-02` | `C2` | Étudier le besoin et cartographier les parties prenantes | Parties prenantes **projet** (pouvoir sur le projet) |
| `KLT-03` | `C1` | Cartographier l'écosystème institutionnel | Institutions (échelle locale→européenne) |

**Verdict** : `OVERLAP` réel de méthode (même geste : identifier/
qualifier/prioriser), **pas** de `DUPLICATION_RISK` — `KLT-02`/M02
distingue explicitement sa cartographie de celle de `KLT-01`/M03 ("un
ensemble souvent plus restreint mais à l'influence plus directe sur le
projet"). Les trois portées (terrain/projet/institutions) sont
réellement disjointes dans le cas fil rouge commun.

### Famille 3 — Documenter/prouver sans fabriquer (`SHARED_COMPETENCY` disciplinaire, `NO_FAKE_OBSERVATORY`)

| KLT | Skill ID | Compétence | Module bloqué sur Observatory ? |
|---|---|---|---|
| `KLT-01` | `C10` | Documenter et produire une preuve exploitable | Oui (`M10`) |
| `KLT-02` | `C9` | Évaluer l'impact d'un projet culturel | Oui (`M09`) |
| `KLT-03` | `C10` | Rendre compte et prouver l'impact partenarial | Oui (`M10`) |
| `KLT-05` | `C9` | Lire signaux d'engagement sans fabriquer | Oui (`M09`, legacy reste autoritaire) |

**Verdict** : `SHARED_COMPETENCY` — c'est la même discipline
(`NO_FAKE_OBSERVATORY`) appliquée quatre fois. `KLT-04` n'a pas
d'équivalent direct mais sa `C12` (Assurer conformité et responsabilité,
`M12`) porte la même exigence de preuve documentée. Aucune duplication —
chaque formation l'applique à son propre objet (dossier de preuve
d'action / rapport d'impact projet / rapport financeur / rapport
d'engagement plateforme).

### Famille 4 — Éthique et gestion de tension (`ROLE_SPECIFIC`, famille reconnaissable)

| KLT | Skill ID | Compétence |
|---|---|---|
| `KLT-01` | `C7` | Naviguer l'interculturel avec éthique, arbitrer sans folkloriser |
| `KLT-03` | `C9` | Pratiquer un lobbying culturel éthique |
| `KLT-04` | `C10` | Prévenir et traiter les conflits d'intérêt |
| `KLT-05` | `C6` | Modérer culturellement — sécurité et pluralité |

**Verdict** : `ROLE_SPECIFIC_COMPETENCY` — même famille de jugement
("tenir une tension sans la fuir ni trancher à la place d'un autre
rôle"), objets disjoints. `KLT-05`/M06 cite explicitement l'arbitrage
déjà posé par `KLT-01`/M07 et `KLT-03`/M07 sur la même tension du cas fil
rouge (spectacle vs rituel) sans le retrancher — c'est un exemple réel de
`CROSSOVER` cohérent, pas de duplication.

### Famille 5 — Communication/représentation externe (`ROLE_SPECIFIC`, frontières explicites)

| KLT | Skill ID | Compétence |
|---|---|---|
| `KLT-02` | `C7` | Communiquer sur un projet (récit et preuves) |
| `KLT-03` | `C7` | Diplomatie culturelle |
| `KLT-05` | `C5` | Animer une communauté diaspora |

**Verdict** : `ROLE_SPECIFIC_COMPETENCY`. `KLT-02`/M07 distingue
explicitement son objet (communication projet, orientée financeurs/
soutiens) du support de médiation `KLT-01`/M06 (orienté public direct).
Aucun `DUPLICATION_RISK`.

### Famille 6 — Financier (`ROLE_SPECIFIC`, échelle différente, `PREREQUISITE` réel)

| KLT | Skill ID | Compétence | Échelle |
|---|---|---|---|
| `KLT-02` | `C3` | Construire un budget culturel prévisionnel | Un projet |
| `KLT-02` | `C4` | Rechercher des financements réels | Un projet |
| `KLT-04` | `C3` | Tenir une comptabilité associative | Toute l'association |
| `KLT-04` | `C4` | Maîtriser la fiscalité culturelle | Toute l'association |

**Verdict** : pas de duplication — `KLT-02`/M03 traite explicitement le
budget d'**un** projet en le faisant apparaître dans la comptabilité
associative globale que `KLT-04`/M03 gère par ailleurs (`KLT-04`/M03
cite littéralement ce lien : "la subvention doit apparaître en produit
associatif"). `PREREQUISITE` naturel : un budget projet (`KLT-02`)
suppose une structure associative déjà existante et régulière (`KLT-04`
M01-M02).

### Famille 7 — Gouvernance / mandat institutionnel (`CROSSOVER` explicite, frontière à surveiller)

| KLT | Skill ID | Compétence |
|---|---|---|
| `KLT-03` | `C6` | Négocier une convention |
| `KLT-04` | `C8` | Organiser comités et décisions |
| `KLT-04` | `C9` | Déléguer et mandater dans un réseau |

**Verdict** : `CROSSOVER` réel — `KLT-03`/M06 prépare une convention
mais **ne la signe jamais** ("le candidat prépare et propose, la
signature finale reste du ressort du CA"), renvoyant explicitement
l'autorité à la gouvernance que `KLT-04` couvre. Frontière saine, déjà
posée dans les deux textes sources, mais à re-vérifier si `KLT-03` et
`KLT-04` sont un jour suivies par la même personne dans un vrai parcours
(risque de lecture redondante, pas de contenu redondant).

## `SKILL` orphelins

**Aucun.** Les 59 skill IDs (`skills/SKILL_ID_REGISTRY.md` × 5) pointent
chacun vers un module réel, un assessment réel, une evidence réelle —
vérifié `QUALITY_GATES.md` de chaque formation (`ORPHAN_SKILL = 0`).

## `PREREQUISITE` réels (déclarés dans les référentiels, pas déduits)

- `KLT-02` : "`KLT-01` recommandé" (`seed_data.py:627`).
- `KLT-03` : "`KLT-01` + `KLT-02`" (`seed_data.py:641`).
- `KLT-05` : "`KLT-01` + `FRK-01` recommandé" (`seed_data.py:669`) — `FRK-01`
  est hors périmètre KLT, non traité ici.
- `KLT-04` : aucun prérequis déclaré (`seed_data.py:655` = "Aucun").
- Cross-pôle (hors KLT) : `GRP-02` liste `"KLT-03 recommandé"` — impact
  réel hors du corpus KLT si `KLT-03` évolue un jour (`KLT-0002` §KLT-03).

## `DUPLICATION_RISK` — verdict global

**Aucun `DUPLICATION_RISK` réel identifié** dans le corpus actuel. Chaque
zone de recouvrement (familles 1, 2, 6, 7 ci-dessus) est déjà résolue
*dans le texte source lui-même* — chaque module qui touche un territoire
voisin cite explicitement la formation voisine et pose sa propre
frontière, plutôt que de la laisser implicite. Ce document consolide ces
frontières déjà posées, il n'en invente aucune de nouvelle.
