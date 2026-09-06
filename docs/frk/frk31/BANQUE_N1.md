# FRK-31 — Banque N1 (formatif)

Réserve `FRK31.SKILL.*`.

1. Cite les 8 vraies valeurs de `VALID_SIGNALS` dans `frek_core.py`
   (`FREK-TIME/WORK/SCORE/LINK/CERT/CONTRIB/SHARE/MISSION`) et explique
   pourquoi le vocabulaire affinité/résonance/cadence enseigné ici n'en
   fait PAS partie.
2. Qu'est-ce qu'un signal d'affinité (proximité d'intérêt entre un
   utilisateur et un contenu) au sens marché-général des plateformes
   culturelles ?
3. Qu'est-ce qu'un signal de cadence (rythme d'engagement dans le
   temps) et en quoi diffère-t-il d'un simple compteur d'événements
   comme `FREK-WORK` ?
4. Pourquoi serait-il une erreur éliminatoire d'implémenter ce
   vocabulaire en appelant `emit_signal()` avec une valeur inventée
   hors de `VALID_SIGNALS` ?

## Corrigé indicatif

1. `frek_core.py` n'accepte que 8 valeurs strictes ; toute valeur hors
   de cet ensemble est silencieusement ignorée (`emit_signal` fait un
   no-op) — le vocabulaire affinité/résonance/cadence est un concept
   marché-général distinct, jamais implémenté dans ce fichier.
2. Un signal d'affinité mesure la proximité thématique/émotionnelle
   entre un profil et un contenu, indépendamment de toute plateforme
   CVLN précise.
3. La cadence mesure la régularité/rythme d'un comportement dans le
   temps (ex. fréquence de visite) ; `FREK-WORK` est un compteur brut
   d'un type d'action, sans dimension temporelle de rythme.
4. `emit_signal()` n'accepte que les 8 valeurs réelles — toute autre
   valeur est un no-op silencieux ; croire qu'on a « émis un signal
   d'affinité » via ce mécanisme serait une fausse déclaration de
   fonctionnalité.
