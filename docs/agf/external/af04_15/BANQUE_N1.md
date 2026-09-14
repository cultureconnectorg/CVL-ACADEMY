# AF-04→15 — Banque N1 (formatif)

Réserve `AF0415.SKILL.AGENT_ENGINEERING_DISCIPLINES.L1`.

1. Liste les 12 disciplines réelles couvertes par ce cluster (usage
   d'outils, mémoire, coordination multi-agent, orchestration, HITL,
   évaluation, observabilité, sécurité, sûreté, fiabilité,
   gouvernance, opérations de production).
2. Pourquoi chacune de ces disciplines est-elle un savoir de marché
   réel et actuel, indépendant de toute implémentation CVLN ?
3. `agent_factory.py` est un simple client de transport de chat avec
   une seule persona — pourquoi cela signifie-t-il qu'aucune des 12
   disciplines n'y est implémentée ?
4. Pourquoi serait-il une erreur éliminatoire d'affirmer qu'un système
   CVLN implémente l'une de ces 12 disciplines ?
5. Quelle est la différence entre l'usage d'outils (discipline 1) et
   l'orchestration (discipline 4) ? Pourquoi sont-ce deux disciplines
   distinctes plutôt qu'une seule ?
6. Un candidat cite le vrai `CVLNAgentfactory` externe (`frekcore/`,
   225 fichiers, Agent Definition Language, cycle de vie à 7 étapes)
   comme preuve que certaines de ces 12 disciplines existent
   réellement dans l'écosystème CVLN. Est-ce légitime, et à quelle
   condition ?
7. Pourquoi la sécurité d'agent (discipline 8) et la sûreté d'agent
   (discipline 9) sont-elles traitées comme deux disciplines
   distinctes plutôt qu'une seule "protection" générique ?
8. Un candidat affirme qu'`agent_factory.py` "prévoit" d'implémenter
   une gouvernance d'agent dans une future version. Pourquoi cette
   formulation reste-t-elle problématique même présentée comme une
   intention future plutôt qu'un état actuel ?

## Corrigé indicatif

1. Usage d'outils/function calling, architecture de mémoire d'agent,
   coordination multi-agent, patrons d'orchestration, conception
   human-in-the-loop, méthodologie d'évaluation d'agent, observabilité
   des systèmes agentiques, sécurité d'agent, sûreté d'agent,
   ingénierie de fiabilité, gouvernance d'agent, opérations de
   production pour systèmes agentiques.
2. Ce sont des disciplines établies et documentées dans l'industrie
   IA/agent actuelle, enseignables et vérifiables indépendamment de
   tout système CVLN précis.
3. `agent_factory.py` n'a ni appel d'outil, ni mémoire, ni
   coordination, ni orchestration, ni harnais d'évaluation, ni
   observabilité, ni couche de gouvernance — un simple transport de
   chat à une persona ne peut porter aucune de ces 12 disciplines.
4. Cela affirmerait une capacité technique inexistante pour chacune de
   ces disciplines — contraire à la discipline `CAPABILITY_NOT_
   IMPLEMENTED`.
5. L'usage d'outils porte sur la décision et l'exécution d'un appel de
   fonction unique par un agent ; l'orchestration porte sur la
   séquence, la ramification, et la supervision de flux impliquant
   potentiellement plusieurs agents ou plusieurs étapes — deux
   niveaux d'abstraction différents.
6. C'est légitime uniquement comme preuve de contexte de marché, en le
   qualifiant explicitement de système externe séparé, jamais comme ce
   qu'`agent_factory.py` implémente ou auquel il est câblé — la même
   discipline de double frontière que pour BRN-15/`/brain/ask`.
7. La sécurité porte sur la défense contre des acteurs malveillants
   (injection de prompt, exfiltration via appel d'outil) ; la sûreté
   porte sur la limitation du comportement de l'agent indépendamment de
   toute malveillance (garde-fous, portée de permission, interrupteur
   d'arrêt) — deux préoccupations distinctes même si les mécanismes se
   recoupent parfois.
8. Parce que certifier une intention future non implémentée revient à
   enseigner une capacité qui n'existe pas dans le code réel — la
   discipline porte strictement sur ce qui existe aujourd'hui, jamais
   sur une roadmap non observée dans le dépôt.
