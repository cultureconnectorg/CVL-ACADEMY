# GMD-33 — Evidence Model

## Chaîne de preuve

M1 diagramme de séquence (login→token→me→logout) → M2 audit complet
public/admin vérifié contre `Depends()` → M3 note de reconnaissance
d'incident (jamais de réponse inventée) → correcteur → (jury si
2.0–2.5) → `GMD33.SKILL.*` (réservé, non lié au runtime).

## Ce qui compte comme preuve

Le diagramme M1 vérifiable contre `server.py:36-70, 261-278` ;
l'audit M2 citant réellement chaque route public/admin avec sa preuve
`Depends()` (ou son absence) ; la note M3 citant l'absence réelle de
révocation de token comme fait structurant.

## Ce qui NE compte PAS comme preuve

Une route de révocation, un mécanisme de dérogation de rôle, ou un
partage de session Academy↔Good Mood inventés.

`READY_FOR_FREK_PROOF = FALSE`. Seule une certification interne
Academy (`GMD33.SKILL.*`) est en jeu — jamais une autorisation
opérationnelle réelle sur le panneau admin de
`gmfest972/goodmooddjsayd`.

## Réservation Skill ID

`GMD33.SKILL.AUTH_LIFECYCLE`, `GMD33.SKILL.ROUTE_BOUNDARY_AUDIT`,
`GMD33.SKILL.INCIDENT_RECOGNITION` — réservés dans
`70_EVIDENCE/EVIDENCE_ARCHITECTURE.md`.
