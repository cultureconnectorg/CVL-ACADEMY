# WAL-26 — Banque N2 (cas appliqués)

## Cas N2-1 — Un crash pendant la soumission d'un settlement

**Situation** : un ticket d'incident signale qu'un déploiement a
crashé juste après qu'un settlement soit passé en `SUBMITTED`, avant
que la référence du fournisseur ne soit écrite. Un opérateur propose de
resoumettre manuellement.

**Décision attendue** : expliquer que le chemin de soumission est
conçu retry-safe précisément pour ce scénario — resoumettre via le
même mécanisme (`submit`) est sûr et ne double-soumettra jamais au
fournisseur ; jamais créer un second settlement manuellement pour
contourner l'état bloqué.

**Critères de notation** : identifie le scénario retry-safe correct
(50%, éliminatoire si absent), refuse la création manuelle d'un second
settlement (30%), cite `settlement_transition` (20%).

## Cas N2-2 — Différence mineure lors d'une réconciliation

**Situation** : une réconciliation ouvre un cas avec un écart mineur et
documenté (frais de conversion connu). Le manager demande de "forcer"
la résolution en `RESOLVED` pour clore rapidement.

**Décision attendue** : proposer `ACCEPTED_DIFFERENCE` plutôt que
`RESOLVED` si l'écart est réel et documenté mais non éliminé — les deux
résolutions ont un sens différent, jamais interchangeables par
commodité.

**Critères de notation** : distingue correctement `RESOLVED` (écart
éliminé) de `ACCEPTED_DIFFERENCE` (écart réel accepté, documenté)
(50%, éliminatoire si confondu), ne cède pas à la pression de clôture
rapide au prix d'une résolution inexacte (30%), vérifie que le cas est
bien en `OPEN`/`INVESTIGATING` avant résolution (20%).

---

**Couverture** : 2 cas, couvrant M1 (retry-safety) et M2 (distinction
des résolutions).
