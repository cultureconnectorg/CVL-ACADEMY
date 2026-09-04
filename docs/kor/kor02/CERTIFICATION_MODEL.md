# KOR-02 — Modèle pédagogique de certification

```
Distingue explicitement ACADEMY_CERTIFICATION de RNCP_OR_STATE_
CERTIFICATION. Ne suggère jamais que KOR-02 possède une reconnaissance
RNCP — ce n'est pas le cas aujourd'hui.
```

## Deux régimes de certification, jamais confondus

| | `ACADEMY_CERTIFICATION` | `RNCP_OR_STATE_CERTIFICATION` |
|---|---|---|
| Ce que c'est | Une évaluation interne à CVLN Academy, sanctionnant `KOR02-A01` | Une certification enregistrée au RNCP (ou équivalent d'État) |
| Délivrée par | Le jury `KOR-02` (`guides/JURY_GUIDE.md`), sur la base de `assessments/RUBRIC.md` | Un organisme certificateur accrédité, hors périmètre |
| Statut aujourd'hui | **Réelle**, dès que M12 est authored et l'assessment mené | **Inexistante pour `KOR-02`** — les références ROME (`external_calibration.py:302-320`, `rome_e1106`/`rome_k1808`) sont des données de calibration marché externe, jamais une certification obtenue |
| Ce qu'elle prouve | Que le candidat a démontré les 12 compétences `C1-C12` dans les limites du rôle `KOR-02` | N/A |
| Ce qu'elle ne prouve pas | Une reconnaissance professionnelle externe | N/A |

## Ce que le badge `Cultural Broadcaster` reste

Per `KOR-0002` §3.4/§3.7, `badge_name = "Cultural Broadcaster"` reste
`DISPLAY_ONLY_LEGACY` — non reconnecté à un mécanisme de délivrance
réel, non conditionné à `KOR02-A01` ni ne le remplace
(`NO_BADGE_REASSIGNMENT` respecté).

## Ce que la certification ne délivre pas — cadrage KORA

La réussite de `KOR02-A01` ne délivre **aucune** autorisation
d'opérateur de plateforme KORA, aucune relation contractuelle réelle
avec un tiers média (*Dyaspora FM* ou autre), et n'implique aucune
diffusion réelle sur une plateforme KORA — cohérent avec `KOR-0002`
§2.5/§3 (aucune compétence `KOR-02` n'est `PRODUCT_DEPENDENCY`).

## Horizon futur (non traité ici)

Une éventuelle démarche RNCP, ou une reconnexion opérationnelle avec
une plateforme KORA réelle, relèveraient de travaux distincts — hors
scope de `KOR-0003`.
