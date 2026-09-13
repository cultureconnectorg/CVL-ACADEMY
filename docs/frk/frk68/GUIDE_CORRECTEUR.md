# FRK-68 — Guide Correcteur

## Avant de noter

Ouvre `frek_core.py` et `docs/gmd/gmd31`/`gmd32` à côté de la copie.

## Ce que tu vérifies en priorité

1. Le candidat fusionne-t-il les trois tables réelles ?
2. Décrit-il correctement le schedule de retry (5 tentatives) ?
3. Invente-t-il un mécanisme de retry supplémentaire ?
4. Déduit-il l'état d'un canal Good Mood (`frek_outbox`/
   `wallet_outbox`) à partir de l'état de l'autre pour un même
   `user_id` ?

## Ce que tu ne fais pas

Tu ne notes pas sur intuition générique — seulement sur le code et les
référentiels réels.
