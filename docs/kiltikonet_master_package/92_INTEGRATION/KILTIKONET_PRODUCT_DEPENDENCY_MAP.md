# Kiltikonet Product Dependency Map

```
Consolide les 59 champs KILTIKONET_DEPENDENCY réels des modules (recomptés
par grep, pas recopiés). NOT_FOUND_IN_ACADEMY != DOES_NOT_EXIST — rappelé
partout où c'est pertinent.
```

## Classification par domaine

| Domaine | Classification | Preuve | Modules concernés (comptés) |
|---|---|---|---|
| `ACADEMY` (ce repo) | `OBSERVED` | C'est le repo lui-même — réel par définition | Tous |
| `KILTIKONET PRODUCT` (Core platform, Culture Connect) | `INTEGRATION_CONTRACT` réel côté Academy (`services/integrations/registry.py:28-29`), `EXTERNAL_EVIDENCE_NOT_AUDITED` au-delà | 5 modules (`KLT-01`×2, `KLT-05`×3) |
| `NETWORK` (Network, Network RBAC, Territories/operators) | `NOT_CONNECTED` en Academy ; `EXTERNAL_EVIDENCE_NOT_AUDITED` pour le système Network réel | 5 modules (`KLT-01`, `KLT-03`, `KLT-04`×3) |
| `OBSERVATORY` | `NOT_CONNECTED` en Academy ; `EXTERNAL_EVIDENCE_NOT_AUDITED` au-delà | 4 modules (`KLT-01`, `KLT-02`, `KLT-03`, `KLT-05`) |
| `FREK` (`frek_signal`, `frek_core.py`) | `OBSERVED` — réel, en repo, utilisé par tous les modules terminaux | 1 mention explicite en dépendance directe (`KLT-01`/M10, agrégée) + `FREK_PROOF_MAPPING` réel dans les 59 modules |
| `IDENTITY` (Auth/RBAC) | `INTEGRATION_CONTRACT` réel, non configuré | 2 modules (`KLT-05`/M02, `KLT-04`/M09 via Network RBAC) |
| `BADGES` — deux réalités distinctes, jamais confondues | `db.badges`/`db.user_badges` = `OBSERVED` (réel, `badges_engine.py`) ; `Badges/NFC` (badge physique Kiltikonet) = `NOT_CONNECTED`, protocole simulé uniquement | `KLT-05`/M04 |
| `OPPORTUNITIES` (`network_opportunities`) | `NOT_CONNECTED` en Academy ; `EXTERNAL_EVIDENCE_NOT_AUDITED` au-delà | 1 module (`KLT-03`/M05) |
| `COMPLIANCE`/`AUDITS`/`GOUVERNANCE` (donnée structurée) | `NOT_IMPLEMENTED` comme donnée structurée en Academy — n'existe même pas comme shim, contrairement à `KILTIKONET PRODUCT` | 5 modules (`KLT-02`/M08, `KLT-03`/M07 implicite, `KLT-04`/M07-M08-M12-M13) |
| `PROGRAMMES/CMS` | `INTEGRATION_CONTRACT` non configuré | 2 modules (`KLT-02`/M01, `KLT-05`/M03) |
| `PRO/SUPPORT` | `NOT_CONNECTED` en Academy | 2 modules (`KLT-03`/M11, `KLT-05`/M07) |
| `ADMIN/ALERTS` | `NOT_CONNECTED` en Academy | 1 module (`KLT-05`/M10) |
| `LEGAL/IP` | **Hors périmètre Kiltikonet** — c'est une expertise externe (conseil juridique), pas un système CVLN. `PROPOSED` uniquement au sens "besoin identifié", jamais classé avec les dépendances produit | 1 module (`KLT-03`/M06) |
| Concepts sans système (`Terrain`, `Admin finance`, `Programmes` générique) | `N/A` — explicitement documentés comme "aucun système requis" | 5 modules |

## Discipline rappelée : `NOT_FOUND_IN_ACADEMY != DOES_NOT_EXIST`

Chaque `NOT_CONNECTED`/`NOT_IMPLEMENTED` ci-dessus décrit l'absence de
visibilité **depuis ce repo**, jamais une affirmation sur la réalité
externe. Reformulé domaine par domaine :

- `Network`, `Observatory`, `Opportunities`, `Pro/support`,
  `Admin/alerts` : zéro trace dans ce repo (ni collection, ni shim) —
  `EXTERNAL_EVIDENCE_NOT_AUDITED` pour leur existence réelle ailleurs
  dans l'écosystème CVLN.
- `Kiltikonet` (le produit lui-même) et `Culture Connect` : un shim
  typé et honnête existe déjà (`services/integrations/registry.py`),
  non configuré — `INTEGRATION_CONTRACT`, un cran au-dessus de l'absence
  totale.
- `Compliance`/`Audits`/`Gouvernance` : `NOT_IMPLEMENTED` — même pas un
  shim, seulement des métadonnées libres (`meta_entities`) côté
  cartographie.

## Ce que seul `KLT-05` ajoute de nouveau par rapport à `KLT-0001`/`KLT-0002`

`Auth/RBAC` et `Badges/NFC` n'apparaissent dans aucune formation
antérieure — ce sont les deux dépendances produit réellement nouvelles
introduites par les modules `KLT-05`/M02 et M04 (thèmes explicitement
demandés par le Founder en `KLT-0002`).
