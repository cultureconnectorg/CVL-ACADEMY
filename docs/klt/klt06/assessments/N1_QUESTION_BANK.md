# KLT-06 — Banque N1

```
Répartition : notions, méthode, éthique, limites. Couvre les 7
compétences (C1-C7) — C5/C6 ajoutées 2026-09-07 après construction sur
le schéma réel vérifié de l'Observatory Kiltikonet.
```

**Q-N1-01** (notions, C1) — Un observatoire de données culturelles se
distingue d'un rapport ponctuel par :
`CORRECT_ANSWER` : la continuité, la granularité définie et une
gouvernance de la donnée dans le temps.
`RATIONALE` : M01.
`DISTRACTOR_RATIONALE` : "le nombre de chiffres qu'il contient" ignore la
définition structurelle posée en M01.
`DIFFICULTY` : facile.

**Q-N1-02** (limites, C1) — Un observatoire Kiltikonet existe-t-il
aujourd'hui dans Academy ?
`CORRECT_ANSWER` : non — `NOT_CONNECTED` (`KLT-0001` §4).
`RATIONALE` : M01, en-tête `KILTIKONET_DEPENDENCY`.
`DISTRACTOR_RATIONALE` : "oui, en version limitée" contredit
l'état réel constaté dans ce repo.
`DIFFICULTY` : moyen.

**Q-N1-03** (méthode, C2) — Un chiffre sans source identifiable doit
être traité comme :
`CORRECT_ANSWER` : non vérifié, ni vrai ni faux tant qu'il n'est pas
qualifié.
`RATIONALE` : M02.
`DISTRACTOR_RATIONALE` : "faux jusqu'à preuve du contraire" est aussi peu
fondé que de le traiter comme vrai.
`DIFFICULTY` : moyen.

**Q-N1-04** (notions, C2) — La traçabilité d'une donnée désigne :
`CORRECT_ANSWER` : la capacité à remonter jusqu'à sa source d'origine.
`RATIONALE` : M02.
`DISTRACTOR_RATIONALE` : "sa présence dans un tableau" confond stockage
et traçabilité.
`DIFFICULTY` : facile.

**Q-N1-05** (méthode, C3) — Face à une demande de données vague ("des
données sur l'impact"), la première étape est :
`CORRECT_ANSWER` : faire préciser l'intention réelle du demandeur.
`RATIONALE` : M03.
`DISTRACTOR_RATIONALE` : "produire un rapport d'impact générique" saute
l'étape de spécification posée en M03.
`DIFFICULTY` : moyen.

**Q-N1-06** (limites, C3) — Une spécification de besoin de données peut-
elle promettre une donnée non réellement mesurable ?
`CORRECT_ANSWER` : non — seules les données réellement mesurables avec
les moyens disponibles doivent être promises.
`RATIONALE` : M03.
`DISTRACTOR_RATIONALE` : "oui, si le demandeur insiste" contredit la
discipline de spécification honnête posée en M03.
`DIFFICULTY` : moyen.

**Q-N1-07** (éthique, C4) — Réutiliser une donnée communautaire au-delà
du périmètre de son consentement initial, même pour "enrichir" une
analyse, est :
`CORRECT_ANSWER` : un dépassement de consentement, jamais acceptable
sans revalidation.
`RATIONALE` : M04.
`DISTRACTOR_RATIONALE` : "acceptable si l'intention est bonne" ignore que
le consentement est scopé, pas une autorisation générale.
`DIFFICULTY` : difficile.

**Q-N1-08** (notions, C4) — Le consentement donné pour une collecte de
donnée est :
`CORRECT_ANSWER` : scopé à un usage précis, pas une autorisation
générale future.
`RATIONALE` : M04.
`DISTRACTOR_RATIONALE` : "valable pour tout usage futur raisonnable"
contredit directement la notion posée en M04.
`DIFFICULTY` : moyen.

**Q-N1-09** (méthode, C7) — Restituer une analyse à un public non
spécialiste signifie :
`CORRECT_ANSWER` : garder le même sens et les mêmes limites, avec un
vocabulaire adapté.
`RATIONALE` : M07.
`DISTRACTOR_RATIONALE` : "simplifier au point de gommer les
incertitudes" est l'erreur explicitement nommée en M07.
`DIFFICULTY` : moyen.

**Q-N1-10** (limites, C7) — Une restitution qui omet de préciser
qu'aucune donnée fiable n'existe sur un point est :
`CORRECT_ANSWER` : trompeuse, même si le reste du contenu est exact.
`RATIONALE` : M07.
`DISTRACTOR_RATIONALE` : "acceptable si le point est mineur" ignore
l'exigence d'honnêteté sur les limites posée en M07.
`DIFFICULTY` : difficile.

**Q-N1-11** (notions, C5) — Une maquette de tableau de bord conçue sur
le schéma réel vérifié de l'Observatory équivaut-elle à une requête live
sur des données réelles ?
`CORRECT_ANSWER` : non — Academy n'a aucun client/credentials appelant
cette API (`NOT_CONNECTED_TO_ACADEMY_RUNTIME`).
`RATIONALE` : M05, en-tête `KILTIKONET_DEPENDENCY`.
`DISTRACTOR_RATIONALE` : "oui, puisque le système est réel" confond
l'existence vérifiée du système et sa connexion réelle à Academy.
`DIFFICULTY` : moyen.

**Q-N1-12** (limites, C5) — Face à une métrique dont la collection
réelle est vide, la maquette doit :
`CORRECT_ANSWER` : afficher explicitement l'état `NOT_CONFIGURED`,
jamais inventer un chiffre plausible.
`RATIONALE` : M05.
`DISTRACTOR_RATIONALE` : "estimer un chiffre réaliste en attendant" est
une fabrication de donnée, interdite par `NO_FAKE_LIVE_CONNECTION`.
`DIFFICULTY` : difficile.

**Q-N1-13** (méthode, C6) — Interpréter un signal territorial réel pour
appuyer une décision signifie :
`CORRECT_ANSWER` : formuler une recommandation d'attention, jamais
décider à la place du rôle réseau.
`RATIONALE` : M06.
`DISTRACTOR_RATIONALE` : "trancher directement la décision réseau à sa
place" dépasse le rôle d'analyste posé en M06.
`DIFFICULTY` : moyen.

---

**Couverture** : 13 questions, réparties sur les 7 compétences
construites (`C1`-`C7`).
