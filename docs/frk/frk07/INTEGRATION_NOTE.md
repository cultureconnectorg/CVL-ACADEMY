# FRK-07 — Integration Academy Package Note

## Réel vs. supposé

**Réel :** la discipline IAM marché-générale réelle (IdP, OAuth2/OIDC,
cycle de vie des credentials, modèle de session/token) comme pratique
professionnelle indépendante de CVLN. Le fait vérifiable que
`mint_frek_id()` (FRK-06) est un minting séquentiel étroit, cité comme
frontière, jamais fusionné.

**Supposé :** un lien `FRK07.SKILL.*` réel dans le runtime de cette
Academy — inexistant (`NO_RUNTIME_BINDING`). Toute implémentation
CVLN d'un IdP, d'OAuth2 ou d'OIDC — jamais accordée
(`CAPABILITY_NOT_IMPLEMENTED`).

## Dépendances

- `FREK_01_75_RECONCILIATION.md`, `docs/frk/frk06/REFERENTIAL.md`
  (frontière, jamais dupliquée), `70_EVIDENCE/
  EVIDENCE_ARCHITECTURE.md`.

## Ce qu'une future intégration exigerait

1. Une entrée `FRK07` dans le registre de certification de cette
   Academy, namespace distinct de `FRK06.SKILL.*`.
2. Une surface candidat réelle (ce corpus est markdown seul).
3. Un vrai design IAM à évaluer par un correcteur humain — inexistant
   aujourd'hui.

## Status

`STATUS = PACKAGE_COMPLETE` — référentiel, banques N1/N2, assessment
+ rubric, evidence model, 3 guides, cette note d'intégration existent
tous, deepened this pass. `FULLY_COMPLETE` non déclaré — requiert un
passage réel vérifié par un humain.
