# KOR-08 — M01 — Diagnostiquer un besoin de métadonnées et son périmètre

```
MODULE_ID: KOR08-M01
COMPETENCY_ID: C1 — Diagnostiquer un besoin de métadonnées et son périmètre (vs LabelOS)
PREREQUISITES: Aucun
ASSESSMENT_LEVEL: N1
KORA_DEPENDENCY: aucune
ROLE_BOUNDARIES: ce module ne redéfinit jamais un standard détenu par LabelOS (LOS-02)
FREK_PROOF_MAPPING: FREK-WORK
ORIGIN: net-new
```

## Situation professionnelle

Le Lanbi Collective, ne connaissant pas LabelOS, envisage d'inventer
son propre système d'identifiants pour *Rasin* — un doublon qui
créerait une incompatibilité future avec les standards réels de
l'industrie.

## Objectifs d'apprentissage

- Diagnostiquer ce qui relève réellement du périmètre `KOR-08`
  (exploitation streaming) vs LabelOS (standards de catalogue label).
- Refuser de dupliquer un standard existant par méconnaissance.

## Notions essentielles

**LabelOS possède la profondeur** des standards de métadonnées de
l'industrie musicale (ISRC, ISWC, DDEX). **KORA-08 possède
l'application streaming** — comment cette métadonnée est affichée,
enrichie culturellement, et rendue découvrable pour l'auditeur. Un
diagnostic correct commence par vérifier si un standard existe déjà
avant d'en inventer un nouveau.

## Méthode

1. Identifier ce que le Lanbi Collective envisage de faire (créer un
   identifiant propre).
2. Vérifier si un standard existant (LabelOS) couvre déjà ce besoin.
3. Recommander l'usage du standard existant plutôt que l'invention.

## Exemple

Le Lanbi Collective envisage un code interne "RASIN-EP0" — ce n'est
pas un identifiant industrie reconnu (ISRC) mais peut servir de
référence interne, tant qu'il n'est pas confondu avec un véritable
ISRC.

## Cas

Le diagnostic porte sur *Rasin* réellement (`case/CASE.md`).

## Erreurs fréquentes

- Inventer un système d'identifiants sans vérifier l'existence d'un
  standard.
- Confondre une référence interne avec un identifiant industrie
  reconnu.

## Activité

Vérification de l'existence de standards pour le besoin identifié.

## Exercice

Rédiger le diagnostic de périmètre (ce qui relève de `KOR-08`, ce qui
relève de LabelOS).

## Livrable

Diagnostic de périmètre.

## Critères de réussite

- Le périmètre est clairement délimité par rapport à LabelOS.
- Aucun doublon de standard n'est proposé.

## Preuve

Diagnostic, signal `FREK-WORK`.

## Auto-évaluation

*Ai-je vérifié qu'un standard existant ne couvrait pas déjà ce
besoin ?*

## Passage au module suivant

Ce diagnostic oriente le pont vers LabelOS développé en M02.
