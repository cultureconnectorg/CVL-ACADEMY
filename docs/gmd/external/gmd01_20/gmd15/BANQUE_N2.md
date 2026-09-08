# GMD-15 — Banque N2 (cas appliqués)

## Cas N2-1 — Procédure de secours inventée

Face à une panne de scan hors des 3 cas connus un soir d'événement,
un stagiaire invente une procédure de contournement ("je laisse
entrer si le badge a l'air correct visuellement"). Corrige.

**Critères de notation:** cite la limite réelle documentée (GMD-25/
GMD-34 : aucun chemin de récupération automatisé n'existe) — la seule
action correcte est l'escalade immédiate vers un humain, jamais une
procédure inventée. Élimination si le candidat valide une décision
d'admission sans escalade dans ce cas.

## Cas N2-2 — Surveillance de densité de foule présentée comme capacité plateforme

Un collègue affirme que "la plateforme surveille automatiquement la
densité de foule et alerte en cas de risque." Corrige.

**Critères de notation:** rappelle que cette capacité n'existe pas
dans le code réel audité (GMD-25 ne couvre que le scan/compteur de
présence) — à enseigner comme protocole de marché-général, jamais
comme capacité de la plateforme. Élimination si le candidat maintient
l'affirmation de capacité plateforme.

## Cas N2-3 — Mauvaise interprétation du compteur

Un opérateur affirme que le compteur `/scan/counter/{eid}` inclut les
scans invalides et dupliqués dans le total de présence. Corrige.

**Critères de notation:** cite le comportement réel — le compteur
reflète la présence basée sur les scans **valides**, pas les scans
invalides/dupliqués. Élimination si le candidat maintient
l'affirmation erronée sans la corriger.
