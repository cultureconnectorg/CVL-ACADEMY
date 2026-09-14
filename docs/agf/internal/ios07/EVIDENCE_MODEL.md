# IOS-07 — Evidence Model

`READY_FOR_FREK_PROOF = FALSE` (non applicable à ce domaine).

## Chaîne de preuve

- Réservation d'ID : `IOS07.SKILL.EVENT_BUS_OPERATOR.L1` — réservé,
  non émis.
- Grounding réel : `backend/services/events.py` (même mécanisme que
  BRN-15).
- Référence croisée : `docs/frk/frk54/REFERENTIAL.md` (même mécanisme,
  traitement unique, jamais re-dérivé).
- Contexte de marché cité, jamais substrat opérant : corpus de
  gouvernance `Cvln-ios-v.1` (21 ADRs, 7 RFCs, constitution, specs
  ADL/AGENT-PROTOCOL/ISA/MCL, self-déclaré non `DEPLOYED_RUNTIME`).

## Ce que cette chaîne ne prouve pas

Elle ne prouve pas que cette Academy dispose d'une "Intelligence OS"
déployée — le seul mécanisme réel est un pub/sub en mémoire, sans
aucune connexion au corpus de gouvernance externe. Elle ne prouve pas
non plus que `events.py` offre une garantie de durabilité ou une
surface webhook.

## Pourquoi aucune preuve mission-éligible aujourd'hui

Aucun chemin FREK n'existe pour ce patron — la certification IOS-07
porte sur la littératie du bus et sa frontière de vocabulaire, pas sur
une preuve d'exécution mission vérifiable par le runtime FREK.

## Conditions d'une future preuve

1. Un vrai passage vérifié par un correcteur humain sur les banques
   N1/N2, avec vérification croisée de la cohérence FRK-54 si le
   dossier du candidat est disponible.
2. Toute évolution vers une intégration réelle avec un système
   "Intelligence OS" externe exigerait une décision produit explicite
   et une nouvelle formation ou révision documentée — jamais une
   extension silencieuse du périmètre actuel.
