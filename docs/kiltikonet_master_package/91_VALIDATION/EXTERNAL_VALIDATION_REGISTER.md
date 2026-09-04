# External Validation Register

```
Aucun élément de ce registre n'est marqué VERIFIED — cette session n'a
mené aucune vérification en direct contre une source institutionnelle
ou juridique vivante. Le classement distingue ce qui est un fait
structurel stable (faible risque) de ce qui est un détail daté (risque
élevé), mais aucune des deux catégories n'a été confirmée en direct.
NO_LEGAL_CLAIM_UNVERIFIED — rien ici n'est présenté comme validé.
```

## Classification utilisée

`VERIFIED` (confirmé en direct — inutilisé dans ce registre à ce
stade) · `NEEDS_CURRENT_SOURCE` (fait structurel probablement stable,
mais daté par nature — calendrier, montant, procédure) ·
`NEEDS_EXPERT_REVIEW` (nécessite un avis d'expert métier/juridique, pas
seulement une source à jour) · `OUTDATED` (connu comme périmé —
inutilisé, rien n'a été identifié comme périmé faute de vérification) ·
`UNRESOLVED` (ambiguïté non tranchée par le corpus lui-même).

## `KLT-03` — dispositifs institutionnels nommés

| Élément | Module | Nature du contenu | Classification |
|---|---|---|---|
| OIF — logique de fonctionnement par relais | M02 | Fait structurel (architecture institutionnelle) | `NEEDS_EXPERT_REVIEW` |
| OIF — calendriers, critères d'éligibilité précis | M02 | Détail daté | `NEEDS_CURRENT_SOURCE` |
| UNESCO — critères de patrimoine culturel immatériel | M03 | Fait structurel | `NEEDS_EXPERT_REVIEW` |
| CARIFESTA — logique de festival régional | M03 | Fait structurel | `NEEDS_EXPERT_REVIEW` |
| DAC — logique de déconcentration de l'État | M04 | Fait structurel | `NEEDS_EXPERT_REVIEW` |
| CTM — logique de collectivité territoriale | M04 | Fait structurel | `NEEDS_EXPERT_REVIEW` |
| DAC/CTM — procédures, montants précis | M04 | Détail daté | `NEEDS_CURRENT_SOURCE` |
| Creative Europe — logique de consortium multi-partenaires | M05 | Fait structurel | `NEEDS_EXPERT_REVIEW` |
| ERDF — mention (nommé, non développé en module dédié) | M05 (référence) | Fait structurel | `UNRESOLVED` — jamais développé au-delà d'une mention, pas assez de matière pour classer plus finement |
| Fonds européens — taux de cofinancement, calendriers | M05 | Détail daté | `NEEDS_CURRENT_SOURCE` |
| Convention pluriannuelle mairie — cadre juridique du type de contrat | M06 | Fait structurel générique (non spécifique à une institution nommée) | `NEEDS_EXPERT_REVIEW` |

**Priorité de revue recommandée** : M02-M05 (les 4 modules
institution-spécifiques) avant toute diffusion au-delà d'un cadre
pédagogique interne — cohérent avec le gate propre
`UNSOURCED_INSTITUTIONAL_FACT` déjà posé dans `docs/klt/klt03/
QUALITY_GATES.md`.

## `KLT-04` — droit associatif, fiscalité, bénévolat

| Élément | Module | Nature du contenu | Classification |
|---|---|---|---|
| Loi 1901 — principes (liberté d'association, non-lucrativité, liberté statutaire) | M01 | Fait structurel, réputé stable | `NEEDS_EXPERT_REVIEW` |
| Loi 1901 — procédures de déclaration précises (formulaires, délais préfectoraux) | M01 | Détail daté | `NEEDS_CURRENT_SOURCE` |
| Rôles associatifs (Président/Trésorier/Secrétaire/DAF) — répartition des responsabilités | M02 | Fait structurel, usage courant | `NEEDS_EXPERT_REVIEW` (léger — pratique répandue, pas une obligation légale stricte) |
| Plan comptable associatif — principes | M03 | Fait structurel | `NEEDS_EXPERT_REVIEW` |
| Distinction 1901 / 1901 lucrative — critères | M04 | Fait structurel réputé stable dans son principe | `NEEDS_EXPERT_REVIEW` |
| Seuils/taux fiscaux précis | M04 | Détail daté, module lui-même le signale déjà (`SOURCE_STATUS`) | `NEEDS_CURRENT_SOURCE` |
| PV d'AGO/AGE — exigences de forme (quorum, vote) | M05 | Fait structurel | `NEEDS_EXPERT_REVIEW` |
| Distinction bénévolat/salariat — critère de subordination | M06 | Fait structurel (droit du travail) | `NEEDS_EXPERT_REVIEW` |
| Défraiement vs rémunération déguisée — seuils précis | M06 | Détail daté, module lui-même le signale déjà (`SOURCE_STATUS`) | `NEEDS_CURRENT_SOURCE` |
| Conflit d'intérêt — traitement (déclaration + abstention) | M10 | Fait structurel, pratique de gouvernance courante | `NEEDS_EXPERT_REVIEW` (léger) |

**Priorité de revue recommandée** : M01 (création/statuts), M04
(fiscalité) et M06 (bénévolat/salariat) — les trois modules où une
erreur non détectée aurait le plus de conséquence réelle pour une
association qui suivrait ce contenu à la lettre.

## Ce que ce registre ne fait pas

Ne corrige, ne complète, ni ne vérifie aucun contenu — c'est un
inventaire des points à faire vérifier, pas une vérification elle-même.
Aucune revendication juridique ou institutionnelle n'est faite au-delà
de ce que les modules sources affirment déjà.
