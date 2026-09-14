# AF-04→15 — Banque N2 (cas appliqués)

## Cas 1 — Conception d'une discipline agentique

Le candidat choisit une des 12 disciplines (ex. observabilité pour
systèmes agentiques) et conçoit une architecture marché-générale
correspondante, sans référence à un système CVLN précis.

**Attendu :** une conception réaliste et complète (ex. pour
l'observabilité : traçage des appels d'outils, journalisation des
décisions, tableau de bord des chaînes de raisonnement) documentée
comme discipline générale, sans jamais présupposer une infrastructure
CVLN qui n'existe pas.

**Critère éliminatoire :** proposer une conception qui présuppose une
infrastructure CVLN existante.

## Cas 2 — Discipline CVLN-gap systématique

Le candidat doit rédiger une note confirmant qu'`agent_factory.py`
n'implémente aucune des 12 disciplines listées, en citant sa nature
réelle (transport de chat à une persona).

**Attendu :** une note précise et honnête, citant `chat_reply()`/
`mentor_reply()` comme l'unique surface réelle du fichier, sans
extension ni charité rédactionnelle envers une capacité qui n'existe
pas.

**Critère éliminatoire :** affirmer qu'`agent_factory.py` implémente
l'une des 12 disciplines.

## Cas 3 — Contexte de marché vs. substrat opérant

Un candidat doit documenter, pour une des 12 disciplines de son choix,
un exemple réel de l'industrie externe à CVLN (ex. le vrai
`CVLNAgentfactory`/`frekcore/` avec son Agent Definition Language et
son cycle de vie à 7 étapes) comme preuve que la discipline existe et
est mature ailleurs dans l'écosystème — sans jamais présenter ce
système externe comme quelque chose que cette Academy opère ou auquel
elle est câblée.

**Attendu :** une citation honnête et correctement bornée du système
externe, clairement distinguée de l'état réel de cette Academy
(`agent_factory.py`, transport de chat à une persona, sans lien
observé avec le système externe cité).

**Critère éliminatoire :** présenter le système externe cité comme
opéré par, ou câblé à, cette Academy.
