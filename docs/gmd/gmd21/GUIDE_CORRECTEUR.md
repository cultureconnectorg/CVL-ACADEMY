# GMD-21 — Guide Correcteur

## Ce que tu corriges

Une copie GMD-21 comprend : un score N1 (auto-corrigeable contre
`BANQUE_N1.md`), un écrit N2 (1 cas parmi 3), et le livrable M1 (carte
de routes annotée). Utilise `ASSESSMENT_AND_RUBRIC.md` pour la grille
complète.

## Comment vérifier le livrable M1 (le plus important à corriger correctement)

La carte de routes du candidat doit être comparée **ligne par ligne**
à la vraie table de routes de `gmfest972/goodmooddjsayd/backend/
server.py`. Ce n'est pas un exercice d'opinion — chaque route existe
ou n'existe pas, est publique ou admin-gated, chaque attribution à une
formation GMD est vérifiable. Un correcteur qui note "au feeling"
sans revérifier le code introduit exactement le risque
`FAKE_PROOF`/`UNPROVEN_FEATURE` que cette Academy existe pour éviter.

## Application du seuil d'élimination

Si une copie affirme qu'un mécanisme d'incident/rollback existe (le
gap GMD-34), ou invente un champ de modèle, applique le 0 automatique
sur la compétence concernée — **même si le reste de la copie est
excellent**. Ce n'est jamais négociable, c'est la règle centrale de
cette formation.

## Cas limites fréquents

- Le candidat cite une route qui existe mais l'attribue à la mauvaise
  formation GMD : erreur mineure (pas d'élimination), pénaliser C2.
- Le candidat propose une hypothèse raisonnable non vérifiable dans le
  temps imparti, en la présentant explicitement comme une hypothèse à
  vérifier : ce n'est **pas** une invention, ne pas éliminer — c'est
  exactement le comportement honnête recherché.
