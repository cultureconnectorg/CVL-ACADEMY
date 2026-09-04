# KOR-02 — Registre de Skill IDs

```
NAMESPACE: KOR02.SKILL.xxx — distinct de KOR01.SKILL.xxx, FMS et KLT.
Aucun ID réutilisé, aucune collision de forme. Document seul —
NO_DB_MUTATION, NO_RUNTIME_BINDING.
```

| Skill ID | Compétence | Module | Assessment | Evidence |
|---|---|---|---|---|
| `KOR02.SKILL.C01` | Analyser le paysage du journalisme culturel et diagnostiquer un sujet | M01 | N1 (`Q-N1-01`) | Note d'analyse + diagnostic éditorial |
| `KOR02.SKILL.C02` | Vérifier des sources et traiter une divergence factuelle | M02 | N1 (`Q-N1-02`) | Fiche source + protocole de vérification |
| `KOR02.SKILL.C03` | Choisir et défendre un angle éditorial | M03 | N1/N2 (`Q-N1-03`, `E-N2-01`) | Note d'angle comparée |
| `KOR02.SKILL.C04` | Conduire une interview journalistique complémentaire | M04 | N2 (`E-N2-02`) | Guide d'interview + interview conduite |
| `KOR02.SKILL.C05` | Écrire une pièce longue intégrant une divergence factuelle | M05 | N2 (`E-N2-03`) | Feature complète publiable |
| `KOR02.SKILL.C06` | Structurer une narration culturelle | M06 | N2 (`Q-N1-04`, `E-N2-04`) | Plan narratif + récit structuré |
| `KOR02.SKILL.C07` | Décliner un contenu en plusieurs formats sans le dénaturer | M07 | N2 (`E-N2-05`) | Sujet décliné en formats multiples |
| `KOR02.SKILL.C08` | Poser un cadre déontologique appliqué | M08 | N1/N2 (`Q-N1-05`, `E-N2-06`) | Charte perso + arbre de décision |
| `KOR02.SKILL.C09` | Arbitrer une tension de représentation | M09 | N2 (`E-N2-07`) | Note d'arbitrage de représentation |
| `KOR02.SKILL.C10` | Décider des conditions d'une diffusion/co-production réelle | M10 | N2 (`Q-N1-06`, `E-N2-08`) | Pitch de co-production |
| `KOR02.SKILL.C11` | Construire un portfolio professionnel honnête | M11 | N2 (`E-N2-08`) | Portfolio + bio publique |
| `KOR02.SKILL.C12` | Conduire un travail de storytelling culturel de bout en bout et le défendre | M12 | N3 (`KOR02-A01`) | Dossier de certification + soutenance |

## Statut

`STATUS = PROPOSED` — aucune donnée en base aujourd'hui
(`NO_DB_MUTATION`, `NO_RUNTIME_BINDING`), même statut que
`skills/SKILL_ID_REGISTRY.md` de `KOR-01`.

## Provenance des compétences (`KOR-0002`, vocabulaire imposé)

| Skill ID | Provenance |
|---|---|
| `KOR02.SKILL.C01`-`C09` | `MARKET_SKILL` |
| `KOR02.SKILL.C10` | `KORA_CURRENT_CAPABILITY` (cadrage narratif du débouché) sur socle `MARKET_SKILL` — aucune API KORA réelle appelée |
| `KOR02.SKILL.C11`-`C12` | `MARKET_SKILL` |

Aucune compétence `KOR-02` n'est `PRODUCT_DEPENDENCY` — confirmé par
`KOR-0002` §3, reconfirmé ici module par module.

## Continuité avec `KOR-01`

`KOR02.SKILL.C04` et `C05` s'appuient sur une source réelle produite
par `KOR-01` (l'interview audio de Man Rosa, `docs/kor/kor01/case/
CAS_FIL_ROUGE.md`) — cohérent avec la doctrine "un cas, plusieurs
angles métier" déjà appliquée à Kiltikonet. Aucune donnée n'est
dupliquée entre les deux registres : chaque Skill ID reste propre à sa
formation.
