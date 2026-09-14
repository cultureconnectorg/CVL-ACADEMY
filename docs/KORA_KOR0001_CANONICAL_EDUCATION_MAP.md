# KOR-0001 — KORA Canonical Education Map

```
WORKSTREAM = KOR (KORA), séparé de FMS (FMS_CLOSED = TRUE) et de KLT
(workstream Kiltikonet en cours, non affecté par ce ticket)
KOR_WORKSTREAM = ACTIVE
NO_CROSS-CONTAMINATION = TRUE — aucun fichier FMS ni KLT touché ici.
METHOD = AUDIT -> CANONICALIZE -> FREEZE -> BUILD -> TEST -> VERIFY -> STOP
(même méthode que KLT-0001, "même niveau" — instruction du Founder,
2026-09-04)
THIS_TICKET_PHASE = AUDIT + CANONICALIZE + FREEZE (carte de haut niveau
uniquement)
MODULES_WRITTEN = FALSE (hors scope explicite de ce ticket)
DB_MUTATION = FALSE (livrable entièrement documentaire)
STOP_AFTER_DELIVERY = TRUE
```

**Source de vérité pour ce ticket** : le tableau des 15 formations
transmis verbatim par le Founder dans son message du 2026-09-04 (colonnes
`Code`/`Formation`/`Contenu principal`) — reproduit intégralement en §2.
Contrairement à `KLT-0001`, aucun fichier Excel n'a été fourni : ce
message **est** le master plan de ce ticket. Aucune colonne
`niveau`/`priorité`/`type` n'y figure — ces informations ne sont donc
**pas inventées** ici (voir §2, note).

---

## 1. Headline finding — un vrai code collision, pas encore résolu

**`KOR-01` et `KOR-02` ne sont pas des codes neufs.** Ils existent déjà,
en direct, dans ce repo — formations seedées avec titre, badge et
modules propres, antérieures à ce nouveau master plan. Le nouveau plan
canonique réutilise ces 2 codes pour des formations à **périmètre
différent**, et en ajoute **13 nouvelles** (`KOR-03`→`KOR-15`).

| Code | **Legacy (en direct dans le repo)** | **Canonique (ce master plan)** | Même code, périmètre différent ? |
|---|---|---|---|
| KOR-01 | *Podcast Production* — 31h, 8 modules (M01-M08), badge `Podcast Producer CVLN` (`seed_data.py:547-559`, `seed_modules.py:226-299`) | *Podcast & Audio Production* — concept éditorial, formats, écriture, interview, prise de son, studio/mobile, montage, sound design, mix/master, identité sonore, RSS/distribution, publication, audience, sponsors/monétisation | **OUI** — même famille de métier, portée élargie (identité sonore, mix/master professionnels, sponsoring explicite absents du legacy) |
| KOR-02 | *Media Storytelling & Cultural Broadcasting* — 28h, 7 modules (M01-M07), badge `Cultural Broadcaster` (`seed_data.py:561-573`, `seed_modules.py:300-364`) | *Cultural Storytelling & Broadcasting* — journalisme culturel, recherche, sources, fact-checking, angle, interview, portrait/reportage, narration culturelle, texte/audio/vidéo, éthique, représentation, adaptation réseaux, diffusion, portfolio/signature | **OUI**, le plus proche des deux — portée quasi identique au legacy (déjà 7/7 thèmes legacy couverts par le contenu principal annoncé) |
| KOR-03 | *(n'existe pas — confirmé, zéro trace)* | *Video & Streaming Production* — 15 modules planned | Pas de collision — **NEW** |
| KOR-04 | *(n'existe pas)* | *Editorial Programming & Curation* | **NEW** |
| KOR-05 | *(n'existe pas)* | *Creator & Content Operations* | **NEW** |
| KOR-06 | *(n'existe pas)* | *Streaming Platform Operations* | **NEW** |
| KOR-07 | *(n'existe pas)* | *Media Rights, Licensing & Distribution* | **NEW** |
| KOR-08 | *(n'existe pas)* | *Metadata & Cultural Catalog Operations* | **NEW** |
| KOR-09 | *(n'existe pas)* | *Audience Development & Growth* | **NEW** |
| KOR-10 | *(n'existe pas)* | *Content Monetization & Media Economics* | **NEW** |
| KOR-11 | *(n'existe pas)* | *Trust, Safety & Content Governance* | **NEW** |
| KOR-12 | *(n'existe pas)* | *Streaming Data & Cultural Intelligence* | **NEW** |
| KOR-13 | *(n'existe pas)* | *Creator Partnerships & Cultural Acquisitions* | **NEW** |
| KOR-14 | *(n'existe pas)* | *Streaming Product & Experience Operations* | **NEW** |
| KOR-15 | *(n'existe pas)* | *KORA Network & International Distribution* | **NEW** |

**13 formations sur 15 sont entièrement nouvelles** — une proportion de
contenu neuf bien plus élevée que pour Kiltikonet (3/8 formations
`NEW`). Aucun ancrage legacy n'existe pour `KOR-03`→`KOR-15` : ni
module, ni référentiel, ni calibration marché.

Legacy `KOR-01`/`KOR-02` sont référencés au-delà de `seed_data.py`/
`seed_modules.py` : `catalog_cartography.py:137-162` (contexts, audience
réels), `external_calibration.py:283-321` (ROME, confiance marché),
`services/integrations/registry.py:23` (`EcosystemIntegration("KORA",
"KORA")`, shim env-gated non configuré, même pattern que Culture
Connect/Kiltikonet), et une mission cross-pole réelle : `MIS-FMS-01`
("Prod caribéenne pour KORA", pole `FMS`, `entity: "KORA"`,
`seed_data.py:1150-1158`) — une mission FMS existante cible déjà KORA
comme plateforme de diffusion, preuve que KORA est déjà pensée comme
un pôle de diffusion transversal, pas seulement un pôle de formation.
Zéro trace côté frontend (`frontend/src` — zéro résultat pour
"kora"/"KORA").

**Ce mirroir exactement la collision `KLT-01`→`05` résolue
méthodologiquement (pas juridiquement) par `KLT-0001`/`0002`.** Per
`NO_CROSS-CONTAMINATION = TRUE`, ce document ne fusionne, ne renomme, ni
ne touche `KOR-01`/`02` legacy — ils restent seedés tels quels
(`DB_FORMATIONS_MUTATION = FORBIDDEN`, hérité de la même règle
appliquée à FMS et KLT). **Un équivalent KOR de `KLT-0002` (stratégie de
réconciliation/lignage) sera nécessaire avant tout référentiel
canonique** — signalé ici comme préalable, non résolu par ce ticket.

## 2. KOR_MASTER_MAP_v1 — les 15 formations canoniques (FROZEN)

Source : message du Founder, 2026-09-04, tableau reproduit verbatim
(colonne "Contenu principal" compressée ici en items séparés par `·`,
sens inchangé).

| # | Code | Formation | Contenu principal (verbatim, Founder) |
|---|---|---|---|
| 1 | KOR-01 | Podcast & Audio Production | Concept éditorial · formats audio · écriture · interview · prise de son · studio/mobile · montage · sound design · mix/master · identité sonore · RSS/distribution · publication · audience · sponsors/monétisation |
| 2 | KOR-02 | Cultural Storytelling & Broadcasting | Journalisme culturel · recherche · sources · fact-checking · angle · interview · portrait/reportage · narration culturelle · texte/audio/vidéo · éthique · représentation · adaptation réseaux · diffusion · portfolio/signature |
| 3 | KOR-03 | Video & Streaming Production | Préproduction · formats streaming · écriture audiovisuelle · tournage · lumière · son · multicam · live · réalisation · régie · montage · postproduction · encodage · publication · contrôle qualité |
| 4 | KOR-04 | Editorial Programming & Curation | Ligne éditoriale · connaissance des publics · programmation · curation musicale/vidéo · playlists · cycles éditoriaux · calendrier · diversité culturelle · contextualisation · recommandations · événements · mesure de performance |
| 5 | KOR-05 | Creator & Content Operations | Onboarding créateur · profil · ingestion contenu · fichiers/assets · contrôle qualité · publication · calendrier releases · corrections · support créateur · workflow éditorial · suivi catalogue · incidents · reporting |
| 6 | KOR-06 | Streaming Platform Operations | Fonctionnement d'un DSP · ingestion→delivery · exploitation quotidienne · disponibilité contenus · player · CDN/streaming concepts · qualité de service · incidents · escalade · SLA/SLO · monitoring · continuité · opérations multi-territoires |
| 7 | KOR-07 | Media Rights, Licensing & Distribution | Copyright/droits voisins · ayants droit · licences · masters · publishing · territoires · fenêtres d'exploitation · exclusivités · clearances · contrats · takedowns · royalties · reporting · distribution internationale |
| 8 | KOR-08 | Metadata & Cultural Catalog Operations | Métadonnées média · IDs · taxonomies · crédits · contributeurs · genres · langues · territoires · œuvres/enregistrements · normalisation · enrichissement culturel · contrôle qualité · recherche · découvrabilité · provenance/interfaçage FREK |
| 9 | KOR-09 | Audience Development & Growth | Segmentation · personas · acquisition · funnel · activation · communautés · social/content marketing · CRM · notifications · rétention · churn · campagnes · ambassadeurs · diaspora · expérimentation · mesure |
| 10 | KOR-10 | Content Monetization & Media Economics | Économie du streaming · free/premium · abonnement · publicité · sponsoring · ARPU/LTV · revenus contenus/créateurs · royalties · partage de valeur · coûts streaming · unit economics · pricing · bundles · Wallet/JCC · CVE |
| 11 | KOR-11 | Trust, Safety & Content Governance | Politiques de contenu · modération · signalements · contenus sensibles · fraude/spam · usurpation · droits · mineurs · harcèlement · recours · sanctions · transparence · gouvernance éditoriale · sécurité culturelle |
| 12 | KOR-12 | Streaming Data & Cultural Intelligence | Événements de lecture · plays/completions · métriques · dashboards · qualité des données · comportement audience · cohortes · rétention · tendances · performance contenus · recommandations · biais · intelligence culturelle · décision éditoriale |
| 13 | KOR-13 | Creator Partnerships & Cultural Acquisitions | Cartographie talents/catalogues · sourcing · qualification · proposition de valeur · négociation · onboarding partenaires · acquisitions · partenariats médias/institutions · relation créateurs · campagnes communes · suivi performance · renouvellement |
| 14 | KOR-14 | Streaming Product & Experience Operations | Parcours utilisateur · discovery · search · home/feed · bibliothèque · player · queue · playlists · recommandations · accessibilité · TV/mobile/web · expérience creator · tests utilisateurs · analytics produit · incidents UX · amélioration continue |
| 15 | KOR-15 | KORA Network & International Distribution | Stratégie territoriale · Caraïbe · diaspora · Afrique · Amériques/Europe · localisation · langues · droits territoriaux · partenaires locaux · distribution · institutions · telcos/médias · déploiement marché · adaptation culturelle · pilotage international |

**Note sur niveau/priorité/type** : contrairement à `KLT-0001` (feuille
*Vue d'ensemble* avec colonnes `Type`/`Statut`/`Niveau`/`Priorité`), le
message source ne fournit pas ces attributs pour KORA. Ils **ne sont
pas inventés ici** — chaque référentiel canonique futur (méthode
`KLT-0003`) devra les établir formation par formation, avec le Founder,
au moment voulu — pas anticipés globalement dans ce ticket.

## 3. PUBLIC/EXTERNAL/BRIDGE — dérivé, avec un vrai écart

Même règle que pour FMS (`ACA-0004`) et Kiltikonet (`KLT-0001` §3) :
le type de livraison n'est jamais inventé, il est lu depuis le champ
réel `contexts` quand il existe.

**Legacy `KOR-01`/`02` portent un vrai `contexts`**
(`catalog_cartography.py:137-162`, même forme `AcademyContext =
Literal["INTERNAL","EXTERNAL","BRIDGE"]`) :

| Code | Legacy `contexts` (réel) | Legacy `audience` (réel) |
|---|---|---|
| KOR-01 | `EXTERNAL, BRIDGE` | `DEBUTANT, INTERMEDIAIRE` |
| KOR-02 | `EXTERNAL, BRIDGE` | `INTERMEDIAIRE, PROFESSIONNEL` |

Comme pour Kiltikonet, ce sont les contextes de la formation **legacy**
— pas nécessairement ceux de la formation canonique élargie, qui reste
à trancher (même question que `KLT-0002` a dû traiter pour `KLT-01`→`05`).

**`KOR-03`→`KOR-15` n'ont aucun `contexts`** (n'existent pas dans
`catalog_cartography.py`). Leur nature (publique vs interne) n'est pas
non plus déductible du contenu principal seul pour toutes : `KOR-06`
(opérations plateforme), `KOR-11` (trust & safety), `KOR-08`
(métadonnées) et `KOR-12` (data) lisent clairement comme des métiers
internes à l'exploitation KORA ; `KOR-01`→`KOR-05`, `KOR-09`,
`KOR-13`, `KOR-14` lisent comme orientés créateurs/publics externes ;
`KOR-07` (droits/licensing) et `KOR-10` (monétisation) sont mixtes par
nature (négociation externe, comptabilité interne) ; `KOR-15` (réseau
international) dépend du modèle de déploiement, non tranché ici.

**Verdict : `PUBLIC/EXTERNAL/BRIDGE` reste `UNRESOLVED` pour
`KOR-03`→`KOR-15`, aucun défaut fabriqué** — à trancher formation par
formation, comme cela a été fait pour `KLT-06`→`08` via `KLT-0008`.

## 4. Dépendances KORA réelles — vérifiées contre ce repo

| Domaine (message Founder) | État réel dans CVL-ACADEMY (vérifié) |
|---|---|
| KORA (plateforme/pôle lui-même) | Shim d'intégration réel, non configuré : `services/integrations/registry.py:23` (`EcosystemIntegration("KORA","KORA")`), même pattern "prête mais découplée" que Kiltikonet/Culture Connect. Aucune collection `db.*` dédiée. |
| Wallet / JCC | **Réel et en direct** — `wallet/models.py`, `wallet/passes.py` (`jcc_balance` déjà un champ réel du compte Wallet). Le seul domaine du tableau Founder avec une implémentation locale réelle. |
| CVE | **Non trouvé, nulle part dans ce repo.** Aucune définition, aucun acronyme développé. Terme non résolu — ce ticket ne devine pas sa signification (Culture Value Exchange ? autre ?) ; à faire préciser par le Founder avant tout référentiel qui en dépend (`KOR-10`). |
| DSP / CDN / streaming, player, SLA/SLO (`KOR-06`, `KOR-14`) | **Zéro footprint** — aucune collection `db.*`, aucun service, aucune mention hors des 4 fichiers de seed/cartographie déjà cités pour `KOR-01`/`02` (où ces termes n'apparaissent que dans la description de modules legacy, jamais comme infrastructure réelle). |
| Media rights / licensing / royalties (`KOR-07`) | **Zéro footprint.** Aucune collection contrats/royalties/territoires. |
| Metadata / taxonomies / catalog (`KOR-08`) | **Zéro footprint.** Aucune collection métadonnées média dédiée (à distinguer de `db.fms_resources`/`db.klt_resources`, qui sont des catalogues **pédagogiques**, pas des catalogues d'œuvres). |
| Trust & safety / modération (`KOR-11`) | **Zéro footprint.** Aucune collection modération, signalement, ou politique de contenu trouvée nulle part dans `backend/`. |
| Streaming data / analytics (`KOR-12`) | **Zéro footprint** pour des données de lecture réelles (plays/completions). `db.progress` existe mais mesure la progression pédagogique Academy, pas une consommation média KORA — domaine différent, à ne pas confondre. |
| FREK (mentionné pour `KOR-08`, "provenance/interfaçage FREK") | **Réel, local** — `services/frek_core.py`, même interface découplée déjà utilisée par FMS et Kiltikonet (`FREK-WORK`/`FREK-SCORE`/`FREK-CONTRIB`/`FREK-CERT`, déjà réellement utilisés par les modules legacy `KOR-01`/`02`, voir §1). |

**Conclusion, pour prévenir toute violation `NO_FAKE_KILTIKONET_
FEATURE`-équivalent côté KORA** : dans ce repo, seuls **Wallet/JCC** et
**FREK** sont des domaines réels et locaux parmi ceux nommés par le
Founder ; **KORA elle-même** a une interface découplée réelle (même
statut que Kiltikonet avant ce workstream) ; **tout le reste — DSP/CDN/
streaming, droits/licensing, métadonnées média, trust & safety, data
streaming — n'a aucun footprint dans ce repo.** Tout futur ticket KOR
qui nommerait ces domaines comme dépendance devra soit obtenir un accès
réel, soit construire le même pattern d'interface découplée déjà utilisé
ailleurs — jamais un substitut fabriqué présenté comme réel.

## 5. Relation à Academy — ce qui existe déjà, ce qui n'existe pas

- **Formations/modules** : `KOR-01`/`02` legacy sont en direct dans
  `db.formations` (via `seed_data.py`) avec de vrais modules (via
  `seed_modules.py`) — indistinguables au niveau API de n'importe quelle
  autre formation Academy.
- **Missions** : `MIS-FMS-01` cible KORA comme plateforme de diffusion
  — préexistante, hors scope des 15 formations, non touchée ici.
- **Frontend** : aucune page, route ou composant spécifique KORA
  n'existe — les formations `KOR-01`/`02` legacy passent par les mêmes
  surfaces génériques `Formations`/`ModuleJourney` que toute autre
  formation.
- **Certification/skills** : aucun schéma de skill ID ni de
  certification spécifique KORA (à la différence de FMS `FMSxx-Ay` ou
  Kiltikonet `KLTxx.SKILL.Cxx`) — terrain vierge pour la couche
  certification, cohérent avec ce qui a déjà été constaté pour
  Kiltikonet en `KLT-0001` §5.

## 6. Standard d'architecture documentaire (référence gelée)

Réutilisation explicite de la même discipline déjà appliquée à FMS et
Kiltikonet (20 couches obligatoires par formation : référentiel métier,
Master Learning/Module Map, doctrine + frontières, cas fil rouge, Case
Competency Matrix, matrice de traçabilité, blueprints, modules complets,
banques N1, évaluations N2, assessment N3, grilles de correction, skill
IDs/preuves, guides candidat/correcteur/jury, templates, intégration
Academy, FREK/progression/certification). Aucune de ces couches n'est
produite par ce ticket.

## 7. Cas fil rouge — question ouverte, non tranchée ici

Kiltikonet a posé la doctrine "même univers, angle métier différent" —
un seul cas (*La Veillée du Tanbou*) traversant les 8 formations. Pour
KORA, deux options réelles se présentent, **non tranchées par ce
ticket** :

1. **Un univers KORA propre** — une œuvre/production culturelle
   caribéenne fictive suivie de la création à la diffusion
   internationale, cohérente avec `KOR-15` (réseau international).
2. **Réutiliser/étendre l'univers Kiltikonet** — *La Veillée du Tanbou*
   est déjà diffusée sur KORA dans le cas `KLT-05` (angle opérateur
   plateforme) ; un cas KORA pourrait suivre sa production éditoriale
   (podcast, reportage, streaming) en amont de cette diffusion déjà
   écrite.

Les deux sont défendables ; le choix relève du Founder et sera posé
explicitement dans le prochain ticket (référentiel de la première
formation), pas ici.

## 8. Tensions de frontière réelles entre les 15 formations — surfacées, pas résolues

Contrairement à Kiltikonet (8 formations, chevauchements limités), 15
formations KORA denses créent des zones de recouvrement réelles,
listées ici pour que chaque référentiel futur les traite explicitement
plutôt que de les découvrir en construisant :

| Tension | Formations concernées | Nature du recouvrement |
|---|---|---|
| Production audio vs vidéo | `KOR-01` / `KOR-03` | Techniques de prise de son, montage, publication — médias différents, méthode proche |
| Opérations plateforme vs expérience produit | `KOR-06` / `KOR-14` | Player, disponibilité, qualité de service vs parcours utilisateur — vue infra vs vue UX du même système |
| Droits/licensing vs partenariats créateurs | `KOR-07` / `KOR-13` | Contrats, négociation, territoires — cadre juridique vs relation business |
| Métadonnées catalogue vs data streaming | `KOR-08` / `KOR-12` | Les deux manipulent des données sur les œuvres/usages — catalogue descriptif vs mesure d'usage |
| Croissance audience vs expérience produit | `KOR-09` / `KOR-14` | Funnel/acquisition vs parcours in-app — frontière activation/rétention à poser |
| Monétisation vs droits/royalties | `KOR-10` / `KOR-07` | Partage de valeur, royalties apparaissent dans les deux contenus principaux |
| Opérations créateur vs partenariats créateur | `KOR-05` / `KOR-13` | Cycle de vie créateur : onboarding/support quotidien vs sourcing/acquisition business — étapes différentes du même parcours |
| Programmation éditoriale vs storytelling | `KOR-04` / `KOR-02` | Curation/mise en avant de contenu existant vs création de contenu original — étapes différentes de la chaîne éditoriale |
| Réseau international vs droits territoriaux | `KOR-15` / `KOR-07` | Déploiement marché vs droits territoriaux — stratégie vs cadre juridique du même sujet |

Aucune de ces tensions n'est un problème en soi (FMS et Kiltikonet en
avaient aussi, résolues référentiel par référentiel) — elles sont
nommées ici pour que le prochain ticket qui construit un référentiel
proche d'une frontière la pose explicitement (méthode déjà appliquée à
`KLT-07`/`KLT-04`/M11 et `KLT-08`/`KLT-04`/M12-M13).

## 9. Ce que ce ticket n'a explicitement PAS fait

- Aucun contenu de module écrit, pour aucune des 15 formations.
- Aucun code touché, aucune collection écrite, aucune mutation de
  `db.formations`.
- Aucune résolution de la collision legacy `KOR-01`/`02` (§1) —
  surfacée, pas réglée (un équivalent `KLT-0002` reste à faire).
- Aucune décision `PUBLIC/EXTERNAL/BRIDGE` forcée pour `KOR-03`→`15`
  (§3) — surfacée comme ouverte, pas fabriquée.
- Aucune tension de frontière (§8) tranchée — nommée, pas résolue.
- Aucun univers de cas fil rouge choisi (§7) — deux options réelles
  posées, aucune tranchée.
- Aucune nouvelle intégration construite pour DSP/CDN/droits/métadonnées/
  trust & safety/data streaming — leur absence de ce repo est rapportée,
  jamais comblée par un substitut.

## 10. Statut du gate

**`KOR-0001 = FROZEN`.** `KOR_MASTER_MAP_v1` (15 formations, collision
legacy, dépendances vérifiées contre ce repo) est canonicalisé dans ce
document. Trois points ouverts bloquent une progression propre vers le
travail par formation : la collision de code legacy/canonique `KOR-01`/
`02` (§1), le statut `PUBLIC/EXTERNAL/BRIDGE` de `KOR-03`→`15` (§3), et
le choix d'univers de cas fil rouge (§7) — tous explicitement nommés,
aucun deviné.

`STOP = TRUE.` Prochaine étape proposée, **en attente du feu vert du
Founder** : `KOR-0002 — Réconciliation Legacy → Canonique pour KOR-01/
02` (même méthode que `KLT-0002`), avant tout référentiel canonique de
formation. Aucun autre scope KOR ou ACA pris au-delà de ce document.
