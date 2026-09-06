# FRK-03 — Banque N2 (cas appliqués)

## Cas N2-1 — Lecture d'un header réel

On te donne un header `FREK_PROOF_MAPPING` référençant `FREK-WORK`
pour un module KOR de production musicale. Explique ce que cela
signifie opérationnellement.

**Critères de notation :** explique que le module est censé émettre
`FREK-WORK` à un moment donné de son cycle (ex. soumission d'un
livrable), que ce signal est un des 8 réels de `VALID_SIGNALS`, et que
sa présence documente une intention, pas une preuve vérifiée.
Élimination si le candidat invente un mécanisme de vérification
externe.

## Cas N2-2 — Un jury demande une preuve d'ancrage externe

Un jury demande "peut-on prouver de manière opposable qu'un candidat a
réellement soumis ce livrable à telle date ?" Réponds avec les faits
réels.

**Critères de notation :** explique que non — `READY_FOR_FREK_PROOF =
FALSE` partout, aucune ancre externe (hash publié, horodatage tiers)
n'existe. La preuve interne (dossier candidat, notes jury) reste la
seule preuve valable aujourd'hui. Élimination si le candidat affirme
qu'une preuve opposable existe.

## Cas N2-3 — Compteur `mint_frek_id()` sous forte charge

Deux requêtes `mint_frek_id()` arrivent simultanément. Explique ce qui
garantit qu'elles n'obtiennent pas le même identifiant.

**Critères de notation :** cite l'opération atomique
`find_one_and_update` sur `db.counters` avec `$inc` — c'est
l'atomicité native de la base de données qui garantit l'unicité,
jamais un verrou applicatif inventé. Élimination si le candidat invente
un mécanisme de verrouillage absent du code.
