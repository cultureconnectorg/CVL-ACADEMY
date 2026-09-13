# FRK-37 — Banque N2 (cas appliqués)

## Cas 1 — Conception d'un mécanisme d'attestation

Le candidat conçoit un mécanisme d'attestation de dispositif (racine de
confiance, certificat signé) pour prouver l'origine d'un actif média,
en citant FRK-36 par référence pour le contexte de capture authentique.

**Critère éliminatoire :** proposer une attestation sans racine de
confiance vérifiable.

**Critères de notation :** la racine de confiance est explicite
(clé/certificat lié matériellement à l'appareil) et le mécanisme de
vérification de la chaîne de certificats est décrit.

## Cas 2 — Ce que l'attestation ne prouve pas

Le candidat doit expliquer pourquoi une attestation de dispositif
valide ne garantit pas, à elle seule, l'intégrité du contenu après
capture (frontière avec FRK-38).

**Critère éliminatoire :** affirmer qu'une attestation de source suffit
à garantir l'intégrité complète du média.

## Cas 3 — Appareil compromis après attestation

Un appareil dont la clé d'attestation est légitime est compromis après
sa fabrication (accès physique non autorisé). Une capture produite
après cette compromission porte-t-elle toujours une attestation
"valide" au sens technique ? Que faudrait-il en plus pour détecter le
problème ?

**Critères de notation :** oui, techniquement la signature reste
valide (la clé n'a pas changé) — l'attestation prouve la possession de
la clé, pas l'intégrité opérationnelle de l'appareil au moment de la
capture. Détecter la compromission exigerait un mécanisme distinct
(révocation de clé, attestation d'intégrité du firmware) hors du
périmètre de cette formation. Élimination si le candidat affirme que
l'attestation de dispositif détecte automatiquement une compromission
physique.
