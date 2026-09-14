# KLT-01 — M10 — Documenter et prouver

```
MODULE_ID: KLT01-M10
COMPETENCY_ID: C10 — Documenter et produire une preuve exploitable (net-new)
PREREQUISITES: M01-M09 (ce module documente leurs livrables réels)
ASSESSMENT_LEVEL: N2/N3
KILTIKONET_DEPENDENCY: Observatory — OBSERVATORY_INTEGRATION = FUTURE / NOT_CONNECTED (KLT-0001 §4, KLT-0002 §Kiltikonet product dependencies). Ce module ne lit, ne simule et ne suppose AUCUNE donnée Observatory réelle.
ROLE_BOUNDARIES: Documenter une preuve n'est pas la certifier officiellement (voir assessments/A01, skills/EVIDENCE_MODEL — READY_FOR_FREK_PROOF n'est pas une ancre externe réelle tant qu'elle n'existe pas)
FREK_PROOF_MAPPING: FREK-WORK + FREK-SCORE + FREK-CONTRIB (les signaux réels produits par M01-M09, agrégés ici — aucun nouveau signal inventé)
ORIGIN: master plan M07 (BUILD_NEW) — KLT0003_CANONICAL_REFERENTIAL §3, attention particulière demandée par le Founder (KLT-0004 §4)
```

## Situation professionnelle

Une action de médiation sans documentation n'a d'existence que dans le
souvenir de ceux qui y étaient. Ce module ne prétend pas connecter le
candidat à un système de preuve externe qui n'existe pas — il construit
la capacité, réellement disponible aujourd'hui, à documenter son propre
travail de façon traçable et défendable.

## Objectifs d'apprentissage

- Constituer un registre de preuves structuré à partir des livrables
  réels produits en M01-M09.
- Distinguer documentation, source, provenance et preuve — quatre
  notions souvent confondues.
- Traiter le consentement et la confidentialité comme des conditions de
  la preuve, pas des options.
- Nommer explicitement ce qui n'est PAS encore possible (lecture
  Observatory) sans le simuler.

## Notions essentielles

Une **preuve** exploitable a quatre propriétés : une **source**
identifiable (qui/quoi l'a produite), une **provenance** traçable (quand,
dans quel contexte), une **forme vérifiable** (le document lui-même,
pas un résumé de mémoire), et — lorsque des personnes sont impliquées —
un **consentement documenté**. Le `frek_signal` déjà utilisé sur chaque
module (`FREK-WORK`/`FREK-SCORE`/`FREK-CONTRIB`) est un signal réel
existant dans la plateforme (`badges_engine.py`, `frek_core.py`) — il
peut servir de brique de traçabilité basique dès aujourd'hui. Une lecture
**Observatory** (data lineage, signaux agrégés à l'échelle du réseau)
serait la couche suivante — mais elle n'existe pas dans ce repo
aujourd'hui (`NOT_CONNECTED`, `KLT-0001` §4) : ce module ne la simule
pas, il la nomme comme un horizon futur explicite.

## Méthode

1. Rassembler tous les livrables réels produits en M01-M09 (note,
   fiches, cartographie, fiche action, grille d'animation, support,
   note d'arbitrage, retours, transcription).
2. Pour chaque pièce, renseigner : source, provenance (date/contexte),
   forme, et — si personne concernée — consentement.
3. Vérifier qu'aucune pièce ne manque de traçabilité (une pièce sans
   source ni date n'est pas une preuve).
4. Marquer explicitement, en fin de registre, la mention
   `OBSERVATORY_INTEGRATION = FUTURE / NOT_CONNECTED` — pas une case
   vide, une déclaration honnête.

## Exemples

L'interview mémorielle de M09 est une preuve complète (source = le
Doyen nommé, provenance = date + lieu, forme = transcription,
consentement = documenté). Une simple mention "on a fait une interview"
sans transcription ni consentement documenté n'en est pas une.

## Cas

Constitution du registre de preuves complet de *La Veillée du Tanbou*, à
partir des 9 livrables produits en M01-M09.

## Erreurs fréquentes

- Présenter un souvenir non documenté comme une preuve.
- Simuler une donnée Observatory ("le système montre que...") pour
  donner une apparence de rigueur technique à un registre qui n'en a pas
  besoin — **interdit explicitement** (`NO_FAKE_OBSERVATORY`).
- Oublier de vérifier le consentement documenté pour les pièces
  impliquant des personnes (M09 en particulier).

## Activité

Audit croisé : chaque candidat vérifie le registre d'un pair et signale
toute pièce sans source, provenance ou consentement documenté.

## Exercice

Rédiger la mention `OBSERVATORY_INTEGRATION = FUTURE / NOT_CONNECTED` en
une phrase qui explique honnêtement, à un lecteur externe, ce qui manque
et pourquoi ce n'est pas simulé.

## Livrable

Registre de preuves structuré (voir gabarit `templates/TEMPLATES.md`
§8 — Registre de preuves), couvrant les 9 livrables de M01-M09.

## Critères de réussite

- Chaque pièce du registre a une source, une provenance et, si
  pertinent, un consentement documenté.
- Aucune donnée Observatory n'est mentionnée comme réellement disponible.
- La mention `OBSERVATORY_INTEGRATION = FUTURE / NOT_CONNECTED` est
  présente et correctement formulée.

## Preuve

Le registre lui-même est la preuve de ce module — auto-référentiel par
construction. Agrégation des signaux `FREK-WORK`/`FREK-SCORE`/
`FREK-CONTRIB` réels de M01-M09.

## Auto-évaluation

*Chaque pièce de mon registre résisterait-elle à la question "qui l'a
produite, quand, avec quel consentement ?" Ai-je été tenté de simuler une
donnée que je n'ai pas réellement ?*

## Passage au module suivant

Le registre constitué ici est l'annexe factuelle du dossier de
certification produit en M11 — sans lui, la soutenance finale n'a rien à
citer comme preuve.
