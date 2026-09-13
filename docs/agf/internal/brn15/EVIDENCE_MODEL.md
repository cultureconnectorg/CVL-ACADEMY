# BRN-15 — Evidence Model

`READY_FOR_FREK_PROOF = FALSE` (non applicable à ce domaine).

## Chaîne de preuve

- Réservation d'ID : `BRN15.SKILL.BRAIN_TOUCHPOINT_OPERATOR.L1` —
  réservé, non émis.
- Grounding réel : `backend/certification/service.py:140`,
  `backend/services/events.py`, `subscribers.py` →
  `/academy/certification-passed`.
- Prérequis : IOS-07 (même mécanisme de bus `events.py`).
- Contexte de marché cité, jamais substrat opérant : `/brain/ask`
  (`metacvln-spec/MetaCVLN`).
- Langage de frontière repris verbatim de `docs/kor/kor12/` et
  `FREK_01_75_RECONCILIATION.md` (FRK-58/60) — convergence, pas
  re-dérivation.

## Ce que cette chaîne ne prouve pas

Elle ne prouve ni ne suggère qu'un moteur de raisonnement, de
mémoire, ou de contexte existe dans cette Academy. Elle ne prouve pas
non plus qu'un câblage existe entre `academy.certification.passed` et
`/brain/ask` — ces deux éléments sont documentés séparément
précisément parce qu'aucune intégration observée ne les relie.

## Pourquoi aucune preuve mission-éligible aujourd'hui

Le touchpoint réel (`service.py:140` → `events.py` → `subscribers.py`)
est fonctionnel en production, mais aucun chemin FREK n'existe pour ce
patron : aucun `emit_signal`/`issue_proof` de `frek_core.py` n'est
câblé à cet événement. La certification BRN-15 porte donc sur la
littératie du touchpoint, pas sur une preuve d'exécution mission
vérifiable par le runtime FREK.

## Conditions d'une future preuve

1. Un vrai passage vérifié par un correcteur humain sur les banques
   N1/N2.
2. Une décision produit explicite avant tout câblage vers un système
   Brain externe (`/brain/ask` ou équivalent) — hors périmètre de
   cette formation.
3. Si un tel câblage était un jour construit, une nouvelle formation
   ou une révision explicite de BRN-15 documenterait ce nouvel état —
   jamais une extension silencieuse du périmètre actuel.
