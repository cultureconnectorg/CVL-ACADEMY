# KOR-01 — M10 — Distribution — hébergeurs, RSS, DSP

```
MODULE_ID: KOR01-M10
COMPETENCY_ID: C10 — Distribuer via hébergeurs/RSS/DSP réels du marché
PREREQUISITES: M09
ASSESSMENT_LEVEL: N2
KORA_DEPENDENCY: aucune — outils marché réels utilisés, aucune plateforme KORA opérationnelle requise (KOR-0002 §2.5, §4 tension #10)
ROLE_BOUNDARIES: ce module ne couvre pas l'exploitation d'une plateforme de streaming (KOR-06, non construit) ni la négociation de droits de diffusion territoriaux (KOR-07, non construit)
FREK_PROOF_MAPPING: FREK-CERT (hérité de seed_modules.py:282-289)
ORIGIN: legacy M07 (KEEP), composante configuration technique — KOR-0002 §2.6
```

## Situation professionnelle

L'épisode est terminé. Sans configuration technique correcte
(hébergement, flux RSS, soumission aux plateformes d'écoute), il reste
un fichier sur un disque dur. Le collectif doit choisir des outils du
marché réels et gratuits ou peu coûteux, sans dépendre d'une
plateforme KORA qui n'existe pas encore de façon opérationnelle.

## Objectifs d'apprentissage

- Comprendre le rôle d'un hébergeur podcast et d'un flux RSS dans la
  distribution.
- Configurer un flux RSS valide et le soumettre aux plateformes
  d'écoute principales du marché.
- Distinguer distribution technique (ce module) et publication
  éditoriale (M11).

## Notions essentielles

Un **hébergeur podcast** stocke les fichiers audio et génère un **flux
RSS** — un fichier structuré qui décrit chaque épisode (titre,
description, date, lien audio). Les **DSP** (plateformes d'écoute)
lisent ce flux pour afficher le podcast à leurs utilisateurs : on ne
"publie" pas un podcast sur chaque plateforme séparément, on soumet un
flux RSS une fois, que chaque plateforme relit ensuite automatiquement.

## Méthode

1. Choisir un hébergeur podcast réel du marché adapté à un collectif
   sans budget (offre gratuite ou très peu coûteuse).
2. Configurer le flux RSS (métadonnées de série : titre, description,
   catégorie, visuel).
3. Soumettre ce flux aux principales plateformes d'écoute et vérifier
   sa validité technique (flux bien formé, lisible).

## Exemples

Un flux RSS mal formé (balise manquante, encodage incorrect) peut être
rejeté silencieusement par une plateforme sans message d'erreur clair —
d'où l'importance de valider techniquement le flux avant de le
soumettre partout.

## Cas

La distribution de l'épisode 0 de *Rasin* (`case/CAS_FIL_ROUGE.md`) se
fait via un hébergeur réel du marché, choisi pour son coût nul ou
minimal — le candidat documente ce choix précis, pas un choix
hypothétique.

## Erreurs fréquentes

- Confondre "publier sur une plateforme" avec "soumettre un flux RSS
  valide une seule fois".
- Ne pas valider techniquement le flux RSS avant soumission.
- Choisir un hébergeur payant hors de portée du budget réel du
  collectif, sans avoir vérifié les alternatives gratuites.

## Activité

Comparaison de deux ou trois hébergeurs podcast réels du marché sur le
critère du coût et des fonctionnalités essentielles pour un collectif
sans budget.

## Exercice

Configurer (ou documenter la configuration complète) un flux RSS pour
*Rasin* et vérifier sa validité technique.

## Livrable

Configuration de distribution : hébergeur choisi et justifié + flux RSS
valide + preuve de soumission à au moins une plateforme d'écoute.

## Critères de réussite (PASS_CRITERIA)

- Le choix d'hébergeur est justifié par le critère budgétaire réel du
  collectif.
- Le flux RSS est techniquement valide (vérifié, pas supposé).
- Aucune dépendance à une plateforme KORA non opérationnelle n'est
  introduite.

## Preuve (EVIDENCE)

Configuration + flux RSS + preuve de soumission, conservés dans le
registre de production — signal `FREK-CERT`.

## Auto-évaluation

*Ai-je vraiment vérifié la validité technique de mon flux, ou supposé
qu'il fonctionnait ? Mon choix d'hébergeur est-il tenable dans la durée
avec le budget du collectif ?*

## Passage au module suivant

Le flux techniquement configuré ici est maintenant prêt à recevoir les
métadonnées éditoriales de publication traitées en M11.
