# GMD-21 — Banque N2 (cas appliqués)

```
Honest count: 3 cases, one per higher-stakes theme this orientation
formation actually covers (route ownership, model boundary, security
escalation). Not padded to a round number.
```

## Cas N2-1 — Nouvel arrivant

*Contexte*: Une nouvelle recrue rejoint l'équipe opérationnelle Good
Mood. On te donne 10 minutes pour la briefer sur le système avant
qu'elle ne prenne son premier quart.

*Tâche*: Rédige le script de ce briefing de 10 minutes. Il doit
couvrir : la carte des sous-systèmes réels (catalogue/events/tickets/
scan/CRM/merch/paiement/reporting/outbox FREK+Wallet/admin), qui
possède quoi (par formation GMD), et une règle absolue à ne jamais
enfreindre.

*Grille d'évaluation*: le script cite au moins 8 des 13 sous-systèmes
réels sans en inventer un 14ème ; il nomme correctement au moins 3
formations GMD associées ; il inclut la règle "escalader, jamais
inventer une procédure d'incident" (GMD-34).

## Cas N2-2 — La question piège du stakeholder

*Contexte*: Un stakeholder demande : "Peut-on savoir combien de fans
achètent à la fois un billet ET un article merch le même jour ?"

*Tâche*: Réponds en identifiant précisément quelles données réelles
existent (`Volume`... non, `TicketType`, `Product`, `/admin/orders`)
et si cette corrélation est directement disponible ou nécessiterait un
travail de rapprochement manuel entre `/admin/orders` et `/admin/
events/{eid}/tickets`.

*Grille d'évaluation*: la réponse ne prétend jamais qu'un rapport
"achats croisés" existe tout fait ; elle identifie correctement que
`/admin/orders` est la source commune la plus proche ; elle propose un
chemin honnête (rapprochement manuel) plutôt que d'inventer une
fonctionnalité.

## Cas N2-3 — Signal de sécurité ambigu

*Contexte*: Un opérateur remarque une session admin active à 3h du
matin, un horaire inhabituel.

*Tâche*: Décris la marche à suivre correcte, en distinguant ce que le
système *permet réellement* de vérifier (`/auth/me`, l'heure de
connexion) de ce qu'il ne permet pas (pas de log d'anomalie
automatique, pas de blocage automatique — GMD-34 n'existe pas).

*Grille d'évaluation*: la réponse escalade à un humain plutôt que
d'agir seule ; elle ne prétend jamais qu'un système de détection
automatique existe.

## Status

`STATUS = N2_BANK_V1`. Referenced by the Assessment
(`ASSESSMENT_AND_RUBRIC.md`).
