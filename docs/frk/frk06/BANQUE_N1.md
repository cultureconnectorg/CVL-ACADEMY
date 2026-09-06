# FRK-06 — Banque N1 (formative, M1→M4)

```
Sourced directly against mint_frek_id() in backend/services/
frek_core.py, re-read this session.
```

## M1 — remote-first minting

1. Que tente `mint_frek_id()` en premier ? (Un `POST /mint` distant
   via `_remote_post`)
2. Que se passe-t-il si le distant répond avec un JSON sans clé
   `frek_id` ? (La condition `remote and "frek_id" in remote` échoue,
   le code retombe sur le compteur local)

## M2 — local counter mechanics

3. Quelle collection réelle porte le compteur local ? (`db.counters`,
   document `_id: "frek_id"`)
4. Quelle opération atomique incrémente ce compteur ? (`find_one_and_
   update` avec `$inc: {seq: 1}`, `upsert=True`)
5. Quel est le format exact de l'identifiant produit ? (`f"FREK-
   {seq:03d}"`, ex. `FREK-001`, `FREK-042`)

## M3 — scope boundary

6. FRK-06 enseigne-t-il l'architecture DID/VC complète ? (Non — jamais,
   c'est le territoire séparé de FRK-07/08/09)
7. Un opérateur FRK-06 peut-il révoquer ou faire tourner un
   FREK-ID existant ? (Non — aucun mécanisme de ce type n'existe dans
   `mint_frek_id()`, qui ne fait qu'incrémenter et retourner)

## M4 — cas limite

8. Si `db.counters` ne contient pas encore de document `_id:
   "frek_id"` lors du tout premier appel, que se passe-t-il ? (`upsert=
   True` crée le document, `seq` démarre à 1 par l'incrément)
