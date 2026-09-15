# CVLN Academy — État et inventaire de la plateforme
**Date du rapport : 15 septembre 2026 — HEAD `efbc44e5064845125a69fe337a318723621733f0` (branche `main`)**

## Résumé exécutif

CVLN Academy est aujourd'hui une plateforme d'apprentissage complète et fonctionnelle pour l'écosystème culturel et créatif CVLN, avec un backend Python (~76 000 lignes, 399 fichiers) exposant 85 domaines d'API et un frontend React (~23 300 lignes, 30 pages) couvrant les parcours apprenant, formateur, jury et admin, en 4 langues (français, anglais, créole, espagnol). La plateforme vient de traverser une réconciliation de plusieurs semaines qui a fusionné sans perte trois branches de développement parallèles (`main`, `claude/cvln-academy-production-r35l31`, `claude/cvln-academy-canonical-fms`) — l'audit final confirme 2701 tests backend passants sur 2701 et un build frontend propre, aucune fonctionnalité perdue. Au-delà du code applicatif, le repo porte un corpus pédagogique considérable et rigoureusement tracé (30 formations "legacy" historiques + des centaines de formations canoniques FMS/Kiltikonet/KORA/FRK et de domaines écosystème externes), avec une doctrine explicite de non-invention : tout ce qui n'est pas construit sur une preuve réelle est déclaré `BLOCKED`, `NOT_AUTHORIZED` ou `NEEDS_EXPERT_REVIEW` plutôt que simulé. Le moteur "Spatial Learning" (monde 3D/WebGL) est en production mais ses couches d'intégration les plus profondes restent désactivées par défaut ; les paiements et la plupart des intégrations écosystème (Wallet, Brain, Command Center, Kiltikonet, etc.) sont du code réel mais fonctionnent en interface découplée avec repli local tant que les identifiants/systèmes externes réels ne sont pas branchés.

---

## 1. Vitals du dépôt

| Métrique | Valeur réelle | Source |
|---|---|---|
| Commits sur `main` (= HEAD `efbc44e5`) | **607** | `git rev-list --count efbc44e5...` |
| Fichiers Python backend (hors `__pycache__`) | **399** | `find backend -name "*.py"` |
| Lignes de code backend | **75 873** | `wc -l` sur tous les .py |
| Fichiers JS/JSX frontend | **220** | `find frontend/src -name "*.js" -o -name "*.jsx"` |
| Lignes de code frontend | **23 318** | `wc -l` |
| Fichiers de tests backend (`backend/tests/test_*.py`) | **116** | `find` |
| Dernier résultat de tests vérifié | **2701/2701 tests backend passants** (2650 via `pytest tests/` + 51 via `backend_test.py` contre un serveur MOCK_DB réel), **build frontend `yarn build` propre, 0 erreur/warning** | `docs/reconciliation/RECONCILE_4_COMPARISON.md` (daté 2026-09-15) |
| Fichiers de specs e2e Playwright | **31** fichiers `.spec.js` dans `frontend/e2e/`, ~132 cas de test individuels comptés directement | `find`/`grep -c "test("` |

**Note d'honnêteté :** `RECONCILE_4_COMPARISON.md` cite un "baseline e2e Playwright de 159 specs" établi dans un rapport antérieur (`RECONCILE_3_RUNTIME_REPORT.md`) — ce chiffre ne correspond pas au compte de fichiers `.spec.js` actuel (31) ni au compte de `test(...)` (~132). Il s'agit très probablement d'une convention de comptage différente (peut-être un compte à un instant antérieur, ou "spec" = assertion/scénario et non fichier). Ce chiffre de 159 est cité tel quel du document source, pas vérifié indépendamment dans ce rapport.

## 2. Architecture backend

**Structure `backend/` (paquets de premier niveau) :**
`api/` (85 routeurs), `canonical_common/`, `certification/`, `commerce/`, `data/`, `fms_canonical/`, `fms_import/`, `fms_lineage/`, `frk_canonical/`, `klt_canonical/`, `kor_canonical/`, `payments/`, `qualification/`, `scripts/`, `services/`, `skills/`, `template_engine/`, `tests/`, `wallet/` — plus des modules racine (`auth.py`, `billing.py`, `economy_3d.py`, `seed_data.py`, `server.py`, etc.).

**85 fichiers routeurs dans `backend/api/`**. Répartition par domaine :

- **Auth / onboarding** : `auth.py`, `onboarding.py`, `mcp_oauth.py`
- **Apprentissage / progression** : `learning.py`, `progression.py`, `formations.py`, `missions.py`, `quizzes.py`, `mentor.py`
- **Curriculum canonique FMS/KLT/KOR/FRK** : `fms.py`, `fms_lineage.py`, `klt_canonical.py`, `kor_canonical.py`, `frk_canonical.py`, `canonical.py`
- **Certification / compétences** : `certification.py`, `skills.py`, `badges.py`, `expert_validations.py`, `professional_governance.py`, `professional_profile.py`
- **Wallet / paiements / commerce** : `wallet.py`, `payments.py`, `billing.py`, `billing_views.py`, `commerce.py`, `commercial.py`, `commercial_access.py`, `economy.py`, `license_entitlement.py`
- **Sessions physiques** : `physical_sessions.py`
- **Légal / gouvernance / conformité / risque / privacy / comptabilité — 26 routeurs (≈31 % des 85)** : 9 `legal_*`, 4 `privacy_*`, 2 `governance_*`, 2 `risk_*`, 3 `quality_*`, 3 `accounting_*`, 3 `security_*`. C'est un poids inhabituellement lourd de surface API "gouvernance/conformité" pour une plateforme e-learning — cohérent avec le corpus de gouvernance documentaire massif observé en sections 6/7 (le produit porte une doctrine anti-invention très formalisée qui se reflète jusque dans l'API).
- **Intégrations écosystème / divers** : `integrations.py`, `institutional.py`, `expert_portal.py`, `assistants.py`, `master_registry.py`, `policy_registry.py`, `authority_policy.py`, `regulatory_applicability.py`, `data_governance.py`, `data_classification.py`, `evidence_graph.py`, `critical_proof.py`, `incident_core.py`, `threat_model.py`, `trust_signature.py`, `assurance.py`, `careops.py`, `stakeholders.py`, `orgs.py`, `workbook_runtime.py`, `templates.py`, `production_gates.py`, `accelerators.py`, `health.py`

## 3. Architecture frontend

**30 pages** dans `frontend/src/pages/*.js` : dashboards par rôle (`Dashboard.js`, `ExpertWorkspace.js`), visualiseurs de formations canoniques par domaine (`CanonicalFormations.js`/`CanonicalFormationDetail.js`/`CanonicalModuleView.js` génériques, plus des variantes dédiées `CanonicalKlt*`, `CanonicalKor*`, `CanonicalFrk*`), `Wallet.js`, `Offers.js`, `EcosystemBuilder.js`, `ProfessionalPublicProfile.js`, `Missions.js`, `Skills.js`, `Certifications.js`, `Badges.js`, `Roadmap.js`, `Onboarding.js`, `Landing.js`, `Pricing.js`, `FrekProfile.js`.

**Moteur spatial** (`frontend/src/lib/spatial/`, 48 fichiers dont ~24 fichiers `.test.js`) : gate par flags dans `frontend/src/lib/featureFlags.js`. Le moteur de base (`SPATIAL_ENGINE`, `SPATIAL_ENVIRONMENT`, `SPATIAL_WEBGL`) est **ON par défaut** en production ("Spatial world rendering is now an approved production capability"). Ce qui reste **OFF par défaut** sont les couches d'intégration profonde H1 et suivantes : `SPATIAL_HUB_ENABLED`, `SPATIAL_CAMERA_INTENT`, `SPATIAL_MODULE_DEPTH`, `SPATIAL_HERO_ENTRY`, `SPATIAL_IDENTITY_ENTRY`, `SPATIAL_ONBOARDING_ENTRY`, ainsi que `SPATIAL_AUDIO`, `SPATIAL_HAPTICS`, `SPATIAL_DEBUG`, `SPATIAL_ROUTE_TRANSITIONS`, `LIFECYCLE_RUNTIME`.

**i18n** : `frontend/src/lib/i18n.jsx`, tableau `LANGS` = **4 langues** : `fr` (Français), `en` (English), `kr` (Kreyòl), `es` (Español).

## 4. Inventaire du corpus pédagogique

**Formations "legacy" (`backend/seed_data.py`)** : le fichier lui-même commente "**30 formations — condensed**", réparties en 13 pôles (FMS, KORA, GMD, SAY, KLT, FRK, LOS, BRN, AGR, BCH, HOS, GRP, CIP). Compte vérifié : **30**.

**Corpus canonique documentaire (`docs/`)** — chiffres réels vérifiés, corrigeant plusieurs valeurs obsolètes de l'historique de tâches :

| Domaine | Chiffre réel vérifié | Détail |
|---|---|---|
| **FMS** (Factory Maker Studio) | FMS-01→06 canon original, Founder-gated (`NOT_AUTHORIZED`/`STOP_AFTER_DELIVERY=TRUE`, changement interdit) + **9 formations d'extension FMS-07→18** (12 candidats fusionnés en 9), toutes `PACKAGE_COMPLETE` | `docs/fms/README.md`, `docs/fms/` (9 sous-dossiers numérotés) |
| **KLT** (Kiltikonet) | **10 formations construites** (KLT-01→08, KLT-13, KLT-18) — **pas 8**, chiffre obsolète — soit **253 documents pédagogiques**. 10 candidats supplémentaires (KLT-09→20 hors 13/18) fermés `BLOCKED_PRODUCT_DEPENDENCY` ou fusionnés par référence | `docs/klt/README.md`, `docs/klt/` (10 sous-dossiers) |
| **KOR** (KORA) | **15 formations canoniques KOR-01→15** — correspond exactement à l'historique | `docs/kor/` (15 sous-dossiers) |
| **FRK** (FREK/trust & provenance) | Le corpus réel couvre **75 candidats au total** — **pas 56**, chiffre obsolète : 54 `PACKAGE_COMPLETE`, 3 `MODULE_CONTENT_DRAFTED`/`NEEDS_EXPERT_REVIEW` (FRK-10, 14, 73 — retenus tant qu'un expert humain réel n'a pas validé), 10 `BLOCKED_PRODUCT_DEPENDENCY` (FRK-19,21,22,24,39,57,64,65,66,67), 8 `EXTEND_EXISTING` (fusionnés dans une formation sœur, sans dossier séparé). 54+3+10+8 = 75 | `docs/frk/README.md`, `docs/frk/` (67 sous-dossiers numérotés) |
| **Domaines écosystème externes/candidats** (WAL, CVE, GMD, etc.) | `docs/wal/` : 10 sous-domaines numérotés · `docs/cve/` : 15 · `docs/gmd/` : 14 · plus 11 domaines de gouvernance sans numérotation (`agf`, `bci`, `ceo`, `cyb`, `fdc`, `gcf`, `grp`, `hos`, `los`, `say`, `xcv`) — chacun structuré en README + `BLOCKED_CANDIDATES.md`/`EXTEND_EXISTING_NOTE.md`/`QUALITY_GATES.md` + un sous-dossier `external/` — des domaines très largement au stade "cadrage/gouvernance/blocages documentés" plutôt que des corpus de formation complets | `find docs/{wal,cve,gmd,...}` |

**Conclusion pour le Founder** : les chiffres "8 KLT / 15 KOR / 56 FRK" cités dans l'historique de tâches sont **partiellement obsolètes** — le corpus a grandi depuis (KLT : 8→10, FRK : 56→75 candidats classifiés). KOR est le seul chiffre qui reste exact (15).

## 5. État des tests

- **116 fichiers de tests backend** (`backend/tests/test_*.py`).
- **Dernière baseline de régression vérifiée** (citée, non ré-exécutée dans ce rapport) : `docs/reconciliation/RECONCILE_4_COMPARISON.md`, daté 2026-09-15 — **2701/2701 tests backend passants** (2650 pytest + 51 tests d'intégration contre un serveur MOCK_DB réel), **0 échec**, et **build frontend CRA (`yarn build`, `CI=true`) propre, 0 erreur/warning**.
- **31 fichiers de specs e2e Playwright** réels dans `frontend/e2e/` (voir remarque §1 sur le chiffre de "159 specs" cité par un document antérieur mais non retrouvé tel quel dans le repo actuel).

## 6. Inventaire de la documentation

**2125 fichiers `.md`** au total sous `docs/` (`find docs -name "*.md" | wc -l`). **25 répertoires** de premier niveau dans `docs/` (corpus par domaine : `agf, bci, ceo, cve, cvln_academy_master, cyb, fdc, fms, frk, gcf, gmd, grp, hos, kiltikonet_master_package, klt, kor, kor_op, kora_master_package, los, product, reconciliation, say, wal, xcv`), plus **101 fichiers `.md` à la racine** de `docs/`.

Comptes par catégorie (fichiers à la racine `docs/`, par préfixe de nom) :

| Catégorie | Compte |
|---|---|
| `SPATIAL_*` | 26 |
| `ACA-*` / `ACADEMY_*` | 45 |
| `RAIL*` | 6 |
| `RECONCILE*` (dans `docs/reconciliation/`) | 6 |
| `*FUNNEL*` (W-FUNNEL) | 8 |

## 7. Lacunes connues / éléments explicitement non faits

Recherche réelle des marqueurs de gouvernance/blocage (pas d'invention) :

- **`NOT_AUTHORIZED`** : présent dans **34 fichiers** de `docs/`.
- **`BLOCKED_PRODUCT_DEPENDENCY`** : présent dans **93 fichiers** de `docs/`.
- **`REPLACE-BLOCKED`** : **10 fichiers**.
- **`TODO`** dans le code source (backend `.py` et frontend `.js`) : **0 occurrence** — le suivi des travaux différés se fait via les marqueurs de gouvernance documentaire ci-dessus, pas via des TODO de code.

**Lacunes précises citées avec leur source réelle :**

1. **Moteur spatial — intégration H1+ désactivée par défaut** : `SPATIAL_HUB_ENABLED`, `SPATIAL_CAMERA_INTENT`, `SPATIAL_MODULE_DEPTH`, `SPATIAL_HERO_ENTRY`, `SPATIAL_IDENTITY_ENTRY`, `SPATIAL_ONBOARDING_ENTRY` sont à `false` par défaut (`frontend/src/lib/featureFlags.js`). Le "handoff" caméra cross-route complet ("REVEALING") reste explicitement `NOT_AUTHORIZED` selon le docstring de `cameraFollow.js`.
2. **Paiements** : `backend/payments/provider.py`/`service.py` contiennent une intégration Stripe réelle (checkout sessions, vérification de signature webhook) mais elle lève une `ProviderNotConfiguredError` tant que `STRIPE_SECRET_KEY`/`STRIPE_WEBHOOK_SECRET` ne sont pas définis en environnement — code réel, non branché sur un compte de production sans ces identifiants.
3. **Intégrations écosystème** : `backend/services/integrations/registry.py` déclare explicitement chaque système du groupe (CVLN Intelligence OS, Brain, Command Center, Laurent.ia, KORA, Factory Maker Studio, Good Mood, Culture Connect, Kiltikonet) comme "**une interface découplée**" avec repli local — "Academy intègre avec Wallet, pas directement avec des PSP externes, pour que les rails de paiement restent centralisés et agnostiques au niveau groupe" (commentaire du fichier).
4. **FMS-01→06** (le canon original) reste **Founder-gated**, `NOT_AUTHORIZED` pour toute modification, `STOP_AFTER_DELIVERY=TRUE` (`docs/fms/README.md`).
5. **KLT-06→08** : 4 compétences classées `BUILT_UNCONNECTED` — contenu réel construit sur le schéma vérifié de `Kiltikonet-Aout2026`, mais "aucune connexion live Academy↔Kiltikonet-Aout2026" (`docs/klt/README.md`).
6. **Registre de lacunes central** : `docs/cvln_academy_master/95_GAPS/GAP_REGISTER.md` documente par exemple que pour CVLN Hospitality, "HOS-31→50 non récupérés dans ce tour" (30 formations sur 50 récupérées) — explicitement marqué "ne pas inventer les 20 manquants".
