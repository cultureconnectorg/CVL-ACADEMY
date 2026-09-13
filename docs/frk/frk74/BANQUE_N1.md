# FRK-74 — Banque N1 (formatif)

Réserve `FRK74.SKILL.*`.

1. Pourquoi la spécification DSP Fingerprint de FREK v3 est-elle
   qualifiée de « la moins résolue » du cluster par son propre document
   `CE_QUI_MANQUE.md` ?
2. Cite les décisions produit explicitement encore ouvertes (taille de
   fenêtre FFT, hop size, nombre de bandes, algorithme lui-même) et
   pourquoi les enseigner comme « ouvertes » est le point pédagogique
   central, pas un défaut à masquer.
3. Pourquoi FRK-74 (empreinte DSP audio) reste-t-elle un domaine
   technique distinct de FRK-29/30 (empreinte culturelle générale,
   non-audio) ?
4. Pourquoi serait-il une erreur éliminatoire de présenter cette
   spécification comme « finalisée » dans une copie ?
5. Qu'est-ce qu'une fenêtre FFT et pourquoi sa taille non fixée
   affecte-t-elle directement la résolution fréquentielle/temporelle
   d'une future empreinte audio ?
6. Pourquoi le hop size (pas d'avancement entre fenêtres successives)
   reste-t-il une décision distincte de la taille de fenêtre, avec son
   propre compromis ?
7. En quoi le nombre de bandes fréquentielles influence-t-il la
   granularité d'une empreinte, indépendamment du choix d'algorithme ?
8. Pourquoi FRK-71 est-il un prérequis structurel pour FRK-74 plutôt
   qu'une simple recommandation ?

## Corrigé indicatif

1. Le document `CE_QUI_MANQUE.md` du corpus lui-même liste
   explicitement ces paramètres comme non verrouillés — l'honnêteté
   de cette auto-évaluation est la source de vérité.
2. Enseigner ces décisions comme ouvertes forme le candidat à
   distinguer une architecture verrouillée d'une architecture encore
   en cours de décision — compétence réelle d'ingénierie.
3. FRK-29/30 couvrent l'empreinte culturelle générale (non-audio) ;
   FRK-74 porte spécifiquement sur le traitement du signal numérique
   audio — domaines techniques différents malgré le mot « empreinte »
   partagé.
4. Cela masquerait le statut réel du travail en cours, contredisant la
   discipline du corpus lui-même qui déclare cette spec inachevée.
5. Une fenêtre FFT plus grande améliore la résolution fréquentielle
   mais dégrade la résolution temporelle (et inversement) — ce
   compromis reste non arbitré tant que la taille n'est pas fixée.
6. Le hop size détermine le chevauchement entre fenêtres successives
   (plus petit = plus de calcul mais plus de précision temporelle) —
   un compromis indépendant de la taille de fenêtre elle-même, avec
   ses propres conséquences sur coût et précision.
7. Plus de bandes offre une granularité fréquentielle plus fine mais
   augmente la dimensionnalité de l'empreinte résultante —
   indépendamment de l'algorithme choisi pour combiner ces bandes en
   signature finale.
8. Parce que FRK-74 s'appuie sur les fondations architecturales de
   FREK v3 déjà établies en FRK-71 (échelle de maturité, distinction
   concept/architecture/ingénierie) — sans cette base, le statut
   « en cours » de cette spécification resterait incompréhensible.
