# FRK-10 — Banque N1 (littératie, non certifiante)

Ces questions vérifient la littératie factuelle et la discipline de
juridiction. Elles ne délivrent aucun Skill ID et ne constituent pas
une certification (voir `EVIDENCE_MODEL.md`).

## Cadre réglementaire

1. Cite le cadre réglementaire réel enseigné. (Règlement (UE)
   2024/1183, révision du règlement eIDAS de 2014 — "eIDAS2" — entré
   en vigueur en mai 2024)
2. Ce cadre s'applique-t-il universellement ? (Non — spécifique à la
   juridiction UE/EEE, jamais enseigné comme standard mondial)
3. Que doit fournir chaque État membre selon eIDAS2 ? (Au moins un
   EUDI Wallet aux citoyens et résidents, selon un calendrier fixé par
   des actes d'exécution sous l'Architecture Reference Framework (ARF)
   de la Commission européenne)

## Modèle de données du wallet

4. Que signifie PID dans ce cadre ? (Person Identification Data — les
   attributs d'identité de base émis par un État membre)
5. Que signifie EAA, et que signifie QEAA ? (Electronic Attestation of
   Attributes — attestation électronique d'attribut ; Qualified EAA —
   émise par un prestataire qualifié/certifié)
6. Le wallet est-il une base de données d'identité centralisée ? (Non
   — c'est un conteneur contrôlé par le détenteur (holder-controlled),
   pas une base centrale)

## Modèle de présentation et SD-JWT

7. Comment fonctionne la présentation à un relying party ? (Le relying
   party demande des attributs précis ; le détenteur consent par
   requête ; seuls les attributs demandés et consentis sont renvoyés)
8. Que signifie SD-JWT techniquement ? (Selective Disclosure JWT —
   spécification IETF où chaque claim est engagé sous forme de
   "disclosure" hachée plutôt qu'inlinée directement dans le JWT)
9. Comment un détenteur prouve-t-il la possession sans tout révéler ?
   (Il révèle un sous-ensemble de disclosures accompagné d'un
   key-binding JWT prouvant la possession, sans exposer les claims non
   divulguées)
10. Que signifie SD-JWT VC ? (SD-JWT-based Verifiable Credentials — le
    profil concret en cours de standardisation pour les attestations
    EUDI Wallet)

## Discipline de juridiction et de certification

11. Cette formation est-elle certifiable sans révision d'expert ? (Non
    — `NEEDS_EXPERT_REVIEW` non résolu ; seule une vérification de
    littératie existe aujourd'hui, sans délivrance de Skill ID)
