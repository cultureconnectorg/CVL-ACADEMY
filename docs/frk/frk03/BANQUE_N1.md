# FRK-03 — Banque N1 (formative, M1→M4)

```
Sourced against real FREK_PROOF_MAPPING headers already carried by
docs/kor/ modules, plus backend/services/frek_core.py's real
VALID_SIGNALS/db writes.
```

## M1 — `FREK_PROOF_MAPPING` literacy

1. Un header `FREK_PROOF_MAPPING` sur un module `docs/kor/korXX/`
   documente-t-il une preuve externe vérifiée, ou une intention de
   signal ? (Une intention de signal — jamais une preuve externe
   vérifiée)
2. D'où vient l'héritage de ce header pour les modules issus du
   legacy ? (`seed_modules.py`)

## M2 — side-effect operation

3. Quelles deux écritures réelles `emit_signal()` produit-il pour un
   signal valide ? (`db.frek_signals` insert + incrément
   `db.users.signals.<signal>`)
4. `mint_frek_id()` garantit-il un identifiant séquentiel sans trou en
   cas d'échecs concurrents ? (Le mécanisme réel est un
   `find_one_and_update` atomique sur `db.counters` — chaque appel
   réussi obtient un `seq` unique et croissant ; le code ne documente
   aucune garantie explicite au-delà de cette atomicité native Mongo)

## M3 — remote-mirror discipline

5. Un opérateur FREK peut-il affirmer qu'un signal a été mirroré à
   distance avec certitude ? (Non — c'est toujours best-effort,
   jamais garanti, jamais vérifiable depuis ce module seul)
6. `is_remote_enabled()` est-il la seule source de vérité sur la
   tentative d'appel distant ? (Oui — si `False`, aucun appel distant
   n'est même tenté)

## M4 — discipline READY_FOR_FREK_PROOF

7. Que signifie `READY_FOR_FREK_PROOF = FALSE` sur un module KOR ?
   (Le signal `frek_signal` est réellement utilisé, mais aucune ancre
   externe vérifiable — hash publié, horodatage tiers — n'existe
   aujourd'hui)
8. Un opérateur FREK peut-il "corriger" ce `FALSE` en marquant `TRUE`
   sans qu'une vraie ancre existe ? (Non — ce serait une affirmation
   non vérifiée, une faute grave)
