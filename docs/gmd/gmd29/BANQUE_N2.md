# GMD-29 — Banque N2 (cas appliqués)

## Cas N2-1 — Demande de campagne en coréen

Un partenaire international demande une campagne en coréen pour un
segment de fans `"kr"`. Que réponds-tu, avec le code réel ?

**Critères de notation:** signale que la clé `"kr"` existe bien dans
`copy`, mais son contenu réel est en **créole haïtien**, pas en
coréen — ce n'est donc pas une vraie prise en charge du coréen.
Recommande de créer une vraie traduction coréenne si le besoin est
réel, plutôt que de prétendre que `"kr"` la fournit déjà. Élimination
si le candidat affirme que le coréen est supporté sans vérifier le
contenu réel de la clé.

## Cas N2-2 — Fan désinscrit puis re-subscrit

Un fan se désinscrit (aucune route de désinscription n'est listée dans
le code audité), puis tente de se réinscrire via `POST /newsletter`.
Que se passe-t-il réellement ?

**Critères de notation:** signale d'abord qu'aucune route de
désinscription n'a été observée dans `server.py` — si le candidat en
invente une, élimination automatique. Sur la ré-inscription : si le
document existe toujours dans `db.newsletter` (jamais supprimé faute
de route de désinscription), `POST /newsletter` renverrait `{"ok":
true, "already": true}`, pas une vraie nouvelle inscription — un
constat honnête à faire, pas un problème à résoudre en inventant un
mécanisme.

## Cas N2-3 — Export demandé pour un rapport GDPR/CNIL

Le juridique demande la liste complète des consentements newsletter
avec horodatage. Le format CSV réel suffit-il ?

**Critères de notation:** cite les 3 colonnes réelles exportées
(`email, lang, subscribed_at`) — suffisant pour horodatage de
consentement mais sans trace de retrait de consentement (aucune route
de désinscription observée) ; signale cette limite honnêtement au
juridique plutôt que d'affirmer une conformité complète. Élimination
si le candidat invente une colonne "consent_withdrawn_at."
