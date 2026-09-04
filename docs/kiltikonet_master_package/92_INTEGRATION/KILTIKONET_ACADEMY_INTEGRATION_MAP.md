# Kiltikonet Academy Integration Map

```
Consolide les 5 INTEGRATION_ACADEMY_PACKAGE_NOTE.md locaux.
NO_RUNTIME_BINDING dans ce document et dans tout ce ticket.
```

## `DOCUMENT_SOURCE → IMPORT_OBJECT → ACADEMY_ENTITY → RUNTIME_CONSUMER → STATUS`

| `DOCUMENT_SOURCE` | `IMPORT_OBJECT` cible | `ACADEMY_ENTITY` équivalente (si elle existait) | `RUNTIME_CONSUMER` potentiel | `STATUS` |
|---|---|---|---|---|
| `modules/MXX_*.md` (59 au total) | Module pédagogique structuré | `fms_canonical.CanonicalModule` (forme comparable, jamais réutilisée telle quelle) | `ModuleJourney` (frontend) | `NEEDS_IMPORTER` — aucun chemin d'import KLT n'existe |
| `skills/SKILL_ID_REGISTRY.md` (5 registres, 59 entrées) | Skill ID adressable | Équivalent `fms_canonical` skill extraction, jamais réutilisé | Système de preuve/certification | `NEEDS_SCHEMA` — namespace `KLTxx.SKILL.Cnn` distinct, décision de stockage non prise |
| `assessments/N1_QUESTION_BANK.md` (66 questions) | Banque de questions N1 | `quiz.py` (générique, formation-agnostique) | Moteur de quiz existant | `NEEDS_IMPORTER` — format compatible en théorie, jamais testé |
| `assessments/N2_EVALUATIONS.md` (30 évaluations) | Évaluation de décision N2 | Aucun équivalent structuré existant dans Academy (les cas N2 legacy FMS sont proches mais non identiques) | — | `NEEDS_SCHEMA` |
| `assessments/A01_CERTIFICATION_ASSESSMENT.md` + `RUBRIC.md` (5 paires) | Assessment certificatif + grille | `certification/service.py` (Rubric Master 0-4, déjà réel pour FMS) | Moteur de certification existant | `NEEDS_SCHEMA` — le moteur existe et la grille 0-4 est déjà compatible en forme, mais aucun mapping KLT n'a été écrit |
| `skills/EVIDENCE_MODEL.md` (5, 59 lignes) | Modèle de preuve | Aucun équivalent générique dans Academy à ce jour | Futur système de preuve FREK | `NOT_CONNECTED` |
| `case/CAS_*.md` (12 documents) | Cas fil rouge pédagogique | Aucun équivalent (FMS utilise des cas différents) | — | `NOT_CONNECTED` — contenu narratif, jamais destiné à un import structuré |
| `guides/*.md` (15 documents) | Guide candidat/correcteur/jury | Aucun équivalent structuré dans Academy | Interface trainer/jury existante (générique) | `NOT_CONNECTED` |
| `templates/TEMPLATES.md` (5) | Gabarit réutilisable | `template_engine/` (existant, générique) | Moteur de templates existant | `NEEDS_SCHEMA` — le moteur existe, aucun type de template KLT n'y est déclaré |
| `CERTIFICATION_MODEL.md` (5) | Modèle de certification par formation | `certification/service.py` | Moteur de certification existant | `BLOCKED` — nécessite d'abord la décision `OPERATOR_AUTHORIZATION` pour `KLT-05` |

## Ce qui manquerait avant un import réel (repris et consolidé des 5 notes locales)

1. **Chemin d'import dédié** — `fms_import`'s `SKILL_ID_RE` et la
   normalisation de code (`FMS-XX-MYY`) sont **spécifiques à FMS** et ne
   doivent **jamais** être étendus silencieusement pour reconnaître
   `KLTxx.SKILL.Cxx` ou `KLTxx-Mxx` — rappelé dans les 5 notes locales,
   confirmé ici comme contrainte transversale.
2. **Décision de stockage** — nouvelle collection (`db.klt_resources`
   ou équivalent) vs réutilisation d'une collection existante — non
   tranchée.
3. **Résolution du gap badge/skill-proof/opérateur** (voir
   `CERTIFICATION_ARCHITECTURE.md`, `OPERATOR_AUTHORIZATION_
   ARCHITECTURE.md`) avant qu'un skill ID ne devienne réellement
   adressable en base.

## `NO_RUNTIME_BINDING`

Ce document ne construit, ne teste, ni n'esquisse de code d'import. Il
consolide ce que 5 notes locales affirmaient déjà séparément.
