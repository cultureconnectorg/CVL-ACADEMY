# FRK-08 — Banque N2

## Cas N2-1 — Audit de conformité DID

Un partenaire demande si `mint_frek_id()` est conforme W3C DID.
Réponds avec les faits réels.

**Critères de notation :** explique que non — c'est un compteur
séquentiel simple, sans document DID, sans méthode de vérification,
sans rapport avec le schéma DID. Élimination si le candidat affirme
une conformité.

## Cas N2-2 — Émission de VC

Explique comment une Verifiable Credential réelle serait émise et
vérifiée, en pratique standard W3C, sans l'attribuer à un système
CVLN.

**Critères de notation :** applique le modèle W3C VC réel
correctement — émetteur signe la credential, détenteur la conserve,
vérificateur contrôle la signature et la structure de la revendication.

## Cas N2-3 — Choix d'une méthode DID

Un projet doit choisir entre `did:web` et `did:key` pour son
identifiant. Explique le compromis réel entre les deux.

**Critères de notation :** identifie que `did:web` dépend d'un domaine
HTTPS contrôlé (simplicité opérationnelle, dépendance DNS/TLS) tandis
que `did:key` est auto-porté sans infrastructure externe
(décentralisation maximale, mais rotation de clé plus délicate).
