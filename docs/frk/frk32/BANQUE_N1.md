# FRK-32 — Banque N1 (formatif)

Réserve `FRK32.SKILL.*`.

1. Qu'est-ce qu'un signal de contexte/device (ex. type d'appareil,
   canal d'accès) et pourquoi reste-t-il distinct de `VALID_SIGNALS`
   (`frek_core.py`) — même règle de frontière que FRK-31 ?
2. Qu'est-ce que la capture technique d'un signal de consentement, et
   pourquoi cette formation ne couvre-t-elle QUE le côté technique
   (capture), jamais la gouvernance du consentement elle-même ?
3. Que dit la doctrine Fondation Cœurvolan §18 sur le consentement, et
   pourquoi cette formation la référence-t-elle sans la dupliquer ?
4. Pourquoi confondre capture technique de signal et gouvernance de
   consentement serait-il éliminatoire ici ?

## Corrigé indicatif

1. Ce vocabulaire (contexte/device/consent) est marché-général et
   distinct des 8 valeurs réelles de `VALID_SIGNALS` — même règle de
   frontière obligatoire que FRK-31.
2. La capture technique enregistre l'événement de consentement (quand,
   comment) ; la gouvernance (qui peut consentir, pour quoi, sous
   quelles conditions légales) relève d'une doctrine séparée.
3. Fondation Cœurvolan §18 gouverne le consentement au sens
   communautaire/légal — cette formation la référence pour ne jamais
   dupliquer ou réinventer cette doctrine.
4. Cela laisserait croire qu'une compétence technique de capture
   suffit à garantir la conformité de gouvernance — un vide de méthode
   grave.
