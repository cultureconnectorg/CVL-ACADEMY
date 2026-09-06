# AF-X-03 — Banque N1 (formatif)

Réserve `AFX03.SKILL.*`.

1. Quels sont les deux vrais blocs de construction cités dans cette
   formation, et pourquoi sont-ils réels malgré l'absence de câblage
   entre eux ?
2. Pourquoi le vrai ADL de `CVLNAgentfactory` (`AGT-\d{3}`, semver,
   cycle de vie à 7 étapes) est-il cité comme preuve que le concept de
   « qualification d'agent » est réel dans l'écosystème, sans jamais
   affirmer que cette Academy l'utilise ?
3. Pourquoi cette formation est-elle qualifiée de « pont le mieux
   ancré parmi les 9 ponts AF-X » — qu'est-ce qui la distingue des
   autres ponts moins ancrés ?
4. Que faudrait-il construire concrètement pour que ce pont existe
   réellement — pourquoi cette liste reste-t-elle documentée, jamais
   construite ?

## Corrigé indicatif

1. Le moteur de compétence/certification de l'Academy (Skill IDs,
   modèles de preuve) et le système de personas (`ai_assistant.py`)
   existent tous deux réellement — mais aucun câblage ne les relie à
   un concept de « qualification d'agent ».
2. Le cycle de vie ADL prouve que l'idée de qualifier formellement un
   agent est réelle et substantielle ailleurs dans l'écosystème — mais
   cela ne dit rien sur ce que cette Academy fait réellement.
3. Les deux blocs de construction (moteur de compétence, personas)
   sont tous deux réels et directement vérifiables dans le code de
   cette Academy — contrairement à d'autres ponts AF-X qui manquent
   même l'un des deux côtés.
4. Un mapping explicite Skill ID ↔ étape de cycle de vie ADL, une API
   de qualification, un mécanisme de validation — rien de tout cela
   n'existe aujourd'hui ; documenté comme exigence future, jamais
   construit faute de câblage réel.
