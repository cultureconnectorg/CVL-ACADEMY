# FRK-73 — Banque N1 (formatif)

Réserve `FRK73.SKILL.*`. Aucun item n'est noté hors cadre de révision
experte — usage formatif uniquement tant que `NEEDS_EXPERT_REVIEW`
n'est pas levé.

1. Décris la chaîne de dérivation de clés réelle documentée dans
   `frek_crypto.py` : `PUF → HKDF → DRK → AK/FK/CK`.
2. Qu'est-ce qu'une signature ECDSA P-256 au format brut `r||s`, et
   pourquoi cet encodage canonique est-il précisé dans la
   spécification ?
3. Pourquoi cette formation ne peut-elle jamais présenter ce code
   comme « audité en production » malgré le fait qu'il soit réel et
   fonctionnel ?
4. Qu'est-ce qui devrait être vrai (nom d'expert réel, revue
   documentée) avant qu'un item de cette formation devienne
   certifiant ?

## Corrigé indicatif

1. Un PUF (fonction physiquement non clonable) alimente HKDF pour
   dériver une clé racine (DRK), elle-même dérivant les clés
   d'application/fonction/chiffrement (AK/FK/CK) — chaîne réelle
   documentée dans le code.
2. Le format brut concatène les deux composantes de signature `r` et
   `s` sans encodage ASN.1 — le message doit être encodé de façon
   canonique pour garantir la reproductibilité de la vérification.
3. Le code étant réel n'implique pas qu'il ait été revu par un
   cryptographe qualifié — la cryptographie appliquée exige une revue
   experte avant toute garantie de sécurité, quelle que soit la
   qualité apparente du code.
4. Un nom de cryptographe réel, une revue documentée du schéma de
   dérivation et de signature — rien de moins ne lève le statut
   `NEEDS_EXPERT_REVIEW`.
