# GMD-22 — Evidence Model

## Chaîne de preuve

M1 field table → M2 runbook exécuté (create → verify via `GET
/catalogue` public → update → verify → delete) → M3 diagnostic writeup
→ correcteur → (jury si copie limite, 2.0–2.5) → `GMD22.SKILL.*`
(réservé, non lié au runtime — voir `INTEGRATION_NOTE.md`).

## Ce qui compte comme preuve

- Le tableau de champs M1, vérifiable ligne à ligne contre
  `server.py:80-98`.
- Le runbook M2 exécuté sur une instance réelle ou sandboxée
  (captures d'écran/logs des 4 appels + les 2 vérifications croisées
  admin/public) — à défaut, une trace de raisonnement complète au
  niveau code, jamais une simple affirmation "ça marche."
- Le diagnostic M3, qui doit citer la ligne de code exacte justifiant
  la conclusion.

## Ce qui NE compte PAS comme preuve

Une affirmation non vérifiable ("j'ai testé et ça marche" sans trace),
une capacité décrite mais non exécutée, ou toute référence à une route/
un champ absent de `server.py`.

`READY_FOR_FREK_PROOF = FALSE` — comme GMD-21, aucun ancrage FREK/
attestation n'existe pour ce module ; seule une certification interne
Academy (`GMD22.SKILL.*`) est en jeu.

## Réservation Skill ID

`GMD22.SKILL.CATALOGUE_LITERACY`, `GMD22.SKILL.CATALOGUE_CRUD`,
`GMD22.SKILL.CATALOGUE_DIAGNOSTIC` — réservés dans
`70_EVIDENCE/EVIDENCE_ARCHITECTURE.md`, non liés à un runtime réel.
