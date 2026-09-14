# KLT-13 — Registre de Skill IDs

```
NAMESPACE: KLT13.SKILL.xxx. STATUS = PROPOSED, aucune donnée en base.
Formation NEW, 5/5 compétences construites. Namespace distinct de FMS
et des autres formations KLT — vérifié sans collision.
```

| Skill ID | Compétence | Module | Assessment | Evidence | Statut |
|---|---|---|---|---|---|
| `KLT13.SKILL.C01` | Concevoir un dispositif d'accréditation terrain | M01 | N1 (`Q-N1-01`, `Q-N1-02`), N2 (`E-N2-01`) | Plan d'accréditation terrain | `BUILT` |
| `KLT13.SKILL.C02` | Étudier un précédent réel de contrôle d'accès (cross-écosystème) | M02 | N1 (`Q-N1-03`, `Q-N1-04`), N2 (`E-N2-02`) | Fiche d'analyse du précédent réel | `BUILT` |
| `KLT13.SKILL.C03` | Spécifier une extension NFC en connaissance de ses limites | M03 | N1 (`Q-N1-05`, `Q-N1-06`), N2 (`E-N2-03`) | Spécification NFC (statut explicite) | `BUILT` |
| `KLT13.SKILL.C04` | Gérer un incident d'accréditation terrain et l'escalader | M04 | N1 (`Q-N1-07`, `Q-N1-08`), N2 (`E-N2-04`) | Fiche d'incident + note d'escalade | `BUILT` |
| `KLT13.SKILL.C05` | Restituer un bilan d'accréditation terrain sans fabriquer de données | M05 | N1 (`Q-N1-09`, `Q-N1-10`), N2 (`E-N2-05`), N2/N3 (`KLT13-A01`) | Bilan d'accréditation terrain | `BUILT` |

Aucune compétence de cette formation ne dépend d'une connexion à un
système externe — le précédent réel étudié en `C2` (Good Mood) est cité
comme étude de cas, jamais interrogé en direct par Academy, et `C3`
spécifie explicitement une technologie non implémentée. Le statut
`BUILT` (et non `BUILT_UNCONNECTED`) s'applique donc partout : cette
formation ne porte pas la même nuance que `KLT-06`/`07`/`08`, dont
certaines compétences dépendent d'un système réel vérifié mais non
connecté.
