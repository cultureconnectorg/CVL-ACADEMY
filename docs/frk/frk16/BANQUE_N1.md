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
6. Que signifie précisément l'état `pending` dans la machine à états
   d'ancrage (`pending`/`confirmed`/`offline`/`unavailable`), et
   pourquoi un digest à cet état ne constitue-t-il pas encore une
   preuve d'ancrage confirmée ?
7. Pourquoi la surface de lecture publique (`/public/notarizations`)
   renforce-t-elle la vérifiabilité du système sans pour autant lui
   conférer un quelconque effet légal ?
8. En quoi le fait que ce système ait été découvert par audit direct
   de `Cvln-ios-v.1` (plutôt que dans le corpus initialement consulté)
   illustre-t-il la discipline repo-truth-first de cette Academy ?

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
6. `pending` signifie que le digest a été soumis à un fournisseur
   d'ancrage mais n'est pas encore inclus dans un bloc confirmé — sans
   confirmation, aucune garantie d'immutabilité temporelle n'est
   encore établie.
7. La lecture publique permet à tout tiers de vérifier
   indépendamment une signature et une notarisation — cette
   vérifiabilité technique reste orthogonale à toute reconnaissance
   légale, qui exigerait un cadre juridique distinct.
8. Cela illustre que l'absence de preuve dans un corpus consulté ne
   vaut jamais absence de système réel — la discipline exige de
   vérifier directement les repos pertinents avant de conclure à un
   `BLOCKED_PRODUCT_DEPENDENCY`, plutôt que de s'arrêter à une
   première réconciliation incomplète.
