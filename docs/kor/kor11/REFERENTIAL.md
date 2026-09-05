# KOR-11 — Référentiel canonique : Trust, Safety & Content Governance

```
FORMATION: KOR-11
STATUT_LEGACY: NEW (aucun ancrage legacy — n'existe pas dans seed_data.py/seed_modules.py)
BASELINE: KOR-01/KOR-02 (squelette, profondeur, architecture documentaire)
NEEDS_EXPERT_REVIEW: TRUE (modération, mineurs, harcèlement, droits, réglementation)
```

## 1. Contenu principal (source : KOR-0001 §3, ligne 11)

Politiques de contenu · modération · signalements · contenus sensibles
· fraude/spam · usurpation · droits · mineurs · harcèlement · recours ·
sanctions · transparence · gouvernance éditoriale · sécurité
culturelle.

## 2. PROFESSIONAL_ROLE → ACTIVITIES → COMPETENCIES

**Rôle professionnel** : Coordinateur/coordinatrice Trust & Safety
d'une plateforme de streaming culturel.

| Activité | Compétence | Sous-compétences |
|---|---|---|
| Poser un cadre | C1 — Distinguer politique de contenu et gouvernance éditoriale | rédaction de politique, périmètre, limites |
| Traiter les signalements | C2 — Recueillir et trier les signalements | recueil, catégorisation, priorisation |
| Modérer | C3 — Conduire un workflow de modération | file de traitement, décision, délai, traçabilité |
| Qualifier | C4 — Classer un contenu sensible avec discernement culturel | distinction offensant/culturellement situé |
| Détecter la fraude | C5 — Identifier fraude et spam | patterns, signaux faibles, faux positifs |
| Protéger l'identité | C6 — Traiter l'usurpation d'identité | vérification, preuve, action proportionnée |
| Articuler les droits | C7 — Articuler un signalement de droits avec `KOR-07` | handoff, ne pas trancher seul un litige de droits |
| Protéger les mineurs | C8 — Appliquer une politique de protection des mineurs | détection, signalement obligatoire, escalade |
| Traiter le harcèlement | C9 — Traiter un signalement de harcèlement | sécurité de la personne, non-victimisation secondaire |
| Statuer | C10 — Décider sanction et recours | proportionnalité, droit de recours, réexamen |
| Rendre compte | C11 — Produire un rapport de transparence | métriques honnêtes, sans sur-vente d'automatisation |
| Sécuriser la culture | C12 — Arbitrer une tension sécurité culturelle vs modération automatisée | protéger l'expression culturelle légitime |
| Synthétiser | C13 — Conduire un dossier Trust & Safety de bout en bout | dossier + soutenance |

`DEPTH_DETERMINES_MODULE_COUNT` : 13 compétences → 13 modules
(`M01`-`M13`), aucune compression, aucun gonflage.

## 3. Provenance des compétences

| Compétence | Provenance |
|---|---|
| C1-C6, C8-C12 | `MARKET_SKILL` |
| C7 | `MARKET_SKILL` (handoff explicite vers `KOR-07`, jamais une compétence de droit) |
| C13 | `MARKET_SKILL` (synthèse) |

**Aucune `KORA_CURRENT_CAPABILITY`** — voir §6.

## 4. Vérification anti-footprint (KOR-0001 §4)

> *"Trust & safety / modération (`KOR-11`) : Zéro footprint. Aucune
> collection modération, signalement, ou politique de contenu trouvée
> nulle part dans `backend/`."*

Confirmé de nouveau ici. Aucun code, aucune collection DB, aucun
service de modération n'existe dans ce repo. Toute pratique de ce
module s'exerce sur un **vehicule fictif générique**, jamais présenté
comme KORA (voir §6 et modules).

## 5. Tensions de frontière actives (posées, non résolues par supposition)

- **#13 — Disambiguïsation "Governance"** : le terme "gouvernance" est
  utilisé ailleurs dans l'écosystème CVLN pour désigner FREK/CVLN
  Brain (gouvernance de la preuve, `services/frek_core.py`). Ici,
  "gouvernance éditoriale" (C1) désigne exclusivement le cadre de
  politique de contenu d'une plateforme de streaming — **ce n'est pas
  la même gouvernance**. Ce module ne doit jamais laisser croire que
  KORA hérite d'un mécanisme de gouvernance FREK pour la modération.
- **#3 (`KOR-07`/`KOR-13`)** reposée : un signalement de droits (C7)
  n'est traité ici que comme *déclencheur de handoff*, jamais comme un
  acte de négociation de droits (`KOR-07`) ni de partenariat créateur
  (`KOR-13`).
- **#9 (`KOR-07`/`KOR-15`)** reposée : la tension chant traditionnel
  (introduite en `KOR-07`) réapparaît ici sous l'angle sécurité
  culturelle (C12) — **toujours non résolue**, jamais tranchée par
  supposition dans ce module non plus.

## 6. KORA_PRODUCT_GAP (jamais une KORA_CURRENT_CAPABILITY fabriquée)

| Capacité évoquée par le contenu | Statut réel |
|---|---|
| File de modération outillée | `CAPABILITY_NOT_IMPLEMENTED` |
| Détection automatique fraude/spam | `CAPABILITY_NOT_IMPLEMENTED` |
| Système de signalement utilisateur | `CAPABILITY_NOT_IMPLEMENTED` |
| Registre de sanctions/recours | `CAPABILITY_NOT_IMPLEMENTED` |
| Rapport de transparence automatisé | `CAPABILITY_NOT_IMPLEMENTED` |

`NO_KORA_PRODUCT_UPGRADE`. Ce gap alimente uniquement le futur
`KORA_PRODUCT_CAPABILITY_GAP_MAP` (après `KOR-15`).

## 7. Cas fil rouge — Trust & Safety à Anba Tonèl Host

Le vehicule générique "Anba Tonèl Host" (introduit en `KOR-06`,
explicitement non-KORA) héberge des centaines d'émissions dont
*Rasin*. Une nouvelle personne, **Widlène**, coordinatrice Trust &
Safety d'Anba Tonèl Host, traite : (a) un signalement infondé contre
*Rasin* ("usurpation" alléguée sans preuve), et (b) un signalement réel
sur un contenu tiers reprenant un chant traditionnel — écho direct de
la tension `KOR-07` jamais résolue, ici sous l'angle sécurité
culturelle plutôt que droits.

`STATUS = PROPOSED`.
