# KOR-01 — Evidence Model

```
Pour chaque compétence : EVIDENCE_TYPE, REQUIRED_FIELDS, SOURCE,
HASHABLE_PAYLOAD, VERIFICATION_RULE, PRIVACY_LEVEL, puis
READY_FOR_FREK_PROOF = TRUE/FALSE — sans jamais prétendre qu'une ancre
externe existe si elle n'existe pas.
```

| Compétence | EVIDENCE_TYPE | REQUIRED_FIELDS | SOURCE | HASHABLE_PAYLOAD | VERIFICATION_RULE | PRIVACY_LEVEL | READY_FOR_FREK_PROOF |
|---|---|---|---|---|---|---|---|
| C1 | Analyse + note | podcast analysé, structure relevée, note de positionnement | candidat | texte de l'analyse + note | structure réelle relevée (pas seulement le sujet) | interne | `FALSE` |
| C2 | One-pager + idées | sujet, format, cadence, justification | candidat | one-pager complet | grille de comparaison présente et priorisée | interne | `FALSE` |
| C3 | Script annoté | zones scriptées, zones d'improvisation guidée | candidat | script complet | distinction explicite des deux zones | interne | `FALSE` |
| C4 | Guide + interview | questions, adaptation accessibilité, trace de conduite | candidat, témoin (Man Rosa) | guide + enregistrement/notes | adaptation réellement appliquée, pas seulement prévue | **confidentiel** — consentement du témoin requis | `FALSE` |
| C5 | Prise de son + note | setup, gain, bruits traités | candidat | fichier brut + note | absence d'écrêtage documentée | interne | `FALSE` |
| C6 | Montage + note d'arbitrage | règle de montage, application | candidat | fichier monté + note | règle appliquée de façon cohérente sur tout l'épisode | interne | `FALSE` |
| C7 | Sound design + justification | sons utilisés, lien au contenu | candidat | piste + note | au moins un son lié directement au contenu réel | interne | `FALSE` |
| C8 | Mix/master + mesures | niveaux, test d'écoute mobile | candidat | fichier final + mesures | test d'écoute mobile documenté | interne | `FALSE` |
| C9 | Générique + note de cohérence | motif sonore, confrontation à M06 | candidat | générique + note | absence de rupture de ton constatée | interne | `FALSE` |
| C10 | Configuration + flux RSS | hébergeur, flux, soumission | candidat | flux RSS | validité technique du flux vérifiée | interne | `FALSE` |
| C11 | Fiche de publication | titre, description, mots-clés, visuel | candidat | fiche complète | titre non putaclick, description non résumante | interne, publique une fois l'épisode réellement publié | `FALSE` |
| C12 | Plan d'audience | canaux évalués, canal priorisé | candidat | plan écrit | priorisation justifiée par effort/public réaliste | interne | `FALSE` |
| C13 | Note de piste monétisation | état du contact, limites du mandat | candidat | note écrite | aucun chiffre non prouvé présenté comme acquis | interne, **sensible** si elle nomme un tiers commercial réel | `FALSE` |
| C14 | Dossier + soutenance | tous les livrables M01-M13, liens explicites, bilan réflexif | candidat, jury (notes) | dossier complet | rubric §RUBRIC.md, seuil global atteint | interne (candidat, jury, admin) | `FALSE` |

## `READY_FOR_FREK_PROOF` — pourquoi `FALSE` partout

Le stack `frek_signal` (`FREK-WORK`/`FREK-SCORE`/`FREK-CONTRIB`/
`FREK-CERT`) est **réel** et déjà utilisé par chaque module (voir
`FREK_PROOF_MAPPING` de chaque fiche module, hérité de
`seed_modules.py` pour les modules issus du legacy). Mais une preuve
"`READY_FOR_FREK_PROOF = TRUE`" impliquerait une ancre vérifiable
externe (hachage publié, horodatage tiers) — **rien de tel n'existe
aujourd'hui** dans `fms_canonical`/`klt_canonical`/`frek_core.py` pour
aucune formation. Marquer `TRUE` ici serait une affirmation non
vérifiée.

## `PRIVACY_LEVEL` — note spécifique à C4 et C13

L'interview de Man Rosa (C4) implique une personne réelle simulée dans
le cas — tout usage au-delà de l'évaluation exigerait un consentement
documenté, comme pour l'équivalent Kiltikonet (`KLT-01`, compétence
C9). La note de monétisation (C13) est marquée sensible dès lors
qu'elle nomme un tiers commercial (Kafé Kreyòl) — elle ne doit jamais
être diffusée comme preuve d'un accord qui n'existe pas.
