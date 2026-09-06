# GMD-22 — Banque N2 (cas appliqués)

## Cas N2-1 — Nouvel album à publier avant un concert

Un artiste sort un nouvel EP demain matin, avant un concert le soir
même. Le manager demande : "mets-le en avant, en premier dans le
catalogue, avec le lien SoundCloud." Décris, dans l'ordre exact des
appels API réels, comment tu procèdes — y compris comment tu garantis
qu'il apparaît **avant** les volumes existants.

**Critères de notation:**
- Utilise `POST /admin/catalogue` avec un `order` inférieur à tous les
  volumes existants (0 déjà suffit si tous les autres sont ≥1 — le
  candidat doit vérifier, pas supposer).
- Cite `sc_track` comme champ optionnel `int`, pas un champ texte —
  une inversion type "sc_track: 'https://soundcloud.com/...'" est une
  erreur de modèle, à signaler.
- Vérifie le résultat via `GET /catalogue` (vue publique), pas
  seulement `GET /admin/catalogue` — un candidat qui ne vérifie que la
  vue admin n'a pas prouvé que le fan verra le changement.
- **Élimination automatique** si le candidat invente un champ
  "featured"/"pinned" qui n'existe pas sur `Volume`.

## Cas N2-2 — Doublon détecté après import

Un stagiaire a créé le même volume deux fois par erreur (deux `POST`
distincts, deux `id` différents, mêmes `title`/`number`). Le manager
demande de nettoyer sans perdre l'historique de lecture (`plays`).
Décris la procédure réelle.

**Critères de notation:**
- Identifie qu'il n'existe **aucune contrainte d'unicité** visible
  dans `VolumeIn`/`Volume` (pas de champ `unique` documenté) — donc
  les deux enregistrements coexistent silencieusement tant qu'aucune
  action n'est prise.
- Propose de comparer les deux valeurs `plays` avant de choisir lequel
  supprimer (`DELETE /admin/catalogue/{vid}`) — si les deux valeurs
  diffèrent, alerter le manager avant de trancher plutôt que de choisir
  arbitrairement (aucune fusion de compteur n'existe dans l'API réelle
  — ne pas inventer un merge automatique).
- Élimination automatique si le candidat invente une route
  `/admin/catalogue/merge` inexistante.

## Cas N2-3 — Panne partielle : réordonnancement demandé sous pression

Le manager veut réorganiser 12 volumes en pleine interview live, en
urgence, par téléphone, sans accès à un tableau de bord visuel. Décris
comment tu traduis une liste orale ("le nouveau single en premier,
puis les 3 derniers albums, puis le reste dans l'ordre existant") en
appels API réels, et comment tu limites le risque d'erreur sous
pression.

**Critères de notation:**
- Reconnaît qu'il n'existe pas de route "reorder batch" — chaque
  changement d'`order` passe par un `PUT /admin/catalogue/{vid}`
  individuel (12 appels, pas un seul) — un candidat qui suppose un
  batch endpoint invente une capacité.
- Propose de noter la correspondance `id ↔ nouvel order` par écrit
  avant d'exécuter les 12 appels, pour permettre une vérification a
  posteriori (`GET /admin/catalogue` trié) plutôt que de travailler à
  l'aveugle sous pression.
- Élimination automatique si le candidat prétend qu'une action
  "publie" un changement séparément de l'appel `PUT` — il n'existe pas
  de distinction save/publish sur ce modèle (contrairement à un futur
  CMS de l'Academy elle-même — ne pas confondre les deux systèmes).
