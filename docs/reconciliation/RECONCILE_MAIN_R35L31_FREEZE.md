# Gel & matrice de réconciliation — `main` ↔ `claude/cvln-academy-production-r35l31`

Branche de travail : `reconcile/canonical-main-r35l31-20260914`, créée depuis
`origin/main` sans rebase ni force-push. Aucune des deux branches sources
n'a été modifiée ou supprimée.

## 1. Gel (figé le 2026-09-14)

| | SHA |
|---|---|
| `origin/main` | `c5dddc83ee09a6ec6fb8fd5e9cfda1ec917ac048` |
| `origin/claude/cvln-academy-production-r35l31` | `f9763b6e27b7f60f29577a4a26bac2710596dfc3` |
| merge-base | `85a41cced8d84c8bba016135689e10d733c585dd` |

| Comptage | Valeur |
|---|---|
| Commits uniques à `main` (absents de r35l31) | 470 |
| Commits uniques à r35l31 (absents de `main`) | 690 |
| Fichiers présents sur `main`, absents de r35l31 (`ONLY_MAIN`) | 196 |
| Fichiers présents sur r35l31, absents de `main` (`ONLY_R35L31`) | 2380 |
| Fichiers présents des deux côtés, contenu différent (`BOTH_DIFFERENT`) | 95 |
| Fichiers identiques des deux côtés | 232 |
| **Total fichiers sur `main` aujourd'hui** | **523** |

Listes exactes (chemin par ligne) : `only_main.txt`, `only_r35l31.txt`,
`both_different.txt` dans ce même dossier — générées par
`git diff --name-status origin/main origin/claude/cvln-academy-production-r35l31`,
sans aucune interprétation.

## 2. Domaines P0 confirmés par le Founder (2026-09-14, après revue de la matrice)

Les trois domaines backend découverts en §2bis sont **officiellement promus
au même rang P0 que FRK/KORA/Kiltikonet/etc.** Ils ne sont plus comptés
dans `APP_CORE` ni `OTHER` — la classification par domaine
(`domain_classification.json`, `*_by_domain.tsv`) les isolait déjà
correctement ; c'est la présentation en §3 qui est mise à jour pour les
sortir explicitement du reste :

1. **LEGAL_PRIVACY_GOVERNANCE_SECURITY** — `legal_*`, `privacy_*`,
   `governance_*`, `risk_*`, `security_*`, `quality_*`, conformité
   réglementaire, et les routes API associées.
2. **ECOSYSTEM_PROFESSIONAL_ACCOUNTING** — comptabilité, profils
   professionnels, gouvernance professionnelle, ecosystem builder, accès
   expert, validations expert, et la logique métier associée.
3. **COMMERCE_PAYMENTS** — `backend/payments/*`, `backend/commerce/*`,
   services/schémas/routes associés.

## 2bis. Découverte qui élargit le périmètre initial

Le plan de domaines demandé (FRK, KORA, Kiltikonet, GMD, CVE, AGF, Wallet,
FMS, canonical backends, master packages, frontend/spatial, auth, mobile,
infra/deploy, tests, docs/config) couvre bien la majorité des 2380 fichiers
`ONLY_R35L31` — mais l'analyse fait apparaître **trois domaines backend non
prévus au départ**, non négligeables :

- **LEGAL_PRIVACY_GOVERNANCE_SECURITY** (117 fichiers `ONLY_R35L31`) —
  `backend/services/legal_*`, `privacy_*`, `governance_*`, `risk_*`,
  `security_*`, `quality_*`, `regulatory_applicability.py`,
  `retention_executor.py`, `threat_model.py`, `evidence_graph.py`,
  `trust_signature.py`, `production_gates.py`, etc. + les routes API
  correspondantes (`backend/api/legal_*`, `privacy_*`, `governance_*`...).
- **ECOSYSTEM_PROFESSIONAL_ACCOUNTING** (30 fichiers) —
  `accounting_core/advanced/mappings/protocols/workspace.py`,
  `professional_profile/governance/workspace.py`,
  `ecosystem_builder.py`, `expert_access.py`, `expert_cost_ledger.py`,
  `external_expert_actions.py/validations.py`.
- **COMMERCE_PAYMENTS** (9 fichiers) — `backend/payments/*`,
  `backend/commerce/*`, `backend/api/payments.py`, `backend/api/commerce.py`.

Ces trois domaines représentent **~156 fichiers backend de logique métier
réelle** (pas de la doc) totalement absents de `main` — un chantier
substantiel en plus de la doc/corpus. Je les ajoute à la matrice ci-dessous
plutôt que de les faire disparaître dans un fourre-tout "APP_CORE".

## 3. Matrice de réconciliation par domaine

Statut : `ONLY_R35L31` (à importer, aucun conflit détecté), `ONLY_MAIN`
(déjà présent, rien à faire), `BOTH_DIFFERENT` (nécessite une vraie
réconciliation sémantique — voir §4), `NEEDS_REVIEW` (domaine mixte, à
traiter fichier par fichier).

| Domaine | ONLY_R35L31 | ONLY_MAIN | BOTH_DIFFERENT | Statut dominant |
|---|---:|---:|---:|---|
| FRK | 535 | 0 | 0 | ONLY_R35L31 — import direct |
| KORA | 480 | 0 | 0 | ONLY_R35L31 — import direct |
| KILTIKONET | 289 | 0 | 0 | ONLY_R35L31 — import direct |
| GMD | 152 | 0 | 0 | ONLY_R35L31 — import direct |
| CVE | 139 | 0 | 0 | ONLY_R35L31 — import direct |
| LEGAL_PRIVACY_GOVERNANCE_SECURITY | 117 | 1 | 1 | NEEDS_REVIEW (99% import direct + 2 fichiers à vérifier) |
| AGF | 105 | 0 | 0 | ONLY_R35L31 — import direct |
| WALLET | 99 | 0 | 5 | NEEDS_REVIEW — corpus + code wallet modifié des 2 côtés |
| FMS | 94 | 0 | 1 | NEEDS_REVIEW (quasi tout import direct + 1 fichier) |
| TESTS (génériques hors domaine) | 46 | 24 | 5 | NEEDS_REVIEW |
| MASTER_PACKAGES | 36 | 0 | 0 | ONLY_R35L31 — import direct |
| ECOSYSTEM_PROFESSIONAL_ACCOUNTING | 30 | 1 | 0 | ONLY_R35L31 (quasi total) |
| CANONICAL_BACKENDS | 15 | 0 | 0 | ONLY_R35L31 — import direct, **puis vérif intégration (§5)** |
| COMMERCE_PAYMENTS | 9 | 0 | 0 | ONLY_R35L31 — import direct |
| DOCS_CONFIG | 165 | 11 | 10 | NEEDS_REVIEW |
| FRONTEND_SPATIAL | 8 | 88 | 10 | NEEDS_REVIEW — main a nettement évolué ici depuis la divergence |
| APP_CORE (reste non classé) | 48 | 52 | 58 | NEEDS_REVIEW — noyau applicatif, réconciliation la plus sensible |
| AUTH | 6 | 5 | 5 | NEEDS_REVIEW |
| INFRA_DEPLOY | 2 | 11 | 0 | ONLY_MAIN essentiellement — vérifier les 2 fichiers r35l31 |
| MOBILE | 1 | 1 | 0 | NEEDS_REVIEW (petit volume) |
| OTHER_CORPUS (say/grp/fdc/bci/los/cyb/kor_op/hos/xcv/gcf) | — | — | — | ONLY_R35L31 — import direct |
| OTHER | 0 | 2 | 0 | ONLY_MAIN |

**Lecture** : les 9 domaines "import direct" (FRK, KORA, KILTIKONET, GMD,
CVE, AGF, MASTER_PACKAGES, COMMERCE_PAYMENTS, OTHER_CORPUS + la quasi-
totalité de LEGAL_PRIVACY_GOVERNANCE_SECURITY/ECOSYSTEM_PROFESSIONAL_
ACCOUNTING/CANONICAL_BACKENDS/FMS) représentent environ **2000 des 2380
fichiers `ONLY_R35L31`** et zéro conflit avec `main` — c'est le plus gros
volume et le plus sûr, aucune réconciliation sémantique requise, juste un
import propre + vérification d'intégration (imports/routes/tests) pour les
backends canoniques.

Les domaines `NEEDS_REVIEW` (APP_CORE, FRONTEND_SPATIAL, AUTH, WALLET,
DOCS_CONFIG, MOBILE, TESTS, FMS, LEGAL_PRIVACY_GOVERNANCE_SECURITY pour
leurs 2 fichiers en commun) concentrent la totalité des 95 fichiers
`BOTH_DIFFERENT` — c'est là qu'est le vrai risque de perte ou de
régression, et où aucune fusion automatique ne sera appliquée.

## 4. Règle de réconciliation sémantique (§4 de la commande)

Pour chaque fichier `BOTH_DIFFERENT`, la méthode appliquée sera : lire la
version au merge-base, lire la version `main`, lire la version r35l31,
identifier précisément ce que chaque côté a changé depuis la base, puis
écrire une version qui conserve les deux apports (ou justifier par écrit
pourquoi l'un est obsolète). Jamais `git checkout --ours/--theirs` ni un
remplacement de dossier entier sans revue ligne par ligne pour ces 95
fichiers.

## 5. Vérification d'intégration pour les backends `*_canonical`

Pour `backend/klt_canonical`, `kor_canonical`, `frk_canonical`,
`fms_canonical`, `master_canonical`, `canonical_common`, `qualification` :
après import, vérifier explicitement — imports Python, enregistrement du
router dans `backend/api/__init__.py`, routes exposées, modèles/schémas,
services appelants, dépendances (`requirements.txt`), seed/migrations,
tests dédiés, appels frontend correspondants, variables d'environnement.
Rien n'est considéré "importé" tant que cette checklist n'est pas validée
par un test réel (pas juste `import` propre).

## Prochaine étape

Import des domaines "import direct" en commits atomiques par domaine,
en commençant par les plus volumineux (FRK, KORA, KILTIKONET), avec test/
build après chaque lot — sous réserve de confirmation de cette matrice,
vu que le périmètre s'est élargi de 3 domaines backend non prévus au départ.
