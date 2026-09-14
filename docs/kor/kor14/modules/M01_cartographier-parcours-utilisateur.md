# KOR-14 — M01 — Cartographier le parcours utilisateur de bout en bout

```
MODULE_ID: KOR14-M01
COMPETENCY_ID: C1 — Cartographier le parcours utilisateur de bout en bout
PREREQUISITES: Aucun
ASSESSMENT_LEVEL: N1
KORA_DEPENDENCY: aucune ; distinct du canal d'acquisition (KOR-09)
ROLE_BOUNDARIES: aucune
FREK_PROOF_MAPPING: READY_FOR_FREK_PROOF = FALSE
ORIGIN: net-new
```

## Situation professionnelle

Djems prend en charge l'expérience produit d'Anba Tonèl Host sans
cartographie existante du parcours réel d'un auditeur — impossible de
concevoir quoi que ce soit (M02-M09) sans d'abord voir où se situent
les frictions.

## Objectifs d'apprentissage

- Cartographier le parcours actuel d'un utilisateur type, des points
  de friction aux moments de valeur.
- Distinguer le parcours in-app (`KOR-14`) du canal qui a amené
  l'utilisateur (`KOR-09`).

## Notions essentielles

Les **étapes typiques** d'un parcours incluent l'arrivée, la
découverte, l'écoute, le retour. La **frontière avec `KOR-09`** est
nette : le canal qui amène l'utilisateur dans l'application relève de
`KOR-09` (acquisition), tandis que tout ce qui se passe une fois
l'utilisateur arrivé relève de `KOR-14` (expérience in-app).

## Méthode

1. Tracer les étapes réelles du parcours d'un auditeur diaspora type.
2. Identifier les points de friction à chaque étape.
3. Vérifier que la cartographie ne remonte pas jusqu'au canal
   d'acquisition (`KOR-09`).

## Exemples

La carte montre qu'un auditeur diaspora arrive via un lien partagé
(`KOR-09`, hors périmètre), puis peine à retrouver *Rasin* une fois
dans l'application (`KOR-14`, point de friction réel à traiter). À
l'inverse, inclure dans la cartographie une analyse de pourquoi le
lien de partage n'a pas généré plus de trafic empiéterait sur le
mandat de `KOR-09` — la carte doit commencer à l'arrivée dans
l'application, pas avant.

## Cas

Épisode A — cartographier le parcours actuel d'un auditeur diaspora
type vers *Rasin* (`case/CASE.md`).

## Erreurs fréquentes

- Remonter la cartographie jusqu'au canal d'acquisition, empiétant sur
  `KOR-09`.
- Identifier des étapes génériques sans lien avec le parcours réel de
  *Rasin*.
- Omettre un point de friction réel pourtant observable.

## Activité

Traçage des étapes réelles du parcours d'un auditeur diaspora type.

## Exercice

Produire la carte de parcours avec points de friction identifiés.

## Livrable

Carte de parcours (`EVIDENCE_TYPE = USER_JOURNEY_MAP`).

## Critères de réussite

- Le parcours commence à l'arrivée dans l'application, pas avant.
- Chaque point de friction réel est identifié.
- La frontière avec `KOR-09` est respectée.

## Preuve

Carte de parcours, `READY_FOR_FREK_PROOF = FALSE`.

## Auto-évaluation

*Ma cartographie reste-t-elle dans le périmètre in-app, ou ai-je
empiété sur le canal d'acquisition ?*

## Passage au module suivant

Les points de friction identifiés orientent la conception de la
discovery et du feed en M02.
