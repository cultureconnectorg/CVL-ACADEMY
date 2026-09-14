# FRK-06 — Banque N2 (cas appliqués)

## Cas N2-1 — Premier appel de tous les temps

`db.counters` ne contient aucun document `frek_id`. Trace exactement
ce qui se passe lors du tout premier `mint_frek_id()` (distant
indisponible).

**Critères de notation :** l'appel distant échoue silencieusement,
`find_one_and_update` avec `upsert=True` crée le document, `seq`
devient 1, l'identifiant retourné est `FREK-001`. Élimination si le
candidat invente un identifiant de départ différent.

## Cas N2-2 — Demande de révocation

Un utilisateur veut "annuler" son FREK-ID et en obtenir un nouveau.
Réponds avec les faits réels.

**Critères de notation :** explique qu'aucun mécanisme de révocation
n'existe dans `mint_frek_id()` — c'est un territoire de FRK-09
(Identity Lifecycle, Recovery & Reconciliation), lui-même
`RECONCILED_NOT_BUILT`. Élimination si le candidat invente une
fonction de révocation.

## Cas N2-3 — Confusion avec DID

Un stagiaire affirme que `mint_frek_id()` "génère un DID W3C
standard." Corrige-le.

**Critères de notation :** explique que c'est un simple compteur
séquentiel formaté, sans rapport avec la norme W3C DID (territoire de
FRK-08) — une frontière de portée explicite, jamais franchie ici.
Élimination si le candidat confirme l'affirmation erronée.

## Cas N2-4 — Appels concurrents

Deux requêtes `mint_frek_id()` arrivent simultanément avec le distant
indisponible. Le candidat doit expliquer pourquoi l'usage de
`find_one_and_update` avec `$inc` garantit que chaque requête reçoit
un identifiant unique, même sans verrouillage applicatif explicite.

**Critères de notation :** explique que l'atomicité de l'opération
MongoDB empêche toute lecture intermédiaire entre les deux
incrémentations — chaque appel reçoit une valeur `seq` distincte par
construction. Élimination si le candidat propose un verrou applicatif
supplémentaire comme nécessaire, ou affirme qu'une collision
d'identifiant serait possible dans ce mécanisme réel.
