# Rapport de validation — import du premier ZIP FMS réel

**Archive validée :** `FMS_Chantier_Complet_20260822.zip` (223 fichiers
Markdown, 6 métiers FMS-01 à FMS-06 + leurs 6 référentiels FMS-A à FMS-F,
verrouillés). Reçue après la mission de mise en production — comme
annoncé dans le brief initial ("Les ZIP des formations arrivent après
cette mission").

**Ce que ce rapport couvre :** la validation du moteur d'import
(`backend/fms_import/`) contre la structure **réelle** de ce premier ZIP,
et sa réconciliation avec la convention qui avait dû être inventée avant
qu'aucun ZIP réel n'existe (voir `docs/DEVELOPER_GUIDE.md` §3, ancienne
version). Ce rapport couvre **deux niveaux de validation** : la partie
pure du pipeline (§3-4), et le chemin d'écriture réel en base
(`import_fms_zip`, upsert, index, navigation, graphe — §5), exécuté contre
une base MongoDB **en mémoire, non persistante**, faute d'accès à une
vraie instance dans cet environnement d'exécution (voir §6).

---

## 1. Écart entre la convention documentée et la réalité

La convention documentée avant ce ZIP (Markdown + frontmatter YAML) ne
correspondait à aucun des 223 fichiers réels : **aucun** ne porte de bloc
`---`. La structure réelle, remarquablement cohérente sur les 6 métiers
parce qu'elle suit un gabarit que les auteurs eux-mêmes ont figé et
documenté (`00_GABARIT_Construction_Metier.md`, extrait du Package FMS-01
et appliqué à l'identique à FMS-02→FMS-06), est :

- un nom de fichier numéroté et porteur de sens : `NN_FMS0<métier>_<Type>.md`
  (ex. `13_FMS01_M01_Blueprint.md`) ou `NN_FMS-<Lettre>_Referentiel_<Nom>.md`
  pour les référentiels métier ;
- du Markdown pur en corps de fichier — prose + tableaux Markdown pour les
  champs structurés, jamais de frontmatter ;
- un identifiant de compétence canonique `FMS0<n>-<Bloc><n°>` (ex.
  `FMS01-B2`), déclaré explicitement par chaque `Skill_IDs_Registry.md`.

Le moteur d'import (`fms_import/models.py`, `parser.py`, `module_map.py`,
`importer.py`, `indexer.py`) a été réécrit pour classifier chaque fichier
depuis son nom (comme le ferait une personne qui parcourt l'archive), et
non plus depuis un frontmatter absent. Le frontmatter reste supporté s'il
est présent (aucun fichier réel n'en a besoin) pour ne rien casser si un
futur fichier en porte un.

## 2. Méthode de validation

Aucune instance MongoDB n'étant disponible dans cet environnement, la
validation ci-dessous exécute la partie **pure** du pipeline (extraction
ZIP → parsing → dérivation des prérequis de module → validation
référentielle — `fms_import/importer.py::_extract_markdown_files`,
`parser.py::parse_markdown_file`, `module_map.py::extract_module_prerequisites`,
`validators.py::validate_batch`), sans les deux étapes qui touchent la
base (`upsert` + reconstruction de l'index de recherche). C'est
exactement la même logique que `POST /api/fms/import` exécute, jusqu'à
l'écriture en base.

## 3. Résultat

```
223 / 223 fichiers .md extraits et classifiés (0 fichier non reconnu)
0 erreur de parsing, 0 avertissement de parsing
0 erreur de validation référentielle, 0 avertissement
```

**Répartition par type** (26 types réels identifiés, contre 10 types
inventés avant ce ZIP) :

| Type | Nombre | Type | Nombre |
|---|---|---|---|
| module (contenu complet) | 95 | rubric_master | 3 |
| blueprint | 15 | evidence_registry | 3 |
| grille_certificative | 7 | infrastructure | 3 |
| guide_correcteur | 6 | skill_ids_registry | 3 |
| banque_n1 | 6 | gabarit | 1 |
| competency_matrix | 6 | note_harmonisation | 1 |
| guide_formateur | 6 | index | 1 |
| cas_inedit | 6 | matrice_pedagogique | 1 |
| module_map | 6 | | |
| sujet_officiel | 6 | | |
| guide_jury | 6 | | |
| cas_fil_rouge | 6 | | |
| guide_candidat | 6 | | |
| banque_n2 | 6 | | |
| learning_map | 6 | | |
| referentiel | 6 | | |
| matrice_tracabilite | 6 | | |
| templates_etudiants | 6 | | |

**Répartition par formation** — chaque métier a un `formation_code`
cohérent avec le catalogue existant (`db.formations`, ex. `FMS-01`) :
FMS-01 (51), FMS-02 (35), FMS-03 (35), FMS-04 (33), FMS-05 (33), FMS-06
(33) ; 3 documents transverses (index, gabarit, matrice pédagogique) n'ont
volontairement pas de `formation_code` — ils précèdent/dépassent tout
métier particulier.

**Skill IDs :** 86 identifiants canoniques (`FMS0<n>-<Bloc><n°>`) détectés
dans le corps des documents, indexés pour la recherche/le cross-linking —
sans jamais être présentés comme un registre faisant autorité (ce rôle
reste celui du fichier `Skill_IDs_Registry.md` propre à chaque métier).

**1 collision détectée et corrigée pendant la validation :** FMS-01
contient à la fois `16_FMS01_A01_Grille_Certificative_Brouillon.md`
(brouillon, remplacé) et `49_FMS01_A01_Grille_Certificative_V1.md`
(verrouillée) — les deux généraient le même code avant correction du
générateur de code (`parser.py::_infer_code`, qui distingue désormais un
fichier "Brouillon" du fichier verrouillé qu'il ne doit pas écraser).
C'est le seul cas de ce type dans les 223 fichiers.

## 4. Graphe de prérequis entre modules — dérivé, pas fabriqué

`fms_import/module_map.py` extrait, pour chaque `Master_Module_Map.md`,
les prérequis déclarés module par module — **jamais** pour la ligne de
certification (`A0n`), dont le champ mélange un prérequis obligatoire et
des modules seulement recommandés ou explicitement jamais requis
(traiter ça en liste plate aurait déformé la doctrine).

Deux mises en page réelles coexistent selon le métier, et le parseur gère
les deux :
- **FMS-01/FMS-02/FMS-03** : un champ par ligne de tableau
  (`| **Prérequis** | M03 |`).
- **FMS-04/FMS-05/FMS-06** : une ligne compacte par module, champs
  séparés par « · » (`FMS04-M03 · **Bloc** : A · ... · **Prérequis** :
  M02 · ...`).

**Constat honnête, pas corrigé :** FMS-01/02/03 ont un prérequis dérivé
pour la quasi-totalité de leurs modules (14/15, 15/16, 15/16 — seul M01,
le module d'entrée, en est légitimement dépourvu). **FMS-04/05/06
n'expriment pas de `**Prérequis**` module par module** dans leur Master
Module Map pour la majorité de leurs modules (seuls les tout derniers
modules du tronc — le module d'intégration finale et le suivant — le
font) ; le graphe de dépendances réel pour ces trois métiers restera donc
partiel tant que ce n'est pas explicité dans le contenu source. Ce n'est
pas un bug du parseur : fabriquer un ordre séquentiel implicite là où le
document ne le déclare pas irait à l'encontre du principe "jamais
fabriquer" qui structure tout ce chantier — mieux vaut un graphe
incomplet et vrai qu'un graphe complet et inventé.

## 5. Validation du chemin d'écriture en base — `import_fms_zip()` réel

Aucune instance MongoDB n'est joignable depuis cet environnement
d'exécution (voir §6 pour le pourquoi exact). Pour valider malgré tout le
code qui écrit réellement en base — pas seulement la partie pure — le
pipeline complet (`import_fms_zip`, upsert, `ensure_search_index`,
`build_navigation`, `build_dependency_graph`) a tourné contre l'archive
réelle avec `db.db` substitué par une base Motor-compatible **en
mémoire** (`mongomock-motor`, PyPI — disponible car `pypi.org` est
accessible depuis ce sandbox, contrairement aux hôtes MongoDB officiels).
**Ce n'est pas un import persistant** — tout disparaît à la fin du
process — mais c'est exactement le même code que `POST /api/fms/import`
exécute sur une vraie base, jusqu'au dernier appel.

Résultat, contre les 223 fichiers réels :

```
ImportReport.status            = "success"
ImportReport.resources_created = 223
ImportReport.issues            = []
db.fms_resources.count()       = 223

GET .../formations/FMS-01/navigation      -> 51 ressources, 22 sections
GET .../formations/FMS-01/dependency-graph -> 51 nœuds, 21 arêtes
  (dont FMS-01-M07/M08/M09/M10 -> FMS-01-M11 -> FMS-01-M12,
   exactement le cas fil rouge cumulatif décrit par le Master Module Map)
```

Seule la recherche plein-texte (`$text` + tri par `$meta: "textScore"`)
n'a pas pu être vérifiée par ce chemin : `mongomock` n'émule pas
complètement cet opérateur (limite connue de la librairie, pas de notre
code) — une requête équivalente sans scoring (`$regex` sur
`body_markdown`) a confirmé que le filtrage par `formation_code` et la
recherche dans le corps fonctionnent ; le scoring `$text` réel dépend
d'un vrai moteur MongoDB (§6).

Restent, eux, non exécutés — nécessitent une vraie base persistante :

- **Aucune synthèse `Formation`/`Module` de catalogue** n'a été tentée
  depuis ces ressources (`db.formations` reste le catalogue existant,
  séparé) — cette synthèse était explicitement différée dans
  `docs/AUDIT_REPORT.md` §8 faute de ZIP réel pour valider le mapping.
  Le ZIP est maintenant disponible ; cette synthèse reste un point
  d'extension pour une prochaine itération, volontairement pas improvisée
  ici sans qu'un humain CVLN valide le mapping proposé (au minimum : quel
  champ du Master Module Map devient quel champ de `Module`, et comment
  les 26 types de ressources FMS s'articulent avec la fiche `Formation`
  existante).
- La recherche `$text` scorée (voir ci-dessus).

## 6. Pourquoi aucun vrai MongoDB n'est joignable ici, et comment en obtenir un

Cet environnement d'exécution est un conteneur éphémère avec un accès
réseau sortant filtré par une politique d'allowlist. Concrètement, pour
MongoDB :

- **Installation locale via un gestionnaire de paquets** : impossible —
  Ubuntu (comme Debian) a retiré `mongodb-server` de ses dépôts officiels
  depuis des années (changement de licence SSPL côté MongoDB Inc.) ;
  `apt-cache search mongo` ne retourne que des pilotes clients
  (`python3-pymongo`, `python3-motor`, ...), jamais le serveur.
- **Téléchargement direct depuis MongoDB Inc.** (`repo.mongodb.org`,
  `www.mongodb.org`, `pgp.mongodb.com`) : bloqué par la politique réseau
  de cette session (`x-deny-reason: host_not_allowed`) — ces hôtes ne
  sont pas sur la liste blanche.
- **Une instance distante/cloud** (MongoDB Atlas ou autre) : le protocole
  MongoDB natif (`mongodb://`, `mongodb+srv://`) est un protocole TCP
  brut, pas du HTTP — explicitement listé comme non supporté par le proxy
  réseau de cette session, quelle que soit l'allowlist d'hôtes.

**Pour un import réellement persistant**, il faut donc l'exécuter en
dehors de ce sandbox, là où `MONGO_URL` peut pointer vers une vraie
instance :

```bash
# Option A — Docker (le plus rapide en local ou sur un serveur de déploiement)
docker run -d --name cvln-mongo -p 27017:27017 -v cvln_mongo_data:/data/db mongo:7

# backend/.env
MONGO_URL=mongodb://localhost:27017
DB_NAME=cvln_academy

cd backend && uvicorn server:app --port 8000
```

```bash
# Option B — MongoDB Atlas (cloud, gratuit en tier M0) : créer un cluster
# sur cloud.mongodb.com, autoriser l'IP du serveur qui lance le backend,
# puis :
# backend/.env
MONGO_URL=mongodb+srv://<user>:<password>@<cluster>.mongodb.net
DB_NAME=cvln_academy
```

Puis, une fois le backend démarré contre cette vraie base :

```bash
curl -X POST http://localhost:8000/api/fms/import \
  -H "Authorization: Bearer <token admin>" \
  -F "file=@FMS_Chantier_Complet_20260822.zip"
```

ou via le bouton "Importer un métier FMS" du CMS admin
(`frontend/src/pages/admin/AdminDashboard.js`). Le rapport JSON retourné
(`ImportReport`) reprendra exactement les chiffres validés en §3 et §5 —
`resources_created: 223`, `resources_by_type` identique, `issues: []` —
avec, cette fois, une recherche plein-texte réellement scorée et des
données qui survivent au redémarrage.
