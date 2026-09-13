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
5. Que se passe-t-il exactement, techniquement, lorsque
   `emit_signal()` est appelé avec une valeur hors de `VALID_SIGNALS`
   — une erreur, ou un no-op silencieux ?
6. Qu'est-ce qu'un signal de résonance et en quoi se distingue-t-il à
   la fois de l'affinité (proximité statique) et de la cadence (rythme
   temporel) ?
7. Pourquoi la frontière entre ce vocabulaire et `VALID_SIGNALS`
   doit-elle être répétée explicitement à chaque module, plutôt
   qu'affirmée une seule fois en introduction ?
8. Si une future extension de `frek_core.py` ajoutait un neuvième
   signal réel, cela changerait-il la nature conceptuelle du
   vocabulaire affinité/résonance/cadence enseigné ici ?

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
5. Un no-op silencieux — aucune exception n'est levée, aucun effet ne
   se produit, ce qui rend l'erreur particulièrement dangereuse car
   elle passe inaperçue sans vérification explicite.
6. La résonance mesure l'intensité de réaction émotionnelle/sociale à
   un contenu (ex. partage, discussion suscitée), distincte de la
   simple proximité d'intérêt (affinité) et du rythme temporel
   (cadence) — trois dimensions complémentaires mais indépendantes.
7. Parce que la confusion entre les deux vocabulaires est le piège le
   plus fréquent et le plus grave de cette formation — la répétition
   à chaque module renforce la discipline plutôt que de risquer un
   oubli après une seule mention.
8. Non — le vocabulaire affinité/résonance/cadence reste un concept
   marché-général indépendant, quel que soit le nombre de valeurs
   réelles dans `VALID_SIGNALS` ; les deux vocabulaires restent
   distincts par conception, pas par accident d'implémentation
   actuelle.
