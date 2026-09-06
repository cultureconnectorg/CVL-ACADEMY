# FRK-58 — Banque N1 (formative, M1→M4)

```
Sourced directly against backend/services/frek_core.py (142 lines,
re-read in full this session) — same file as FRK-01, this formation's
prerequisite.
```

## M1 — remote/local fallback pattern

1. Que fait `_remote_post()` si `FREK_CORE_BASE_URL` n'est pas défini
   (le cas par défaut) ? (Retourne `None` immédiatement, sans tenter
   d'appel réseau — vérifié via `is_remote_enabled()`)
2. Que se passe-t-il si l'appel distant échoue (timeout, exception) ?
   (L'exception est capturée silencieusement — `except Exception:
   pass` — et la fonction retombe sur `None`, déclenchant le chemin
   local dans l'appelant)
3. Le timeout de l'appel distant est-il configurable dans le code
   réel ? (Fixé en dur à 8.0 secondes, `httpx.AsyncClient(timeout=8.0)`)

## M2 — signal emission & validation

4. `emit_signal()` lève-t-il une exception si le signal n'est pas dans
   `VALID_SIGNALS` ? (Non — retour silencieux, aucune écriture en
   base, aucune erreur)
5. Le miroir distant de `emit_signal()` est-il bloquant pour
   l'utilisateur ? (Non — "best-effort remote mirror", jamais
   bloquant, jamais garanti)

## M3 — progression-tier resolution

6. Si `cc_credits = 99`, quel palier `resolve_stade()` retourne-t-il ?
   (`branches` — seuil 100 non atteint, palier `racine`... attention:
   vérifier l'ordre décroissant réel : foret=300, arbre=150,
   branches=100, racine=50, pousse=10, graine=0 — 99 < 100 donc ne
   passe pas `branches`, retombe sur `racine` puisque 99 ≥ 50)
7. Quel est le palier retourné pour `cc_credits = 0` ? (`graine`)

## M4 — frontière avec le système externe

8. `frek_core.py` (ce module Academy) est-il le même code que
   `frekcoreAout2026`/`frek_v3/` (FRK-71→75) ? (Non — deux couches
   réelles distinctes du même produit éventuel, jamais fusionnées)
9. Existe-t-il une preuve d'intégration observée entre `frek_core.py`
   et n'importe quel autre système CVLN réel (Wallet, KORA,
   Agent Factory) ? (Non — aucune intégration observée nulle part)
