# Kiltikonet Certification Architecture

```
Six concepts distincts. Aucun badge legacy ne devient automatiquement
une certification. Aucune certification Academy n'est présentée comme
RNCP/État.
```

## Les six concepts

| # | Concept | Définition | Statut réel dans KLT-01→05 |
|---|---|---|---|
| 1 | `COURSE_COMPLETION` | Avoir suivi les modules d'une formation | Implicite — suivre `M01`→`Mxx` d'une formation, non tracé formellement aujourd'hui |
| 2 | `SKILL_VALIDATION` | Une compétence individuelle démontrée à un module donné (N1/N2) | Réel, granulaire — chaque module a ses `PASS_CRITERIA` propres |
| 3 | `ACADEMY_CERTIFICATION` | La réussite de l'assessment terminal (`KLTxx-A01`) + `RUBRIC.md` | **Réelle** — c'est ce que chaque `CERTIFICATION_MODEL.md` local délivre |
| 4 | `BADGE` | `Formation.badge_name` — un champ d'affichage sur la fiche formation | **`DISPLAY_ONLY_LEGACY` partout** — jamais réellement délivré (`badges_engine.py` fonctionne par seuil CC, pas par `badge_name`, découverte `KLT-0002`) |
| 5 | `OPERATOR_AUTHORIZATION` | Un accès opérationnel réel à un système Kiltikonet | **`NOT_IMPLEMENTED / NOT_GRANTED` partout**, particulièrement `KLT-05` — voir `OPERATOR_AUTHORIZATION_ARCHITECTURE.md` |
| 6 | `RNCP_OR_STATE_CERTIFICATION` | Une certification enregistrée au Répertoire National / reconnaissance d'État | **Inexistante pour toute formation KLT** — la seule référence RNCP présente dans le corpus (`external_calibration.py`, `CERT_PROJECT_CULTURE`) est une donnée de calibration marché, jamais une certification obtenue |

## Table de correspondance par formation

| KLT | `ACADEMY_CERTIFICATION` | `BADGE` (`DISPLAY_ONLY_LEGACY`) | `RNCP_OR_STATE` | `OPERATOR_AUTHORIZATION` |
|---|---|---|---|---|
| `KLT-01` | `KLT01-A01` | `Kiltikonet Ambassador` | Non | N/A (métier non concerné) |
| `KLT-02` | `KLT02-A01` | `Cultural Project Manager` | Non | N/A |
| `KLT-03` | `KLT03-A01` | `Institutional Strategist` | Non | N/A |
| `KLT-04` | `KLT04-A01` | `Governance Associative` | Non (confiance calibration `low`) | N/A |
| `KLT-05` | `KLT05-A01` | `Kiltikonet Platform Operator` | Non | `NOT_IMPLEMENTED/NOT_GRANTED` — **explicitement concerné**, discipline renforcée |

## Pourquoi ces six concepts ne doivent jamais fusionner

L'erreur la plus dangereuse identifiée dans ce corpus (`KLT-0002`,
découverte cross-cutting) est que `BADGE` (concept 4) porte un nom qui
ressemble à une vraie reconnaissance ("Institutional Strategist",
"Platform Operator") alors qu'il n'est câblé à rien de réel. Sans cette
architecture à six niveaux, un lecteur pressé pourrait confondre :
- `ACADEMY_CERTIFICATION` (réelle, 3) avec `RNCP_OR_STATE_CERTIFICATION`
  (inexistante, 6) — erreur traitée dans chaque `CERTIFICATION_MODEL.md`
  local.
- `BADGE` (affichage, 4) avec `ACADEMY_CERTIFICATION` (réelle, 3) —
  erreur explicitement interdite (`NO_BADGE_REASSIGNMENT`, tous les
  tickets `KLT-0003`+).
- `ACADEMY_CERTIFICATION` (évaluation pédagogique, 3) avec
  `OPERATOR_AUTHORIZATION` (accès système, 5) — l'erreur la plus grave,
  spécifique à `KLT-05` (voir document dédié).

## Ce que ce document ne fait pas

Ne crée aucun mécanisme de délivrance réel pour aucun des six concepts.
Consolide ce que les 5 `CERTIFICATION_MODEL.md` locaux affirment déjà,
sans en modifier le contenu.
