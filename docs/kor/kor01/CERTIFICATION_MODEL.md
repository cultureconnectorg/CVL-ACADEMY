# KOR-01 — Modèle pédagogique de certification

```
Distingue explicitement ACADEMY_CERTIFICATION de RNCP_OR_STATE_
CERTIFICATION. Ne suggère jamais que KOR-01 possède une reconnaissance
RNCP — ce n'est pas le cas aujourd'hui.
```

## Deux régimes de certification, jamais confondus

| | `ACADEMY_CERTIFICATION` | `RNCP_OR_STATE_CERTIFICATION` |
|---|---|---|
| Ce que c'est | Une évaluation interne à CVLN Academy, sanctionnant `KOR01-A01` | Une certification enregistrée au Répertoire National des Certifications Professionnelles (ou équivalent d'État) |
| Délivrée par | Le jury `KOR-01` (`guides/JURY_GUIDE.md`), sur la base de `assessments/RUBRIC.md` | Un organisme certificateur accrédité, hors périmètre de ce document |
| Statut aujourd'hui | **Réelle**, dès que le module M14 est authored et l'assessment mené | **Inexistante pour `KOR-01`** — les références ROME présentes dans ce dossier (`external_calibration.py:283-301`, `rome_l1302`/`rome_e1106`) sont des données de **calibration marché externe** (à quoi ressemble un métier comparable sur le marché), jamais une certification obtenue par la formation |
| Ce qu'elle prouve | Que le candidat a démontré les 14 compétences `C1-C14` dans les limites du rôle `KOR-01` | N/A pour l'instant |
| Ce qu'elle ne prouve pas | Une reconnaissance professionnelle externe, un niveau de qualification d'État | N/A |

## Pourquoi cette distinction est non négociable

Un badge ou une évaluation Academy présentés comme une certification
RNCP sans l'être constituerait une fausse déclaration vis-à-vis de tout
candidat qui s'en prévaudrait professionnellement — l'inverse exact de
la discipline `EVIDENCE_FIRST`/`NO_RNCP_CLAIM` qui gouverne ce ticket.

## Ce que le badge `Podcast Producer CVLN` reste

Per `KOR-0002` §2.4/§2.7, `badge_name = "Podcast Producer CVLN"` reste
`DISPLAY_ONLY_LEGACY` : un nom affiché sur la fiche formation, non
reconnecté à un mécanisme de délivrance réel (`db.user_badges`), et non
utilisé ici comme preuve de certification. La réussite de `KOR01-A01`
(`ACADEMY_CERTIFICATION`) est documentée indépendamment de ce badge, pas
conditionnée par lui ni ne le remplace — `NO_BADGE_REASSIGNMENT`
respecté (aucune mutation de `seed_data.py`).

## Ce que la certification ne délivre pas — cadrage KORA

La réussite de `KOR01-A01` ne délivre **aucune** autorisation
d'opérateur de plateforme KORA, aucune relation contractuelle réelle
avec un tiers (Kafé Kreyòl ou tout autre), et n'implique aucune
publication réelle sur une plateforme KORA — cohérent avec
`KOR-0002` §2.5 (aucune compétence `KOR-01` n'est `PRODUCT_DEPENDENCY`).

## Horizon futur (non traité ici)

Une éventuelle démarche RNCP pour `KOR-01`, ou une reconnexion
opérationnelle avec une plateforme KORA réelle, relèveraient de travaux
distincts — hors scope de `KOR-0003`, non même esquissés ici pour
éviter toute confusion avec le modèle Academy décrit ci-dessus.
