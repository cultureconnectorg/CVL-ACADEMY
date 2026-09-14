# GMD-33 — Banque N2 (cas appliqués)

## Cas N2-1 — Token admin divulgué publiquement

Un token JWT admin est accidentellement collé dans un canal Slack
public. Décris la procédure réelle de mitigation avec le code
disponible.

**Critères de notation:** reconnaît qu'**aucune route de révocation de
token n'existe** dans le code audité — le token reste valide jusqu'à
expiration naturelle (12h) quoi qu'il arrive côté client
(`/auth/logout` ne fait qu'effacer le cookie local, pas invalider le
token ailleurs). Propose la vraie mitigation disponible : rotation de
`JWT_SECRET` (invalide tous les tokens existants, y compris ceux des
admins légitimes — à peser) et changement de mot de passe admin,
escaladé à un humain technique. Élimination si le candidat invente une
route "révoquer ce token."

## Cas N2-2 — Session admin inattendue

Un `GET /auth/me` révèle un rôle `"admin"` pour un compte qui ne
devrait pas en avoir un. Que vérifies-tu ?

**Critères de notation:** cite que `get_current_admin` fait confiance
au champ `role` stocké sur `db.users` — si ce champ a été modifié à
tort (erreur manuelle, faille applicative ailleurs), le token reste
valide et autorisé jusqu'à correction du champ `role` lui-même ou
expiration ; propose de corriger directement le rôle en base
(hors périmètre de ce candidat opérateur, à escalader) plutôt que
d'inventer un mécanisme de dérogation.

## Cas N2-3 — Distinction avec la sécurité de cette Academy

Un stagiaire affirme que l'authentification JWT de Good Mood "utilise
le même système d'auth" que cette Academy. Corrige.

**Critères de notation:** explique que ce sont deux implémentations
JWT distinctes, dans deux repos distincts, chacune avec son propre
`JWT_SECRET` et son propre modèle utilisateur — même schéma
technologique (JWT + bcrypt), jamais le même secret ni la même base.
Élimination si le candidat affirme un partage réel de session entre
les deux systèmes.
