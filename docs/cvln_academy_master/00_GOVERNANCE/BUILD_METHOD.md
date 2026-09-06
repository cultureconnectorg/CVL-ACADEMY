# CVLN Academy Master — Build Method (W0→W17)

```
SOURCE: mission directive §22 (Founder). STATUS: DECIDED (process),
applied per-domain in 95_GAPS/REPO_TRUTH_AUDIT.md and per-domain folders.
```

| Phase | Contenu | Statut à date de ce document |
|---|---|---|
| W0 | Audit repo + cartographie | **DONE** pour le tronc commun (voir `99_REPORTS/W0_AUDIT_REPORT.md`) ; repos externes vérifiés : `fms-os/fms`, `gmfest972/goodmooddjsayd` |
| W1 | Capability map | **PARTIAL** — dérivée du repo truth pour KORA/Wallet/FREK/FMS/GoodMood ; en attente pour les domaines sans aucun repo (CyberSecure, Blockchain, Group, Fondation, Hospitality) |
| W2 | Role map | **PARTIAL** — `Operator_Roles` (130 lignes candidates) indexé, non validé rôle par rôle |
| W3 | Boundary map | **PARTIAL** — tensions connues reportées (`CVLN_BOUNDARY` héritées de KOR-0002/KLT-0002 + nouvelles, voir `60_CROSS_ECOSYSTEM/`) |
| W4 | Competency map | **NOT_STARTED** à l'échelle des 812 lignes — fait uniquement pour KOR-01→15 (corpus déjà livré, `docs/kor/`) |
| W5 | Canonical freeze | **NOT_STARTED** — aucune ligne candidate de cette cartographie n'est encore gelée |
| W6-W11 | Référentiel → Certification | **NOT_STARTED** pour les domaines candidats de cette cartographie (KOR-01→15 et KLT-01→08/FMS-01→06 restent les seuls corpus canoniques livrés, antérieurs à cette cartographie) |
| W12-W13 | Rôle interne / habilitation | **PARTIAL** — registres proposés (`40_OPERATOR_ROLES/`, `50_AUTHORIZATIONS/`), aucune instance canonique |
| W14 | Cross-ecosystem map | **PARTIAL** — `60_CROSS_ECOSYSTEM/` indexe les 153 lignes candidates + 10 pipelines |
| W15 | Quality gates | **DONE** pour la méthode (`QUALITY_GATES.md`), **PARTIAL** pour l'application (corpus KOR/KLT/FMS déjà couverts, cartographie candidate non encore auditée ligne à ligne) |
| W16 | Master Package | **CE DOSSIER** (`docs/cvln_academy_master/`) |
| W17 | Runtime integration | **NOT_STARTED** — `NO_RUNTIME_BINDING` tant que W6-W11 ne sont pas faits domaine par domaine |

## Discipline

`CONTINUOUS_PORTFOLIO_BUILD = TRUE` — ce Master Package ne s'arrête pas
après l'audit ; il établit le socle (W0-W5, W12-W16 partiels) sur
lequel les prochaines vagues W6-W11 par domaine s'appuient, en
commençant par les domaines à ancrage repo réel le plus fort
(KORA-internal, Wallet-internal, FMS-07→18, LabelOS, Good Mood/DJ Sayd)
avant les domaines sans aucun ancrage (Fondation, CVLN Group, Blockchain,
Hospitality) qui nécessitent une décision Founder ou une revue experte
avant tout référentiel (voir `95_GAPS/GAP_REGISTER.md`).
