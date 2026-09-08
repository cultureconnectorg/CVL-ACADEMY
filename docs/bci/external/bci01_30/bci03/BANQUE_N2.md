# BCI-03 — Banque N2 (cas appliqués)

## Cas N2-1 — Contrat testnet présenté comme audité

Un candidat affirme que le smart contract de `BCH-01-M03` "a passé un
audit de sécurité professionnel puisqu'il fonctionne en testnet."
Corrige.

**Critères de notation:** cite le périmètre réel de `BCH-01-M03` —
un déploiement testnet pédagogique, jamais un audit de sécurité
professionnel. Un déploiement testnet réussi démontre que le code
s'exécute, pas qu'il est exempt de vulnérabilités. Élimination si le
candidat maintient qu'un audit a eu lieu.

## Cas N2-2 — Système financier de production affirmé

Un stagiaire affirme que "CVLN opère un système de royalties
automatiques en production via blockchain." Corrige.

**Critères de notation:** rappelle que `BCH-01-M03` reste un exercice
pédagogique testnet, jamais un système de production réel — aucune
infrastructure blockchain CVLN de production n'existe au-delà de cet
exercice. Élimination si le candidat maintient l'affirmation de
système de production.

## Cas N2-3 — Checklist de vulnérabilités incomplète validée

Un collègue propose un audit se limitant à vérifier uniquement les
erreurs de syntaxe, sans examiner la réentrance ni le contrôle
d'accès. Corrige.

**Critères de notation:** cite les classes de vulnérabilités
standards du marché (réentrance, overflow/underflow, contrôle
d'accès, manipulation d'oracle) — une checklist qui les omet n'est pas
un audit de sécurité complet. Élimination si le candidat valide cette
checklist incomplète comme un audit rigoureux.
