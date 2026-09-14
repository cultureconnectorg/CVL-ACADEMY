# KOR-08 — Note d'intégration Academy (package, pas import)

```
NO_RUNTIME_BINDING_YET.
```

Même patron que `KOR-01`→`07`. Point spécifique : un futur
`kor_canonical` devrait explicitement **ne jamais** synchroniser ses
métadonnées avec un futur système LabelOS sans une passerelle
documentée et validée séparément — cette frontière (§5 du
`REFERENTIAL.md`) doit être préservée dans toute implémentation
technique future. Aucun code touché ici (`NO_RUNTIME_BINDING`,
`NO_KORA_PRODUCT_UPGRADE`).
