# FRK-02 — Guide Candidat

## Avant de commencer

Prérequis : FRK-01, FRK-58. Sache décrire le positionnement
architectural réel de `frek_core.py` sans jamais inventer DID/VC/
provenance-graphe comme construits.

## Ce que tu dois savoir faire

Décrire la frontière client de `frek_core.py` (docstring : « the sole
boundary through which the app talks to FrekCore ») et son
positionnement conceptuel parmi Wallet/KORA/Agent Factory, sans jamais
affirmer de wiring observé.

## Comment réviser

1. Lis `REFERENTIAL.md` §Objectives et §Modules.
2. Révise `frek_core.py`.
3. Fais les 8 questions de `BANQUE_N1.md` + 3 cas de `BANQUE_N2.md`.

## Piège le plus fréquent

Inventer une architecture DID/VC/provenance-graphe comme construite —
élimination automatique. Second piège : confondre le contenu de
FRK-01 (system map opérationnel) avec celui de FRK-02
(positionnement architectural conceptuel).

## Règle absolue

Aucune architecture inventée.
