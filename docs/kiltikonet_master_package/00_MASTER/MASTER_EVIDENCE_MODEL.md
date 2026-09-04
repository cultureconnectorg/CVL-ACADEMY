# Master Evidence Model

```
Consolide les 5 EVIDENCE_MODEL.md locaux (docs/klt/kltXX/skills/
EVIDENCE_MODEL.md) sans les réécrire. Distingue quatre concepts que le
corpus ne doit jamais confondre.
```

## Les quatre concepts, jamais confondus

| Concept | Définition | Statut dans le corpus KLT-01→05 |
|---|---|---|
| `LEARNING_ARTIFACT` | Un livrable produit pendant l'apprentissage (note, fiche, cartographie) — preuve que le module a été travaillé | **Réel** — chaque module en produit un (voir chaque `EVIDENCE_TYPE` local) |
| `PROFESSIONAL_EVIDENCE` | Un artefact assemblé en dossier de certification, avec source/provenance/consentement documentés | **Réel** — chaque registre de preuves terminal (module `-A01`) en dépend |
| `VERIFIED_EXTERNAL_EVIDENCE` | Une preuve validée par une source externe réelle (expert, institution, système tiers) | **Inexistant à ce jour** — aucune validation externe n'a encore eu lieu (voir `91_VALIDATION/`) |
| `FREK_PROOF` | Une preuve ancrée de façon vérifiable dans le système FREK réel (hachage, horodatage tiers) | **Inexistant à ce jour** — `READY_FOR_FREK_PROOF = FALSE` partout, sans exception |

**La confusion la plus dangereuse à éviter** : présenter un
`LEARNING_ARTIFACT` comme une `VERIFIED_EXTERNAL_EVIDENCE`, ou un
protocole simulé (`KLT-05`/M04) comme un `FREK_PROOF` réel. Aucun des 5
corpus ne commet cette confusion — vérifié : chaque module qui produit
un artefact sensible porte une mention explicite de son statut réel
(`SOURCE_STATUS`, "simulé, non opposable", `READY_FOR_FREK_PROOF =
FALSE`).

## `READY_FOR_FREK_PROOF` — consolidation

| Formation | Compétences couvertes | `READY_FOR_FREK_PROOF` |
|---|---|---|
| KLT-01 | 11/11 | `FALSE` partout |
| KLT-02 | 11/11 | `FALSE` partout |
| KLT-03 | 12/12 | `FALSE` partout |
| KLT-04 | 14/14 | `FALSE` partout |
| KLT-05 | 11/11 | `FALSE` partout |

**59/59 compétences du corpus, `FALSE` sans exception.** La raison est
identique partout (reprise textuellement des 5 modèles locaux) : le
stack `frek_signal` est réel et déjà utilisé (chaque module cite son
`FREK_PROOF_MAPPING`), mais aucune ancre de preuve externe vérifiable
(hachage publié, horodatage tiers) n'existe encore dans ce repo, pour KLT
comme pour FMS.

## Préparer la compatibilité future — sans inventer le fonctionnement de FREK

Les 5 `EVIDENCE_MODEL.md` locaux documentent déjà, pour chaque
compétence, la **forme** qu'une ancre FREK prendrait (`HASHABLE_PAYLOAD`,
`VERIFICATION_RULE`) — sans jamais prétendre que cette ancre existe. Ce
document ne fait qu'agréger cette structure, il n'ajoute aucune donnée
sur le fonctionnement réel de FREK au-delà de ce que `services/
frek_core.py` documente déjà dans le repo.

## `PRIVACY_LEVEL` — cas sensible signalé

Une seule compétence du corpus manipule une donnée personnelle
sensible d'un tiers non-candidat : `KLT01.SKILL.C09` (interview de
mémoire orale), marquée `confidentiel` dans son modèle local. Aucune
autre compétence des 59 ne porte ce niveau — vérifié par relecture des
5 tableaux `PRIVACY_LEVEL`.

## Ce que ce document consolide, sans le dupliquer

Le détail champ par champ (`EVIDENCE_TYPE`, `REQUIRED_FIELDS`, `SOURCE`,
`VERIFICATION_RULE`) pour chacune des 59 compétences reste dans les 5
fichiers locaux — ce document n'en fait pas une copie, il en tire la
lecture transversale que les fichiers locaux, pris séparément, ne
peuvent pas donner.
