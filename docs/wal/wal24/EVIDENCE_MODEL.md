# WAL-24 — Evidence Model

## Chaîne de preuve

M1 payload annoté par plateforme → M2 note de correction HTTP écrite →
M3 tableau plateforme→dépendance manquante → correcteur → (jury si
2.0–2.5) → `WAL24.SKILL.*` (réservé, non lié au runtime).

## Ce qui compte comme preuve

Le payload M1 vérifiable contre `passes.py` ; la note M2 citant le
comportement HTTP réel (200 + `unsigned`), pas le commentaire "501" du
fichier ; le tableau M3 nommant précisément les dépendances réelles
manquantes.

## Ce qui NE compte PAS comme preuve

Une affirmation qu'une carte signée/installable existe, ou une
répétition non vérifiée du commentaire "501" du fichier comme
comportement HTTP réel.

`READY_FOR_FREK_PROOF = FALSE`. Seule une certification interne Academy
(`WAL24.SKILL.*`) est en jeu.

## Réservation Skill ID

`WAL24.SKILL.PAYLOAD_LITERACY`, `WAL24.SKILL.HTTP_BEHAVIOR_VERIFICATION`,
`WAL24.SKILL.SIGNING_GAP_LITERACY` — réservés dans
`70_EVIDENCE/EVIDENCE_ARCHITECTURE.md`.
