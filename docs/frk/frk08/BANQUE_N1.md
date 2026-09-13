# FRK-08 — Banque N1 (formative, M1→M3)

## M1 — DID method fundamentals

1. Cite les 2 standards W3C réels enseignés. (DID — Decentralized
   Identifier, VC — Verifiable Credentials)
2. Quelle est la syntaxe générale d'un DID ? (`did:method:identifier`
   — par exemple `did:web:example.com` ou `did:key:z6Mk...`)
3. Que contient un document DID ? (L'`id` du DID, ses méthodes de
   vérification — clés publiques —, et ses points de terminaison de
   service)
4. Pourquoi un DID est-il résolvable indépendamment d'un registraire
   unique ? (La résolution dépend de la méthode DID choisie — did:web
   résout via HTTPS, did:key est auto-porté sans registre —, jamais
   d'une seule autorité centrale imposée par le standard lui-même)

## M2 — Verifiable Credentials issuance/verification model

5. Quels sont les 3 rôles du modèle VC ? (Émetteur/issuer, détenteur/
   holder, vérificateur/verifier)
6. Quelle est la différence entre émission et présentation d'une
   credential ? (L'émission crée la credential complète pour le
   détenteur ; la présentation peut divulguer une preuve dérivée sans
   remettre la credential entière)
7. Qu'est-ce que la divulgation sélective ? (Une technique réelle
   permettant au détenteur de prouver certains attributs d'une
   credential sans révéler les autres)

## M3 — discipline de gap CVLN

8. `mint_frek_id()` implémente-t-il un schéma DID W3C ? (Non — simple
   compteur séquentiel formaté en chaîne)
9. Un candidat peut-il présenter `frek_core.py` comme conforme W3C
   DID ? (Non — élimination automatique si affirmé)
10. Que manque-t-il précisément à `mint_frek_id()` pour être un DID ?
    (Aucun document DID, aucune méthode de vérification, aucun schéma
    d'identifiant résolvable)
11. FRK-08 est prérequis de quelle formation ? (FRK-09, Identity
    Lifecycle, Recovery & Reconciliation)
