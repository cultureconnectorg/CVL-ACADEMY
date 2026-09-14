# GMD-05 — Integration Academy Package Note

## Réel vs. supposé

**Réel (cité par référence à GMD-24, jamais re-audité ni contredit
ici) :** `TicketTypeIn`/`TicketType` (`server.py:115-131`), le check
non-atomique au checkout, l'incrément `$inc` atomique + upsert fan
dans `_issue_tickets_for_session` (`server.py:574-620`), la contrainte
email spécifique aux billets.

**Supposé :** un lien `GMD05.SKILL.*` réel dans le runtime de cette
Academy — inexistant (`NO_RUNTIME_BINDING`). Toute pratique de marché
non implémentée (tarification dynamique, revente, liste d'attente) —
enseignée comme connaissance de marché, jamais comme capacité
plateforme.

## Dépendances

- `docs/gmd/gmd24/` (exemple travaillé, jamais re-dérivé),
  `docs/gmd/gmd25/` (hand-off), `docs/cvln_academy_master/20_EXTERNAL/
  GOOD_MOOD_DJ_SAYD_RECONCILIATION.md`, `70_EVIDENCE/
  EVIDENCE_ARCHITECTURE.md`.

## Ce qu'une future intégration exigerait

1. Une entrée `GMD05` dans le registre de certification de cette
   Academy.
2. Une surface candidat réelle (ce corpus est markdown seul).
3. Un vrai rôle opérateur de billetterie à staffer — inexistant
   aujourd'hui.

## Status

`STATUS = PACKAGE_COMPLETE_FOR_GMD05` — référentiel, banques N1/N2,
assessment + rubric, evidence model, 3 guides, cette note
d'intégration existent tous. `FULLY_COMPLETE` non déclaré.
