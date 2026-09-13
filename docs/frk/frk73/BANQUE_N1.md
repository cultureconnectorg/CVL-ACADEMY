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
5. Qu'est-ce qu'un PUF (fonction physiquement non clonable) et
   pourquoi constitue-t-il un point de départ approprié pour une
   chaîne de dérivation de clés ?
6. Pourquoi HKDF est-il utilisé entre le PUF et la clé racine (DRK)
   plutôt qu'une dérivation directe ?
7. En quoi la présence de tests passants sur `frek_crypto.py`
   (rattachés à FRK-75) ne constitue-t-elle pas, à elle seule, une
   preuve de sécurité cryptographique du schéma ?
8. Pourquoi la distinction entre AK, FK et CK (clés dérivées
   distinctes) importe-t-elle du point de vue de la sécurité, plutôt
   que d'utiliser une seule clé pour tous les usages ?

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
5. Un PUF exploite des variations physiques microscopiques uniques à
   chaque puce, impossibles à cloner — un point d'ancrage matériel
   propre à un dispositif spécifique, approprié comme racine d'une
   chaîne de dérivation liée au matériel.
6. HKDF (fonction de dérivation de clé basée sur HMAC) étend et
   renforce l'entropie brute du PUF en une clé cryptographiquement
   robuste — une dérivation directe risquerait d'exposer des biais ou
   une entropie insuffisante du signal PUF brut.
7. Des tests passants prouvent que cette implémentation produit des
   résultats attendus sur des vecteurs connus — ils ne constituent en
   rien une revue de la conception cryptographique elle-même
   (résistance aux attaques, choix de primitives, gestion des cas
   limites), qui exige un cryptographe qualifié.
8. Séparer les clés par usage limite l'impact d'une compromission :
   si une seule clé servait à tout, sa fuite compromettrait
   simultanément l'authentification, les fonctions et le chiffrement —
   la séparation contient le dommage à un seul domaine.
