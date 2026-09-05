# KOR-10 — M08 — Appliquer Wallet/JCC au modèle économique

```
MODULE_ID: KOR10-M08
COMPETENCY_ID: C8 — Appliquer Wallet/JCC au modèle économique
PREREQUISITES: M07
ASSESSMENT_LEVEL: N1
KORA_DEPENDENCY: KORA_CURRENT_CAPABILITY — Wallet/JCC réel et local (wallet/models.py:44-46, wallet/service.py:49, wallet/passes.py)
ROLE_BOUNDARIES: aucune
FREK_PROOF_MAPPING: FREK-LINK
ORIGIN: net-new
```

## Situation professionnelle

Contrairement à la plupart des autres mécanismes explorés dans ce
référentiel, Wallet/JCC est **réel et déjà câblé** dans ce repo — le
seul domaine du tableau Founder avec une implémentation locale réelle
(`KOR-0001` §4). Le modèle économique de *Rasin* peut donc s'appuyer
dessus de façon concrète, pas seulement conceptuelle.

## Objectifs d'apprentissage

- Comprendre le mécanisme réel Wallet/JCC (`jcc_balance`).
- Explorer comment le partage de valeur (M05) pourrait s'appuyer sur
  ce mécanisme réel plutôt qu'un système fictif.

## Notions essentielles

**Wallet** (`wallet/models.py`) gère un solde `jcc_balance` réel par
compte utilisateur ; `wallet/service.py` permet de créditer ce solde.
C'est le **seul mécanisme réel** parmi les options économiques
explorées dans ce référentiel — contrairement au sponsoring (informel)
ou aux royalties (incertaines), Wallet/JCC existe et fonctionne déjà
dans ce repo.

## Méthode

1. Comprendre le mécanisme réel de `jcc_balance`.
2. Explorer comment il pourrait matérialiser une part du partage de
   valeur de M05 (sans construire de nouveau code — exploration
   conceptuelle sur la base réelle).
3. Documenter cette exploration en citant précisément les fichiers
   réels concernés.

## Exemple

Une part du revenu de sponsoring pourrait, en théorie, être créditée
aux contributeurs via `jcc_balance` — une exploration réaliste puisque
le mécanisme existe déjà, contrairement à un système fictif inventé.

## Cas

L'exploration porte sur le modèle économique réel du cas (`case/
CASE.md`).

## Erreurs fréquentes

- Traiter Wallet/JCC comme un système fictif alors qu'il est réel.
- Proposer une implémentation technique (hors mandat — ceci reste une
  exploration pédagogique, pas un développement).

## Activité

Étude du mécanisme réel `jcc_balance`.

## Exercice

Documenter comment le partage de valeur pourrait s'y appuyer.

## Livrable

Note Wallet/JCC, citant les fichiers réels.

## Critères de réussite

- Le mécanisme est décrit fidèlement, avec citation des fichiers réels.
- Aucune implémentation technique n'est proposée (hors mandat
  pédagogique).

## Preuve

Note, signal `FREK-LINK`.

## Auto-évaluation

*Ma note cite-t-elle les fichiers réels, ou décrit-elle un système
imaginé ?*

## Passage au module suivant

Le terme CVE, parfois associé à ces mécanismes, doit être clarifié
sans invention en M09.
