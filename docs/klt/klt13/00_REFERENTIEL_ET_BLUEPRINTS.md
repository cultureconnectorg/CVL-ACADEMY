# KLT-13 — Responsable Accréditation Terrain / Terrain Accreditation Operator — Référentiel canonique + Blueprints

```
Formation NEW construite le 2026-09-07, sur autorisation Founder scopée
(docs/klt/README.md §FOUNDER_AUTHORIZATION_UPDATE, KLT_09_20_
RECONCILIATION.md §KLT-13). Verdict de reconciliation : SPECIALIZE_
EXISTING, ancrée par référence sur KLT-05/C4 ("Gérer participants,
badges et preuves de participation (scans/NFC)"). Ne rouvre pas
KLT-05/M04 ; construit un rôle de spécialisation terrain distinct, sur
le même principe que FMS-08/09 spécialisant FMS-03.
STRUCTURAL_STATUS = COMPLETE — 5/5 compétences construites.
FULLY_COMPLETE = TRUE — aucune compétence de cette formation ne dépend
d'une connexion live à un système externe (contrairement à
KLT-06/07/08, dont C5/C6/C4 restent `BUILT_UNCONNECTED`) : le registre
`skills/SKILL_ID_REGISTRY.md` ne porte aucune ligne `BLOCKED` ni
`BUILT_UNCONNECTED`, donc `fully_complete` se calcule honnêtement à
`TRUE` (même dérivation que KLT-01→05, voir `klt_canonical/read_model.py`).
Ce champ ne dit rien de l'import en base `db.formations` (toujours
`NO_RUNTIME_BINDING_YET` — voir INTEGRATION_ACADEMY_PACKAGE_NOTE.md),
qui est une question distincte et séparément suivie.
contexts = [EXTERNAL]. BRIDGE non retenu (spécialisation avancée, pas
un point d'entrée du parcours).
```

## Avertissement central de cette formation — `NFC_NOT_IMPLEMENTED`

Le titre du métier nomme la NFC ("Near Field Communication") parce que
c'est la technologie d'accréditation terrain la plus citée dans le
secteur événementiel réel — **mais aucun système NFC réel n'existe
nulle part dans l'écosystème vérifié de ce repo**, ni chez Kiltikonet
(`KLT-05`/M04 : "Aucun système de badge/scan réel n'est utilisé"), ni
ailleurs. Le seul dispositif électronique de contrôle d'accès **réel et
vérifié** trouvé à ce jour dans l'écosystème CVLN est celui de **Good
Mood** (`gmfest972/goodmooddjsayd`, `GOOD_MOOD_DJ_SAYD_RECONCILIATION.md`)
— un système **QR code**, pas NFC : `/scan/check`, `/scan/counter/{eid}`
(`GMD-25`). Cette formation enseigne donc à concevoir un protocole
d'accréditation terrain rigoureux, en étudiant ce précédent réel comme
**étude de cas cross-écosystème** (jamais présenté comme un système
Kiltikonet), et en spécifiant une extension NFC en toute connaissance de
son statut non implémenté. `NO_FAKE_LIVE_CONNECTION` s'applique ici sous
la forme `NFC_NOT_IMPLEMENTED = TRUE, partout, sans exception`.

## Métier cible

**Responsable Accréditation Terrain / Terrain Accreditation & Access
Operator** — niveau `Avancé`, priorité `P2` (spécialisation, pas un
métier d'entrée). Pas de correspondance ROME calibrée dans ce repo
(formation `NEW`, sans legacy).

## Responsabilités réelles (périmètre buildable, 5/5)

Concevoir un dispositif d'accréditation terrain pour un événement
physique (rôles, zones, niveaux d'accès) · étudier un précédent réel de
contrôle d'accès électronique pour en tirer les exigences d'un protocole
rigoureux · spécifier une extension NFC en connaissance de ses limites
actuelles (non implémentée) · gérer un incident d'accréditation terrain
le jour J et l'escalader correctement · restituer un bilan
d'accréditation terrain sans fabriquer de données non mesurées.

## Limites du rôle — ce que le métier n'est PAS

N'anime pas de médiation terrain (`KLT-01`), ne gère pas de budget
(`KLT-02`), ne négocie pas de partenariat institutionnel (`KLT-03`), n'a
pas d'autorité de gouvernance (`KLT-04`). Ne remplace ni ne rouvre le
protocole badge/scan générique de `KLT-05`/M04 (opérateur plateforme
généraliste) — spécialise un rôle terrain dédié aux événements physiques
de plus grande complexité (zones multiples, volume de flux, incidents
d'accès). Ne conçoit jamais un système NFC comme s'il existait déjà —
`NFC_NOT_IMPLEMENTED` reste vrai à chaque module.

## Publics / Contextes

`contexts = [EXTERNAL]` — e-learning disponible en canal externe,
physique `ELIGIBLE_PENDING_OFFER` (jamais réservable sans offre réelle,
même si le métier lui-même porte sur des opérations physiques). `BRIDGE`
non retenu (niveau `Avancé`, spécialisation, pas un point d'entrée du
parcours `KILTIKONET_PROFESSIONAL_PATHWAY.md`).

## Compétences (5) et modules — statut de construction

| # | Compétence | Module | Statut |
|---|---|---|---|
| C1 | Concevoir un dispositif d'accréditation terrain pour un événement physique | M01 | `BUILT` |
| C2 | Étudier un précédent réel de contrôle d'accès électronique (cross-écosystème) | M02 | `BUILT` |
| C3 | Spécifier une extension NFC en connaissance de ses limites actuelles (non implémentée) | M03 | `BUILT` |
| C4 | Gérer un incident d'accréditation terrain et l'escalader | M04 | `BUILT` |
| C5 | Restituer un bilan d'accréditation terrain sans fabriquer de données | M05 | `BUILT` |

**5/5 compétences construites.**

## Blueprints

| Module | WHY_THIS_MODULE_EXISTS | ASSESSED | WHAT_REAL_OUTPUT |
|---|---|---|---|
| M01 | Un dispositif d'accréditation conçu sans distinguer rôles/zones/niveaux d'accès laisse des failles évidentes le jour J | N1/N2 | Plan d'accréditation terrain |
| M02 | Concevoir un protocole rigoureux sans étudier un précédent réel revient à réinventer, souvent mal, des exigences déjà connues | N1/N2 | Fiche d'analyse du précédent réel |
| M03 | Spécifier une extension NFC sans nommer son statut non implémenté fabrique une promesse technique qui n'existe pas | N2 | Spécification NFC (statut explicite) |
| M04 | Un incident d'accréditation non maîtrisé le jour J peut dégénérer en incident de sécurité ou d'image | N2 | Fiche d'incident + note d'escalade |
| M05 | Un bilan qui invente un taux de contrôle non mesuré discrédite tout le dispositif | N2 | Bilan d'accréditation terrain |

Cohérence transversale vérifiée : progression N1→N2 monotone sur les 5
modules construits, aucune compétence testée sans module,
`NFC_NOT_IMPLEMENTED` rappelé dans M01, M03, M05.
