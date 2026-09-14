# KORA Master Package — CVLN Boundary Map

Toutes les tensions de frontière posées à travers le corpus KOR-01→15
(numérotation reprise de `KOR-0002` §4, plus les tensions inter-pôles
CVLN découvertes en cours de construction).

## Tensions intra-KOR (KOR-0002 §4)

| # | Frontière | Résolution |
|---|---|---|
| #1 | `KOR-01`/`KOR-03` (audio vs vidéo) | Résolu — montage arbitré en KOR-03/M03,M07, écho KOR-01/M06 |
| #2 | `KOR-06`/`KOR-14` (exploitation vs expérience) | Résolu — même système Anba Tonèl Host, disponibilité vs ergonomie |
| #3 | `KOR-07`/`KOR-13` (droits vs partenariats) | Résolu — clauses de droits toujours renvoyées à KOR-07 |
| #5 | `KOR-09`/`KOR-14` (acquisition vs in-app) | Résolu — frontière canal/première session |
| #6 | `KOR-07`/`KOR-10` (royalties vs monétisation) | Posé, géré par renvoi mutuel — pas de chevauchement de contenu |
| #7 | `KOR-05`/`KOR-13` (onboarding vs sourcing) | Résolu — handoff explicite KOR-13/C6 → KOR-05 |
| #8 | `KOR-04`/`KOR-02` (curation vs création) | Résolu — étapes différentes de la chaîne éditoriale |
| #9 | `KOR-07`/`KOR-15` (droits vs déploiement international) | Résolu — handoff systématique, litige jamais tranché par KOR-15 |
| #10 | `KOR-08`/LabelOS | Résolu — "règle d'application KORA", LabelOS garde la profondeur |
| #13 | Gouvernance éditoriale vs gouvernance FREK | Résolu — disambiguïsation explicite KOR-11/M01 |

## Tensions inter-pôles CVLN découvertes en construction

| Pôle CVLN | Formation KOR concernée | Statut |
|---|---|---|
| Wallet/JCC (réel) | `KOR-10`/C8 | `CAPABILITY_ALREADY_REAL` — seule capacité réelle du corpus |
| LabelOS (réel, pôle `LOS-02`) | `KOR-08` | `CAPABILITY_NOT_CONNECTED` — handoff documenté, jamais dupliqué |
| CVLN Brain (réel, `registry.py`, `academy.certification.passed`) | `KOR-12` | `CAPABILITY_NOT_CONNECTED` — Brain sert la certification Academy, pas la recommandation KORA |
| FREK (réel, `services/frek_core.py`) | Toutes (Evidence Models) | `KORA_CURRENT_CAPABILITY` limité à Academy — jamais un `FREK_PROOF` réel côté KORA |
| Kiltikonet `KLT-07` (réel, réseau d'opérateurs territoriaux) | `KOR-15` | Vérifié **non dupliqué** — objets et mandats différents (réseau associatif interne vs distribution produit externe) |

## Litiges volontairement non résolus (jamais tranchés par supposition)

- Chant traditionnel sans attribution claire (`KOR-07`, repris en
  `KOR-11`/M12 et `KOR-15`/M05,M10) — **toujours ouvert** à la fin du
  corpus. `NEEDS_EXPERT_REVIEW = TRUE`.

`UNRESOLVED_CRITICAL_BOUNDARY = 0` bloquant à l'échelle du corpus — le
litige de droits ci-dessus est documenté et géré (jamais ignoré),
distinct d'une frontière non posée.
