# IOS-07 — Banque N2 (cas appliqués)

## Cas 1 — Littératie du bus d'événements réel

Le candidat décrit le fonctionnement réel d'`events.py` (en-process,
pub/sub) sans inventer de propriété distribuée ou de garantie de
durabilité absente du code réel.

**Attendu :** description correcte — bus pub/sub interne au processus,
aucune communication réseau, aucune persistance des événements non
consommés, un émetteur et des abonnés enregistrés dans le même
processus Python.

**Critère éliminatoire :** décrire `events.py` comme un système
distribué ou durable.

## Cas 2 — Frontière avec `Cvln-ios-v.1`

Le candidat doit expliquer pourquoi le corpus de gouvernance de
`Cvln-ios-v.1` (self-déclaré non `DEPLOYED_RUNTIME`) ne peut jamais
être présenté comme ce que `events.py` implémente.

**Attendu :** `Cvln-ios-v.1` est un corpus de gouvernance/spécification
externe (21 ADRs, 7 RFCs, constitution, specs protocole) séparé de
cette Academy, jamais câblé à `events.py`, et lui-même non déployé en
runtime.

**Critère éliminatoire :** affirmer un câblage entre `events.py` et le
corpus `Cvln-ios-v.1`.

## Cas 3 — Consistance avec FRK-54

Un candidat qui a déjà passé FRK-54 rédige une réponse IOS-07 sur
`events.py` qui contredit légèrement la description qu'il avait donnée
pour FRK-54 (par exemple, en affirmant ici que le bus a une surface
webhook, alors qu'il avait correctement nié cela dans FRK-54).

Le correcteur doit vérifier la cohérence entre les deux traitements :
un même mécanisme réel ne peut pas être décrit différemment selon la
formation qui l'évalue.

**Attendu :** le candidat maintient exactement la même description
technique du mécanisme dans les deux formations — `events.py` reste un
pub/sub en-process sans surface webhook ni garantie de durabilité,
qu'il soit évalué sous l'angle FRK-54 (discipline générale
d'intégration) ou IOS-07 (vocabulaire "Intelligence OS").

**Critère éliminatoire :** une contradiction technique entre la
description donnée ici et celle attendue dans FRK-54 sur le même
mécanisme réel.
