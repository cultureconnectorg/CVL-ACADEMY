# FRK-11 — Banque N1

## Frontière et réutilisation FRK-04 (M0)

1. FRK-11 est spécialisation de quelle formation ? (FRK-04)
2. FRK-11 réutilise-t-il le contenu FRK-04 en le réécrivant ? (Non —
   par référence uniquement, vers `docs/frk/frk04/REFERENTIAL.md`)

## Construction avancée de chaîne (M1)

3. Que modélise une approche PROV-O pour une chaîne de provenance ?
   (Entités, activités, et agents — qui a détenu/transformé l'actif,
   quand, sous quelle attestation)
4. Que fait un manifeste de provenance de contenu façon C2PA ? (Une
   assertion signée liée à l'actif, référençant le manifeste précédent
   pour former une chaîne vérifiable)
5. Cite un signe qu'une chaîne de provenance est cassée. (Un maillon
   manquant, une incohérence de timestamp, ou une attestation qui ne
   se vérifie pas contre son signataire déclaré)
6. Une chaîne cassée doit-elle toujours être "réparée" par le
   praticien ? (Non — elle doit parfois être signalée comme non
   vérifiable plutôt que rafistolée)

## Résolution de litiges & confiance inter-institutions (M2)

7. Comment résoudre un litige entre deux chaînes de custody
   conflictuelles ? (Comparer maillon par maillon, identifier le
   premier point de divergence, appliquer la charge de la preuve au
   côté à l'attestation la plus faible à ce point)
8. Quelle est la différence entre confiance fédérée et autorité
   centrale ? (Fédérée : chaque institution garantit dans son propre
   domaine, un registre/web-of-trust relie les domaines ; centrale :
   une autorité unique)
9. Quel est le compromis réel entre les deux ? (Fédération évite un
   point unique de contrôle/défaillance mais exige que chaque
   institution maintienne une pratique interne fiable ; autorité
   centrale est plus simple mais crée un point unique de défaillance
   et de contrôle)

## Discipline de gap (héritée de FRK-04)

10. Un système CVLN réel implémente-t-il ces compétences avancées ?
    (Non — même discipline de gap que FRK-04, `CAPABILITY_NOT_IMPLEMENTED`)
11. Un candidat peut-il inventer un registre de confiance CVLN pour
    résoudre l'exercice ? (Non — élimination automatique si un système
    CVLN inventé est utilisé)
