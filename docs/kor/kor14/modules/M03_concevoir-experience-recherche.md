# KOR-14 — M03 — Concevoir une expérience de recherche

```
MODULE_ID: KOR14-M03
COMPETENCY_ID: C3 — Concevoir une expérience de recherche
PREREQUISITES: M02
ASSESSMENT_LEVEL: N2
KORA_DEPENDENCY: aucune ; métadonnées de recherche renvoyées à KOR-08
ROLE_BOUNDARIES: aucune
FREK_PROOF_MAPPING: READY_FOR_FREK_PROOF = FALSE
ORIGIN: net-new
```

## Situation professionnelle

Un auditeur ne retrouve pas *Rasin* via la recherche — la variabilité
orthographique du créole et des translittérations multiples fait
échouer une recherche trop stricte.

## Objectifs d'apprentissage

- Concevoir une recherche tolérante à la variabilité orthographique.
- Éviter le résultat "aucun résultat" quand une correspondance
  partielle existe.

## Notions essentielles

La **tolérance orthographique** doit couvrir le créole et ses
translittérations multiples, avec des suggestions plutôt qu'un échec
sec. Des **résultats partiels** valent mieux qu'un "aucun résultat"
quand une correspondance proche existe. Les **métadonnées** nécessaires
à une bonne recherche (titres, mots-clés) sont renvoyées à `KOR-08`,
pas reconstruites ici.

## Méthode

1. Identifier les variantes orthographiques plausibles pour les termes
   de recherche pertinents.
2. Concevoir un comportement de résultats partiels/suggestions plutôt
   qu'un échec sec.
3. Vérifier que les métadonnées nécessaires relèvent bien de `KOR-08`.

## Exemples

Une recherche "Rasin" échouant sur "Rasine" ou une translittération
alternative propose des suggestions ("Vouliez-vous dire Rasin ?")
plutôt qu'un écran vide. À l'inverse, concevoir une recherche qui
n'accepte que l'orthographe exacte enregistrée en métadonnées
(`KOR-08`) exclurait précisément les auditeurs dont l'orthographe
créole varie — la tolérance orthographique n'est pas un détail
technique, c'est une condition d'accès pour cette audience.

## Cas

Épisode B — un auditeur ne retrouve pas *Rasin* via la recherche
(`case/CASE.md`).

## Erreurs fréquentes

- Concevoir une recherche qui échoue sec sans suggestion.
- Ignorer la variabilité orthographique réelle du créole.
- Reconstruire des métadonnées de recherche au lieu de les renvoyer à
  `KOR-08`.

## Activité

Identification des variantes orthographiques plausibles pour les
termes pertinents.

## Exercice

Produire la maquette de recherche tolérante avec cas de test
orthographiques.

## Livrable

Maquette de recherche (`EVIDENCE_TYPE = SEARCH_UX_MOCKUP`).

## Critères de réussite

- La recherche propose des suggestions plutôt qu'un échec sec.
- Les cas de test orthographiques couvrent des variantes réelles.
- Les métadonnées nécessaires sont renvoyées à `KOR-08`.

## Preuve

Maquette de recherche, `READY_FOR_FREK_PROOF = FALSE`.

## Auto-évaluation

*Ma recherche resterait-elle accessible à une orthographe créole
variable, ou n'accepterait-elle qu'une forme unique ?*

## Passage au module suivant

Une fois le contenu trouvé, il doit être organisé simplement dans une
bibliothèque personnelle, conçue en M04.
