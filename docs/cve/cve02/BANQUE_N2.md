# CVE-02 — Banque N2 (cas appliqués)

## Cas N2-1 — Contestation d'un événement écarté

Un artiste conteste qu'une de ses écoutes n'a pas été comptée. Explique
le mécanisme réel qui pourrait en être la cause, sans inventer de
justification.

**Critères de notation:** cite le Filtre de Validation
(`TS_i(t_e) ≥ τ_fraude`) comme seule cause documentée d'exclusion
d'un événement dans ce document — propose de vérifier le vrai Trust
Score de l'événement contre le seuil publié du cycle, jamais une
raison inventée (ex. "limite géographique," "quota journalier"
inexistants dans le spec). Élimination si le candidat invente un
second mécanisme de filtrage.

## Cas N2-2 — Confusion entre composante brute et composante dérivée

Un stagiaire traite `L_i,c` comme une simple lecture de données brutes
au même titre que `S`, `E`, `F`, `C`. Corrige.

**Critères de notation:** cite explicitement que `L` est **dérivé** de
l'intégrale de la courbe CHL (§3.3), pas un signal brut — c'est la
seule des 5 composantes dans ce cas. Élimination si le candidat
affirme que les 5 composantes sont toutes de même nature.

## Cas N2-3 — Demande de choix de transformation de saturation

Le manager demande "utilisons `log(1+x)` ou `x^0.5` pour la
transformation ?" et veut une réponse définitive aujourd'hui.

**Critères de notation:** répond honnêtement que le document lui-même
renvoie ce choix au chantier 2 (simulation, non encore réalisé) —
propose de documenter les deux formes et d'attendre les résultats
empiriques plutôt que de trancher arbitrairement aujourd'hui.
Élimination si le candidat affirme qu'un choix a déjà été fait dans le
document frozen v1.0.
