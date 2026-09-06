# CMD-15 — Banque N2 (cas appliqués)

## Cas N2-1 — Un dirigeant demande un accès au Command Center CVLN

Un dirigeant CVLN demande "peut-on se connecter au vrai Command Center
et voir le tableau de bord en direct depuis l'Academy ?" Réponds avec
les faits réels de cette session.

**Critères de notation :** confirme que `MetaCVLN` possède réellement
les routes `/command-center/overview`/`/timeline` (grep direct,
lignes 184/221), mais qu'aucune intégration n'est observée entre
`CVL-ACADEMY` et `MetaCVLN` — aucun accès réel n'existe aujourd'hui.
Élimination si le candidat affirme un accès réel possible immédiatement
ou nie l'existence réelle des routes.

## Cas N2-2 — Confusion avec `fms-os/fms`

Un stagiaire confond le `/os/command-center` de `fms-os/fms` avec le
vrai Command Center CVLN. Corrige-le avec les faits.

**Critères de notation :** explique que ce sont deux systèmes
totalement différents (l'un est un tableau de bord d'opérations de
studio, l'autre le vrai Command Center CVLN dans `MetaCVLN`) qui
partagent seulement le nom. Élimination si le candidat les fusionne ou
n'explique pas la distinction clairement.

## Cas N2-3 — "MetaCVLN est-il en production ?"

Un candidat certifié CMD-15 doit répondre honnêtement à cette question
lors d'un entretien.

**Critères de notation :** cite le propre audit de `MetaCVLN`
("aucun composant v1.0 n'est affirmé `DEPLOYED_RUNTIME`", "rien
d'audité ne dépend de lui") — jamais une affirmation de maturité
gonflée. Élimination si le candidat affirme que `MetaCVLN` est un
système de production pleinement opérationnel.
