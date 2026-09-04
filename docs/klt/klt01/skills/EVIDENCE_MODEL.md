# KLT-01 — Evidence Model

```
Pour chaque compétence : EVIDENCE_TYPE, REQUIRED_FIELDS, SOURCE,
HASHABLE_PAYLOAD, VERIFICATION_RULE, PRIVACY_LEVEL, puis
READY_FOR_FREK_PROOF = TRUE/FALSE — sans jamais prétendre qu'une ancre
externe existe si elle n'existe pas.
```

| Compétence | EVIDENCE_TYPE | REQUIRED_FIELDS | SOURCE | HASHABLE_PAYLOAD | VERIFICATION_RULE | PRIVACY_LEVEL | READY_FOR_FREK_PROOF |
|---|---|---|---|---|---|---|---|
| C1 | Document texte | auteur, date, contenu | candidat | texte de la note + carte des rôles | présence des 3 rôles (détenteur/public/tiers) pour chaque acteur cité | interne (candidat + jury) | `FALSE` — aucune ancre de hachage réelle implémentée aujourd'hui |
| C2 | Fiches sourcées | source, élément documenté, plan (matériel/immatériel/linguistique) | candidat, validé si possible par un détenteur | 5 fiches concaténées | chaque fiche cite une source identifiable | interne | `FALSE` |
| C3 | Cartographie structurée | acteur, nature, posture, influence, catégorie, priorité, justification | candidat | tableau rempli | tous les acteurs du cas présents, priorisation justifiée | interne | `FALSE` |
| C4 | Fiche action | public, objectif, format, ressources, contraintes | candidat | fiche complète | 5 champs obligatoires renseignés, contraintes connues incluses | interne | `FALSE` |
| C5 | Grille d'animation | règles annoncées, ajustements réels, posture | candidat, observé en séance | grille + notes de séance | au moins un ajustement réel documenté | interne | `FALSE` |
| C6 | Support produit | format, contenu, choix éditoriaux justifiés | candidat | fichier du support + note de choix | traçabilité aux fiches C2 | interne, diffusable si validé par les détenteurs | `FALSE` |
| C7 | Note d'arbitrage | positions en présence, décision, motivation | candidat | texte de la note | décision explicite (pas de compromis évasif), motivation citant la légitimité du détenteur | interne | `FALSE` |
| C8 | Atelier + retour | public, adaptation appliquée, retour | candidat, participants | retour écrit | adaptation d'accessibilité réellement appliquée (pas seulement prévue) | interne, anonymisé pour les mineurs | `FALSE` |
| C9 | Interview transcrite | témoin (anonymisable), date, consentement, transcription | candidat, témoin | transcription | consentement documenté avant l'entretien, passages incertains signalés | **confidentiel** — consentement explicite requis pour tout usage au-delà de l'évaluation | `FALSE` |
| C10 | Registre de preuves | liste des pièces, source, provenance par pièce | candidat | registre complet | aucune pièce sans source/provenance ; mention `OBSERVATORY_INTEGRATION = FUTURE/NOT_CONNECTED` présente | interne | `FALSE` |
| C11 | Dossier + soutenance | toutes les pièces ci-dessus + bilan réflexif | candidat, jury (notes) | dossier complet | rubric §RUBRIC.md, seuil global atteint | interne (candidat, jury, admin) | `FALSE` |

## `READY_FOR_FREK_PROOF` — pourquoi `FALSE` partout

Le stack `frek_signal` (`FREK-WORK`/`FREK-SCORE`/`FREK-CONTRIB`/
`FREK-CERT`) est **réel** et déjà utilisé par chaque module (voir
`FREK_PROOF_MAPPING` dans chaque fiche module). Mais une preuve
"`READY_FOR_FREK_PROOF = TRUE`" impliquerait une ancre vérifiable
externe (hachage publié, horodatage tiers, ou équivalent) — **rien de
tel n'existe aujourd'hui** dans `fms_canonical`/`frek_core.py` pour
aucune formation, FMS incluse. Marquer `TRUE` ici serait une
affirmation non vérifiée. Ce tableau documente la **forme** que
prendrait cette ancre le jour où elle existe (les colonnes
`HASHABLE_PAYLOAD`/`VERIFICATION_RULE` sont prêtes à recevoir une
implémentation réelle), sans prétendre qu'elle existe.

## `PRIVACY_LEVEL` — note spécifique à C9

L'interview de mémoire orale (C9) est la seule pièce de ce dossier
impliquant des données personnelles sensibles d'un tiers non-candidat (le
témoin). Elle est marquée `confidentiel` : son usage au-delà de
l'évaluation `KLT01-A01` (publication, diffusion) requiert un
consentement distinct, renouvelé pour cet usage spécifique — pas
déductible du consentement donné pour l'entretien initial.
