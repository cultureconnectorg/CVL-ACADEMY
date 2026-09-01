# Audit des langues — état réel, et ajout de l'espagnol

**Contexte :** demande explicite — auditer honnêtement l'état du multilinguisme
(le PRD et le README affirment "trilingue FR/EN/Kreyòl") et ajouter l'espagnol.
Ce document sépare deux choses souvent confondues dans les livrables
précédents : la **coquille UI** (menus, boutons, libellés de navigation) et le
**contenu réel** (formations, modules, FMS, quiz) — leur niveau de couverture
linguistique est très différent, et le mélanger aurait été trompeur.

---

## 1. Résumé

| | État réel |
|---|---|
| Système i18n frontend | 1 dictionnaire JS (`frontend/src/lib/i18n.jsx`), 53 clés (47 + 6 imbriquées `stades`), 3 langues avant ce chantier |
| Fichiers frontend qui utilisent `t()` | **9 sur 19** (composants + pages) |
| Fichiers frontend à **0%** de couverture i18n | **8 sur 19** — entièrement en français en dur, y compris pour les rôles trainer/jury/admin |
| Fuites même dans les fichiers "câblés" | Oui — messages toast, titres d'étapes d'onboarding, etc. |
| Contenu pédagogique (formations, modules, FMS) | **100% français**, aucune infrastructure de traduction de contenu n'existe |
| Backend — sélecteur de langue exposé | `GET /api/onboarding/options` (hardcodé, 3→4 langues maintenant) |
| Backend — utilisation réelle de `User.lang` | Prompt système du Mentor IA (dynamique, robuste) ; tag sur les notifications (pas de corps localisé, la transport elle-même est un no-op tant qu'aucun provider n'est configuré) |
| Espagnol | **Ajouté aujourd'hui**, au même niveau de support que EN/KR — c'est-à-dire la coquille UI, pas plus (voir §2) |

**Verdict honnête :** la mention "trilingue" du README/PRD était vraie pour la
coquille de navigation (menus, dashboard, landing, formulaires d'auth,
onboarding — partiellement) mais fausse si on l'entend comme "toute
l'expérience utilisateur est disponible dans les 3 langues". L'espagnol
ajouté aujourd'hui est au même niveau — ni plus, ni moins avancé que
l'anglais ou le kreyòl existants.

---

## 2. Couverture réelle, fichier par fichier

Mesuré par comptage direct des appels `t("clé")` réels (en excluant les faux
positifs du type `api.get(...)` qui se terminent aussi par `t(`) contre les
chaînes de caractères en dur contenant des mots français dans le JSX.

### Fichiers câblés à `useI18n()` (9/19)

| Fichier | Appels `t()` réels | Chaînes françaises en dur restantes |
|---|---|---|
| `pages/Landing.js` | 12 | quelques-unes (stat headline, etc.) |
| `pages/Dashboard.js` | 11 | quelques-unes |
| `pages/FormationDetail.js` | 7 | quelques-unes |
| `pages/Missions.js` | 3 | **2 messages toast en dur** |
| `components/MentorPanel.js` | 2 | **1 message toast en dur** |
| `pages/Formations.js` | 2 | 0 |
| `components/Layout.js` | 1 | 0 |
| `pages/Badges.js` | 1 | quelques-unes |
| `pages/FrekProfile.js` | 1 | plusieurs libellés |
| `pages/Roadmap.js` | 1 | plusieurs libellés |
| `pages/Onboarding.js` | **0** | **la totalité des titres/sous-titres/kickers de chaque étape** ("Étape 1", "Dans quelle langue veux-tu apprendre ?", "Ton FREK Origin Story est lancé.", etc.) — seul le sélecteur de langue lui-même passait par `LANGS` (corrigé aujourd'hui, voir §4) |

`pages/Onboarding.js` importe `useI18n` uniquement pour `lang`/`setLang`
(l'état, pas les traductions) — la totalité du texte de l'assistant
d'onboarding, l'un des tout premiers écrans vus par un nouvel utilisateur,
reste français quelle que soit la langue choisie à l'étape 1. C'est
l'incohérence la plus visible trouvée dans cet audit.

### Fichiers à 0% de couverture i18n (8/19)

| Fichier | Lignes | Rôle concerné |
|---|---|---|
| `pages/ModuleJourney.js` | 546 | Étudiant — parcours LX v2 (plus gros fichier du frontend) |
| `pages/admin/AdminDashboard.js` | 270 | Admin — CMS, import FMS, orgs/cohortes |
| `pages/Certifications.js` | 125 | Étudiant — certifications |
| `pages/jury/JuryDashboard.js` | 117 | Jury — file de correction |
| `pages/Wallet.js` | 101 | Étudiant — wallet JCC/tokens |
| `pages/trainer/TrainerDashboard.js` | 99 | Trainer — cohortes |
| `pages/Skills.js` | 72 | Étudiant — Skill Engine |
| `components/BackButton.js` | 40 | Transverse |

**~1 370 lignes** de composants livrés lors du chantier de mise en production
(certification, skills, wallet, dashboards trainer/jury/admin — rules 3, 4, 6,
7, 10 du brief) n'ont jamais été raccordées au dictionnaire i18n. Ce n'est pas
une régression du jour — c'était déjà l'état livré le 30 août — mais ce n'était
pas non plus mentionné explicitement dans `docs/AUDIT_REPORT.md` à l'époque, ce
que cet audit corrige.

---

## 3. Backend — ce qui est réellement multilingue

- **`User.lang`** (`backend/models.py`) : simple `str`, pas de `Literal`
  strict côté schéma — rien n'empêche en base une valeur hors de
  `fr/en/kr/es` sauf aux deux points de validation explicite
  (`api/onboarding.py::onboarding_complete`, et implicitement le frontend qui
  ne propose que les valeurs de `LANGS`). Pas un bug bloquant, mais une
  garde-fou plus faible qu'un `Literal` l'aurait été.
- **Mentor IA** (`services/agent_factory.py`) : le prompt système instruit le
  modèle de répondre "en français, anglais, kreyòl ou espagnol selon la
  langue de l'apprenant" — c'est le seul mécanisme **réellement robuste** de
  cette plateforme pour le multilinguisme, parce qu'il génère la réponse
  dans la langue demandée à la volée plutôt que de dépendre d'un dictionnaire
  figé. L'espagnol y "fonctionne" dès l'ajout du mot dans le prompt (fait
  aujourd'hui) sans autre changement de code.
- **Notifications** (`services/notifications.py`) : chaque envoi porte un tag
  `lang`, mais **aucun corps de message localisé n'existe** — le transport
  réel n'est pas branché (voir `docs/INTEGRATIONS_REPORT.md`), donc ce
  n'était de toute façon pas un gap spécifique à l'espagnol.
- **Quiz auto-généré** (`backend/quiz.py`) : 100% français, y compris une
  question méta sur les langues du livrable — mise à jour aujourd'hui pour
  citer l'espagnol dans sa réponse correcte, pour rester exacte.
- **Contenu pédagogique** (`seed_data.py`, `seed_modules.py`, et tout le ZIP
  FMS réel importé — voir `docs/FMS_IMPORT_VALIDATION_REPORT.md`) : aucune
  traduction, aucune infrastructure pour en stocker une (pas de champ
  `lang` sur `Formation`/`Module`/`FmsResource`). Traduire ~30 formations et
  225 fichiers FMS réels serait un chantier de contenu à part entière, pas
  un chantier de code — hors du périmètre de cette session.

---

## 4. Ce qui a été fait aujourd'hui

Espagnol ajouté **au même niveau que l'anglais et le kreyòl existants** —
c'est-à-dire la coquille UI + le tag backend, pas la résolution des gaps du
§2 (qui préexistaient et ne sont pas propres à l'espagnol) :

- `frontend/src/lib/i18n.jsx` : 4ᵉ entrée `es` (53 clés traduites),
  `LANGS` gagne un champ `name` (le nom de chaque langue dans sa propre
  langue) pour que le sélecteur reste générique — un ajout de langue futur
  n'a plus qu'un seul endroit à toucher pour son libellé complet.
- `pages/Onboarding.js` : le sous-titre de chaque carte de langue à l'étape 1
  utilisait un `if`/`else` en dur pour "Français"/"English"/"Kreyòl" — corrigé
  pour lire `l.name` depuis `LANGS` (sinon l'espagnol serait apparu sans
  sous-titre). Grille réajustée de 3 à 4 colonnes.
- Backend : `GET /api/onboarding/options` (4 langues), validation
  `onboarding_complete` (accepte `es`), doc-commentaires `models.py`, prompt
  système du Mentor (`agent_factory.py`), question méta du quiz (`quiz.py`),
  assertion du test E2E (`tests/backend_test.py`).
- Docs : README, DEVELOPER_GUIDE, PRD, `design_guidelines.json` — mention
  "trilingue" → "4 langues".

**Ce qui n'a délibérément pas été fait** (pour ne pas élargir le périmètre
sans que ce soit demandé) : câbler les 8 fichiers à 0% de couverture (§2) au
dictionnaire i18n, ni traduire le contenu pédagogique. Les deux restent des
chantiers identifiés, pas silencieusement ignorés.

---

## 5. Réserve sur la qualité des traductions

Les traductions kreyòl (déjà présentes) et espagnol (ajoutées aujourd'hui)
ont été produites par moi (Claude), pas relues par un locuteur natif ni par
un·e pédagogue CVLN. Deux points de vigilance réels avant un lancement :

- **Kreyòl** existe en plusieurs variantes orthographiques régionales
  (Guadeloupe/Martinique/Guyane vs Haïti) — la forme utilisée ici n'a pas été
  validée contre la convention CVLN attendue.
- **Espagnol** a été rédigé dans un registre neutre, informel ("tú"),
  cohérent avec le tutoiement du français d'origine — mais sans arbitrage
  Espagne/Amérique latine si la cible CVLN a une préférence régionale
  (vocabulaire, ex. "correo electrónico" vs "mail/correo").

Recommandation : faire relire les 4 dictionnaires (`frontend/src/lib/i18n.jsx`)
par une personne CVLN avant tout lancement public, en particulier pour le
kreyòl et l'espagnol.

---

## 6. Recommandations (non exécutées, pour arbitrage)

1. Câbler les 8 fichiers du §2 au dictionnaire i18n (plus gros chantier :
   `ModuleJourney.js` à lui seul est le plus gros composant du frontend).
2. Traiter `pages/Onboarding.js` comme prioritaire — c'est le tout premier
   écran vu après inscription, actuellement 100% français malgré le choix de
   langue à l'étape 1.
3. Nettoyer les messages `toast.*()` restés en dur dans les fichiers déjà
   câblés (`Missions.js`, `MentorPanel.js`, `Onboarding.js`).
4. Envisager un `Literal["fr", "en", "kr", "es"]` pour `User.lang` côté
   backend plutôt qu'un `str` libre, pour un garde-fou schéma plutôt
   qu'applicatif seul.
5. Si CVLN veut un jour traduire le contenu pédagogique (formations/FMS),
   ça suppose un modèle de données différent (contenu versionné par langue)
   — à concevoir séparément, ce n'est pas une extension mineure du système
   actuel.
