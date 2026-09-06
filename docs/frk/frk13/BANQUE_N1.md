# FRK-13 — Banque N1 (formative, M1→M4)

```
Sourced against issue_proof() in backend/services/frek_core.py,
re-read this session, plus the market-general proof-engine concept.
```

## M1 — proof-engine concept (market-general)

1. Cite les 3 piliers réels d'un vrai proof engine professionnel.
   (Chaîne de custody, signature cryptographique, horodatage tiers)
2. Ces 3 piliers sont-ils indépendants de tout système CVLN ?
   (Oui — ce sont des standards professionnels réels, enseignables
   indépendamment)

## M2 — `issue_proof()` reality

3. Que retourne `issue_proof()` en fallback local, exactement ?
   (`f"PROOF-{uuid.uuid4().hex[:10].upper()}"`)
4. Ce retour porte-t-il une signature cryptographique ? (Non — aucune)
5. Que tente `issue_proof()` en premier ? (Un `POST /proof` distant,
   même pattern remote-first que les autres méthodes)

## M3 — honest gap communication

6. Un candidat doit-il dire à un dirigeant que "cette Academy a un
   moteur de preuve" ? (Non — elle a un stub d'identifiant, jamais un
   moteur de preuve complet)
7. Cette réalité doit-elle être minimisée ou dramatisée ? (Ni l'un ni
   l'autre — communiquée honnêtement, avec la valeur professionnelle
   du concept reconnue séparément)

## M4 — frontière avec FRK-75

8. FRK-75 (Reference Verifier Engineering) est-il le même système que
   `issue_proof()` ? (Non — FRK-75 est le vérificateur Python réel et
   testé du cluster `frek_v3`, une couche bien plus mature et
   distincte, jamais confondue avec le stub Academy)
