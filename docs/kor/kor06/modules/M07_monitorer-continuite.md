# KOR-06 — M07 — Monitorer en continu et assurer la continuité

```
MODULE_ID: KOR06-M07
COMPETENCY_ID: C7 — Monitorer en continu et assurer la continuité
PREREQUISITES: M06
ASSESSMENT_LEVEL: N2
KORA_DEPENDENCY: aucune
ROLE_BOUNDARIES: aucune
FREK_PROOF_MAPPING: FREK-WORK
ORIGIN: net-new
```

## Situation professionnelle

L'incident de M06 n'a été détecté que par un signalement du Lanbi
Collective — aucun monitoring n'aurait alerté l'équipe plus tôt. Cela
doit changer.

## Objectifs d'apprentissage

- Concevoir un plan de monitoring qui aurait détecté l'incident plus
  tôt.
- Distinguer une alerte utile d'un bruit d'alertes ignorées.

## Notions essentielles

Un **monitoring efficace** détecte un problème avant qu'un utilisateur
ne le signale, sans pour autant générer tant d'alertes qu'elles soient
ignorées ("fatigue d'alerte"). Le choix des seuils d'alerte est aussi
important que leur existence.

## Méthode

1. Identifier quel indicateur (temps de réponse, taux d'erreur) aurait
   signalé la saturation avant le signalement du créateur.
2. Fixer un seuil d'alerte réaliste, ni trop sensible ni trop tardif.
3. Documenter le plan de monitoring et son lien avec le SLA/SLO de M05.

## Exemple

Un seuil d'alerte sur le temps de réponse (>2 secondes pendant plus de
2 minutes) aurait signalé la saturation bien avant le signalement du
Lanbi Collective.

## Cas

Le plan de monitoring porte sur l'incident réel du cas (`case/
CASE.md`).

## Erreurs fréquentes

- Fixer des seuils si sensibles qu'ils génèrent une fatigue d'alerte.
- Ne relier le monitoring à aucun seuil du SLA/SLO.

## Activité

Identification de l'indicateur qui aurait détecté l'incident plus tôt.

## Exercice

Documenter le plan de monitoring complet.

## Livrable

Plan de monitoring.

## Critères de réussite

- Le plan aurait détecté l'incident de M06 plus tôt.
- Les seuils sont réalistes, pas source de fatigue d'alerte.

## Preuve

Plan, signal `FREK-WORK`.

## Auto-évaluation

*Mon plan de monitoring aurait-il vraiment détecté l'incident plus
tôt, ou est-il conçu après coup sans rigueur ?*

## Passage au module suivant

Ce plan doit encore tenir compte de la dispersion géographique du
public diaspora, traitée en M08.
