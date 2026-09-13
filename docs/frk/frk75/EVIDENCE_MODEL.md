# FRK-75 — Evidence Model

`READY_FOR_FREK_PROOF = FALSE`.

## Chaîne de preuve

Lecture de sortie de test annotée (16/16 vecteurs d'or) + distinction
implémentation/spécification + frontière FRK-13 → correcteur → (jury
si 2.0–2.5) → `FRK75.SKILL.REFERENCE_VERIFIER_ENGINEERING.L1`
(réservé).

## Ce qui compte comme preuve

Une lecture correcte de la sortie de test réelle, distinguant
précisément ce qui est prouvé (cette implémentation Python) de ce qui
ne l'est pas (agnosticisme de la spécification) ; une frontière
explicite avec FRK-13.

## Ce qui NE compte PAS comme preuve

Toute affirmation que les 16 tests prouvent l'agnosticisme
d'implémentation de la spécification ; toute fusion avec `issue_proof()`
(FRK-13) ; une analyse incorrecte du scénario d'échec croisé Rust.

- Réservation d'ID : `FRK75.SKILL.REFERENCE_VERIFIER_ENGINEERING.L1`
  — réservé, non émis.
- Grounding réel : `frek_v3/reference_verifier/` (7 modules réels, 16
  tests passants contre vecteurs d'or) — le mieux ancré du cluster
  FRK-71→75, `coverage SUBSTANTIAL`.
- Limitation honnêtement disclosée : implémentation Python unique,
  Rust cross-implémentation nommée comme étape suivante requise —
  jamais présenté comme protocole prouvé implementation-agnostic.
- Frontière permanente vs. FRK-13 (`issue_proof()` stub Academy).
- Mapping `VALID_SIGNALS` : aucun aujourd'hui.
