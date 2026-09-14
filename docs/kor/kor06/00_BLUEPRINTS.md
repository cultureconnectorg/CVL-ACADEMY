# KOR-06 — Blueprints canoniques (9 modules)

## M01 — Comprendre le fonctionnement d'un DSP
COMPETENCY : C1. ASSESSED : N1. OUTPUT : note de fonctionnement.

## M02 — Modéliser une chaîne ingestion→delivery
COMPETENCY : C2. ASSESSED : N1. OUTPUT : schéma de chaîne.

## M03 — Exploiter quotidiennement (disponibilité des contenus)
COMPETENCY : C3. ASSESSED : N2. OUTPUT : rapport de disponibilité.

## M04 — Player et CDN — concepts
COMPETENCY : C4. ASSESSED : N1. OUTPUT : note technique.

## M05 — Définir un SLA/SLO et la qualité de service
COMPETENCY : C5. ASSESSED : N2. OUTPUT : SLA/SLO documenté.

## M06 — Gérer un incident et l'escalade
COMPETENCY : C6. ASSESSED : N2. OUTPUT : rapport d'incident.

## M07 — Monitorer en continu et assurer la continuité
COMPETENCY : C7. ASSESSED : N2. OUTPUT : plan de monitoring.

## M08 — Opérer à l'échelle multi-territoires
COMPETENCY : C8. ASSESSED : N1. OUTPUT : note multi-territoires.

## M09 — Synthèse et certification
COMPETENCY : C9. ASSESSED : N3, `KOR06-A01`. OUTPUT : dossier +
soutenance.

---

## Vérification de cohérence transversale

| Test | Résultat |
|---|---|
| Compétence unique et traçable | OK |
| Progression N1→N2→N3 monotone | OK — N1 (M01,M02,M04,M08), N2 (M03,M05-M07), N3 (M09) |
| Aucune capacité KORA simulée (`NO_FAKE_KORA_CAPABILITY`) | OK — véhicule "Anba Tonèl Host" explicitement distinct de KORA, `REFERENTIAL.md` §6 |
| Frontière `KOR-06`/`KOR-14` (tension #2) posée | OK — `REFERENTIAL.md` §5 |

9 blueprints cohérents. Rédaction complète autorisée.
