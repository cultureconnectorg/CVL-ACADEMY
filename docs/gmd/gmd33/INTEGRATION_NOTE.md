# GMD-33 — Integration Academy Package Note

## Réel vs. supposé

**Réel (vérifié cette session) :** `hash_password`/`verify_password`
(bcrypt), `create_token` (12h expiry), `get_current_admin`
(dual-source: Bearer header or cookie, strict `role=="admin"` check,
distinct expired/invalid error handling) — `server.py:36-70`; auth
routes `server.py:261-278`. **No token revocation mechanism exists**
in the audited code — a real, citable gap this formation teaches
candidates to recognize and escalate, never invent around.

**Supposé :** un lien `GMD33.SKILL.*` réel dans le runtime de cette
Academy — inexistant.

## Dépendances

- `GOOD_MOOD_DJ_SAYD_RECONCILIATION.md`, `EVIDENCE_ARCHITECTURE.md`,
  `ECONOMIC_MODEL.md`, GMD-21 (prérequis) ; toutes les autres
  formations GMD-22→32 dépendent de cette frontière d'authentification.

## Ce qu'une future intégration exigerait

1. Entrée `GMD33` dans le registre de certification.
2. Surface candidat réelle.
3. Décision séparée sur les identifiants admin réels — jamais plus
   sensible que pour cette formation spécifiquement.

## Status

`STATUS = PACKAGE_COMPLETE_FOR_GMD33` — **13/13 formations GMD-21→33
sont maintenant au niveau package canonique complet.** GMD-34 reste
`BLOCKED_PRODUCT_DEPENDENCY` par construction (`gmd34/GAP.md`).
`FULLY_COMPLETE` non déclaré pour aucune des 13 — requiert un passage
réel vérifié par un humain.
