# FRK-68 — Banque N1 (formative, M1→M4)

```
Sourced against db.frek_signals (frek_core.py) and Good Mood's two
outbox tables (frek_outbox, wallet_outbox), re-read this session.
```

## M1 — `db.frek_signals` audit literacy

1. Quels champs réels une entrée `db.frek_signals` porte-t-elle ?
   (`user_id`, `signal`, `meta`, `ts`)
2. Un auditeur peut-il attribuer une entrée `db.frek_signals` au
   système FREK de Good Mood ? (Non — cette table appartient
   exclusivement à `frek_core.py` de cette Academy)

## M2 — outbox status & retry-schedule literacy

3. Quels sont les 3 états réels d'une entrée d'outbox ? (`delivered`,
   `pending`, `failed`)
4. Après combien de tentatives une entrée passe-t-elle à `failed` ?
   (Après les 5 tentatives du schedule `[30s, 2m, 10m, 1h, 6h]`)

## M3 — three-system discipline

5. Nomme les trois tables réelles distinctes que ce module couvre.
   (`db.frek_signals` — cette Academy ; `db.frek_outbox` — Good Mood ;
   `db.wallet_outbox` — Good Mood)
6. Un auditeur peut-il présenter ces trois tables comme un seul
   pipeline d'audit unifié ? (Non — ce sont trois systèmes séparés,
   jamais fusionnés dans un rapport)

## M4 — cas limite

7. Si une entrée `db.frek_outbox` est `pending` depuis 3 heures,
   quelles tentatives ont déjà eu lieu selon le schedule réel ? (30s,
   2m, 10m — la tentative à 1h n'est pas encore due si le compteur
   part de l'insertion initiale)
