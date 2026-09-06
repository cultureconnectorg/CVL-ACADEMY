# GMD-31 — Banque N2 (cas appliqués)

## Cas N2-1 — Entrée bloquée en `pending` depuis 3 heures

Un opérateur remarque une entrée `frek_id_outbox` toujours `pending`
après 3 heures. Diagnostique où elle en est dans le cycle de retry.

**Critères de notation:** calcule que 3h = 10800s, ce qui correspond à
un passage après les backoffs 30s+120s+600s+3600s cumulés (~4350s au
4e essai) — l'entrée est probablement en attente du 5e essai (backoff
6h). Propose de vérifier `attempts` et `next_attempt_at` réels plutôt
que de supposer un blocage. Élimination si le candidat invente un
mécanisme d'accélération manuelle du retry qui n'existe pas dans le
code lu.

## Cas N2-2 — Confusion avec le FREK de l'Academy

Un stagiaire, formé sur cette Academy, affirme que `frek_service.py`
de Good Mood et `backend/services/frek_core.py` de cette Academy
"parlent au même service FREKCORE." Corrige cette erreur.

**Critères de notation:** explique que ce sont deux clients distincts,
dans deux repos distincts, chacun pointé vers son propre `FREK_ID_URL`/
endpoint configuré indépendamment — même motif architectural (outbox
env-gated), jamais le même canal. **Élimination automatique** si le
candidat ne corrige pas cette confusion ou la renforce.

## Cas N2-3 — Toutes les tentatives épuisées

Une entrée passe `"failed"` après 6 tentatives. Le manager demande de
la relancer manuellement. Que peux-tu faire avec les routes
réellement disponibles ?

**Critères de notation:** signale qu'aucune route de relance manuelle
n'existe dans le code audité (`GET /admin/outbox/frek-id` est en
lecture seule) — propose d'escalader vers un correctif technique
(nouvelle tentative programmatique, hors périmètre opérateur) plutôt
que d'inventer une route `/admin/outbox/frek-id/{id}/retry`.
