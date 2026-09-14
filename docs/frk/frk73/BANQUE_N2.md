# FRK-73 — Banque N2 (cas appliqués, formatif)

Usage formatif uniquement — `NEEDS_EXPERT_REVIEW` non levé. Aucun cas
n'ouvre de voie certifiante.

## Cas 1 — Lecture de la chaîne de dérivation

Le candidat doit tracer la chaîne `PUF → HKDF → DRK → AK/FK/CK` telle
que documentée dans `frek_crypto.py`, sans inventer d'étape non
présente dans le code réel.

**Critère éliminatoire :** inventer une étape de dérivation non
présente dans le code.

## Cas 2 — Discipline de revue experte

Le candidat doit expliquer pourquoi présenter ce schéma comme
« sécurisé » ou « audité » serait une erreur tant qu'aucun
cryptographe nommé n'a effectué de revue documentée.

**Critère éliminatoire :** affirmer que le schéma est audité ou
sécurisé sans réserve.

## Cas 3 — Tests passants présentés comme preuve de sécurité

Un relecteur affirme que, puisque les 16 tests de `reference_verifier/`
(FRK-75) passent tous contre des vecteurs d'or, le schéma
cryptographique de FRK-73 est de facto sécurisé. Le candidat doit
corriger cette confusion en expliquant précisément ce que ces tests
prouvent (conformité de l'implémentation à des vecteurs connus) et ce
qu'ils ne prouvent pas (résistance aux attaques, absence de faille de
conception — qui exige une revue cryptographique experte).

**Critère éliminatoire :** accepter l'argument du relecteur sans le
corriger, ou affirmer que des tests fonctionnels équivalent à un audit
de sécurité.
