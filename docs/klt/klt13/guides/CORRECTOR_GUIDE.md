# KLT13_CORRECTOR_GUIDE

## Rôle

Évaluer `M01`-`M05` par critère observable (5/5 modules).

## Points de vigilance spécifiques

| Module | Vigilance particulière |
|---|---|
| M01 | Chaque rôle a-t-il un accès scoped à sa mission réelle ? Le parcours PMR est-il traité explicitement, pas seulement mentionné ? |
| M02 | Le précédent réel (Good Mood) est-il correctement attribué, jamais présenté comme un système Kiltikonet ? |
| M03 | La mention `NOT_IMPLEMENTED` figure-t-elle sur l'intégralité de la spécification ? |
| M04 | Aucun accès non autorisé n'a-t-il été cédé, même sous pression sociale simulée ? La décision d'escalade est-elle justifiée ? |
| M05 | Chaque chiffre du bilan correspond-il à une mesure réelle ? Le non mesuré est-il nommé explicitement ? |

## Vigilance transversale — `NFC_NOT_IMPLEMENTED` / `NO_FAKE_LIVE_CONNECTION`

À aucun moment un livrable ne doit laisser entendre qu'un système NFC ou
un système de scan Kiltikonet réel existe aujourd'hui — le seul
précédent réel cité (Good Mood, QR) doit toujours être attribué
correctement, jamais confondu avec Kiltikonet. Si un livrable suggère le
contraire, même implicitement, le signaler explicitement au candidat.

## Ce que le correcteur ne fait pas

Ne pas évaluer une compétence hors mandat (médiation, budget,
représentation institutionnelle, gouvernance, protocole badge/scan
générique de `KLT-05`).
