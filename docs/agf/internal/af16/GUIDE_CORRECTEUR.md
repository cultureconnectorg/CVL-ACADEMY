# AF-16 — Guide Correcteur

## Avant de noter

Relis `REFERENTIAL.md` §Objectives et §Modules — en particulier la
frontière avec `CVLNAgentfactory` et la discipline anti-invention.

## Ce que tu vérifies en priorité

1. La description de `chat_reply()`/`mentor_reply()` est-elle exacte,
   sans logique de persona inventée ?
2. Le candidat invente-t-il un registre, une mission, ou un rollback,
   même présenté comme en cours de développement ? Éliminatoire si
   oui.
3. La frontière avec le vrai `CVLNAgentfactory` est-elle explicite et
   correcte (échelle, absence d'intégration observée) ?
4. Si une proposition future est présentée (Cas 3 de `BANQUE_N2.md`),
   est-elle clairement qualifiée d'hypothétique ?

## Ce que tu ne fais pas

Tu ne notes jamais sur une description élégante qui affirme malgré
tout, même en passant, qu'un registre ou une intégration existe — la
règle éliminatoire prime toujours.

## Score

Utilise la grille 0–4 et le tableau de compétences de
`ASSESSMENT_AND_RUBRIC.md`. Le seuil de passage est ≥2.5/4.
