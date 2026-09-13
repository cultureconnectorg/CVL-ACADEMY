# FRK-52 — Banque N2 (cas appliqués)

## Cas 1 — Conception d'une API REST générique

Le candidat conçoit une API REST avec versionnage et gestion d'erreur
cohérente, comme exercice marché-général, sans référence à un système
CVLN précis.

**Critère éliminatoire :** proposer une API sans stratégie de
versionnage.

**Critères de notation :** stratégie de version explicite (ex. `/v1/`)
et structure d'erreur cohérente (code HTTP sémantique + corps d'erreur
structuré).

## Cas 2 — Discipline CVLN-gap

Le candidat doit rédiger une note confirmant que `frek_core.py` n'a
aucune surface HTTP publique aujourd'hui.

**Critère éliminatoire :** affirmer que `frek_core.py` expose une API
publique.

## Cas 3 — Changement d'interface sans versionnage

Une équipe déploie une API sans stratégie de versionnage. Six mois
plus tard, elle doit renommer un champ de réponse critique. Explique
les conséquences concrètes de l'absence de versionnage dans ce
scénario, et ce qu'il aurait fallu faire dès le départ.

**Critères de notation :** identifie que tous les intégrateurs
existants verront leur code casser silencieusement dès le déploiement
du changement, sans aucun moyen de migrer à leur rythme. Explique
qu'une version dès le départ (`/v1/`) aurait permis de déployer `/v2/`
en parallèle, laissant `/v1/` fonctionnel pour une période de
transition. Élimination si le candidat propose de corriger après coup
sans reconnaître le problème structurel.
