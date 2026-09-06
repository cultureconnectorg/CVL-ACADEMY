# FRK-16 — Banque N1 (formatif)

Réserve `FRK16.SKILL.*`.

1. Le vrai système "Notary & Public Audit" de MetaCVLN
   (`backend/server.py`, routes `/notarizations` et
   `/public/notarizations`, clés Ed25519) est classé `IMPLEMENTED`
   dans `COMPONENT-MATRIX.md` de `Cvln-ios-v.1`. Que prouve
   concrètement ce système ?
2. Pourquoi `proof/NOTARIAL-BOUNDARY.md` précise-t-il explicitement que
   "le mot 'notary' dans le code MetaCVLN audité nomme un rôle de clé
   de signature. Il ne désigne pas un notaire légal" ?
3. Qu'est-ce que l'ancrage externe via OpenTimestamps (`chain_hash`,
   digest SHA-256) prouve, et que ne prouve-t-il explicitement PAS
   (legal_effect, timestamp qualifié eIDAS) ?
4. Pourquoi ce système MetaCVLN ne doit-il jamais être confondu avec
   `issue_proof()` (FRK-13, stub `frek_core.py`) ni présenté comme une
   infrastructure FREK ?
5. `COMPONENT-MATRIX.md` documente honnêtement : "Notary private key
   stored unencrypted at rest." Pourquoi cette formation enseigne-t-elle
   cette limite plutôt que de la masquer ?

## Corrigé indicatif

1. Il prouve l'intégrité et l'attribution d'un enregistrement (via
   signature Ed25519 vérifiable) et offre une surface de lecture
   publique auditable — jamais un effet légal.
2. Pour éviter toute confusion avec un notariat légal réel : c'est un
   rôle technique de clé de signature, sans portée juridique (Décision
   D-007, `legal_effect` reste `"none"`).
3. L'ancrage prouve que le digest existait à un instant donné et n'a
   pas changé depuis (une fois inclus dans un bloc Bitcoin) ; il ne
   prouve jamais un horodatage qualifié eIDAS ni un effet légal.
4. `issue_proof()` est un stub UUID sans signature cryptographique ni
   ancrage — le système MetaCVLN est un système distinct, réel, non
   FREK-brandé ; les fusionner inventerait une capacité FREK
   inexistante.
5. La discipline du corpus source (repo-truth-first) exige de
   transmettre les limites documentées telles quelles — masquer cette
   limite reviendrait à fausser l'évaluation réelle du système.
