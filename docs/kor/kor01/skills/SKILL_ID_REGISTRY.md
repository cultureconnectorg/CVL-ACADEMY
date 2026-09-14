# KOR-01 — Registre de Skill IDs

```
NAMESPACE: KOR01.SKILL.xxx — distinct de FMS (FMSxx-Ay) et de KLT
(KLTxx.SKILL.Cxx). Aucun ID FMS/KLT réutilisé, aucune collision de
forme. Ce registre est un document — il ne crée aucune donnée en base
(NO_DB_MUTATION) et n'est lu par aucun code aujourd'hui
(NO_RUNTIME_BINDING).
```

Chaque Skill ID pointe vers exactement une compétence, un module, un
mode d'évaluation, et une preuve.

| Skill ID | Compétence | Module | Assessment | Evidence |
|---|---|---|---|---|
| `KOR01.SKILL.C01` | Analyser le paysage podcast et diagnostiquer une opportunité éditoriale | M01 | N1 (`Q-N1-01`, `Q-N1-02`) | Analyse podcast référence + note de positionnement |
| `KOR01.SKILL.C02` | Choisir sujet, format, cadence | M02 | N1 (`Q-N1-03`) | One-pager concept + 10 idées |
| `KOR01.SKILL.C03` | Écrire un script d'épisode, doser scripté/improvisé | M03 | N1/N2 (`Q-N1-04`, `E-N2-01`) | Script complet annoté |
| `KOR01.SKILL.C04` | Préparer et conduire une interview adaptée | M04 | N2 (`E-N2-02`) | Guide d'interview + interview conduite |
| `KOR01.SKILL.C05` | Capturer une prise de son adaptée à l'environnement | M05 | N2 (`Q-N1-05`, `E-N2-03`) | Prise de son brute + note de setup |
| `KOR01.SKILL.C06` | Monter un épisode, arbitrer une tension éditoriale de style | M06 | N2 (`E-N2-04`) | Épisode monté + note d'arbitrage |
| `KOR01.SKILL.C07` | Concevoir un sound design au service du contenu | M07 | N2 (`Q-N1-06`, `E-N2-05`) | Piste sound design + justification |
| `KOR01.SKILL.C08` | Mixer et masteriser pour une écoute mobile fiable | M08 | N2 (`E-N2-06`) | Épisode mixé/masterisé + mesures |
| `KOR01.SKILL.C09` | Construire une identité sonore cohérente | M09 | N2 (`Q-N1-07`, `E-N2-04`) | Générique + note de cohérence |
| `KOR01.SKILL.C10` | Distribuer via hébergeurs/RSS/DSP réels | M10 | N2 (`Q-N1-08`) | Flux RSS + preuve de soumission DSP |
| `KOR01.SKILL.C11` | Publier et référencer un épisode | M11 | N2 (`E-N2-07`) | Épisode publié + fiche de référencement |
| `KOR01.SKILL.C12` | Construire un premier plan d'audience réaliste | M12 | N2 (`Q-N1-09`, `E-N2-08`) | Plan de croissance d'audience |
| `KOR01.SKILL.C13` | Explorer une piste de croissance/monétisation réaliste | M13 | N2 (`Q-N1-10`, `E-N2-08`) | Note de piste de monétisation |
| `KOR01.SKILL.C14` | Conduire une production de podcast de bout en bout et la défendre | M14 | N3 (`KOR01-A01`) | Dossier de certification + soutenance |

## Statut

`STATUS = PROPOSED` — ce registre n'existe dans aucune base de données
aujourd'hui (`NO_DB_MUTATION`, `NO_RUNTIME_BINDING`). Il documente la
forme que prendrait un futur registre `db.kor_skills` (ou équivalent),
sur le modèle de l'extraction canonique déjà réelle côté FMS/KLT
(`fms_canonical/read_model.py`, `klt_canonical/read_model.py`), sans
réutiliser leur code ni leurs identifiants.

## Différence explicite avec FMS et KLT

FMS utilise `FMSxx-Ay`. KLT utilise `KLTxx.SKILL.Cnn`. `KOR` reprend la
forme `KLTxx.SKILL.Cnn` (namespace `KOR01.SKILL.Cxx`) — choix délibéré
de cohérence de méthode entre les deux workstreams "métiers-évidence"
(FMS = certification courte historique, KLT/KOR = format explicite plus
récent), sans jamais risquer de collision visuelle : `KOR01` ne
commence par aucun préfixe partagé avec `KLTxx` ou `FMSxx`.

## Provenance des compétences (`KOR-0002`, vocabulaire imposé)

| Skill ID | Provenance |
|---|---|
| `KOR01.SKILL.C01`-`C07` | `MARKET_SKILL` |
| `KOR01.SKILL.C08` | `MARKET_SKILL` |
| `KOR01.SKILL.C09` | `KORA_CURRENT_CAPABILITY` (cadrage narratif) sur socle `MARKET_SKILL` — aucune API KORA réelle appelée |
| `KOR01.SKILL.C10`-`C13` | `MARKET_SKILL` |
| `KOR01.SKILL.C14` | `MARKET_SKILL` (synthèse) |

Aucune compétence `KOR-01` n'est `PRODUCT_DEPENDENCY` — confirmé par
`KOR-0002` §2.5, reconfirmé ici module par module.
