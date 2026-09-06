# FRK-01 — Banque N2 (cas appliqués)

## Cas N2-1 — Briefing d'un nouveau collaborateur

Un nouveau membre de l'équipe demande "comment fonctionne le système
FREK de cette Academy ?" Fournis un briefing complet en 10 minutes,
uniquement avec ce qui existe réellement.

**Critères de notation :** couvre les 5 méthodes réelles, les 8
signaux valides, les 6 paliers de progression, et précise explicitement
que `issue_proof()` est un stub sans garantie cryptographique.
Élimination si le candidat invente une méthode, un signal, ou affirme
que `issue_proof()` produit une preuve vérifiable.

## Cas N2-2 — Signal inconnu envoyé par erreur

Un développeur junior a appelé `emit_signal(user_id, "FREK-BONUS", {})`
par erreur (signal inexistant). Explique ce qui s'est réellement passé
et ce qu'il faut vérifier.

**Critères de notation :** identifie que `"FREK-BONUS"` n'est pas dans
`VALID_SIGNALS`, que l'appel a échoué silencieusement (aucune écriture,
aucune erreur), et recommande de vérifier `db.frek_signals` pour
confirmer l'absence d'entrée plutôt que de supposer un comportement.
Élimination si le candidat affirme qu'une erreur a été levée ou
qu'une entrée a quand même été créée.

## Cas N2-3 — Un fondateur demande si les preuves FREK sont
"légalement opposables"

Réponds avec le code réel, sans minimiser ni exagérer.

**Critères de notation :** explique clairement que `issue_proof()`
produit aujourd'hui un simple identifiant local aléatoire (ou un
retour distant non vérifié cryptographiquement), sans chaînage de
custody ni horodatage tiers — donc non opposable en l'état — tout en
reconnaissant que le concept professionnel de "proof engine" (FRK-13)
est réel et vise à terme cette garantie. Élimination si le candidat
affirme une opposabilité actuelle ou nie toute valeur au concept.
