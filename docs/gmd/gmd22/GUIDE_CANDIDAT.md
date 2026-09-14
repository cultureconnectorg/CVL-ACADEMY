# GMD-22 — Guide Candidat

## Avant de commencer

Tu dois avoir GMD-21 (ou une équivalence validée) — ce module suppose
que tu sais déjà lire une définition de route et un modèle Pydantic.

## Ce que tu dois savoir faire à la fin

Créer, lire, mettre à jour et retirer un `Volume` via les 4 routes
admin réelles (`GET/POST/PUT/DELETE /admin/catalogue`), sans jamais
inventer un champ ou une route qui n'existe pas dans
`gmfest972/goodmooddjsayd/backend/server.py`.

## Comment réviser

1. Lis `server.py` lignes 80-98 (le modèle) et 219-305 (les routes)
   toi-même — ne mémorise pas un résumé, vérifie contre le code.
2. Fais les 16 questions de `BANQUE_N1.md` à livre fermé, puis corrige
   contre le code, pas contre ta mémoire.
3. Traite les 3 cas de `BANQUE_N2.md` par écrit avant de regarder les
   critères de notation.

## Piège le plus fréquent

Confondre `GET /catalogue` (public, cap 200) et `GET /admin/catalogue`
(admin, cap 500) — ils se ressemblent, ne servent pas le même usage,
et un diagnostic qui ne vérifie que l'un des deux est incomplet.

## Règle absolue

N'invente jamais un champ, une route, ou un mécanisme (batch reorder,
merge, flag "featured", distinction save/publish) qui n'existe pas
dans le code réel — c'est une élimination automatique, quelle que soit
la qualité du reste de ta copie.
