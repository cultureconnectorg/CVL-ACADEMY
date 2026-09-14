# FRK-31 — Affinity, Resonance & Cadence Signals

## Grounding

Per `FREK_01_75_RECONCILIATION.md` : coverage `NONE`, distinctness
`DISTINCT_SPECIALIZATION`, action `NEW_EXTERNAL`. **Frontière
(obligatoire)** : c'est un vocabulaire de signaux *différent* du vrai
ensemble `VALID_SIGNALS` (`FREK-TIME/WORK/SCORE/...`) défini dans
`frek_core.py` — ne jamais confondre les deux dans le contenu.

## Objectives

Un candidat qui complète FRK-31 sait concevoir un vocabulaire de
signaux d'engagement (affinité/résonance/cadence) marché-général, sans
jamais le confondre avec `VALID_SIGNALS` réel :

- Enseigner le concept marché-général de signaux d'affinité/
  résonance/cadence (signaux de patron d'engagement dans les
  plateformes culturelles) comme vocabulaire professionnel distinct.
- Définir précisément un signal d'affinité : la proximité thématique
  ou émotionnelle entre un profil et un contenu, indépendamment de
  toute plateforme CVLN précise.
- Définir précisément un signal de cadence : la régularité ou le
  rythme d'un comportement dans le temps (ex. fréquence de visite) —
  et expliquer pourquoi cette dimension temporelle le distingue d'un
  simple compteur brut d'événements comme `FREK-WORK`.
- Frontière explicite et répétée, obligatoire : ce vocabulaire n'est
  **pas** implémenté comme `VALID_SIGNALS` où que ce soit dans ce
  dépôt — les 8 vrais types de signaux de `frek_core.py` forment un
  vocabulaire différent, plus étroit, déjà livré.
- Expliquer précisément pourquoi implémenter ce vocabulaire en
  appelant `emit_signal()` avec une valeur inventée hors de
  `VALID_SIGNALS` serait une erreur éliminatoire : `frek_core.py`
  n'accepte que les 8 valeurs strictes ; toute autre valeur est un
  no-op silencieux — croire qu'on a « émis un signal d'affinité » via
  ce mécanisme serait une fausse déclaration de fonctionnalité.
- Citer de mémoire les 8 valeurs réelles de `VALID_SIGNALS`
  (`FREK-TIME/WORK/SCORE/LINK/CERT/CONTRIB/SHARE/MISSION`) comme
  preuve de la maîtrise de la frontière, sans jamais les mélanger au
  vocabulaire enseigné ici.

## Modules

1. **Fondamentaux du concept affinité/résonance/cadence** — comme
   vocabulaire professionnel marché-général distinct.
2. **Pratique de conception de signaux d'engagement** — schémas de
   signaux applicables à toute plateforme culturelle générique.
3. **Discipline de frontière obligatoire vs. `VALID_SIGNALS` réel** —
   citation exacte des 8 valeurs, jamais de fusion conceptuelle.

## Assessment

Un examen de concept : le candidat conçoit un petit schéma de signaux
d'affinité/résonance/cadence pour une plateforme culturelle générique,
sans référence à CVLN, puis cite de mémoire les 8 valeurs réelles de
`VALID_SIGNALS` — noté avec règle éliminatoire obligatoire sur toute
confusion entre ce vocabulaire et `VALID_SIGNALS`, ou toute affirmation
qu'`emit_signal()` accepte ces valeurs.

## Evidence / mission eligibility

Aucun chemin d'éligibilité mission aujourd'hui.
`FRK31.SKILL.ENGAGEMENT_SIGNALS.L1` réservé une fois approfondi (voir
`EVIDENCE_MODEL.md`).

## Status

`STATUS = PACKAGE_COMPLETE` — référentiel, banques N1/N2, assessment +
rubric, evidence model, 3 guides, cette note d'intégration existent
tous, deepened this pass. `FULLY_COMPLETE` non déclaré — requiert un
passage réel vérifié par un humain.
