# KOR-11 — M05 — Identifier fraude et spam

```
MODULE_ID: KOR11-M05
COMPETENCY_ID: C5 — Identifier fraude et spam
PREREQUISITES: M04
ASSESSMENT_LEVEL: N1
KORA_DEPENDENCY: aucune
ROLE_BOUNDARIES: aucune
FREK_PROOF_MAPPING: READY_FOR_FREK_PROOF = FALSE
ORIGIN: net-new
```

## Situation professionnelle

Un compte se prépare à imiter Marc-Andy pour solliciter des paiements
de sponsors (épisode C, traité en M06) — avant d'agir, Widlène doit
savoir reconnaître les signaux de fraude/spam sans multiplier les faux
positifs sur des comptes légitimes.

## Objectifs d'apprentissage

- Identifier des patterns de fraude/spam réels.
- Éviter de multiplier les faux positifs sur des comptes légitimes.

## Notions essentielles

Les **signaux typiques** de fraude/spam incluent un volume anormal, du
contenu dupliqué, des liens suspects, des demandes de paiement hors
canal officiel. Les **faux positifs fréquents** touchent des créateurs
actifs multi-plateformes ou menant des campagnes de promotion
légitimes — un volume élevé n'est pas en soi un signal de fraude s'il
s'explique par une activité réelle.

## Méthode

1. Recenser les signaux typiques de fraude/spam présents.
2. Vérifier chaque signal contre une explication légitime possible
   avant de conclure.
3. Documenter la distinction entre compte suspect et compte légitime
   actif.

## Exemples

Un compte sollicitant un paiement via un lien externe non officiel,
avec un nom très proche de "Marc-Andy" mais légèrement modifié,
présente plusieurs signaux cumulés de fraude. À l'inverse, un compte
légitime de Marc-Andy publiant soudainement beaucoup de contenu parce
qu'il mène une campagne de promotion (`KOR-09`/M08) présenterait un
volume élevé sans qu'il s'agisse de spam — le volume seul ne suffit
jamais à conclure.

## Cas

Préparation de l'épisode C (faux compte imitant Marc-Andy) (`case/
CASE.md`).

## Erreurs fréquentes

- Conclure à la fraude sur un seul signal isolé, sans recouper.
- Traiter un volume élevé d'activité légitime comme un signal de spam.
- Ignorer une demande de paiement hors canal officiel parce que le
  reste du profil semble normal.

## Activité

Identification des signaux de fraude dans un jeu de comptes simulés.

## Exercice

Identifier les signaux de fraude dans un jeu de comptes simulés,
distinguer le vrai compte du faux.

## Livrable

Note de détection (`EVIDENCE_TYPE = FRAUD_DETECTION_NOTE`).

## Critères de réussite

- Les signaux identifiés sont recoupés, pas isolés.
- Un compte légitime actif n'est pas classé à tort comme suspect.
- La demande de paiement hors canal est explicitement relevée si
  présente.

## Preuve

Note de détection, `READY_FOR_FREK_PROOF = FALSE`.

## Auto-évaluation

*Ai-je recoupé plusieurs signaux avant de conclure, ou me suis-je fié
à un seul indice ?*

## Passage au module suivant

Le faux compte identifié ici est traité comme usurpation d'identité en
M06.
