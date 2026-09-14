# KLT-05 — Modèle pédagogique de certification

```
Même distinction que les formations précédentes : ACADEMY_CERTIFICATION
!= RNCP_OR_STATE_CERTIFICATION. Discipline supplémentaire propre à
KLT-05 : OPERATOR_AUTHORIZATION = NOT_IMPLEMENTED / NOT_GRANTED.
```

| | `ACADEMY_CERTIFICATION` | `RNCP_OR_STATE_CERTIFICATION` |
|---|---|---|
| Statut aujourd'hui | Réelle, dès `KLT05-A01` mené | Inexistante — la référence RNCP présente (`external_calibration.py:464`, `CERT_PROJECT_CULTURE`) est une calibration marché, jamais une certification obtenue |
| Ce qu'elle prouve | Les 11 compétences `C1-C11` dans les limites du rôle | N/A |

## Badge

`badge_name = "Kiltikonet Platform Operator"` reste `DISPLAY_ONLY_
LEGACY` — un nom qui, plus que pour toute autre formation KLT, invite à
la confusion avec une autorisation réelle. C'est précisément pour cette
raison que la discipline ci-dessous est renforcée.

## `OPERATOR_AUTHORIZATION` — la règle la plus stricte de tout le corpus KLT

```
OPERATOR_AUTHORIZATION = NOT_IMPLEMENTED / NOT_GRANTED
```

Aucun module, aucun assessment, aucun badge de `KLT-05` — y compris son
module terminal explicitement titré "devenir opérateur senior" dans le
legacy — ne confère, ne simule, ni ne laisse entendre un accès
administrateur réel à une plateforme Kiltikonet. Cette règle est
rappelée : dans le référentiel (`00_REFERENTIEL_ET_BLUEPRINTS.md`), dans
chaque module concerné (M02, M04, M11), dans le guide candidat, le guide
jury, et comme critère éliminatoire explicite de la grille
(`RUBRIC.md`, critère 10).

## Préparation future — ce qui n'existe pas encore

Le Founder a nommé trois concepts à préparer plus tard pour cette
formation : `SKILL_PROOF` (le registre `skills/SKILL_ID_REGISTRY.md` en
pose la structure, `STATUS = PROPOSED`), `CERTIFICATION` (ce document),
et `OPERATOR_AUTHORIZATION` (explicitement non implémentée ici). Aucun
des trois n'est construit au-delà de sa documentation dans ce ticket.
