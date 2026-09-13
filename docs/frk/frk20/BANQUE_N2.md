# FRK-20 — Banque N2 (cas appliqués)

## Cas 1 — Conception d'un flux offline-first

Le candidat conçoit le flux de vérification locale d'un artefact signé
sans connexion réseau, puis sa synchronisation différée, en identifiant
où la garantie cryptographique doit être vérifiée (localement).

**Critère éliminatoire :** faire dépendre la garantie de preuve d'un
appel réseau synchrone.

**Critères de notation :** la vérification cryptographique (signature/
hash-chain) a lieu entièrement en local, avant toute tentative de
synchronisation.

## Cas 2 — Discipline CVLN-gap

Le candidat doit expliquer pourquoi `is_remote_enabled()` (`frek_core.py`,
`bool(FREK_CORE_BASE_URL)`, faux par défaut) ne constitue pas une
vérification offline au sens de cette formation — c'est une bascule de
disponibilité réseau, pas une garantie cryptographique locale.

**Critère éliminatoire :** confondre fallback local simple et
vérification cryptographique offline.

## Cas 3 — Synchronisation échouée après vérification locale

Un artefact signé est vérifié avec succès en local (signature valide),
mais sa synchronisation vers le serveur distant échoue de façon
répétée. L'artefact reste-t-il valide ? Justifie en te référant au
patron store-and-forward.

**Critères de notation :** oui — la garantie de validité a été établie
entièrement lors de la vérification locale ; l'échec de synchronisation
est un problème de livraison distinct, sans effet rétroactif sur la
validité déjà prouvée localement. Élimination si le candidat affirme
que l'artefact devient invalide ou incertain tant que la
synchronisation n'a pas réussi.
