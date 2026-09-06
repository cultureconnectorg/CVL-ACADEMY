# FRK-58 — Banque N2 (cas appliqués)

## Cas N2-1 — Panne réseau simulée

`FREK_CORE_BASE_URL` est défini mais l'endpoint distant ne répond pas
(timeout). Décris précisément ce qui se passe pour un appel
`mint_frek_id()`.

**Critères de notation :** l'appel distant échoue après 8 secondes,
l'exception est capturée silencieusement, le code retombe sur le
compteur local `db.counters` — l'utilisateur final ne voit aucune
erreur, juste un léger délai. Élimination si le candidat affirme
qu'une erreur est levée à l'utilisateur ou que l'opération échoue
entièrement.

## Cas N2-2 — Un développeur veut ajouter un nouveau signal

Un développeur veut émettre `"FREK-BONUS"` pour récompenser un
comportement. Explique ce qu'il doit faire dans le code réel.

**Critères de notation :** explique qu'il faut ajouter `"FREK-BONUS"`
à l'ensemble réel `VALID_SIGNALS` dans `frek_core.py` avant que
`emit_signal()` ne l'accepte — sans cette modification, l'appel est
silencieusement ignoré. Élimination si le candidat affirme que
n'importe quelle chaîne est acceptée telle quelle.

## Cas N2-3 — Comparaison avec le vrai `CVLNAgentfactory`

Un stagiaire demande "cette Academy a-t-elle le même niveau de
sophistication FREK que le vrai `frekcoreAout2026` ?" Réponds
honnêtement.

**Critères de notation :** explique que `frek_core.py` est un client
fin (5 méthodes, remote/local fallback), alors que `frekcoreAout2026`/
`frek_v3/` est une couche d'architecture bien plus mature
(`ARCHITECTURE_LEVEL_2`, vérificateur Python réel testé) — deux
couches réelles distinctes, jamais fusionnées, sans intégration
observée entre elles. Élimination si le candidat affirme qu'elles sont
le même système ou que l'une opère l'autre.
