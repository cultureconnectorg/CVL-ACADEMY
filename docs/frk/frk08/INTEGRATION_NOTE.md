# FRK-08 — Integration Academy Package Note

## Réel vs. supposé

**Réel :** les standards W3C DID (document, méthodes de vérification,
points de service) et Verifiable Credentials (issuer/holder/verifier,
émission vs. présentation) comme littératie professionnelle
indépendante de CVLN. Le fait vérifiable que `mint_frek_id()` (dans
`backend/services/frek_core.py`) est un compteur séquentiel formaté en
chaîne — sans document DID, sans méthode de vérification, sans
résolveur.

**Supposé :** un lien `FRK08.SKILL.*` réel dans le runtime de cette
Academy — inexistant (`NO_RUNTIME_BINDING`). Toute conformité W3C
DID/VC pour un système CVLN — jamais accordée
(`CAPABILITY_NOT_IMPLEMENTED`).

## Dépendances

- `FREK_01_75_RECONCILIATION.md`, `backend/services/frek_core.py`
  (source du fait `mint_frek_id() ≠ DID`, jamais réécrite ni
  réinterprétée), `docs/frk/frk09/REFERENTIAL.md` (séquencement aval),
  `70_EVIDENCE/EVIDENCE_ARCHITECTURE.md`.

## Ce qu'une future intégration exigerait

1. Une entrée `FRK08` dans le registre de certification de cette
   Academy, namespace distinct de toute autre formation d'identité.
2. Une surface candidat réelle (ce corpus est markdown seul).
3. Un vrai document DID ou une vraie Verifiable Credential à évaluer —
   inexistant aujourd'hui côté CVLN.

## Status

`STATUS = PACKAGE_COMPLETE` — référentiel, banques N1/N2, assessment
+ rubric, evidence model, 3 guides, cette note d'intégration existent
tous, deepened this pass. `FULLY_COMPLETE` non déclaré — requiert un
passage réel vérifié par un humain.
