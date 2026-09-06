# FRK-59 — Banque N1 (formative, M1→M4)

```
Sourced against Good Mood's real frek_service.py/wallet_service.py,
already cited in docs/gmd/gmd31, gmd32.
```

## M1 — `frek_service.py` literacy

1. Vers quelle variable d'environnement `frek_service.py` poste-t-il ?
   (`FREK_ID_URL`, propre à Good Mood, distincte de
   `FREK_CORE_BASE_URL` de cette Academy)
2. Quel est le schedule exact de retry en cas d'échec ? (`[30s, 2m,
   10m, 1h, 6h]`)

## M2 — `wallet_service.py` literacy

3. Vers quelle variable d'environnement `wallet_service.py` poste-t-il ?
   (`WALLET_URL`, propre à Good Mood)
4. Ces deux services partagent-ils la même table d'outbox ? (Non —
   chacun a la sienne : `db.frek_outbox` et `db.wallet_outbox`)

## M3 — "not yet an integration" discipline

5. `frek_service.py` et `wallet_service.py` s'appellent-ils l'un
   l'autre ? (Non — aucune observation de ce type ; ce sont deux
   clients sortants indépendants)
6. Peut-on dire que "FREK × Wallet" est une intégration fonctionnelle
   aujourd'hui ? (Non — deux clients découplés dans le même code base
   n'est pas une intégration)

## M4 — frontière avec les systèmes Academy

7. `wallet_service.py` (Good Mood) est-il le même code que
   `backend/wallet/service.py` de cette Academy ? (Non — deux systèmes
   distincts ; l'un est un client sortant, l'autre un ledger interne
   additif)
8. `backend/wallet/` de cette Academy appelle-t-il `frek_core` ?
   (Non — aucun appel observé, les deux systèmes internes ne se
   parlent pas non plus)
