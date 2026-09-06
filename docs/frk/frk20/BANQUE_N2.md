# FRK-20 — Banque N2 (cas appliqués)

## Cas 1 — Conception d'un flux offline-first

Le candidat conçoit le flux de vérification locale d'un artefact signé
sans connexion réseau, puis sa synchronisation différée, en identifiant
où la garantie cryptographique doit être vérifiée (localement).

**Critère éliminatoire :** faire dépendre la garantie de preuve d'un
appel réseau synchrone.

## Cas 2 — Discipline CVLN-gap

Le candidat doit expliquer pourquoi `is_remote_enabled()` (`frek_core.py`,
`bool(FREK_CORE_BASE_URL)`, faux par défaut) ne constitue pas une
vérification offline au sens de cette formation — c'est une bascule de
disponibilité réseau, pas une garantie cryptographique locale.

**Critère éliminatoire :** confondre fallback local simple et
vérification cryptographique offline.
