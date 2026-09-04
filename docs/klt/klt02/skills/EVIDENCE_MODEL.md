# KLT-02 — Evidence Model

```
Même discipline que KLT-01 : READY_FOR_FREK_PROOF = FALSE partout,
honnêtement (aucune ancre externe réelle n'existe aujourd'hui).
```

| Compétence | EVIDENCE_TYPE | REQUIRED_FIELDS | SOURCE | VERIFICATION_RULE | PRIVACY_LEVEL | READY_FOR_FREK_PROOF |
|---|---|---|---|---|---|---|
| C1 | Note de cadrage | périmètre, ressources, autorité, échéance | candidat | 4 champs renseignés | interne | `FALSE` |
| C2 | Étude + carte | parties prenantes, pouvoir qualifié | candidat | pouvoir qualifié par acteur, pas seulement listé | interne | `FALSE` |
| C3 | Budget chiffré | postes, sources, statut confirmé/à obtenir | candidat | chaque poste a une source qualifiée | interne | `FALSE` |
| C4 | Dossier(s) de financement | piste, délai, montant, statut | candidat | priorisation justifiée par délai/écart | interne, diffusable au financeur si validé | `FALSE` |
| C5 | Planning + organigramme | tâche, ressource, disponibilité, relais | candidat | au moins un relais documenté sur tâche fragile | interne | `FALSE` |
| C6 | Tableau de bord | prévu, réel, écart, décision | candidat | au moins un écart réel documenté | interne | `FALSE` |
| C7 | Kit de communication | destinataire, angle, faits cités | candidat | faits vérifiables, pas de promesse non tenue | diffusable si validé | `FALSE` |
| C8 | Registre des risques | risque, probabilité, impact, réponse | candidat | chaque risque prioritaire a une réponse | interne | `FALSE` |
| C9 | Rapport d'évaluation | indicateur, donnée observée, interprétation | candidat | observé/interprété distingués | interne | `FALSE` |
| C10 | Bilan + feuille de route | faits, recommandation, justification | candidat | recommandation tracée aux faits | interne | `FALSE` |
| C11 | Dossier + soutenance | toutes les pièces + bilan réflexif | candidat, jury | rubric, seuil global atteint | interne (candidat, jury, admin) | `FALSE` |

`READY_FOR_FREK_PROOF = FALSE` partout — même justification que
`klt01/skills/EVIDENCE_MODEL.md` : le stack `frek_signal` est réel et
utilisé (voir `FREK_PROOF_MAPPING` de chaque module), mais aucune ancre
de preuve externe vérifiable n'existe encore dans ce repo.
