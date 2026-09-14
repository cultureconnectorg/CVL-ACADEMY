# KOR-0002 — Legacy → Canonical Reconciliation (KOR-01, KOR-02) + Boundary Map (15 formations) + Cas fil rouge KORA

```
WORKSTREAM = KOR (KORA), séparé de FMS (FMS_CLOSED = TRUE) et de KLT
(NO_CROSS-CONTAMINATION = TRUE — aucun fichier FMS ni KLT touché ici)
AUTHORIZED = TRUE (Checklist opérationnelle KOR-0002, Founder, 2026-09-04)
SCOPE = KOR-0002 STRICT — réconciliation legacy/canonique KOR-01 et
        KOR-02, Boundary Map des 15 formations (analytique seulement),
        cas fil rouge KORA (écrit en entier), propositions de structure
        haut niveau KOR01/KOR02 (blocs, pas de curriculum détaillé).
KORA_CASE_UNIVERSE = SEPARATE_FROM_KILTIKONET (décision Founder,
2026-09-04 — tranche l'option 1 du §7 de KOR-0001)
KOR03_15_STATUS = NEW_CANONICAL_TARGET, CURRICULUM_BUILT = FALSE (INCHANGÉ
par ce ticket — usage strictement analytique en §4)
DB_MUTATION = FALSE (livrable entièrement documentaire)
NO_KOR03_15_BUILD = TRUE
STOP_AFTER_DELIVERY = TRUE
```

**Méthode** : `AUDIT → RECONCILE → BOUNDARY_MAP → CANONICAL_PROPOSAL →
COMMIT → PUSH → REPORT → STOP` (séquence imposée, §8 du ticket). Ce
document suit cette séquence dans l'ordre.

**Vocabulaire d'incertitude imposé pour ce ticket** (remplace toute
formulation antérieure moins précise) :
- `UNRESOLVED` — question ouverte, non tranchée, à trancher par le
  Founder ou un ticket ultérieur.
- `ACADEMY_LOCAL_EVIDENCE = NOT_FOUND` — recherché dans ce repo,
  absent. Ne dit rien sur l'existence réelle du système hors de ce repo.
- `EXTERNAL_PRODUCT_EVIDENCE_NOT_AUDITED` — système externe (CVLN) dont
  l'état réel n'a pas été vérifié par ce ticket (pas d'accès, pas de
  mandat). **Jamais** utilisé pour conclure qu'un système/acronyme
  "n'existe pas" — seulement que ce repo ne permet pas de le confirmer.
- Statut par élément : exactement un parmi `{KEEP, MERGE, EXTEND,
  SUPERSEDE, DEPRECATE, MIGRATE, UNRESOLVED}`. `UNRESOLVED` est utilisé
  chaque fois qu'aucun objet legacy n'existe pour asseoir un diff (ex.
  couche assessments/skills, totalement absente de KOR-01/02 legacy) —
  ce n'est pas une esquive, c'est le statut honnête quand les 6 autres
  supposent tous un objet de départ qui n'existe pas.
- Provenance des compétences : exactement un parmi `{MARKET_SKILL,
  KORA_CURRENT_CAPABILITY, KORA_TARGET_CAPABILITY, PRODUCT_DEPENDENCY}`.

---

## 0. Cadre général et autorisation

Confirmé conforme au ticket reçu :

| Point du cadre | Statut |
|---|---|
| `AUTHORIZED = TRUE`, périmètre strictement KOR-0002 | Respecté — aucun contenu KOR-03→15 écrit, voir §4 et §9 |
| `KORA_CASE_UNIVERSE = SEPARATE_FROM_KILTIKONET` | Enregistré ici comme décision Founder tranchant l'option 1 du §7 de `KOR-0001` ; cas écrit en entier en §6 |
| KOR-03→15 restent `NEW_CANONICAL_TARGET` / `CURRICULUM_BUILT = FALSE` | Confirmé — usage strictement analytique dans la Boundary Map (§4), aucune ligne de contenu pédagogique |
| Construction détaillée KOR-03→15 | Explicitement différée à un ticket ultérieur, hors périmètre de KOR-0002 |

---

## 1. Audit préparation

### 1.1 Ce qui était déjà établi par `KOR-0001` (repris, pas refait)

`KOR-0001` §1/§2/§4/§8 a déjà : figé `KOR_MASTER_MAP_v1` (15 formations),
identifié la collision legacy `KOR-01`/`KOR-02`, vérifié les dépendances
KORA contre ce repo, et nommé 9 tensions de frontière. Ce ticket ne
refait pas cet audit — il l'**étend** sur les points explicitement
requis par le Founder et non encore vérifiés : `LabelOS` et `CVLN Brain`
comme entités à part entière (pas seulement comme noms cités dans des
champs `meta_entities`/`bridge_entities`).

### 1.2 Audit étendu — `LabelOS` et `CVLN Brain` (nouveau dans ce ticket)

`KOR-0001` §4 avait vérifié `LabelOS`/`CVLN Brain` uniquement comme
*noms référencés* (dans `bridge_entities` de `FMS-02` et dans le shim
`services/integrations/registry.py`). Un audit direct sur `seed_data.py`
révèle que ce sont en réalité **deux pôles Academy réels et complets**,
distincts de `KOR` et de `BRN`/`LOS` en tant que pôles de code :

| Entité | Pôle réel | Formations réelles (seedées) | Evidence |
|---|---|---|---|
| **LabelOS** | `LOS` | `LOS-01` Label Operations Manager (42h) · `LOS-02` **Metadata & Catalog Management** (26h, badge `Metadata Specialist`, ISRC/ISWC/DDEX) · `LOS-03` AI-Assisted Label Workflow (26h) | `seed_data.py:791-833` |
| **CVLN Brain** | `BRN` | `BRN-01` Strategic Ecosystem Design (32h) · `BRN-02` AI Creative Operations (32h, module `BRN-02-M06` "CVLN Brain en pratique — 4 endpoints") | `seed_data.py:834-931`, module détail `seed_modules.py:1294+` |
| **CVLN Brain** (couche intégration, en plus du pôle formation) | — | Interface d'écosystème réelle mais non configurée (`registry.py:20`, `brain = EcosystemIntegration("CVLN Brain","CVLN_BRAIN")`), **déjà câblée à un événement réel** : `academy.certification.passed` → best-effort vers `brain`/`command_center` | `services/integrations/subscribers.py:14-29`, `services/events.py` |
| **FREK** (nécessaire pour §4, tension `KOR-11`) | `FRK` | `FRK-01` FREK Operator (31h, module `FRK-01-M07` "Détecter et signaler des violations") · `FRK-02` Digital Provenance Specialist (28h) · `FRK-03` Archivage culturel sécurisé (22h) — en plus du service réel `services/frek_core.py` déjà utilisé par tous les workstreams (`frek_signal` legacy `KOR-01`/`02` inclus) | `seed_data.py:675-790` |

**Conséquence directe pour la Boundary Map (§4)** : `LabelOS` et `CVLN
Brain` ne sont pas des inconnues externes à traiter par prudence — ce
sont des pôles Academy voisins, avec un vrai contenu, un vrai
recouvrement thématique potentiel (`LOS-02` "Metadata & Catalog
Management" vs `KOR-08` "Metadata & Cultural Catalog Operations" est la
collision la plus directe de toute la carte — voir tension #10). Ceci
**corrige/étend** `KOR-0001` §4, qui avait classé "Metadata/taxonomies/
catalog (`KOR-08`)" comme "zéro footprint" — c'était vrai pour un pôle
`KOR-08` qui n'existe pas encore, mais faux pour le domaine métadonnées
en général : `LOS-02` en a un, réel et détaillé.

### 1.3 Reconfirmation — ce qui reste `ACADEMY_LOCAL_EVIDENCE = NOT_FOUND`

| Domaine | Statut (reconfirmé par grep direct dans `backend/`) |
|---|---|
| `CVE` (acronyme cité par le Founder pour `KOR-10`) | `ACADEMY_LOCAL_EVIDENCE = NOT_FOUND` — zéro occurrence du terme dans `backend/*.py`. **Non traduit ici en `CVE_DOES_NOT_EXIST`** — le terme peut désigner un système CVLN réel non présent dans ce repo (`EXTERNAL_PRODUCT_EVIDENCE_NOT_AUDITED`) ; à faire préciser par le Founder avant tout référentiel `KOR-10` qui en dépendrait. |
| DSP/CDN/player/SLA/SLO (`KOR-06`, `KOR-14`) | `ACADEMY_LOCAL_EVIDENCE = NOT_FOUND` — reconfirmé, aucune collection `db.*`, aucun service |
| Media rights/licensing/royalties contractuelles (`KOR-07`) | `ACADEMY_LOCAL_EVIDENCE = NOT_FOUND` — reconfirmé |
| Trust & safety / modération de contenu dédiée (`KOR-11`) | `ACADEMY_LOCAL_EVIDENCE = NOT_FOUND` en tant que **système de modération** ; en revanche `ACADEMY_LOCAL_EVIDENCE = FOUND` pour l'infrastructure de preuve/signalement voisine (`FRK`, voir §1.2 et tension #13) — les deux ne doivent pas être confondus |
| Streaming data / plays / completions (`KOR-12`) | `ACADEMY_LOCAL_EVIDENCE = NOT_FOUND` pour une donnée d'usage média ; `db.progress` existe mais mesure la progression pédagogique Academy — domaine différent, non réutilisable tel quel |
| Wallet / JCC (`KOR-10`) | `ACADEMY_LOCAL_EVIDENCE = FOUND`, réel et local — `wallet/models.py:44-46` (`jcc_balance`), `wallet/service.py:49`, `wallet/passes.py:35,62` |

---

## 2. KOR-01 — Réconciliation legacy → canonique

### 2.1 Legacy (en direct dans ce repo)

`code=KOR-01`, `pole=KOR`, `name="Podcast Production"`, `duration_h=31`,
`cc=31`, `stades=[graine,branches]`, `badge_name="Podcast Producer
CVLN"`, `prerequisites="Aucun"`, `debouches="Producer KORA, animateur
podcast diaspora"`, `objective_strategic="Peupler KORA de voix
caribéennes structurées."` (`seed_data.py:547-559`). 8 modules
`KOR-01-M01`→`M08` (`seed_modules.py:226-299`). `contexts=[EXTERNAL,
BRIDGE]`, `audience=[DEBUTANT,INTERMEDIAIRE]`, `level="opérationnel"`,
`meta_entities=[KORA]` (`catalog_cartography.py:137-147`).
`market_job_title="Producteur podcast / producteur audiovisuel"`,
`refs=[rome_l1302,rome_e1106]`, `confidence="low"`
(`external_calibration.py:283-301`).

### 2.2 Canonique cible (rappel, `KOR-0001` §1/§2)

*Podcast & Audio Production* — concept éditorial · formats audio ·
écriture · **interview** · prise de son · studio/mobile · montage ·
sound design · **mix/master** · identité sonore · RSS/distribution ·
publication · audience · sponsors/monétisation (14 items, verbatim
Founder).

### 2.3 Diff — ce que le legacy couvre déjà, ce qu'il ne couvre pas

| Item canonique | Couvert par un module legacy ? | Module | Diff |
|---|---|---|---|
| Concept éditorial | Oui | M01, M02 | — |
| Formats audio | Oui | M02 | — |
| Écriture | Oui | M03 | — |
| **Interview** | **Non** | — | **Manquant** — aucun module dédié dans les 8 existants |
| Prise de son | Oui | M04 | — |
| Studio/mobile | Oui | M04 | — |
| Montage | Oui | M05 | — |
| Sound design | Oui | M05 | — |
| **Mix/master** | Partiel | M05 | Implicite dans "montage et sound design", jamais une étape professionnelle explicite |
| Identité sonore | Oui | M06 ("habillage sonore et générique KORA") | — |
| RSS/distribution | Oui | M07 | — |
| Publication | Oui | M07 | — |
| Audience | Partiel | M08 | Fusionné avec monétisation, pas traité seul |
| Sponsors/monétisation | Oui | M08 | — |

**Conclusion diff** : 6/8 modules legacy couvrent le canonique sans
écart notable ; 2 lacunes réelles identifiées : **interview** (absente),
**mix/master** (implicite, pas explicite). Aucune autre lacune trouvée
— la portée canonique est proche de la portée legacy (contrairement à
la lecture initiale de `KOR-0001` §1 qui présentait un écart plus large ;
un diff module-par-module montre un recouvrement plus élevé qu'anticipé).

### 2.4 Audit par élément (14 éléments, statut unique + justification)

| Élément | Statut | Justification | Evidence | Impact structurel | Dépendances | Risque duplication (vs KOR-03→15) | Suivi |
|---|---|---|---|---|---|---|---|
| Titre | `EXTEND` | "Podcast Production" → "Podcast & Audio Production" reflète l'élargissement mix/master + identité sonore déjà quasi couvert | `seed_data.py:548` vs `KOR-0001` §2 | Renommage cosmétique, pas de mutation DB dans ce ticket | Aucune | Faible | Renommage à faire au référentiel `KOR-0003`-équivalent |
| Finalité | `EXTEND` | Trajectoire "concept → monétisation" déjà juste, élargie à l'identité sonore professionnelle | `seed_data.py:556` | Faible | Aucune | Faible | — |
| Métier cible | `KEEP` | "Producer KORA, animateur podcast diaspora" reste exact ; `market_job_title` marché cohérent | `seed_data.py:555`, `external_calibration.py:284` | Aucun | Aucune | Faible | Ajouter "réalisateur audio" en synonyme marché possible, non tranché |
| Compétences | `EXTEND` | Voir §2.5 (provenance par compétence) | §2.5 | Moyen | Aucune bloquante | Moyen (`KOR-01`/`KOR-03`, tension #1) | — |
| Modules | `EXTEND` | Voir §2.6 (fate par module) | §2.6 | Moyen | Aucune | Faible | — |
| Prérequis | `KEEP` | "Aucun" cohérent avec `stades=[graine,branches]` (formation d'entrée) | `seed_data.py:554` | Aucun | Aucune | Aucun | — |
| Durée | `UNRESOLVED` | 31h legacy ; extension (interview + mix/master) demanderait plus d'heures, mais **aucun chiffrage final n'est imposé par ce ticket** (règle explicite du Founder : pas de compte de module fixé à l'avance) | `seed_data.py:550` | À trancher au référentiel | Aucune | Aucun | Chiffrage à faire au ticket de référentiel |
| Livrables | `EXTEND` | Livrables legacy réels et solides par module (script, prise de son montée, épisode monté, jingle, publication 3 plateformes, plan de croissance) ; à compléter d'un livrable interview et d'un livrable mix/master dédié | `seed_modules.py:228-298` | Faible | Aucune | Faible | — |
| Assessments | `UNRESOLVED` | Aucun objet legacy — `KOR-0001` §5 confirme l'absence de tout schéma de certification/skill ID pour `KOR-01`. Statut honnête : rien à `KEEP`/`MERGE`/`EXTEND`, construction neuve requise, hors du périmètre de ce ticket de réconciliation | `KOR-0001` §5 | Élevé (couche complète à construire) | Méthode `KLT-0003`→`0004` réutilisable | Aucun | Ticket de référentiel dédié |
| Badge | `KEEP` | "Podcast Producer CVLN" cohérent avec le périmètre canonique, aucune raison de renommer | `seed_data.py:553` | Aucun — `NO_BADGE_REASSIGNMENT` respecté | Aucune | Aucun | — |
| Contexts | `KEEP` | `[EXTERNAL, BRIDGE]` réel, cohérent avec un métier accessible sans CVLN puis passerelle KORA | `catalog_cartography.py:140` | Aucun — `NO_CONTEXT_OVERRIDE` respecté | Aucune | Aucun | — |
| Dépendances KORA | `KEEP` | `meta_entities=[KORA]` est un cadrage narratif (le générique/jingle est "KORA", le débouché est "producer KORA") — **aucune brique KORA vivante n'est requise pour rendre ce contenu buildable**, à la différence des compétences bloquées `Observatory`/`Network` de KLT-06/07 | `catalog_cartography.py:143-144`, croisé avec §1.2/§1.3 | Aucun — pas de `BLOCKED` à prévoir pour `KOR-01` | Aucune | Aucun | — |
| Éléments transférables | `UNRESOLVED` | Techniques prise de son/montage transférables vers `KOR-03` (vidéo/streaming) à un niveau conceptuel, médium différent — tension #1 déjà nommée par `KOR-0001` §8, non résolue ici (hors périmètre `NO_KOR03_15_BUILD`) | `KOR-0001` §8 | — | `KOR-03` (non construit) | Moyen | Confirmé en §4 |
| Éléments trop spécifiques | `KEEP` (aucun retrait) | Aucun élément legacy identifié comme à retirer — "générique KORA" reste pertinent en cadrage narratif, pas une dépendance technique | §1.2/§1.3 | Aucun | Aucune | Aucun | — |
| Éléments manquants | `EXTEND` | Interview (absent), mix/master (implicite → à expliciter) — voir §2.3 | §2.3 | Moyen | Aucune | Faible | Modules candidats, non décidés ici (voir §5) |

### 2.5 Compétences — provenance (`MARKET_SKILL` / `KORA_CURRENT_CAPABILITY` / `KORA_TARGET_CAPABILITY` / `PRODUCT_DEPENDENCY`)

| Compétence (module source) | Provenance | Justification |
|---|---|---|
| Analyser un podcast référence (M01) | `MARKET_SKILL` | Compétence d'analyse éditoriale transférable, aucune brique KORA requise |
| Concevoir sujet/format/cadence (M02) | `MARKET_SKILL` | Idem |
| Écrire un script d'épisode (M03) | `MARKET_SKILL` | Idem |
| Prise de son home/studio (M04) | `MARKET_SKILL` | Technique audio générique |
| Montage et sound design (M05) | `MARKET_SKILL` | Idem |
| Habillage sonore et générique **KORA** (M06) | `KORA_CURRENT_CAPABILITY` (cadrage) sur un socle `MARKET_SKILL` | Le geste technique (créer un jingle) est un `MARKET_SKILL` ; le nom "KORA" est un habillage narratif du livrable, pas une dépendance technique — aucune API KORA appelée |
| Distribution — hébergeurs/RSS/DSP (M07) | `MARKET_SKILL` | Outils du marché (Spotify, Apple Podcasts, RSS) ; **pas** `PRODUCT_DEPENDENCY` — aucune publication sur une plateforme KORA réelle n'est requise ni possible (`ACADEMY_LOCAL_EVIDENCE = NOT_FOUND` pour un DSP KORA, §1.3) |
| Croissance et monétisation (M08) | `MARKET_SKILL` | Sponsoring/Patreon — pratiques marché génériques |
| Interview (manquant) | `MARKET_SKILL` (cible) | À construire — aucune dépendance produit identifiée |
| Mix/master professionnel (à expliciter) | `MARKET_SKILL` (cible) | Extension technique, aucune dépendance produit |

**Constat notable** : contrairement à `KLT-06`/`07`/`08`, **aucune
compétence de `KOR-01` n'est `PRODUCT_DEPENDENCY` bloquante.** "KORA"
n'apparaît que comme cadrage narratif des livrables (nom du générique,
nom de la plateforme de débouché visée), jamais comme brique technique
requise pour valider une compétence. `KOR-01` est donc, à ce stade de
l'audit, **buildable en intégralité** sans aucun `BLOCKED` — ce constat
n'implique cependant aucune décision de construction : celle-ci reste
hors périmètre de ce ticket de réconciliation.

### 2.6 Fate des 8 modules legacy (argumenté individuellement)

| Module | Statut | Argument |
|---|---|---|
| M01 Anatomie d'un podcast qui accroche | `KEEP` | Fondation d'analyse toujours pertinente, aucun écart canonique |
| M02 Choisir sujet, format, cadence | `KEEP` | Idem |
| M03 Écriture d'un script d'épisode | `EXTEND` | Ajouter un volet interview (préparation de questions, conduite) — lacune identifiée §2.3 |
| M04 Prise de son — home vs studio | `KEEP` | Couvre bien "prise de son" + "studio/mobile" canoniques |
| M05 Montage et sound design | `EXTEND` | Expliciter une étape mix/master distincte du montage brut |
| M06 Habillage sonore et générique KORA | `KEEP` | Couvre "identité sonore" canonique sans écart |
| M07 Distribution — hébergeurs, RSS, DSP | `KEEP` | Couvre "RSS/distribution" + "publication" |
| M08 Croissance et monétisation | `EXTEND` | Séparer "audience" de "sponsors/monétisation" comme le fait la table canonique, sans retirer le contenu existant |

Aucun module `MERGE`/`SUPERSEDE`/`DEPRECATE`/`MIGRATE` — le corpus
legacy `KOR-01` est structurellement sain, aucun module ne fait double
emploi ni ne devient obsolète à la lecture du plan canonique.

### 2.7 Recommandation canonique KOR-01 (synthèse)

- **Legacy state** : 31h, 8 modules, badge `Podcast Producer CVLN`,
  `contexts=[EXTERNAL,BRIDGE]`, aucune couche certification/skill ID.
- **Canonical target** : *Podcast & Audio Production*, 14 items
  (§2.2), quasi entièrement couvert par le legacy (§2.3).
- **Diff** : 2 lacunes (interview, mix/master explicite) sur 14 items.
- **Evidence** : `seed_data.py:547-559`, `seed_modules.py:226-299`,
  `catalog_cartography.py:137-147`, `external_calibration.py:283-301`.
- **Keep** : titre de métier cible, prérequis, badge, contexts, 6/8
  modules tels quels.
- **Merge** : aucun.
- **Extend** : titre, finalité, compétences (interview, mix/master),
  2/8 modules (M03, M05), 1/8 (M08, séparation audience/monétisation).
- **Supersede** : aucun.
- **Deprecate** : aucun.
- **Migrate** : aucun.
- **Unresolved** : durée finale, couche assessments/skills complète,
  éléments transférables vers `KOR-03` (tension #1, §4).
- **Recommandation canonique** : `KOR-01` legacy est une base saine et
  réutilisable — aucune reconstruction depuis zéro n'est justifiée. Un
  futur référentiel canonique devrait **étendre** (pas remplacer) les 8
  modules existants, combler les 2 lacunes identifiées, et construire la
  couche assessments/skills manquante — même méthode que `KLT-0003`.

---

## 3. KOR-02 — Réconciliation legacy → canonique

### 3.1 Legacy

`code=KOR-02`, `pole=KOR`, `name="Media Storytelling & Cultural
Broadcasting"`, `duration_h=28`, `cc=28`, `stades=[pousse,arbre]`,
`badge_name="Cultural Broadcaster"`, `prerequisites="Aucun"`,
`debouches="Journaliste culturel, storyteller KORA"`,
`objective_strategic="Créer un journalisme culturel caribéen
indépendant."` (`seed_data.py:561-573`). 7 modules
`KOR-02-M01`→`M07` (`seed_modules.py:300-364`). `contexts=[EXTERNAL,
BRIDGE]`, `audience=[INTERMEDIAIRE,PROFESSIONNEL]`,
`level="professionnalisation"`, `meta_entities=[KORA,Kiltikonet]`
(`catalog_cartography.py:148-159`) — **seule formation `KOR` avec un
`meta_entities` incluant `Kiltikonet`**, evidence réelle et
pré-existante d'un pont entre les deux workstreams (non construit ni
modifié ici, `NO_CROSS-CONTAMINATION` respecté : constat, pas action).
`market_job_title="Journaliste / storyteller culturel"`,
`refs=[rome_e1106,rome_k1808]`, `confidence="medium"`
(`external_calibration.py:302-320`).

### 3.2 Canonique cible (rappel)

*Cultural Storytelling & Broadcasting* — journalisme culturel ·
recherche · sources · fact-checking · angle · **interview** ·
portrait/reportage · narration culturelle · texte/audio/vidéo · éthique
· **représentation** · adaptation réseaux · diffusion ·
portfolio/signature (14 items, verbatim Founder).

### 3.3 Diff par sous-domaine (mandat explicite du Founder pour KOR-02)

| Sous-domaine | Couvert par legacy ? | Module | Diff |
|---|---|---|---|
| Journalisme culturel (état des lieux) | Oui | M01 | — |
| Recherche | Partiel | M01, M02 | Implicite dans "note d'analyse", pas de méthode de recherche dédiée |
| Sources | Oui | M02 | — |
| Fact-checking | Oui | M02 ("fake news culturelle démontée") | — |
| Angle | Partiel | M01, M03 | Traité en pratique, jamais nommé comme compétence isolée |
| **Interview** | **Non** | — | **Manquant** — même lacune que `KOR-01` (§2.3), constat croisé |
| Storytelling | Oui | M03 | — |
| Diffusion | Oui | M06 | — |
| Multiformat | Oui | M04 | — |
| Broadcasting | Partiel | M06 | "Distribution KORA et co-productions" couvre le broadcasting business, pas la pratique technique de diffusion (studio, direct) |

### 3.4 Audit par élément (14 éléments)

| Élément | Statut | Justification | Evidence |
|---|---|---|---|
| Titre | `KEEP` | "Media Storytelling & Cultural Broadcasting" (legacy) est déjà quasi identique à "Cultural Storytelling & Broadcasting" (canonique) — écart cosmétique seulement | `seed_data.py:562` vs `KOR-0001` §2 |
| Finalité | `KEEP` | "Raconter la culture caribéenne avec justesse et impact" reste exact et suffisant | `seed_data.py:570` |
| Métier cible | `KEEP` | "Journaliste culturel, storyteller KORA" cohérent avec `market_job_title` marché | `seed_data.py:569`, `external_calibration.py:303` |
| Compétences | `EXTEND` | Voir §3.5 | §3.5 |
| Modules | `EXTEND` | Voir §3.6 | §3.6 |
| Prérequis | `KEEP` | "Aucun" cohérent, bien que `audience=[INTERMEDIAIRE,PROFESSIONNEL]` suggère un public déjà avancé — **écart noté, non résolu** : le champ `prerequisites` texte et le champ `audience` structuré ne sont pas alignés dans le legacy lui-même | `seed_data.py:568` vs `catalog_cartography.py:156` |
| Durée | `UNRESOLVED` | 28h ; pas de chiffrage final imposé par ce ticket | `seed_data.py:564` |
| Livrables | `EXTEND` | Livrables legacy réels (note d'analyse, fiche source, feature 2500 mots, sujet 4 formats, charte éthique, pitch co-production, portfolio) ; ajouter un livrable interview dédié | `seed_modules.py:302-362` |
| Assessments | `UNRESOLVED` | Même constat que `KOR-01` §2.4 — aucun objet legacy, construction neuve hors périmètre | `KOR-0001` §5 |
| Badge | `KEEP` | "Cultural Broadcaster" cohérent, aucune raison de renommer | `seed_data.py:567` |
| Contexts | `KEEP` | `[EXTERNAL,BRIDGE]` réel et cohérent | `catalog_cartography.py:155` |
| Dépendances KORA | `KEEP` | `meta_entities=[KORA,Kiltikonet]` — cadrage narratif + pont pré-existant réel avec Kiltikonet (constaté, non modifié) ; aucune brique KORA vivante requise | `catalog_cartography.py:158` |
| Éléments transférables | `UNRESOLVED` | Tension #8 déjà nommée (`KOR-04`/`KOR-02`, programmation vs storytelling), non résolue ici | `KOR-0001` §8 |
| Éléments trop spécifiques | `KEEP` (aucun retrait) | Aucun élément à retirer identifié | §3.3 |
| Éléments manquants | `EXTEND` | Interview (absent), angle et recherche (implicites → à expliciter), représentation (absent en tant que thème isolé de l'éthique générale) | §3.3 |

### 3.5 Compétences — provenance

| Compétence (module) | Provenance | Justification |
|---|---|---|
| Analyser le journalisme culturel actuel (M01) | `MARKET_SKILL` | — |
| Angle, source, vérification (M02) | `MARKET_SKILL` | — |
| Écriture longue — feature/portrait/reportage (M03) | `MARKET_SKILL` | — |
| Multiformats (M04) | `MARKET_SKILL` | — |
| Éthique et déontologie (M05) | `MARKET_SKILL` | — |
| Distribution **KORA** et co-productions (M06) | `KORA_CURRENT_CAPABILITY` (cadrage) sur socle `MARKET_SKILL` | Compétence business de co-production réelle et transférable ; "KORA" nomme le débouché, aucune API/plateforme requise pour valider la compétence |
| Portfolio et signature (M07) | `MARKET_SKILL` | — |
| Interview (manquant) | `MARKET_SKILL` (cible) | À construire |
| Représentation (manquant) | `MARKET_SKILL` (cible) | À construire, distincte de l'éthique générale déjà couverte |

**Même constat que `KOR-01`** : aucune compétence `KOR-02`
n'est `PRODUCT_DEPENDENCY` bloquante — `KOR-02` est, à ce stade
d'audit, buildable en intégralité sans `BLOCKED`.

### 3.6 Fate des 7 modules legacy

| Module | Statut | Argument |
|---|---|---|
| M01 Journalisme culturel caribéen aujourd'hui | `KEEP` | Fondation toujours pertinente |
| M02 Angle, source, vérification | `KEEP` | Couvre déjà sources + fact-checking canoniques |
| M03 Écriture longue | `EXTEND` | Ajouter un volet interview explicite (même lacune que `KOR-01`) |
| M04 Multiformats | `KEEP` | Couvre "texte/audio/vidéo/réseaux" canonique |
| M05 Éthique et déontologie culturelle | `EXTEND` | Ajouter un volet représentation explicite, distinct de l'éthique générale |
| M06 Distribution KORA et co-productions | `KEEP` | Couvre "diffusion" canonique, business réel |
| M07 Portfolio et signature | `KEEP` | Couvre "portfolio/signature" canonique |

Aucun module `MERGE`/`SUPERSEDE`/`DEPRECATE`/`MIGRATE`.

### 3.7 Recommandation canonique KOR-02 (synthèse)

- **Legacy state** : 28h, 7 modules, badge `Cultural Broadcaster`,
  `contexts=[EXTERNAL,BRIDGE]`, aucune couche certification/skill ID,
  seul `KOR` avec un pont `meta_entities` réel vers Kiltikonet.
- **Canonical target** : *Cultural Storytelling & Broadcasting*, 14
  items (§3.2), très proche du legacy (le plus proche des deux formations
  legacy, confirmé — cf. `KOR-0001` §1).
- **Diff** : 2 lacunes nettes (interview, représentation), 2 lacunes
  partielles (recherche, angle — implicites, jamais nommées).
- **Evidence** : `seed_data.py:561-573`, `seed_modules.py:300-364`,
  `catalog_cartography.py:148-159`, `external_calibration.py:302-320`.
- **Keep** : titre, finalité, métier cible, prérequis, badge, contexts,
  5/7 modules tels quels.
- **Merge** : aucun.
- **Extend** : compétences (interview, représentation), 2/7 modules
  (M03, M05).
- **Supersede / Deprecate / Migrate** : aucun.
- **Unresolved** : durée finale, couche assessments/skills, écart
  `prerequisites`/`audience` non aligné (legacy lui-même), éléments
  transférables vers `KOR-04` (tension #8, §4).
- **Recommandation canonique** : même conclusion que `KOR-01` —
  extension du corpus existant, pas de reconstruction. `KOR-02` est la
  formation legacy la plus proche de sa cible canonique des deux.

---

## 4. Boundary Map — 15 formations (analytique seulement, `NO_KOR03_15_BUILD`)

Reprise intégrale des 9 tensions déjà nommées par `KOR-0001` §8, mises
au format strict imposé par ce ticket, **plus 4 tensions nouvelles**
(entités CVLN nommées par le Founder), auditées pour la première fois
dans ce ticket (§1.2). Aucune de ces tensions n'est tranchée ici —
nommée, structurée, laissée ouverte pour le référentiel qui construira
la formation concernée.

**Règle d'application KORA** (imposée pour chaque tension impliquant
une entité CVLN hors `KOR`) : l'entité propriétaire porte la profondeur
métier réelle ; `KOR` ne porte que l'application streaming-spécifique de
ce domaine ; le point de passage (handoff) est documenté explicitement ;
aucune capacité non prouvée n'est revendiquée côté KORA.

### 4.1 Tensions internes aux 15 formations KORA (reprises de `KOR-0001` §8)

| # | FORMATION_A | FORMATION_B | SHARED_DOMAIN | OWNERSHIP_A | OWNERSHIP_B | HANDOFF | Overlap | Dup. risk | Frontier status | Open question |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | KOR-01 | KOR-03 | Prise de son, montage, publication | Production audio (podcast) | Production vidéo/streaming | Techniques de captation/montage proches, médium différent | Medium | Medium | UNRESOLVED | Un module "audio pour vidéaste" partagé, ou duplication assumée ? |
| 2 | KOR-06 | KOR-14 | Player, disponibilité, qualité de service | Infra/opérations plateforme | Parcours utilisateur/expérience | Vue infra vs vue UX du même système | Medium | Medium | UNRESOLVED | Où finit l'ops, où commence le produit ? |
| 3 | KOR-07 | KOR-13 | Contrats, négociation, territoires | Cadre juridique droits/licensing | Relation business/sourcing créateurs | Le contrat encadre, le partenariat négocie | Medium | Low | UNRESOLVED | Qui forme à la négociation elle-même ? |
| 4 | KOR-08 | KOR-12 | Données sur les œuvres/usages | Catalogue descriptif (métadonnées) | Mesure d'usage (analytics) | Le catalogue décrit l'objet, l'analytics mesure son usage | High | Medium | UNRESOLVED | Une métadonnée enrichie par l'usage appartient à qui ? |
| 5 | KOR-09 | KOR-14 | Funnel, activation, rétention | Croissance/acquisition audience | Parcours in-app | Frontière activation/rétention à poser | Medium | Medium | UNRESOLVED | L'onboarding produit est-il KOR-09 ou KOR-14 ? |
| 6 | KOR-10 | KOR-07 | Partage de valeur, royalties | Économie/monétisation | Droits/royalties contractuelles | Le contrat fixe le taux, l'économie applique le modèle | High | Medium | UNRESOLVED | Le calcul de royalties est-il enseigné une fois ou deux ? |
| 7 | KOR-05 | KOR-13 | Cycle de vie créateur | Opérations quotidiennes créateur | Sourcing/acquisition business | Étapes différentes du même parcours | Medium | Low | UNRESOLVED | Le passage acquisition → onboarding est-il documenté une fois ? |
| 8 | KOR-04 | KOR-02 | Chaîne éditoriale | Programmation/curation (contenu existant) | Storytelling (création de contenu) | Étapes différentes : créer vs mettre en avant | Medium | Low | UNRESOLVED | `KOR-02-M06` (distribution KORA) chevauche-t-il déjà `KOR-04` ? |
| 9 | KOR-15 | KOR-07 | Déploiement marché vs droits territoriaux | Réseau international/stratégie | Droits/licensing territoriaux | Stratégie vs cadre juridique du même sujet | Medium | Low | UNRESOLVED | Qui pose le cadre légal avant l'expansion ? |

### 4.2 Tensions avec des entités CVLN externes à `KOR` (nouvelles, auditées §1.2)

| # | FORMATION_A | ENTITÉ_B | SHARED_DOMAIN | OWNERSHIP_A (KORA) | OWNERSHIP_B (entité) | HANDOFF | Overlap | Dup. risk | Frontier status | Open question |
|---|---|---|---|---|---|---|---|---|---|---|
| 10 | KOR-08 (Metadata & Cultural Catalog Operations) | **LabelOS** (`LOS-02` Metadata & Catalog Management, réel) | Métadonnées/catalogue d'œuvres (IDs, taxonomies, crédits) | Métadonnées orientées diffusion/streaming KORA — découvrabilité, recherche, provenance FREK | Métadonnées orientées gestion de label — ISRC/ISWC/DDEX, récupération de royalties | Un label structure son catalogue avec les standards LabelOS **en amont** ; KOR-08 consomme/normalise ces métadonnées pour l'exploitation KORA **en aval** | **High** — recouvrement le plus fort de toute la carte | **High** si KOR-08 réinvente ISRC/ISWC/DDEX | UNRESOLVED | KOR-08 présuppose-t-il LOS-02 (prérequis/pont) ou réenseigne-t-il les standards ? |
| 11 | KOR-10 (Content Monetization & Media Economics) | **Wallet/JCC** (réel, local, `wallet/models.py`) | Partage de valeur, royalties, paiement créateur | Modèle économique (freemium, pub, sponsoring, ARPU/LTV, pricing) | Mécanisme réel de solde/règlement (`jcc_balance`) | KOR-10 enseigne combien/quand payer ; Wallet est le seul mécanisme réel déjà câblé pour matérialiser ce paiement | Medium-High (seul domaine avec implémentation locale réelle, `KOR-0001` §4) | Low pour la brique technique (déjà réelle) ; **risque réel = présenter CVE/PSP comme existants** | UNRESOLVED | Le référentiel KOR-10 doit-il inclure un exercice réel sur `wallet_service`, ou rester conceptuel ? |
| 12 | KOR-12 (Streaming Data & Cultural Intelligence) | **CVLN Brain** (pôle `BRN` réel + shim événementiel réel) | Données, intelligence, décision assistée | Analytics d'usage streaming (plays/completions, tendances) | Pôle Academy IA/écosystème séparé (`BRN-01/02`) + interface best-effort câblée à `academy.certification.passed` | Brain n'est **pas** un moteur de données de streaming — au mieux KOR-12 pourrait un jour **émettre** vers Brain (même pattern que la certification), jamais l'inverse | Low en contenu réel, **High en risque de confusion de nommage** ("Cultural Intelligence" vs "Brain") | Medium — risque conceptuel, pas de duplication de contenu | UNRESOLVED | Le référentiel KOR-12 doit-il seulement citer le pattern d'event bus générique, sans dépendance métier réelle à Brain ? |
| 13 | KOR-11 (Trust, Safety & Content Governance) | **FREK / "Governance"** (pôle `FRK` réel + `frek_core.py`) | Confiance, signalement, protection | Politique de modération streaming-spécifique (contenus sensibles, mineurs, harcèlement, sanctions) | Infrastructure de preuve/provenance/signalement technique (`FRK-01-M07`, empreintes FREK, FREK-ID) | FREK fournit la preuve/le signalement technique réutilisable par toute entité CVLN ; KOR-11 décide de la politique (quoi sanctionner, comment) | Medium | Medium — risque de réinventer un mécanisme de preuve déjà réel | UNRESOLVED — **et le terme "Governance" lui-même est ambigu, voir note ci-dessous** | Le Founder confirme-t-il que "Governance" renvoie à FREK, et non à un système de modération de contenu dédié encore à construire ? |

**Note de désambiguïsation (`#13`, jamais devinée)** : le terme
"Governance" ne correspond à aucun objet unique dans ce repo. Deux
objets distincts portent un nom proche et n'ont **aucun rapport avec la
modération de contenu** : le badge `"Governance Associative"` (pôle
`KLT`, gouvernance associative/organisationnelle, `seed_data.py:654`) et
le module `"Governance token et DAO culturelles"` (`BCH-01-M06`, pôle
blockchain, gouvernance de token/DAO, `seed_modules.py:1549`). La
lecture retenue ici — FREK comme infrastructure de confiance la plus
proche fonctionnellement de "Trust, Safety & Content Governance" — est
la plus défendable au vu du contenu réel (`FRK-01-M07`), **mais n'est
pas confirmée par le Founder** et reste marquée `UNRESOLVED`.

---

## 5. Propositions de structure canonique haut niveau (blocs, aucun curriculum détaillé)

Aucun nombre de modules final n'est fixé. Chaque bloc documente
objectif, compétences, statut legacy, dépendances, recouvrement,
maturité, points ouverts — pas de leçons/exercices/évaluations.

### 5.1 `KOR01_CANONICAL_STRUCTURE`

| Bloc | Objectif | Compétences | Statut legacy | Dépendances | Recouvrement | Maturité | Points ouverts |
|---|---|---|---|---|---|---|---|
| A — Fondations éditoriales | Concevoir un podcast (sujet, format, script, interview) | Concept, écriture, **interview** (nouveau) | `EXTEND` (M01-M03) | Aucune | Tension #1 (léger, vs KOR-03 écriture audiovisuelle) | Élevée (3/4 modules existants) | Interview à construire |
| B — Production audio | Capter et fabriquer un épisode | Prise de son, montage, sound design, **mix/master** (à expliciter) | `EXTEND` (M04-M05) | Aucune | Tension #1 (fort, vs KOR-03 captation) | Élevée | Étape mix/master à isoler |
| C — Identité & habillage sonore | Donner une signature sonore | Générique, identité sonore | `KEEP` (M06) | Cadrage narratif KORA (non bloquant) | Faible | Élevée | Aucun |
| D — Distribution & publication | Publier sur les canaux du marché | RSS, DSP, hébergeurs | `KEEP` (M07) | Aucune (outils marché, pas de KORA vivant) | Faible | Élevée | Aucun |
| E — Audience & monétisation | Faire grandir et monétiser | Croissance, sponsors, séparation audience/monétisation | `EXTEND` (M08) | Wallet/JCC en évocation possible (tension #11), non tranché | Faible | Élevée | Lien Wallet à trancher plus tard |

### 5.2 `KOR02_CANONICAL_STRUCTURE`

| Bloc | Objectif | Compétences | Statut legacy | Dépendances | Recouvrement | Maturité | Points ouverts |
|---|---|---|---|---|---|---|---|
| A — Fondamentaux du journalisme culturel | Comprendre le paysage, chercher, vérifier | Recherche, sources, fact-checking | `KEEP` (M01-M02) | Aucune | Faible | Élevée | Aucun |
| B — Écriture & interview | Écrire long, interviewer | Feature/portrait/reportage, **interview** (nouveau) | `EXTEND` (M03) | Aucune | Tension #8 (léger, vs KOR-04) | Élevée | Interview à construire |
| C — Multiformats & narration | Décliner un sujet sur plusieurs formats | Texte/audio/vidéo/réseaux, narration | `KEEP` (M04) | Tension #1 croisée (KOR-01 audio, KOR-03 vidéo) | Moyen | Élevée | Aucun |
| D — Éthique, déontologie & représentation | Poser un cadre déontologique | Éthique, **représentation** (nouveau) | `EXTEND` (M05) | Aucune | Faible | Élevée | Représentation à construire |
| E — Diffusion & co-production KORA | Distribuer et co-produire | Diffusion, business co-production | `KEEP` (M06) | Cadrage KORA + pont Kiltikonet réel (non modifié) | Tension #8 (moyen, vs KOR-04) | Élevée | Aucun |
| F — Portfolio & signature | Se positionner comme référence | Portfolio, bio publique | `KEEP` (M07) | Aucune | Faible | Élevée | Aucun |

---

## 6. Cas fil rouge KORA — *L'Antenne Lanbi* (univers séparé de Kiltikonet)

Conformément à `KORA_CASE_UNIVERSE = SEPARATE_FROM_KILTIKONET`, cet
univers est **distinct** de *La Veillée du Tanbou* (Kiltikonet) — même
doctrine ("un seul cas, un angle métier différent par formation"), autre
symbole, autre trajectoire narrative, aucune dépendance à l'univers
Kiltikonet même si un pont réel existe déjà entre `KOR-02` et
`Kiltikonet` en base (`catalog_cartography.py:158`, constaté §3.1, non
utilisé narrativement ici).

### 6.1 Prémisse

**Le lanbi** (conque marine) est, dans plusieurs traditions caribéennes,
l'instrument utilisé pour appeler une communauté, annoncer une
nouvelle, ouvrir une cérémonie — un signal qui porte loin. *L'Antenne
Lanbi* est le récit fictif d'un collectif indépendant de la diaspora
caribéenne qui part d'un podcast fait dans une chambre et construit,
sur plusieurs années, un réseau média structuré — jusqu'à la
distribution internationale sous bannière KORA.

### 6.2 Univers et personnages centraux

- **Le collectif** : *Lanbi Collective*, fondé par trois voix de la
  diaspora (Martinique, Haïti, Guadeloupe) qui ne se sont jamais
  rencontrées physiquement avant le podcast.
- **L'objet central** : une série audio puis multi-format,
  *"Rasin"* (racine), qui documente des histoires de familles
  caribéennes dispersées — le contenu produit et raconté traverse
  ensuite tous les métiers KORA, de sa fabrication à sa diffusion
  internationale.
- **La tension narrative** : faire grandir *Rasin* sans perdre sa
  justesse culturelle ni sa rigueur journalistique — un fil qui traverse
  naturellement production, storytelling, droits, données, confiance et
  expansion internationale.

### 6.3 Traversée conceptuelle des 15 formations (angle métier seulement — aucun contenu pédagogique)

Chaque ligne décrit l'angle professionnel qu'un futur référentiel
pourrait adopter sur *Rasin* — **rien ici n'est un module, un exercice
ou une évaluation** ; c'est la description narrative requise pour
que le cas soit "conçu pour traverser les 15 formations", conformément
au mandat, sans construire `KOR-03`→`15`.

| Formation | Angle métier sur *Rasin* |
|---|---|
| KOR-01 | Enregistrer et monter le tout premier épisode de *Rasin*, dans une chambre |
| KOR-02 | Raconter culturellement l'histoire derrière *Rasin*, vérifier les sources familiales |
| KOR-03 | Filmer un making-of vidéo puis une captation live de *Rasin* |
| KOR-04 | Programmer *Rasin* dans une grille éditoriale plus large |
| KOR-05 | Gérer le flux de production et les livrables du collectif *Lanbi* |
| KOR-06 | Exploiter la disponibilité et la qualité de diffusion de *Rasin* une fois en ligne |
| KOR-07 | Négocier les droits de diffusion internationale de *Rasin* |
| KOR-08 | Structurer les métadonnées et crédits de chaque épisode de *Rasin* |
| KOR-09 | Faire grandir l'audience diaspora de *Rasin* |
| KOR-10 | Construire le modèle économique (sponsors, abonnement) de *Rasin* |
| KOR-11 | Gérer un signalement sur un épisode sensible de *Rasin* |
| KOR-12 | Analyser les données d'écoute de *Rasin* pour orienter la suite |
| KOR-13 | Sourcer et acquérir de nouveaux créateurs pour élargir *Rasin* en collection |
| KOR-14 | Améliorer le parcours d'écoute/découverte de *Rasin* dans l'app |
| KOR-15 | Déployer *Rasin* dans de nouveaux territoires (Afrique, Amériques, Europe) |

**Statut** : cas décrit en entier au niveau conceptuel demandé par le
Founder. Aucun cas de formation individuel (Case Competency Matrix,
matrice de traçabilité, module complet) n'est écrit ici pour `KOR-03`→
`15` — cela resterait un acte de construction de curriculum, explicitement
interdit à ce ticket (`NO_KOR03_15_BUILD`). Pour `KOR-01`/`KOR-02`, cette
traversée n'est elle-même qu'une esquisse d'angle — l'écriture du cas
complet (fil rouge détaillé, façon *La Veillée du Tanbou* pour
Kiltikonet) reste également un acte de référentiel, pas de
réconciliation, et n'est donc pas produite ici.

---

## 7. Vérification des interdictions (avant commit)

| Interdiction | Statut | Vérification |
|---|---|---|
| `NO_DB_MUTATION` | Respecté | Aucune collection Mongo touchée — livrable 100% documentaire |
| `NO_RUNTIME_BINDING` | Respecté | Aucun fichier `.py`/`.js` créé ou modifié |
| `NO_SEED_REPLACEMENT` | Respecté | `seed_data.py`/`seed_modules.py` non ouverts en écriture, lus uniquement |
| `NO_BADGE_REASSIGNMENT` | Respecté | `KEEP` recommandé pour les deux badges (§2.4, §3.4) |
| `NO_CONTEXT_OVERRIDE` | Respecté | `KEEP` recommandé pour les deux `contexts` (§2.4, §3.4) |
| `NO_KOR03_15_BUILD` | Respecté | §4 et §6.3 strictement analytiques/narratifs, zéro module/exercice/évaluation écrit |
| `NO_KORA_PRODUCT_UPGRADE` | Respecté | Aucune intégration/service/API modifiée |
| `NO_FAKE_CVE` | Respecté | `CVE` marqué `ACADEMY_LOCAL_EVIDENCE = NOT_FOUND` / `EXTERNAL_PRODUCT_EVIDENCE_NOT_AUDITED` (§1.3), jamais défini ni déclaré inexistant |
| `NO_FAKE_STREAMING_CAPABILITY` | Respecté | DSP/CDN/player/SLA marqués `ACADEMY_LOCAL_EVIDENCE = NOT_FOUND` (§1.3), aucune capacité fabriquée |

Vérification structurelle complémentaire (`git diff --stat` avant
commit) : seul ce fichier est nouveau, confirmée en §8.

---

## 8. Séquence d'exécution — statut

| Étape | Statut | Note |
|---|---|---|
| `AUDIT` | `DONE` | §1 — extension `LabelOS`/`CVLN Brain`/`FREK`, reconfirmation `CVE`/DSP/rights/T&S/data |
| `RECONCILE` | `DONE` | §2, §3 — KOR-01/KOR-02, 14 éléments chacun, statuts uniques justifiés |
| `BOUNDARY_MAP` | `DONE` | §4 — 9 tensions reprises + 4 nouvelles (LabelOS, Wallet/JCC, CVLN Brain, FREK/Governance) |
| `CANONICAL_PROPOSAL` | `DONE` | §5 — blocs haut niveau KOR-01/KOR-02, aucun curriculum détaillé ; §6 — cas fil rouge KORA écrit en entier |
| `COMMIT` | En cours (juste après ce document) | — |
| `PUSH` | À suivre | Branche `claude/cvln-academy-canonical-fms` |
| `REPORT` | Ce document + résumé de fin de tour | — |
| `STOP` | **`TRUE` après livraison** | Aucun ticket `KOR-0003` démarré, aucun contenu `KOR-03`→`15` construit |

---

## 9. Ce que ce ticket n'a explicitement PAS fait

- Aucune mutation de `db.formations`/`seed_data.py`/`seed_modules.py`.
- Aucun renommage de badge, aucun changement de `contexts`.
- Aucun contenu pédagogique (module, exercice, évaluation) pour
  `KOR-03`→`15` — utilisées uniquement pour détecter des recouvrements
  en §4.
- Aucune tension de frontière tranchée (§4) — nommée et structurée,
  pas résolue.
- Aucun cas de formation individuel écrit pour `KOR-01`→`15` — seule la
  traversée conceptuelle du cas maître (§6.3) existe.
- Aucune décision `PUBLIC/EXTERNAL/BRIDGE` pour `KOR-03`→`15` (question
  laissée ouverte par `KOR-0001` §3, non traitée ici — hors périmètre).
- Aucune nouvelle intégration/service construit pour DSP/CDN/droits/
  metadata/trust & safety/data streaming.

## 10. Statut du gate

**`KOR-0002 = FROZEN` dès commit/push.** La collision legacy `KOR-01`/
`KOR-02` (`KOR-0001` §1) est désormais réconciliée élément par élément
(§2-§3). Le cas fil rouge KORA est choisi et écrit (§6). La Boundary Map
est étendue aux 4 entités CVLN nommées par le Founder (§4). Points
encore ouverts, explicitement non résolus par ce ticket : durée finale
des deux formations, couche assessments/skills complète, `PUBLIC/
EXTERNAL/BRIDGE` pour `KOR-03`→`15`, 13 tensions de frontière (aucune
tranchée), désambiguïsation du terme "Governance" (tension #13).

**Attendre une autorisation explicite pour toute étape suivante — pas de
`KOR-0003`, pas de construction `KOR-03`→`15` engagée par ce ticket.**
