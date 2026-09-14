# CVE — Cultural Value Engine Internal Formation Corpus (CVE-01 → CVE-15)

```
WORKSTREAM = CVE (KORA Cultural Value Engine methodology), W6 Wave 3
of the CVLN Academy Master 2D reconciliation (docs/cvln_academy_master/).
SOURCE OF TRUTH (repo-verified this session): kora2024/Kora-app/memory/
KORA_CVE_Specification_Mathematique_v1.0.md ("Formal Reference
Document, Frozen on Theory v1.4", CVLN Group / Tech & Data Pole) —
this corpus teaches exactly what that document formalizes, per
Founder decision FD-CVE-001. GUARD: never conflate with
Cvln-ios-v.1/economics/CVE-v1.2.md ("CVLN Value Engine" — a distinct
system, see WALLET_CVE_RECONCILIATION.md's naming-collision guard).
STATUT (deepené 2026-09-08) = 15/15 formations à package canonique
complet (CVE-01→15, niveau KOR/KLT/GMD/WAL) — **le corpus CVE entier
est désormais au niveau package complet**, grâce à un re-lecture
directe de la spécification intégrale cette session
(kora2024/kora-app/memory/, 161 lignes, §0→§6). CVE-06 (Shapley) et
CVE-08 (VCF) restent explicitement `FORMALIZATION_PENDING` pour leur
contenu KORA-spécifique — jamais comblé par une formule inventée, la
discipline `FORMALIZATION_PENDING` est préservée à travers
l'approfondissement, pas levée. Aucune formation n'est
BLOCKED_PRODUCT_DEPENDENCY : contrairement à Good Mood/Wallet, le
"produit" ici est la spécification mathématique elle-même
(FORMALIZED_METHODOLOGY/SOURCE_OBSERVED), pas un runtime — donc
chaque formation a un ancrage réel disponible, à des degrés de
formalisation différents.
```

## Pourquoi ce corpus existe

`WALLET_CVE_RECONCILIATION.md` a fermé `FD-CVE-001` : la méthodologie
CVE existe réellement, formalisée dans un document mathématique
rigoureux et vérifiable, cité en entier ci-dessous. Les 15 candidats
CVE-01→15 (source : `10_PORTFOLIO/raw/Internal_CVLN.csv`) sont tous
`SYSTEM_CVLN`/`INTERNAL` — ce corpus construit leur contenu
pédagogique en citant la spécification section par section, jamais en
inventant une formule ou un mécanisme que la spécification ne
contient pas.

## Discipline spécifique à ce corpus (au-delà de la discipline standard)

Cette spécification déclare elle-même : *"This document introduces no
new concepts. It consolidates in unique notation everything
established between CVE versions v1.0 and v1.4. This is chantier 1 of
the proof roadmap — a prerequisite for simulation (chantier 2) and
prototyping (chantier 3)."* Deux conséquences pédagogiques directes :

1. **Chantier 1 = spécification formelle, chantier 2 = simulation
   (non encore faite), chantier 3 = prototypage (non encore fait).**
   CVE-13 (Simulation & Scenario Analysis) enseigne donc **comment**
   la simulation serait conduite et **quels paramètres restent à
   calibrer** — jamais un résultat de simulation qui n'a pas eu lieu.
2. **Deux noms de formation (CVE-06 "Shapley Value for Cultural
   Contribution", CVE-08 "VCF — Value/Contribution Framework")
   promettent un contenu que la spécification frozen v1.0 ne
   formalise pas entièrement** — le mot "Shapley" n'apparaît nulle
   part dans le document réel, et VCF est utilisé (`VCF_i^{corrected}
   (t)`, `dVCF_i/dt`) sans qu'une équation de VCF y soit donnée. Ce
   n'est ni un rejet ni une invention : c'est un
   `CALIBRATION_PENDING`/`FORMALIZATION_PENDING` honnête, documenté
   dans chaque `REFERENTIAL.md` concerné, jamais comblé par une
   formule inventée.

## Ce que contient ce corpus

| Formation | Dossier | Section(s) réelle(s) de la spécification | Statut |
|---|---|---|---|
| CVE-01 — Cultural Value Economics Foundations | `cve01/` | §0 (conventions, H0), vue d'ensemble des 4 couches | `PACKAGE_COMPLETE_FOR_CVE01` |
| CVE-02 — Cultural Value Measurement | `cve02/` | §1 (Layer 1 — Trust Score, S/E/F/C/L) | `PACKAGE_COMPLETE_FOR_CVE02` |
| CVE-03 — Cultural Contribution & Attribution | `cve03/` | §1.2 (composante C — attribution de conversions, fenêtre 14j) | `PACKAGE_COMPLETE_FOR_CVE03` |
| CVE-04 — CES & Cultural Engagement Signals | `cve04/` | §3.1 (agrégation CES) | `PACKAGE_COMPLETE_FOR_CVE04` |
| CVE-05 — ρ / Cultural Relationship & Value Dynamics | `cve05/` | §3.1 (paramètre ρ_c, cas spéciaux : somme pondérée / Cobb-Douglas / Leontief) | `PACKAGE_COMPLETE_FOR_CVE05` |
| CVE-06 — Shapley Value for Cultural Contribution | `cve06/` | **Non formalisé dans le document réel** | `PACKAGE_COMPLETE_FOR_CVE06` (`FORMALIZATION_PENDING` explicite, préservé) |
| CVE-07 — Nebula Cultural Value Modeling | `cve07/` | §3.2 (Nebula Score, entropie, axes k) | `PACKAGE_COMPLETE_FOR_CVE07` |
| CVE-08 — VCF — Value/Contribution Framework | `cve08/` | Référencé (§3.3, §6) mais **non dérivé** dans ce document | `PACKAGE_COMPLETE_FOR_CVE08` (`FORMALIZATION_PENDING` explicite, préservé) |
| CVE-09 — UVC Allocation & Distribution | `cve09/` | §5 (Layer 4 — allocation UVC) | `PACKAGE_COMPLETE_FOR_CVE09` |
| CVE-10 — Cultural Revenue Allocation | `cve10/` | §5 (même base, angle "revenu distribuable" `MD_c`) | `PACKAGE_COMPLETE_FOR_CVE10` |
| CVE-11 — Creator & Contributor Economics | `cve11/` | §5 (angle créateur/contributeur de la même allocation) | `PACKAGE_COMPLETE_FOR_CVE11` |
| CVE-12 — Cultural Network Economics | `cve12/` | §3.2 (axes réseau : diaspora, collaboration, territoire) | `PACKAGE_COMPLETE_FOR_CVE12` |
| CVE-13 — CVE Simulation & Scenario Analysis | `cve13/` | Le document's propre feuille de route "chantier 2" — paramètres à calibrer (H1/H2/H3, ρ_c, N_min, τ_fraude) | `PACKAGE_COMPLETE_FOR_CVE13` |
| CVE-14 — CVE Data, Explainability & Audit | `cve14/` | H0 (principe de clôture), contrainte C6 (auditabilité) | `PACKAGE_COMPLETE_FOR_CVE14` |
| CVE-15 — CVE Governance & Economic Policy | `cve15/` | §6 (Loi Fondamentale, contraintes C1→C8, Protocole de Gouvernance) | `PACKAGE_COMPLETE_FOR_CVE15` |

## Doctrine partagée

- `CVE_CANONICAL_EDUCATION_MAP.md` — squelette de compétences partagé.
- `CERTIFICATION_MODEL.md` — un seul modèle de certification.
- `QUALITY_GATES.md` — un seul passage de gates.
- Chaque `REFERENTIAL.md` cite la spécification avec numéro de
  section précis — jamais une formule "probablement" dans le
  document.

## Ce que ce corpus NE fait PAS

Ne modifie aucun fichier de `kora2024/kora-app` (lecture seule).
N'invente aucune formule absente du document (Shapley value, VCF
explicite) — ces manques sont déclarés `FORMALIZATION_PENDING`,
jamais comblés, y compris après l'approfondissement complet de
CVE-06/CVE-08. Ne fusionne jamais ce CVE avec `Cvln-ios-v.1/
economics/CVE-v1.2.md` ("CVLN Value Engine", système distinct). Ne
prétend à aucune simulation ou prototype réel — la spécification
elle-même les situe dans des chantiers futurs non encore réalisés.
Aucune certification n'a été délivrée à un candidat réel —
`FULLY_COMPLETE = FALSE` pour l'ensemble du corpus, même à 15/15
`PACKAGE_COMPLETE`.

**Canonical state, full CVE domain (15 rows):** 15/15
`PACKAGE_COMPLETE` (CVE-01→15). This closes task #183 in full.
