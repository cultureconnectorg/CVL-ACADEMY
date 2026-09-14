# KLT-08 — Banque N1

```
Répartition : notions, méthode, limites. Couvre les 7 compétences
(C1-C7) — C4 ajoutée 2026-09-07 après construction sur le schéma réel
vérifié du Network Kiltikonet.
```

**Q-N1-01** (notions, C1) — Un audit réseau, par rapport à un audit
d'association, ajoute principalement :
`CORRECT_ANSWER` : une dimension de consolidation et de comparaison
entre plusieurs structures.
`RATIONALE` : M01.
`DISTRACTOR_RATIONALE` : "une méthode entièrement différente" ignore que
la méthode de fond reste la même, seule l'échelle change.
`DIFFICULTY` : moyen.

**Q-N1-02** (limites, C1) — Refaire, pour Mémoire Vive, un audit
identique à celui déjà mené en `KLT-04`/M13 est :
`CORRECT_ANSWER` : une confusion d'échelle — les résultats existants
doivent être réutilisés, pas reproduits.
`RATIONALE` : M01.
`DISTRACTOR_RATIONALE` : "nécessaire pour la rigueur" ignore l'exigence
de réutilisation posée en M01.
`DIFFICULTY` : moyen.

**Q-N1-03** (méthode, C2) — Une grille d'audit réseau doit :
`CORRECT_ANSWER` : hériter explicitement de la méthode déjà validée à
l'échelle association.
`RATIONALE` : M02.
`DISTRACTOR_RATIONALE` : "être reconstruite entièrement à partir de
zéro" contredit le principe d'héritage posé en M02.
`DIFFICULTY` : moyen.

**Q-N1-04** (notions, C3) — Consolider des audits individuels signifie :
`CORRECT_ANSWER` : préserver les disparités réelles entre opérateurs,
pas les lisser.
`RATIONALE` : M03.
`DISTRACTOR_RATIONALE` : "en faire une moyenne globale" est exactement
l'erreur nommée en M03.
`DIFFICULTY` : difficile.

**Q-N1-05** (limites, C3) — Une vue réseau qui absorbe un point de
fragilité connu dans une conclusion flatteuse est :
`CORRECT_ANSWER` : une consolidation stérile, à corriger.
`RATIONALE` : M03.
`DISTRACTOR_RATIONALE` : "acceptable si la majorité des opérateurs sont
solides" ignore l'exigence de fidélité posée en M03.
`DIFFICULTY` : difficile.

**Q-N1-06** (méthode, C5) — Un support de formation opérateurs efficace
doit :
`CORRECT_ANSWER` : expliquer comment appliquer la règle, pas seulement
la répéter.
`RATIONALE` : M05.
`DISTRACTOR_RATIONALE` : "lister exhaustivement toutes les obligations
légales" ignore l'exigence d'actionnabilité posée en M05.
`DIFFICULTY` : moyen.

**Q-N1-07** (limites, C6) — Une recommandation d'audit réseau formulée
comme une instruction impérative est :
`CORRECT_ANSWER` : un dépassement du rôle d'audit, même à l'échelle
réseau.
`RATIONALE` : M06, héritage `KLT-04`/M13.
`DISTRACTOR_RATIONALE` : "acceptable si la situation est urgente"
contredit directement la discipline posée en M06.
`DIFFICULTY` : difficile.

**Q-N1-08** (notions, C6) — À l'échelle réseau, la règle "l'audit
recommande, il ne décide pas" :
`CORRECT_ANSWER` : reste identique, avec un poids supplémentaire.
`RATIONALE` : M06.
`DISTRACTOR_RATIONALE` : "s'assouplit, car l'enjeu réseau est plus
large" est l'inverse de ce que pose M06.
`DIFFICULTY` : moyen.

**Q-N1-09** (méthode, C7) — Face à une non-conformité réseau qui dépasse
son mandat, le responsable d'audit doit :
`CORRECT_ANSWER` : la documenter et l'escalader, sans tenter de la
corriger seul.
`RATIONALE` : M07.
`DISTRACTOR_RATIONALE` : "la corriger directement pour gagner du temps"
dépasse le rôle d'audit défini en M06/M07.
`DIFFICULTY` : difficile.

**Q-N1-10** (limites, C7) — Une escalade sans documentation suffisante
est :
`CORRECT_ANSWER` : insuffisante pour permettre une décision informée.
`RATIONALE` : M07.
`DISTRACTOR_RATIONALE` : "acceptable si la situation est évidente"
ignore l'exigence de documentation posée en M07.
`DIFFICULTY` : moyen.

**Q-N1-11** (notions, C4) — Une fiche de suivi de conformité conçue sur
le schéma réel vérifié du Network équivaut-elle à une requête live sur
des données réelles ?
`CORRECT_ANSWER` : non — Academy n'a aucun client/credentials appelant
cette API (`NOT_CONNECTED_TO_ACADEMY_RUNTIME`).
`RATIONALE` : M04, en-tête `KILTIKONET_DEPENDENCY`.
`DISTRACTOR_RATIONALE` : "oui, puisque le système est réel" confond
l'existence vérifiée du système et sa connexion réelle à Academy.
`DIFFICULTY` : moyen.

**Q-N1-12** (limites, C4) — Face à un score de conformité agrégé non
disponible (`compliance_available = false`), la fiche de suivi doit :
`CORRECT_ANSWER` : afficher explicitement l'état `NOT_CONFIGURED`,
jamais inventer un score plausible.
`RATIONALE` : M04.
`DISTRACTOR_RATIONALE` : "estimer un score réaliste en attendant" est
une fabrication de donnée, interdite par `NO_FAKE_LIVE_CONNECTION`.
`DIFFICULTY` : difficile.

---

**Couverture** : 12 questions, réparties sur les 7 compétences
construites (`C1`-`C7`).
