# FRK-43 — Guide Correcteur

## Avant de noter

Relis `REFERENTIAL.md` §Objectives et §Modules — en particulier le
calendrier réel de Good Mood (`[30s, 2m, 10m, 1h, 6h]`) et la
discipline de citation.

## Ce que tu vérifies en priorité

1. Le mécanisme proposé persiste-t-il le message localement avant
   tentative d'envoi ?
2. Le backoff est-il réellement progressif, ou seulement à intervalle
   fixe ? Applique la règle éliminatoire sans exception si absence
   totale de mécanisme d'échec persistant.
3. La copie présente-t-elle l'outbox de Good Mood comme une
   infrastructure FREK ? Applique la règle éliminatoire sans exception
   si oui.

## Ce que tu ne fais pas

Tu ne notes jamais sur une intuition personnelle de fiabilité
distribuée — seulement sur la solidité technique réelle du mécanisme
et l'exactitude de la citation de Good Mood.
