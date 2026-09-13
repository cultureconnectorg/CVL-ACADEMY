# IOS-07 — Integration Academy Package Note

## Réel vs. supposé

**Réel :** `backend/services/events.py` — bus pub/sub en-process, même
mécanisme que BRN-15 (`academy.certification.passed`) et que le
traitement marché-général de FRK-54.

**Réel, mais externe et non câblé :** le vrai corpus de gouvernance
`cultureconnectorg/Cvln-ios-v.1` (21 ADRs, 7 RFCs, constitution, specs
protocole ADL/AGENT-PROTOCOL/ISA/MCL, backend de contrôle de dérive) —
self-déclaré non `DEPLOYED_RUNTIME`.

**Supposé :** `IOS07.SKILL.*` réel au-delà de la littératie de ce bus,
ou un câblage entre `events.py` et le corpus de gouvernance
`Cvln-ios-v.1` — ni l'un ni l'autre n'existe (`NO_RUNTIME_BINDING`).

## Dépendances

`AGENT_FACTORY_IOS_BRAIN_CMD_LAURENTIA_RECONCILIATION.md`,
`docs/frk/frk54/REFERENTIAL.md` (même mécanisme, référencé, jamais
re-dérivé), `docs/agf/internal/brn15/REFERENTIAL.md` (même bus,
touchpoint distinct), `cultureconnectorg/Cvln-ios-v.1` (contexte de
marché cité, jamais câblé).

## Ce qu'une future évolution exigerait

1. Une décision produit explicite avant tout câblage vers un système
   Intelligence OS externe — hors périmètre de cette formation
   aujourd'hui.
2. Une nouvelle formation ou une révision explicite documentant le
   nouvel état, jamais une extension silencieuse d'IOS-07.
3. Un correcteur humain réévaluant la formation à la lumière du
   nouveau périmètre, si celui-ci se matérialisait.

## Status

`STATUS = PACKAGE_COMPLETE` — package complet construit cette passe,
deepened. `FULLY_COMPLETE` requiert un passage réel vérifié par un
humain.
