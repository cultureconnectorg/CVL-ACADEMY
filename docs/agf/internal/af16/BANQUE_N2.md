# AF-16 — Banque N2 (cas appliqués)

## Cas 1 — Trace d'un appel `chat_reply()`/`mentor_reply()`

Le candidat reçoit une séquence d'appel représentative et doit décrire
précisément ce que fait chaque fonction, sans inventer de logique de
routage de persona qui n'existe pas dans le code réel.

**Attendu :** description exacte — `chat_reply()` transporte le
message vers Claude sans logique de persona ; `mentor_reply()` appelle
`chat_reply()` avec la configuration figée de "Mentor CVLN".

**Critère éliminatoire :** inventer une logique de sélection de
persona autre que la persona unique "Mentor CVLN".

## Cas 2 — Frontière avec `CVLNAgentfactory`

Le candidat doit expliquer pourquoi le vrai ADL/cycle de vie/gates de
`CVLNAgentfactory` ne peut jamais être présenté comme ce que cette
Academy opère réellement, malgré leur proximité conceptuelle.

**Attendu :** une explication claire de la différence d'échelle
(2 fonctions vs. 225 fichiers/143 routes/ADL/cycle de vie à 7 étapes)
et de l'absence d'intégration observée entre les deux.

**Critère éliminatoire :** affirmer qu'une intégration existe entre
`CVLNAgentfactory` et cette Academy.

## Cas 3 — Proposition hypothétique qualifiée

Un candidat, invité à imaginer une évolution future de
`agent_factory.py`, propose l'ajout d'un registre de personas
multiples avec un mécanisme de rollback en cas d'échec de génération.

Le correcteur doit vérifier que cette proposition est présentée
strictement comme une idée future, jamais comme un état actuel ou en
cours de développement, et que le candidat identifie correctement
qu'aucune trace de ce travail n'existe dans le code aujourd'hui.

**Attendu :** proposition clairement qualifiée d'hypothétique, avec
mention explicite qu'elle ne correspond à rien d'observé dans le dépôt
actuel.

**Critère éliminatoire :** présenter la proposition comme un
développement déjà entamé ou partiellement réalisé.
