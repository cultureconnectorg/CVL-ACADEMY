# AF-01→03 — Banque N1 (formatif)

Réserve `AF0103.SKILL.*`.

1. Qu'est-ce que la conception de prompt/persona en ingénierie d'agent
   IA, et pourquoi est-ce une discipline distincte de l'orchestration
   multi-agent ?
2. Le vrai `ASSISTANT_PERSONAS` de cette Academy (`ai_assistant.py`)
   configure les personas comme des **données**, pas des branches de
   code. Pourquoi ce patron est-il un bon exemple d'ingénierie de
   persona, indépendamment de la simplicité du système ?
3. Pourquoi cette formation ne doit-elle jamais impliquer que le
   système de persona de cette Academy relève de l'orchestration
   multi-agent, de l'usage d'outils, ou de la mémoire ?
4. Donne un exemple de principe d'architecture de system prompt
   (séparation instructions/contexte/contraintes) indépendant de tout
   système CVLN.
5. Pourquoi le fait que `ASSISTANT_PERSONAS` ne compte que 4 personas
   réelles (étudiant/formateur/jury/correcteur) ne limite-t-il en rien
   la validité du principe persona-comme-donnée qu'il illustre ?
6. Que se passerait-il concrètement, en termes de modification de
   code, si une cinquième persona devait être ajoutée à un système
   encodé en branches conditionnelles plutôt qu'en données ?

## Corrigé indicatif

1. La conception de prompt/persona définit le rôle et le comportement
   d'un agent unique ; l'orchestration multi-agent coordonne plusieurs
   agents entre eux — deux disciplines à des altitudes différentes.
2. Encoder les personas comme données (dictionnaire de configuration)
   plutôt que comme branches conditionnelles rend le système extensible
   sans modification de code — un vrai principe d'ingénierie, illustré
   ici sur un cas réel et simple.
3. Le système réel de cette Academy n'a qu'une persona opérationnelle
   (`mentor_reply()`) — l'orchestration/outils/mémoire sont des
   disciplines distinctes couvertes ailleurs (`af04_15`), jamais
   implémentées ici.
4. Séparer clairement les instructions de rôle, le contexte
   dynamique injecté, et les contraintes de sortie dans un system
   prompt — principe général, applicable à tout système d'agent.
5. Le principe d'ingénierie (extensibilité sans modification de code)
   reste valable quel que soit le nombre de personas — 4 personas
   réelles suffisent à démontrer le patron, la validité du principe
   n'est pas proportionnelle à l'échelle du système qui l'illustre.
6. Un système en branches conditionnelles exigerait d'ajouter une
   nouvelle branche de code (avec tests, revue, déploiement) pour
   chaque nouvelle persona ; un système en données permettrait
   d'ajouter une entrée de configuration sans toucher au code
   exécutable.
