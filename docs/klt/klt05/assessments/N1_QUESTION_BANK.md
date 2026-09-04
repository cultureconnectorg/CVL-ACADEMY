# KLT-05 — Banque N1

```
Répartition : notions, responsabilités, limites, publics, éthique,
méthode, reconnaissance de situation, lecture de contexte.
```

**Q-N1-01** (notions, C1) — Une plateforme culturelle de type Kiltikonet
relie principalement :
`CORRECT_ANSWER` : plusieurs surfaces fonctionnelles (contenus,
communauté, badges, support, analytics) qui doivent rester cohérentes.
`RATIONALE` : M01.
`DISTRACTOR_RATIONALE` : "un seul flux de publication" ignore
l'architecture réelle décrite en M01.
`DIFFICULTY` : facile.

**Q-N1-02** (notions, C2) — Le RBAC attribue des droits :
`CORRECT_ANSWER` : à un rôle, pas directement à une personne.
`RATIONALE` : M02.
`DISTRACTOR_RATIONALE` : "à chaque personne individuellement, de façon
ad hoc" contredit le principe même du RBAC.
`DIFFICULTY` : moyen.

**Q-N1-03** (responsabilités, C3) — Adapter un contenu source à un
format plateforme signifie :
`CORRECT_ANSWER` : ajuster la forme sans modifier le fond sans mandat.
`RATIONALE` : M03.
`DISTRACTOR_RATIONALE` : "enrichir le contenu avec des informations
supplémentaires" est l'erreur nommée en M03.
`DIFFICULTY` : moyen.

**Q-N1-04** (limites, C4) — Un protocole de badge/scan conçu en formation
peut-il être présenté comme une preuve réellement opposable ?
`CORRECT_ANSWER` : non — il doit être marqué comme simulé/pédagogique.
`RATIONALE` : M04, `ROLE_BOUNDARIES`.
`DISTRACTOR_RATIONALE` : "oui, s'il est bien documenté" confond rigueur
de conception et opposabilité réelle.
`DIFFICULTY` : difficile.

**Q-N1-05** (limites, `OPERATOR_AUTHORIZATION`) — Réussir la
certification `KLT-05` donne-t-elle un accès administrateur réel à
Kiltikonet.fr ?
`CORRECT_ANSWER` : non — `OPERATOR_AUTHORIZATION = NOT_IMPLEMENTED/
NOT_GRANTED`.
`RATIONALE` : `00_REFERENTIEL_ET_BLUEPRINTS.md`, avertissement central ;
M11.
`DISTRACTOR_RATIONALE` : "oui, au niveau opérateur senior" est
exactement l'erreur que ce référentiel interdit explicitement.
`DIFFICULTY` : difficile (question centrale de cette formation).

**Q-N1-06** (publics, C1) — Le public visé par `KLT-05` est :
`CORRECT_ANSWER` : `INTERMEDIAIRE, PROFESSIONNEL`.
`RATIONALE` : référentiel `KLT-05`, publics.
`DISTRACTOR_RATIONALE` : "INSTITUTIONNEL" ne fait pas partie du public
visé pour cette formation, à la différence de `KLT-03`/`KLT-04`.
`DIFFICULTY` : moyen.

**Q-N1-07** (éthique, C6) — Modérer un commentaire exprimant un désaccord
respectueux sur le sens du tanbou signifie :
`CORRECT_ANSWER` : le laisser, éventuellement recadré, sans le retirer.
`RATIONALE` : M06.
`DISTRACTOR_RATIONALE` : "le retirer pour préserver l'image de
l'association" contredit le principe de pluralité posé en M06.
`DIFFICULTY` : moyen.

**Q-N1-08** (éthique, C7) — Face à une question de support dont la
réponse n'est pas certaine, l'opérateur doit :
`CORRECT_ANSWER` : vérifier l'information réelle ou escalader, jamais
deviner.
`RATIONALE` : M07.
`DISTRACTOR_RATIONALE` : "répondre au mieux avec une estimation
raisonnable" contredit l'exigence d'exactitude posée en M07.
`DIFFICULTY` : moyen.

**Q-N1-09** (méthode, C8) — Référencer un partenaire sur la plateforme
doit être fidèle :
`CORRECT_ANSWER` : au niveau de partenariat réellement convenu.
`RATIONALE` : M08.
`DISTRACTOR_RATIONALE` : "à ce qui serait le plus flatteur pour la
plateforme" contredit la discipline de fidélité posée en M08.
`DIFFICULTY` : moyen.

**Q-N1-10** (reconnaissance de situation, C9) — Un rapport d'engagement
sur des chiffres modestes qui conclut à "un engouement fort" est :
`CORRECT_ANSWER` : une interprétation disproportionnée par rapport aux
données réelles.
`RATIONALE` : M09.
`DISTRACTOR_RATIONALE` : "une lecture optimiste mais acceptable" ignore
l'exigence de proportionnalité posée en M09.
`DIFFICULTY` : moyen.

**Q-N1-11** (lecture de contexte, C10) — Une correction d'incident faite
sans documentation est :
`CORRECT_ANSWER` : incomplète — sans trace, aucune leçon n'est tirée
pour l'avenir.
`RATIONALE` : M10.
`DISTRACTOR_RATIONALE` : "suffisante si le problème est résolu" ignore
l'exigence de documentation posée en M10.
`DIFFICULTY` : moyen.

**Q-N1-12** (lecture de contexte, C9) — Face à une donnée Observatory
absente pour le rapport d'engagement, l'opérateur doit :
`CORRECT_ANSWER` : nommer explicitement l'absence plutôt que la simuler.
`RATIONALE` : M09, `NO_FAKE_OBSERVATORY`.
`DISTRACTOR_RATIONALE` : "l'estimer à partir d'événements comparables"
revient à fabriquer une preuve non réelle.
`DIFFICULTY` : difficile.

---

**Couverture** : 12 questions, réparties sur les 8 catégories, tracées à
`C1`-`C10` (`C11` réservée à l'assessment terminal).
