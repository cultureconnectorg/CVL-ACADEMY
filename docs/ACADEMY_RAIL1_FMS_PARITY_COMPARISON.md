# Rail 1 — FMS-Parity Comparison

```
Question du Founder (2026-09-07) : "je parle de savoir si c'est au même
niveau que le travail que j'ai fait avec FMS qui est la base pour savoir
si les autres ont le même niveau." Ce document répond directement à
cette question, domaine par domaine, à partir des statuts réels déjà
déclarés dans `docs/cvln_academy_master/99_REPORTS/W6_GLOBAL_STATUS.md`
(aucune réconciliation rouverte, aucun statut recalculé — seulement
réorganisé pour répondre à "qui est au niveau FMS, qui ne l'est pas").
```

## Ce que "niveau FMS" veut dire concrètement

FMS-01→06 est la référence : chaque formation porte le **package
canonique complet** — référentiel, banque de questions N1, évaluations
N2, assessment + rubric de certification A01, modèle de preuve
(evidence model), 3 guides (candidat/correcteur/jury), note
d'intégration — et, seul cas de tout le chantier, un **runtime réel et
déjà branché** (`backend/fms_import/`, `backend/fms_canonical/`), pas
seulement des fichiers Markdown. C'est la barre `PACKAGE_COMPLETE` +
`RUNTIME_BOUND` que ce document utilise pour comparer.

## Réponse directe : qui est au niveau FMS aujourd'hui

| Niveau | Domaines / formations | Ce que ça veut dire concrètement |
|---|---|---|
| **= FMS** (package complet **et** branché au runtime) | **FMS-01→06** (le canon d'origine) ; **KOR-01** (RAIL 2, 2026-09-06) | Un candidat peut suivre le parcours complet, être noté, certifié, en code réel, pas seulement en Markdown. KOR-01 est la première formation d'un autre domaine à atteindre ce niveau exact. |
| **Package complet, pas encore branché au runtime** | KOR-02→10 (10 formations KORA) ; KLT-01→05 (5 formations Kiltikonet) ; GMD-21→33 (13) ; WAL-19, CVE-02 ; FMS-07 (l'ombrelle FMS-07→18) ; FRK — 54/75 formations ; AGF — 59/109 lignes (dont CMD-15 flagship) ; CYB-32 ; SAY-LAB | Le corpus pédagogique est écrit à la même profondeur que FMS (les 9 fichiers du package), mais aucun code ne le sert encore — exactement où FMS lui-même en était avant ACA-0006. KOR-02→10 viennent d'être vérifiés runtime-importables ce jour (RAIL 2) : le mécanisme marche, seul le "branchage" définitif (routes dédiées, pilote KOR-01 excepté) reste à faire domaine par domaine. |
| **Partiel, honnêtement incomplet** | KLT-06→08 (5/7, 6/7, 6/7 compétences réelles, le reste `BLOCKED` par gouvernance) ; KOR-11→15 (5 formations — squelette de modules réel mais dans une convention plus légère, sans `MODULE_ID`/prérequis/niveau d'évaluation structurés — **confirmé aujourd'hui par le runtime lui-même**, `fully_complete=False`, 0 module canonique résolu par formation, voir capture d'écran) ; FMS-08→18 sauf FMS-07 (8 formations en `MODULE_CONTENT_DRAFTED`) ; FREK — 3/75 (`NEEDS_EXPERT_REVIEW`) ; le reste des domaines W6 (GMD-01→20, WAL-01→18, CYB/BCI/GCF/HOS/LOS hors flagship, CEO/GRP/FDC, XCV) — `MODULE_CONTENT_DRAFTED`/`SPECIALIZE_EXISTING`/`MERGE`/`EXTEND_EXISTING` selon la ligne | Contenu réel, jamais fabriqué, mais moins profond que FMS — soit le format lui-même est plus léger (KOR-11→15), soit seul un sous-ensemble a reçu le traitement complet à 9 fichiers, soit la ligne est par nature un renvoi/convergence (XCV) plutôt qu'une formation autonome. |
| **Bloqué, honnêtement déclaré** | FRK — 10/75 ; AGF — 39/109 ; CYB/BCI/GCF/LOS — 60/214 ; GRP/FDC — 27/158 ; XCV-67 ; GMD-34 ; GMD-X-04/05/07/08 ; WAL-X-08/09 ; KLT-09→20 (gouvernance `STOP=TRUE`) | Aucune capacité inventée pour combler l'écart — chaque ligne cite précisément la dépendance produit ou la porte d'autorisation manquante (`BLOCKED_CANDIDATES.md`/`GAP.md` par domaine). |
| **Nécessite un vrai expert, jamais une recette universelle** | GRP-11, GRP-32→40 ; FDC-21→35 ; WAL-15 ; FRK-10/14/73 | Contenu juridique/fiscal/philanthropique/cryptographique — la doctrine du chantier interdit explicitement d'inventer une réponse ici. |

## Ce que RAIL 2 vient de vérifier, en direct, sur le vrai corpus KORA

Avant aujourd'hui, "KOR-01→10 sont au niveau FMS" et "KOR-11→15 sont
plus légères" n'étaient affirmés que par les rapports Markdown eux-mêmes
(`docs/kor/README.md`, `W6_GLOBAL_STATUS.md`). Le binding runtime
(`backend/kor_canonical/`, RAIL 2) vient de **re-vérifier cette
affirmation indépendamment, en import réel** :

```
KOR-01  modules=14  skills=14  fully_complete=True
KOR-02  modules=12  skills=12  fully_complete=True
KOR-03  modules=11  skills=11  fully_complete=True
KOR-04  modules=9   skills=9   fully_complete=True
KOR-05  modules=10  skills=10  fully_complete=True
KOR-06  modules=9   skills=9   fully_complete=True
KOR-07  modules=9   skills=9   fully_complete=True
KOR-08  modules=9   skills=9   fully_complete=True
KOR-09  modules=11  skills=11  fully_complete=True
KOR-10  modules=10  skills=10  fully_complete=True
KOR-11  modules=0   skills=13  fully_complete=False  (fichiers modules réels, mais convention SKILL_ID-only, pas MODULE_ID)
KOR-12  modules=0   skills=13  fully_complete=False  (idem)
KOR-13  modules=0   skills=13  fully_complete=False  (idem)
KOR-14  modules=0   skills=14  fully_complete=False  (idem)
KOR-15  modules=0   skills=12  fully_complete=False  (idem)
```

Le runtime ne fait jamais confiance aveuglément ni au README (qui
affirmait encore KOR-03→15 entièrement non construites) ni à une
supposition de parité : il importe chaque fichier réel et dérive
`fully_complete` du fait vérifiable que chaque compétence référence bien
un module réellement résolu — jamais d'un statut auto-déclaré. Le
résultat confirme, avec du code qui tourne, exactement la gradation déjà
pressentie par les rapports : KOR-01→10 sont au niveau FMS
(package complet), KOR-11→15 ne le sont pas encore (squelette réel,
convention plus légère) — voir la capture d'écran `05_canonical_kor_
list.png` livrée avec ce rapport, qui affiche cette gradation en direct
dans l'interface, pas seulement dans un rapport texte.

## Ce que ça implique pour la suite

- **FMS reste la seule référence à `PACKAGE_COMPLETE` + `RUNTIME_BOUND`
  sur 6/6 formations** — aucun autre domaine n'atteint ce double niveau
  sur l'intégralité de son périmètre. KOR-01 est désormais la deuxième
  formation de tout le chantier (hors FMS) à l'atteindre, mais elle est
  seule dans son domaine à ce niveau.
- **Amener un domaine entier "au niveau FMS"** demanderait deux choses
  distinctes, jamais confondues : (1) porter chaque formation partielle
  à `PACKAGE_COMPLETE` (travail de contenu, déjà fait pour beaucoup —
  KOR-02→10, KLT-01→05, GMD-21→33, etc.) et (2) la brancher au runtime
  comme KOR-01 (travail RAIL 2, un domaine à la fois). Aucun raccourci
  qui ferait les deux en même temps sans code réel derrière.
- **KOR-11→15 et KLT-06→08 ne peuvent pas atteindre le niveau FMS sans
  travail de contenu réel d'abord** — pas un problème d'intégration
  runtime, un problème de corpus (fichiers modules dans un format plus
  léger pour KOR-11→15, compétences réellement `BLOCKED` pour KLT-06→08).
