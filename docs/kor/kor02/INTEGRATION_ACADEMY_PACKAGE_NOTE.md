# KOR-02 — Note d'intégration Academy (package, pas import)

```
NO_RUNTIME_BINDING_YET. Aucun contrat d'import n'est autorisé à ce
stade. Cette note documente comment ce package SERAIT compatible avec
le moteur d'import existant, sans y toucher.
```

## Ce que ce document n'est pas

Ni une spécification technique d'import, ni une extension de schéma
appliquée. Aucun fichier de `fms_import/`, `fms_canonical/`,
`klt_canonical/` n'a été modifié pour produire ce package
(`NO_RUNTIME_BINDING`, `NO_KORA_PRODUCT_UPGRADE` — vérifié par `git
diff --stat` avant commit).

## Compatibilité structurelle

Même patron que `docs/kor/kor01/INTEGRATION_ACADEMY_PACKAGE_NOTE.md` —
structure analogue à `klt_canonical` (scan direct d'un dossier
`docs/kor/`, sans ZIP), registre de compétences à 5 colonnes (sans
colonne de statut BUILT/BLOCKED, cohérent avec l'absence de
`PRODUCT_DEPENDENCY` confirmée par `KOR-0002` §3).

## Continuité inter-formations — un point d'attention réel pour un futur parsing

`KOR-02` référence, dans son cas fil rouge, une ressource produite par
`KOR-01` (l'interview audio de Man Rosa). Un futur `kor_canonical`
devrait donc permettre une référence croisée entre formations d'un même
pôle (`KOR`), à la différence de `klt_canonical` et `fms_canonical` qui
traitent chaque formation en isolation. Ce point est signalé ici comme
**besoin identifié, non construit** — le cas pédagogique fonctionne dès
aujourd'hui sans cette brique technique (les deux cas sont des
documents autonomes qui se référencent en texte, pas via un lien de
données réel).

## Ce qui resterait à faire avant tout import réel (non fait ici)

- Écrire `backend/kor_canonical/` pour `KOR-01` et `KOR-02` ensemble
  (au moins deux formations avant de justifier un moteur d'import,
  cohérent avec la remarque de `docs/kor/kor01/
  INTEGRATION_ACADEMY_PACKAGE_NOTE.md`).
- Modéliser la référence croisée `KOR-01`→`KOR-02` si elle doit devenir
  une donnée réelle plutôt qu'un simple renvoi textuel entre cas.
- Répéter la construction pour `KOR-03`→`15` — non engagé par ce
  ticket (`NO_KOR03_15_BUILD`, hérité de `KOR-0002`).

Rien de ce qui précède n'est engagé par ce ticket — c'est un futur
raisonnable, pas une promesse.
