# KLT-04 — Gouvernance des organisations et réseaux culturels — Référentiel canonique + Blueprints

```
Méthode identique à KLT-01/02/03. KLT-0002 a validé pour KLT-04
(STATUS=RESOLVED) : le droit associatif loi 1901 reste une fondation du
parcours ; le canon l'étend selon la progression :
association -> gouvernance -> comités -> délégations ->
réseau multi-opérateurs -> conformité -> audit.
Aucune suppression du contenu legacy.
```

## Taille réelle de cette formation — pourquoi 14 modules, pas 11

`KLT-0002` a établi que legacy et master plan ont un **recouvrement
module-à-module quasi nul** pour `KLT-04` : le legacy est entièrement
spécifique au droit associatif français (loi 1901) — une **fondation**
—, le master plan est entièrement centré sur la gouvernance réseau/
multi-opérateurs — une **extension**. Ce n'est pas une divergence à
arbitrer (contrairement à `KLT-03`) : c'est exactement le scope plus
large que le statut `UPGRADE` du master plan annonçait. Forcer un compte
de module identique aux autres formations couperait soit la fondation
associative réelle, soit l'extension réseau réelle. **14 modules**, pas
11 — la matrice de compétences commande le nombre, honnêtement, même
quand il diffère des formations voisines.

## Métier cible

**Responsable administration culturelle / gouvernance associative** —
ROME `k1808`/`k1604`, confiance marché **low**, avec un flag explicite
("conformité associative à vérifier", `external_calibration.py:442-459`)
— préservé comme signal d'humilité, pas effacé.

## Responsabilités réelles

Fonder et faire vivre une association culturelle dans le cadre légal
réel (loi 1901) · assumer ou superviser les rôles associatifs · tenir une
comptabilité et une fiscalité culturelle conformes · produire les
documents obligatoires · distinguer association, réseau, opérateur et
comité · organiser des comités et des décisions au-delà d'une seule
structure · déléguer et mandater dans un réseau · prévenir les conflits
d'intérêt · gouverner un réseau multi-opérateurs/multi-territoires ·
assurer conformité et responsabilité · auditer un dispositif de
gouvernance.

## Limites du rôle

**Ne conduit pas** l'action de médiation de terrain (`KLT-01`) · **ne
gère pas** le budget opérationnel d'un projet unique (`KLT-02`) · **ne
représente pas** institutionnellement Kiltikonet dans une négociation
externe (`KLT-03`) · **n'opère pas** la plateforme Kiltikonet.fr
(`KLT-05`). C'est la seule des 5 formations dont le mandat porte sur la
structure elle-même (gouvernance), pas sur une action ou un projet
qu'elle mène.

## Publics / Contextes

Public : `INTERMEDIAIRE, PROFESSIONNEL, INSTITUTIONNEL`
(`catalog_cartography.py:258`, `KEEP`). Contexts : `EXTERNAL, BRIDGE`
(`:257`, `KEEP` pour l'instant) — **mais** `KLT-0002` a validé un
`PROPOSE_CHANGE` : le scope élargi vers la gouvernance réseau (comités,
RBAC, gouvernance territoriale multi-opérateurs) touche plausiblement des
surfaces internes à CVLN, pas seulement externes. **Ce référentiel ne
mute rien** (`DB_CONTEXT_MUTATION = FORBIDDEN`) — la proposition reste
ouverte pour le futur ticket de migration dédié mentionné dans
`KLT-0002`.

## Compétences (14) et modules — correspondance LEGACY → CANON

| # | Compétence | Origine | Module | Étape (progression Founder) |
|---|---|---|---|---|
| C1 | Fonder et faire vivre une association culturelle (loi 1901) | legacy M01+M02 (`MERGE`) | M01 | association |
| C2 | Assumer les rôles associatifs (Président/Trésorier/Secrétaire/DAF) | legacy M03 (`KEEP`) | M02 | association |
| C3 | Tenir une comptabilité associative | legacy M04 (`KEEP`) | M03 | association |
| C4 | Maîtriser la fiscalité culturelle | legacy M05 (`KEEP`) | M04 | association |
| C5 | Produire les documents obligatoires (AG, PV) | legacy M06 (`KEEP`) | M05 | association |
| C6 | Gérer la dimension salariale et bénévole | legacy M07 (`KEEP`) | M06 | association |
| C7 | Distinguer association, réseau, opérateur, comité | master plan M01 (`BUILD_NEW`) | M07 | gouvernance |
| C8 | Organiser comités et décisions | master plan M03 (`BUILD_NEW`) | M08 | comités |
| C9 | Déléguer et mandater dans un réseau | master plan M02 (`BUILD_NEW`) | M09 | délégations |
| C10 | Prévenir et traiter les conflits d'intérêt | master plan M05 (`BUILD_NEW`) | M10 | (éthique transversale) |
| C11 | Gouverner un réseau multi-opérateurs/multi-territoires | master plan M06 (`BUILD_NEW`) | M11 | réseau multi-opérateurs |
| C12 | Assurer conformité et responsabilité | master plan M04 (`BUILD_NEW`) | M12 | conformité |
| C13 | Auditer un dispositif de gouvernance | legacy M08 + master plan M07 (`MERGE`) | M13 | audit |
| C14 | Arbitrer une crise de gouvernance sous contrainte (synthèse) | master plan M08 (`BUILD_NEW`, terminal) | M14 | synthèse |

**Aucun module legacy n'est perdu.** Les 6 premiers modules (M01-M06)
sont la fondation associative réelle, intégralement conservée ; M07-M14
sont l'extension réseau que le statut `UPGRADE` appelait.

## Blueprints (résumé)

| Module | WHY_THIS_MODULE_EXISTS | ASSESSED | WHAT_REAL_OUTPUT |
|---|---|---|---|
| M01 | Sans cadre légal réel, une association culturelle n'a pas d'existence juridique | N1 | Statuts modèles annotés + dossier de création |
| M02 | Des rôles mal répartis produisent des conflits internes évitables | N1/N2 | Fiches de rôles + charte |
| M03 | Sans comptabilité tenue, une association perd sa crédibilité et son financement | N2 | Bilan + compte de résultat |
| M04 | Une erreur fiscale peut menacer l'existence légale d'une structure culturelle | N2 | Note fiscale + arbre de décision |
| M05 | Sans PV et documents obligatoires, une décision associative n'a pas de valeur opposable | N1/N2 | PV type AGO/AGE |
| M06 | Le bénévolat et le salariat obéissent à des règles distinctes qu'une association mélange souvent à tort | N2 | Fiche paie + convention bénévolat |
| M07 | Sans distinguer association/réseau/opérateur/comité, "gouvernance" reste un mot vague | N1 | Schéma de gouvernance |
| M08 | Une décision prise hors comité formel n'est pas traçable ni opposable | N2 | Registre de décisions |
| M09 | Un réseau sans délégation claire recentralise tout sur une seule personne | N2 | Matrice des autorités |
| M10 | Un conflit d'intérêt non traité discrédite toute la gouvernance | N2 | Note éthique |
| M11 | Gérer plusieurs opérateurs/territoires n'est pas gérer une association démultipliée | N2 | Modèle de gouvernance réseau |
| M12 | Ignorer une obligation de conformité expose la structure à un risque réel | N2 | Check de conformité |
| M13 | Sans méthode d'audit, "vérifier la gouvernance" reste une impression | N2/N3 | Rapport d'audit |
| M14 | La synthèse sous crise distingue un vrai responsable de gouvernance d'un exécutant de procédure | N3 (`KLT04-A01`) | Assessment + plan correctif |

Cohérence transversale vérifiée : progression N1→N3 monotone, aucune
compétence testée sans module, aucune dépendance Kiltikonet simulée.
