# GMD-21 — Assessment certificatif & Rubric

## Structure de l'épreuve

1. **N1 (10 questions tirées de `BANQUE_N1.md`, 16 disponibles)** — 40%
   de la note.
2. **N2 (1 cas tiré de `BANQUE_N2.md`, 3 disponibles)** — 30% de la
   note.
3. **Livrable M1** (carte de routes annotée, voir `REFERENTIAL.md` §M1)
   — 30% de la note, noté contre la vraie table de routes de
   `server.py`.

## Rubric (échelle 0-4 par compétence, convention FMS déjà en usage dans cette Academy)

| Compétence | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| C1 — Carte système correcte | Aucune carte produite | Carte avec >50% d'erreurs | Carte avec 2-3 erreurs | Carte correcte, 1 erreur mineure | Carte entièrement correcte, sourcée à `server.py` |
| C2 — Attribution formation→route | Aucune attribution | <50% correctes | 50-75% correctes | 75-95% correctes | 100% correctes |
| C3 — Identification des gaps (GMD-34) | Prétend qu'un mécanisme existe | Ne mentionne pas le gap | Mentionne le gap sans détail | Mentionne le gap et la règle d'escalade | Mentionne le gap, la règle, et l'explique dans ses propres mots |

## Seuil d'élimination

Toute réponse qui **invente** une capacité absente du repo réel (ex :
un mécanisme d'incident qui n'existe pas, un champ de modèle
inexistant) reçoit automatiquement **0 sur la compétence concernée**,
quel que soit le reste de la copie — cohérent avec `UNPROVEN_FEATURE
= 0` appliqué au niveau candidat.

## Seuil de passage

Moyenne ≥ 2.5/4 sur les 3 compétences, aucune compétence à 0.

## Mentions

- 2.5-3.0 : Validé
- 3.0-3.5 : Validé avec mention Bien
- 3.5-4.0 : Validé avec mention Très Bien

## Status

`STATUS = ASSESSMENT_MODEL_V1`. Jamais administré à un candidat réel.
