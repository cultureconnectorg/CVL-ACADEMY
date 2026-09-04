# KOR-02 — Evidence Model

```
Pour chaque compétence : EVIDENCE_TYPE, REQUIRED_FIELDS, SOURCE,
HASHABLE_PAYLOAD, VERIFICATION_RULE, PRIVACY_LEVEL, puis
READY_FOR_FREK_PROOF = TRUE/FALSE — sans jamais prétendre qu'une ancre
externe existe si elle n'existe pas.
```

| Compétence | EVIDENCE_TYPE | REQUIRED_FIELDS | SOURCE | HASHABLE_PAYLOAD | VERIFICATION_RULE | PRIVACY_LEVEL | READY_FOR_FREK_PROOF |
|---|---|---|---|---|---|---|---|
| C1 | Note + diagnostic | pièces recensées, diagnostic | candidat | note complète | structure réelle relevée, pas seulement le sujet | interne | `FALSE` |
| C2 | Fiche source + protocole | versions, méthode de recoupement | candidat | fiche complète | les deux versions documentées | interne | `FALSE` |
| C3 | Note d'angle | angles comparés, défense | candidat | note complète | au moins 3 angles comparés dont celui du partenaire | interne | `FALSE` |
| C4 | Guide + interview | questions, trace de conduite | candidat, témoin (Josette) | guide + notes | aucune suggestion de réponse documentée | **confidentiel** — consentement du témoin requis | `FALSE` |
| C5 | Feature | texte complet, sources citées | candidat | texte | divergence intégrée, aucune invention non sourcée | interne, publique une fois réellement publiée | `FALSE` |
| C6 | Plan narratif + récit | structure, tension identifiée | candidat | plan + texte | tension réelle mise en avant, pas fabriquée | interne | `FALSE` |
| C7 | Déclinaisons | versions par format | candidat | fichiers/textes | cohérence vérifiée avec le texte long | interne, publique une fois publiée | `FALSE` |
| C8 | Charte + arbre de décision | conflits d'intérêt, consentement | candidat | document complet | lien familial rendu transparent, consentement documenté | **confidentiel** pour la partie consentement de Man Rosa | `FALSE` |
| C9 | Note d'arbitrage | problème identifié, compromis | candidat | note complète | contre-proposition concrète documentée | interne, **sensible** si elle nomme un tiers média réel | `FALSE` |
| C10 | Pitch | conditions, attribution | candidat | pitch complet | cohérence avec l'arbitrage M09 vérifiée | interne, sensible si tiers média nommé | `FALSE` |
| C11 | Portfolio + bio | contexte de production, bio | candidat | portfolio complet | au moins une difficulté réelle assumée | interne, publique une fois publiée par le candidat | `FALSE` |
| C12 | Dossier + soutenance | tous les livrables, bilan réflexif | candidat, jury (notes) | dossier complet | rubric §RUBRIC.md, seuil global atteint | interne (candidat, jury, admin) | `FALSE` |

## `READY_FOR_FREK_PROOF` — pourquoi `FALSE` partout

Même justification que `KOR-01` (`docs/kor/kor01/skills/
EVIDENCE_MODEL.md`) : le stack `frek_signal` est réel et déjà utilisé
(voir `FREK_PROOF_MAPPING` de chaque module), mais aucune ancre
vérifiable externe n'existe aujourd'hui dans `fms_canonical`/
`klt_canonical`/`frek_core.py` pour aucune formation.

## `PRIVACY_LEVEL` — note spécifique à C4, C8, C9, C10

L'interview de Josette (C4) implique une personne réelle simulée dans
le cas — consentement requis pour tout usage au-delà de l'évaluation.
La compétence C8 traite spécifiquement du consentement de Man Rosa pour
un usage journalistique, **distinct** du consentement pédagogique déjà
couvert par `KOR-01` — les deux ne doivent jamais être confondus. Les
notes C9/C10 sont sensibles dès lors qu'elles nomment un média réel
(ici, *Dyaspora FM*, fictif dans le cas) — elles ne doivent jamais être
diffusées comme preuve d'un accord réel qui n'existe pas.
