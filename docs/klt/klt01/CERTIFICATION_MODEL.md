# KLT-01 — Modèle pédagogique de certification

```
Distingue explicitement ACADEMY_CERTIFICATION de RNCP_OR_STATE_
CERTIFICATION. Ne suggère jamais que KLT-01 possède une reconnaissance
RNCP — ce n'est pas le cas aujourd'hui.
```

## Deux régimes de certification, jamais confondus

| | `ACADEMY_CERTIFICATION` | `RNCP_OR_STATE_CERTIFICATION` |
|---|---|---|
| Ce que c'est | Une évaluation interne à CVLN Academy, sanctionnant `KLT01-A01` | Une certification enregistrée au Répertoire National des Certifications Professionnelles (ou équivalent d'État) |
| Délivrée par | Le jury `KLT-01` (`guides/JURY_GUIDE.md`), sur la base de `assessments/RUBRIC.md` | Un organisme certificateur accrédité, hors périmètre de ce document |
| Statut aujourd'hui | **Réelle**, dès que le module M11 est authored et l'assessment mené | **Inexistante pour `KLT-01`** — la seule référence RNCP présente dans ce dossier (`external_calibration.py:377`, `CERT_PROJECT_CULTURE` = RNCP `40912`/`32052`) est une donnée de **calibration marché externe** (à quoi ressemble un métier comparable sur le marché), jamais une certification obtenue par la formation |
| Ce qu'elle prouve | Que le candidat a démontré les 11 compétences `C1-C11` dans les limites du rôle `KLT-01` | N/A pour l'instant |
| Ce qu'elle ne prouve pas | Une reconnaissance professionnelle externe, un niveau de qualification d'État | N/A |

## Pourquoi cette distinction est non négociable

Un badge ou une évaluation Academy présentés comme une certification
RNCP sans l'être constituerait une fausse déclaration vis-à-vis de tout
candidat qui s'en prévaudrait professionnellement — l'inverse exact de
la discipline `EVIDENCE_FIRST`/`NO_RNCP_CLAIM` qui gouverne ce ticket.

## Ce que le badge `Kiltikonet Ambassador` reste

Per `KLT-0002`/`KLT-0003`, `badge_name = "Kiltikonet Ambassador"` reste
`DISPLAY_ONLY_LEGACY` : un nom affiché sur la fiche formation, non
reconnecté à un mécanisme de délivrance réel (`db.user_badges`), et non
utilisé ici comme preuve de certification (`KLT-0004` §15). La réussite
de `KLT01-A01` (`ACADEMY_CERTIFICATION`) est documentée indépendamment de
ce badge, pas conditionnée par lui ni ne le remplace.

## Horizon futur (non traité ici)

Une éventuelle démarche RNCP pour `KLT-01` relèverait d'un travail
distinct (dossier de certification professionnelle, organisme
certificateur, référentiel officiel) — hors scope de `KLT-0004`, non
même esquissée ici pour éviter toute confusion avec le modèle Academy
décrit ci-dessus.
