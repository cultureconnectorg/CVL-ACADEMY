# KOR-03 — Blueprints canoniques (11 modules)

```
Chaque blueprint répond à : pourquoi il existe, quelle compétence il
prouve, comment il est évalué, quelle production réelle est attendue.
```

## M01 — Panorama vidéo/streaming diaspora et diagnostic
WHY : sans lecture du paysage existant, aucun teaser n'est positionné.
COMPETENCY : C1. ASSESSED : N1. OUTPUT : analyse + diagnostic.

## M02 — Préproduction et écriture pour l'image
WHY : un tournage d'une seule journée avec une source âgée et fatigable
ne tolère pas l'improvisation totale. COMPETENCY : C2. ASSESSED : N1.
OUTPUT : script visuel + repérage.

## M03 — Éclairer et sonoriser un plateau
WHY : le salon de Man Rosa n'est pas équipé — la qualité vient du
setup, pas du matériel. COMPETENCY : C3. ASSESSED : N2. OUTPUT : plan
lumière/son + test.

## M04 — Tourner en single-cam
WHY : capter le segment de Man Rosa exige un cadrage respectueux de son
rythme. COMPETENCY : C4. ASSESSED : N2. OUTPUT : rushes exploitables.

## M05 — Tourner et réaliser en multicam
WHY : le teaser demande plusieurs points de vue coordonnés avec deux
personnes seulement. COMPETENCY : C5. ASSESSED : N2. OUTPUT : rushes
multicam.

## M06 — Diriger une régie
WHY : décider en direct ce qui doit être gardé évite de tout re-tourner
— impossible ici (une seule journée). COMPETENCY : C6. ASSESSED : N1.
OUTPUT : journal de tournage.

## M07 — Monter une vidéo
WHY : c'est ici que la tension documentaire/vérité doit être arbitrée,
en écho direct à `KOR-01`/M06. COMPETENCY : C7. ASSESSED : N2. OUTPUT :
montage + note d'arbitrage.

## M08 — Postproduire (étalonnage, effets, son)
WHY : corriger sans trahir l'arbitrage déjà posé en M07. COMPETENCY :
C8. ASSESSED : N2. OUTPUT : vidéo postproduite.

## M09 — Encoder pour la livraison
WHY : un fichier mal encodé est illisible sur la plateforme cible, quel
que soit le montage. COMPETENCY : C9. ASSESSED : N1. OUTPUT : fichiers
encodés.

## M10 — Publier et contrôler la qualité
WHY : vérifier avant mise en ligne évite un défaut découvert après
publication. COMPETENCY : C10. ASSESSED : N2. OUTPUT : vidéo publiée +
fiche QC.

## M11 — Synthèse et certification
WHY : synthèse de bout en bout. COMPETENCY : C11. ASSESSED : N3,
`KOR03-A01`. OUTPUT : dossier + soutenance.

---

## Vérification de cohérence transversale

| Test | Résultat |
|---|---|
| Compétence unique et traçable par module | OK, voir `case/TRACEABILITY_MATRIX.md` |
| Progression N1→N2→N3 monotone | OK — N1 (M01,M02,M06,M09), N2 (M03-M05,M07,M08,M10), N3 (M11) |
| Aucune capacité KORA simulée (`NO_FAKE_KORA_FEATURE`) | OK — aucune dépendance produit, `REFERENTIAL.md` §6 |
| Cohérence avec la tension `KOR-01`/`KOR-03` (`KOR-0002` §4 #1) | OK — M03 (son synchrone à l'image) n'est pas un doublon de `KOR-01`/M05 (prise de son autonome) |

11 blueprints cohérents. Rédaction complète autorisée.
