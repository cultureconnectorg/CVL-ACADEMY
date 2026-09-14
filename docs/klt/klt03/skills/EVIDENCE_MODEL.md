# KLT-03 — Evidence Model

```
Même discipline que KLT-01/02 : READY_FOR_FREK_PROOF = FALSE partout.
```

| Compétence | EVIDENCE_TYPE | REQUIRED_FIELDS | VERIFICATION_RULE | PRIVACY_LEVEL | READY_FOR_FREK_PROOF |
|---|---|---|---|---|---|
| C1 | Cartographie + stratégie | institutions, échelle, priorité | priorisation justifiée par maturité | interne | `FALSE` |
| C2 | Dossier OIF | registre, relais identifié, `SOURCE_STATUS` | mention `SOURCE_STATUS` présente | interne, diffusable si validé | `FALSE` |
| C3 | Note UNESCO/CARIFESTA | horizon, justification, `SOURCE_STATUS` | distinction horizon respectée | interne | `FALSE` |
| C4 | Dossier DAC/CTM | logique propre, cohérence KLT-02, `SOURCE_STATUS` | cohérence avec dossier KLT-02 vérifiée | interne | `FALSE` |
| C5 | Budget + lettre consortium | partenaire, répartition, `SOURCE_STATUS` | caractère exploratoire signalé | interne | `FALSE` |
| C6 | Term sheet | termes, mandat, statut non signé | mention "non signé" présente | interne | `FALSE` |
| C7 | Note de diplomatie | message, registre, limites | aucun engagement non mandaté | interne | `FALSE` |
| C8 | Intervention préparée | statut, contenu, réponses de renvoi | statut clarifié avant instance | interne | `FALSE` |
| C9 | Plan de lobbying | objectif, arguments, plan de relance | aucune pression illégitime | interne | `FALSE` |
| C10 | Rapport financeur | données réelles, observé/interprété | cohérence avec bilan KLT-02 | interne, diffusable au financeur si validé | `FALSE` |
| C11 | Plan relationnel | partenaire, fréquence, objet non-sollicitation | au moins un contact non-sollicitation | interne | `FALSE` |
| C12 | Dossier + soutenance | toutes pièces + bilan réflexif | rubric, seuil atteint | interne | `FALSE` |

`READY_FOR_FREK_PROOF = FALSE` partout — même justification que
`klt01/skills/EVIDENCE_MODEL.md`.
