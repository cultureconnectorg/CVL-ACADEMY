# FRK-28 — Guide Correcteur

## Avant de noter

Relis `REFERENTIAL.md` §Objectives et §Modules — en particulier la
nature réelle de `events.py` (bus pub/sub en mémoire) et les trois
garanties d'un registre de provenance (append-only, horodatage,
chaînage).

## Ce que tu vérifies en priorité

1. Le registre proposé est-il append-only par mécanisme technique, ou
   seulement par convention documentaire ? Applique la règle
   éliminatoire sans exception si mutable.
2. Le candidat confond-il `events.py` avec un registre de provenance
   existant ? Applique la règle éliminatoire sans exception si oui.
3. Le mécanisme de correction proposé passe-t-il par un événement
   compensatoire, jamais par une réécriture ou une suppression ?

## Ce que tu ne fais pas

Tu ne notes jamais sur une intuition personnelle d'architecture
événementielle — seulement sur la solidité technique réelle du
registre et l'exactitude de la frontière avec `events.py`.
