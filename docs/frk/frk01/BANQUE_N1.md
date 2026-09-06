# FRK-01 — Banque N1 (formative, M1→M4)

```
Sourced directly against backend/services/frek_core.py (142 lines,
re-read in full this session).
```

## M1 — system map

1. Nomme les 5 méthodes publiques réelles de `FrekCoreClient`.
   (`mint_frek_id`, `emit_signal`, `issue_proof`, `resolve_stade`,
   `is_remote_enabled`)
2. Que fait `mint_frek_id()` si `FREK_CORE_BASE_URL` n'est pas défini
   (le cas par défaut) ? (Tente quand même l'appel distant, échoue
   silencieusement, puis retombe sur le compteur local `db.counters`,
   format `FREK-{seq:03d}`)
3. Existe-t-il une route permettant à un utilisateur final de créditer
   directement son propre wallet/compte via ce module ? (Non — aucune
   des 5 méthodes ne fait cela)
4. `is_remote_enabled()` retourne quoi par défaut, et pourquoi ?
   (`False` — car `FREK_CORE_BASE_URL` n'est pas défini par défaut
   dans l'environnement)

## M2 — vocabulaire de signal

5. Cite les 8 valeurs réelles de `VALID_SIGNALS`. (`FREK-TIME`,
   `FREK-WORK`, `FREK-SCORE`, `FREK-LINK`, `FREK-CERT`,
   `FREK-CONTRIB`, `FREK-SHARE`, `FREK-MISSION`)
6. Que fait `emit_signal()` si on lui passe un signal hors de cette
   liste ? (Rien — retour silencieux, aucune écriture en base, aucune
   erreur levée)
7. Quelles deux écritures réelles en base `emit_signal()` produit-il
   pour un signal valide ? (Insertion dans `db.frek_signals` +
   incrément de `db.users.signals.<signal>`)

## M3 — paliers de progression

8. Cite les 6 paliers réels et leurs seuils exacts de `cc_credits`.
   (`graine`=0, `pousse`=10, `racine`=50, `branches`=100, `arbre`=150,
   `foret`=300)
9. Dans quel ordre `resolve_stade()` vérifie-t-il les seuils ?
   (Décroissant — du plus haut seuil au plus bas, retourne dès la
   première correspondance)

## M4 — réalité honnête de `issue_proof()`

10. Que retourne `issue_proof()` en fallback local exactement ?
    (`f"PROOF-{uuid.uuid4().hex[:10].upper()}"` — un UUID aléatoire)
11. Cette "preuve" locale porte-t-elle une signature cryptographique,
    un chaînage de custody, ou un horodatage tiers ? (Non — aucun des
    trois, c'est un simple identifiant aléatoire)
12. Pourquoi cette réalité doit-elle être enseignée dès FRK-01, avant
    toute spécialisation ? (Parce que chaque formation en aval du
    domaine FREK dépend de cette réalité — la contredire ou la
    minoraliser plus tard casserait la cohérence de tout le corpus)
