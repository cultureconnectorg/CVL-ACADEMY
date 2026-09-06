# CVLN Academy Master — Reconciliation Matrix

```
SOURCE: CVLN_Academy_Cartographie_2D_Master.xlsx (812 rows, sheet
Master_Catalogue = External_Market + Internal_CVLN + Cross_Ecosystem).
Raw CSVs preserved verbatim in 10_PORTFOLIO/raw/ — nothing lost.
STATUS_OF_SOURCE: 781/812 CANDIDATE, 30/812 PARTIAL_RETRIEVAL
(CVLN Hospitality), 1/812 REQUIRES_RECONCILIATION.
```

Per rule §27 (Founder): every row keeps its provenance. This matrix
reconciles at the **domain** level (27 domains) against verified repo
truth — it does not re-litigate individual rows, which stay exactly as
delivered in `raw/Master_Catalogue.csv`.

| Domaine | Lignes | SOURCE | CONFIDENCE | VERIFICATION | Repo truth vérifié |
|---|---|---|---|---|---|
| FREK | 75 (FRK-01→75) | PROPOSED (candidate map, per Founder §6) | MEDIUM | **RECONCILED** (`20_EXTERNAL/FREK_01_75_RECONCILIATION.md`) | Deep audit of the sole real implementation, `backend/services/frek_core.py` (142 lines: `mint_frek_id`, `emit_signal` on 8 signal types, `issue_proof` — **UUID stub, no real cryptography** —, `resolve_stade`). Two-dimension reconciliation of all 75 candidates: 0 rejected, 51 `NEW_EXTERNAL`, 12 `NEW_INTERNAL`, 5 `NEW_CROSS_ECOSYSTEM` (FRK-56→60), 1 `SPECIALIZE_EXISTING`, 3 `EXTEND_EXISTING` (reuse `00_GOVERNANCE/AUTHORIZATION_MODEL.md` + KOR-11's governance disambiguation), 6 `NEEDS_FOUNDER_DECISION` (FREK-security vs CVLN CyberSecure boundary). Majority of the domain (`.fk` format, FREKANSLA, notary, watchdog, production ops, v3 architecture) stays `BLOCKED_PRODUCT_DEPENDENCY` — no separate FREKCORE repo was named/found this session. Best-grounded candidate: FRK-58 (FREK × Academy) — this IS `frek_core.py`, already documented across every `docs/kor/korXX/` module. |
| KORA | 19 | ACADEMY_EXISTING + PROPOSED | HIGH | NEEDS_REPO_AUDIT→partially VERIFIED | KOR-01→15 marché déjà construit (`docs/kor/`, hors périmètre de cette cartographie). KOR-OP-01→12 (interne) et KOR-X-01→07 (cross) : **zéro footprint** dans CVL-ACADEMY sauf Wallet/JCC (`KOR-OP-08` recoupe `KOR10.SKILL.C08`). |
| CVLN Wallet | 28 | REPO_OBSERVED (partial) | MEDIUM | PARTIAL | `backend/wallet/` réel mais **simple** (ledger append-only, `jcc_balance`/`token_balance`/badges) — ne couvre PAS holds, double-entry complet, cartes, marketplace/escrow, FinOps décrits par WAL-01→18. WAL-19→28 (interne) largement `CAPABILITY_NOT_IMPLEMENTED` au-delà du ledger de base. |
| FMS | 12 (FMS-07→18) | REPO_OBSERVED + ACADEMY_EXISTING | HIGH | **RECONCILED v2** (`20_EXTERNAL/FMS_07_18_RECONCILIATION.md`) | `fms-os/fms` (repo réel, cloné) grounds FMS-07/15/18. Cross-checked against the real canonical FMS-01→06 corpus (95 modules) on **two dimensions** (curriculum coverage × occupational distinctness — `CONTENT_OVERLAP != PROFESSIONAL_DUPLICATE`): none of the 12 rejected. FMS-08/09 (Recording, Mixing/Mastering) = real distinct professions with complete/substantial existing coverage → specialization tracks anchored on FMS-03, not new formations. FMS-14/16 → merged as blocks into FMS-07. FMS-17 → merged into FMS-18. FMS-11 → hybrid path reusing FMS-04 by reference. Net: **9 formations/paths** for 12 candidates, zero true duplicates. |
| LabelOS | 37 | PROPOSED | LOW | NEEDS_REPO_AUDIT | Aucun repo LabelOS accessible ni cité avec une URL dans le message Founder. Mentionné uniquement comme pôle nommé dans `seed_data.py`/`seed_modules.py`/`catalog_cartography.py`/`external_calibration.py`/`agent_factory.py` (concept, pas implémentation). `CAPABILITY_NOT_IMPLEMENTED` pour l'ensemble LOS-01→14/LOS-OP-01→15/LOS-X-01→08. |
| CVE | 15 | PROPOSED | LOW | NEEDS_REPO_AUDIT | **Zéro footprint** — confirmé déjà par le corpus KOR-10 (`EXTERNAL_PRODUCT_EVIDENCE_NOT_AUDITED`). Aucune mention CVE dans `registry.py` ni ailleurs. |
| Wallet/CVE (cross) | 9 | PROPOSED | LOW | BLOCKED_DEPENDENCY | Dépend de CVE (inexistant) et d'un Wallet plus riche que l'actuel — bloqué tant que les deux briques ne sont pas clarifiées. |
| Agent Factory | 25 | REPO_OBSERVED (partial) | MEDIUM | PARTIAL | `backend/services/agent_factory.py` réel, mais **un seul client généraliste** — ne couvre pas à ce jour le detachment/mission-scope/escalation détaillés en §11. |
| Agent Factory / Laurentia | 9 | PROPOSED | LOW | NEEDS_REPO_AUDIT | Laurentia non trouvée dans CVL-ACADEMY (`registry.py` la déclare comme `EcosystemIntegration("Laurent.ia", "LAURENTIA")`, générique, aucune logique propre). |
| Laurentia | 10 | PROPOSED | LOW | NEEDS_REPO_AUDIT | Idem — stub générique seulement. |
| Intelligence OS | 25 | REPO_OBSERVED (stub) | LOW | PARTIAL | `registry.py`: `EcosystemIntegration("CVLN Intelligence OS", ...)` — interface décorrélée, aucune logique de raisonnement/routage réelle. |
| CVLN Brain | 15 | REPO_OBSERVED (partial) | MEDIUM | VERIFIED (narrow) | Réel et vérifié pour **un seul usage** : l'événement `academy.certification.passed` (`backend/certification/service.py:140`, `backend/services/events.py`, `backend/services/integrations/subscribers.py`) posté vers `/academy/certification-passed` sur l'intégration générique Brain. Aucune capacité de raisonnement/recommandation réelle au-delà. |
| Command Center | 15 | REPO_OBSERVED (stub) | LOW | PARTIAL | `registry.py` stub générique seulement ; `fms-os/fms` a par ailleurs sa **propre** route `/os/command-center` (produit FMS, pas CVLN Command Center central — à ne pas confondre, `CROSS_DOMAIN_CONTAMINATION` évitée). |
| Intelligent Operations | 10 | PROPOSED | LOW | NEEDS_REPO_AUDIT | Pipeline conceptuel (`Missions_Pipelines` sheet) — aucune implémentation. |
| Kiltikonet | 12 (KLT-09→20) | ACADEMY_EXISTING + PROPOSED | HIGH | NEEDS_FOUNDER_DECISION | KLT-01→08 déjà construits (`docs/klt/`, hors périmètre de cette cartographie). KLT-09→20 candidats : aucun repo Kiltikonet distinct identifié/cité avec URL — `CAPABILITY_NOT_IMPLEMENTED`, en attente d'un repo réel ou d'une décision Founder. |
| Good Mood | 43 | REPO_OBSERVED | HIGH | VERIFIED | `gmfest972/goodmooddjsayd` (repo réel, cloné). Confirme : catalogue, events, ticket types, tickets+QR, door-scan (`/scan/check`, `/scan/counter/{eid}`), fans/newsletter, merch, orders, Stripe (`/payments/checkout`, `/stripe/webhook`), **FREK-ID outbox réel** (`frek_service.py`, retry loop, `db.frek_id_outbox`) et **Wallet outbox réel** (`wallet_service.py`, `db.wallet_outbox`) — les deux `NOT_CONNECTED` par défaut (`FREK_ID_URL`/`WALLET_URL` vides). |
| DJ Sayd | 51 | REPO_OBSERVED | HIGH | REQUIRES_RECONCILIATION | **Même repo** que Good Mood (`gmfest972/goodmooddjsayd` — "sayd" apparaît dans `email_service.py`, `server.py`, `i18n.js`, `Landing.jsx`). La cartographie traite "Good Mood" et "DJ Sayd" comme deux domaines séparés (94 lignes à eux deux) alors qu'un seul produit réel existe. **Action requise avant tout référentiel** : fusionner ou clarifier la frontière marque/produit (DJ Sayd = artiste/marque ; Good Mood = plateforme événementielle) sans dupliquer les compétences opérateur. |
| CVLN CyberSecure | 42 | PROPOSED | LOW | NEEDS_REPO_AUDIT | Aucun module de sécurité applicative dédié observé dans CVL-ACADEMY, fms-os/fms, ou goodmooddjsayd au-delà de l'auth JWT standard. `CAPABILITY_NOT_IMPLEMENTED`. |
| Blockchain Innovations | 40 | PROPOSED | LOW | NEEDS_REPO_AUDIT | Aucun repo blockchain cité ni trouvé. `CAPABILITY_NOT_IMPLEMENTED`. |
| Blockchain / Tokenomics | 11 | PROPOSED | LOW | NEEDS_REPO_AUDIT | Idem. |
| Tokenomics | 15 | PROPOSED | LOW | NEEDS_REPO_AUDIT | Idem — à ne jamais fusionner avec CVE ni Wallet (règle §16). |
| Gala Cook & Food | 38 | PROPOSED | LOW | NEEDS_FOUNDER_DECISION | Aucun repo identifié. Domaine métier autonome (restauration/événementiel culinaire) — aucun chevauchement évident avec un repo déjà audité. |
| CVLN Hospitality | 31 | PARTIAL_RETRIEVAL | LOW | NEEDS_FOUNDER_DECISION | La cartographie elle-même déclare (`Coverage_Gaps`) que la version précédente comptait 50 formations dont seules 30 ont été récupérées précisément — **20 titres manquants non inventés ici**, conformément à la règle explicite de la source. |
| Founder / CEO | 12 | PROPOSED | LOW | NEEDS_FOUNDER_DECISION | Par nature `EXECUTIVE_ONLY` — contenu à valider exclusivement par le Founder lui-même, jamais construit par supposition. |
| CVLN Group | 72 | PROPOSED | LOW | NEEDS_EXPERT_REVIEW | Holding/legal/fiscal — la cartographie exige elle-même une revue experte par juridiction (`Coverage_Gaps` ligne 7). Aucun contenu juridique/fiscal universel ne sera rédigé sans cette revue. |
| Fondation Cœurvolan | 74 | PROPOSED | LOW | NEEDS_EXPERT_REVIEW | Patrimoine/mémoire/transmission — doctrine "Collecter sans déposséder" (§18) à valider avec des porteurs de mémoire réels avant tout référentiel. |
| Cross-CVLN | 67 | PROPOSED | LOW | NEEDS_REPO_AUDIT (partial) | Couche transversale (XCV) — pipelines déjà repris dans `Missions_Pipelines` (10 lignes, voir `80_MISSIONS/`). Ne doit jamais dupliquer un enseignement vertical (règle §19). |

## Lecture agrégée

- **Domaines avec repo réel vérifié et substantiel** : KORA (Wallet/JCC),
  Wallet, FMS (`fms-os/fms`), Good Mood/DJ Sayd (`goodmooddjsayd`),
  Agent Factory (partiel), CVLN Brain (usage étroit réel).
- **Domaines stub générique seulement** (interface découplée, zéro
  logique propre) : Intelligence OS, Command Center, Laurentia.
- **Domaines sans aucun ancrage repo** : LabelOS, CVE, CyberSecure,
  Blockchain (tous), Tokenomics, Gala Cook & Food, CVLN Hospitality
  (partiellement rappatriée), Founder/CEO, CVLN Group, Fondation
  Cœurvolan, Kiltikonet KLT-09→20.
- **Conflit de duplication détecté** : Good Mood / DJ Sayd (même repo,
  deux domaines dans la cartographie — `GAP_REGISTER.md`).

Aucune ligne candidate ci-dessus n'est promue `VERIFIED`/`DECIDED` par
ce document seul — chaque verdict `VERIFICATION` reste tel quel jusqu'à
un ticket W1-W5 dédié par domaine.
