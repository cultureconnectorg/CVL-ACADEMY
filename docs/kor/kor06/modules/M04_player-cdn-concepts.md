# KOR-06 — M04 — Player et CDN — concepts

```
MODULE_ID: KOR06-M04
COMPETENCY_ID: C4 — Comprendre player et CDN (concepts)
PREREQUISITES: M03
ASSESSMENT_LEVEL: N1
KORA_DEPENDENCY: aucune
ROLE_BOUNDARIES: aucune
FREK_PROOF_MAPPING: FREK-WORK
ORIGIN: net-new
```

## Situation professionnelle

Des auditeurs de *Rasin* dans différents pays signalent des temps de
chargement variables — comprendre le rôle du CDN (réseau de diffusion
de contenu) et du player aide à diagnostiquer si le problème vient de
la distance géographique ou d'autre chose.

## Objectifs d'apprentissage

- Comprendre le rôle d'un CDN dans la réduction de latence
  géographique.
- Comprendre les responsabilités d'un player (lecture, mise en
  mémoire tampon).

## Notions essentielles

Un **CDN** rapproche géographiquement le contenu de l'auditeur (via des
serveurs distribués) pour réduire la latence. Un **player** gère la
lecture, la mise en mémoire tampon, et l'affichage — un problème de
lecture peut venir du CDN (distance, congestion) ou du player
(bug, format non supporté), et les distinguer est essentiel au
diagnostic.

## Méthode

1. Comprendre le principe de rapprochement géographique d'un CDN.
2. Comprendre les responsabilités d'un player.
3. Documenter comment distinguer un problème CDN d'un problème player
   face à un signalement d'auditeur.

## Exemple

Un auditeur en Guyane signale une lecture saccadée alors qu'un auditeur
à Paris n'a aucun problème — indice probable d'un problème CDN
(distance), pas de player (qui affecterait tous les auditeurs
également).

## Cas

Le diagnostic porte sur les signalements réels du cas (`case/
CASE.md`).

## Erreurs fréquentes

- Confondre systématiquement problème CDN et problème player.
- Ignorer la dimension géographique dans le diagnostic.

## Activité

Analyse de plusieurs signalements géographiquement distincts.

## Exercice

Documenter comment distinguer CDN et player face à un signalement.

## Livrable

Note technique player/CDN.

## Critères de réussite

- Le rôle de chaque composant est correctement expliqué.
- La méthode de distinction est applicable à un cas réel.

## Preuve

Note, signal `FREK-WORK`.

## Auto-évaluation

*Ma méthode de diagnostic distinguerait-elle vraiment un problème CDN
d'un problème player ?*

## Passage au module suivant

Ces notions techniques informent la définition du SLA/SLO en M05.
