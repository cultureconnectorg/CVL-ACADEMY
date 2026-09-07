# KLT06_CORRECTOR_GUIDE

## Rôle

Évaluer `M01`-`M07` par critère observable (7/7 modules, mise à jour
2026-09-07).

## Points de vigilance spécifiques

| Module | Vigilance particulière |
|---|---|
| M01 | L'écart entre ce qu'un observatoire capterait en théorie et ce qui est réellement disponible est-il nommé, pas comblé ? |
| M02 | La source d'un chiffre a-t-elle été effectivement recherchée avant réutilisation ? |
| M03 | La spécification promet-elle uniquement des données réellement mesurables ? |
| M04 | Le périmètre du consentement initial est-il respecté, jamais dépassé ? |
| M05 | Chaque métrique de la maquette cite-t-elle un endpoint/collection réel ? L'état "non configuré" est-il prévu, jamais masqué ? |
| M06 | L'interprétation reste-t-elle une recommandation, jamais une décision prise à la place du rôle réseau ? Le caractère illustratif du signal est-il rappelé ? |
| M07 | Les limites réelles de l'analyse sont-elles présentées, pas gommées ? |

## Vigilance transversale — `NO_FAKE_LIVE_CONNECTION`

À aucun moment un livrable ne doit laisser entendre qu'une donnée
Observatory réelle a été consultée **en direct** aujourd'hui — le
schéma réel vérifié (endpoints, RBAC, collections) peut être cité, mais
toute métrique ou signal manipulé doit rester explicitement
`PEDAGOGICAL_ILLUSTRATIVE`. Si un livrable suggère le contraire, même
implicitement, le signaler explicitement au candidat.

## Ce que le correcteur ne fait pas

Ne pas évaluer une compétence hors mandat (médiation, budget,
représentation institutionnelle, gouvernance, opération plateforme).
