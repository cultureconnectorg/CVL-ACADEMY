# FRK-15 — Banque N1 (formatif)

Réserve `FRK15.SKILL.*`.

1. Pourquoi un rapport de preuve technique doit-il citer explicitement
   ses fondations (FRK-12 pour l'ingénierie de la preuve, FRK-14 pour
   la chaîne de custody) par référence, plutôt que les re-décrire ?
2. Quelle est la différence entre « vérifier un rapport » et
   « produire un rapport » — pourquoi la formation couvre les deux
   compétences séparément ?
3. Un rapport technique de preuve omet la section chaîne de custody en
   argumentant qu'elle est « hors périmètre ». Le candidat doit
   expliquer pourquoi ceci est une erreur structurelle, pas une
   simplification acceptable.
4. Pourquoi cette formation ne peut-elle pas être passée sans que le
   candidat maîtrise déjà FRK-12 ET FRK-14 (prérequis, pas suggestion) ?
5. Un rapport cite un artefact `issue_proof()` de `frek_core.py` comme
   preuve. Pourquoi ce stub ne peut-il jamais être présenté comme une
   preuve techniquement vérifiée ?
6. En quoi une conclusion « vérifiée » sans méthodologie documentée
   diffère-t-elle d'une simple affirmation d'autorité ?
7. Pourquoi la réutilisation par référence de FRK-12/FRK-14 évite-t-elle
   un risque de divergence de contenu entre formations ?
8. Quelle serait la conséquence pratique d'un rapport de preuve
   technique qui mélangerait la méthodologie de vérification et la
   méthodologie de production sans les distinguer ?

## Corrigé indicatif

1. Réutiliser par référence évite la duplication et la dérive de
   contenu entre formations — chaque brique reste la source unique de
   vérité pour son sujet.
2. Vérifier suppose un standard externe contre lequel comparer ;
   produire suppose de construire ce standard — deux disciplines
   distinctes malgré leur proximité.
3. Un rapport de preuve technique sans section chaîne de custody est
   incomplet par construction (FRK-14) — ce n'est jamais un choix de
   scope, c'est un vide de méthode.
4. Le rapport de preuve s'appuie structurellement sur les deux
   disciplines amont ; sans elles, la « vérification » resterait une
   coquille vide.
5. `issue_proof()` reste un stub sans garantie cryptographique réelle
   (frontière FRK-13) — l'affirmer vérifié introduirait une conclusion
   non appuyée par une méthode réelle, contraire à toute la discipline
   enseignée ici.
6. Une conclusion vérifiée s'appuie sur une méthode reproductible et
   documentée ; une affirmation d'autorité demande d'être crue sans
   moyen de contrôle indépendant — c'est exactement ce que la
   méthodologie de vérification prévient.
7. Parce que chaque brique amont reste l'unique source de vérité — sans
   citation par référence, une copie locale pourrait diverger
   silencieusement de l'original au fil des mises à jour.
8. Le rapport perdrait sa clarté méthodologique — un lecteur ne
   pourrait plus distinguer ce qui a été vérifié contre un standard
   externe de ce qui a été construit ex nihilo, rendant le rapport
   inutilisable comme preuve.
