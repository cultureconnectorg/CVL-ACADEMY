# AF-X-03 — Banque N2 (cas appliqués)

## Cas 1 — Documenter les exigences d'un pont réel

Le candidat rédige les exigences d'un futur pont Skill ID ↔ ADL, en
citant les deux blocs de construction réels par référence (le moteur de
compétence de l'Academy, `docs/kor/`'s architecture, et l'ADL réel de
`CVLNAgentfactory`), sans jamais affirmer que le pont existe.

**Attendu :** une liste d'exigences concrètes (mapping explicite, API
de qualification, mécanisme de validation) présentée uniquement comme
travail futur, avec citation précise des deux blocs réels existants.

**Critère éliminatoire :** présenter les exigences documentées comme un
système déjà construit.

## Cas 2 — Prérequis AF-16/AF-17

Le candidat doit expliquer pourquoi ce pont ne peut être conceptualisé
sans une maîtrise préalable d'AF-16/AF-17 (le système de personas réel
de l'Academy).

**Attendu :** une explication correcte du système de personas réel
(`ASSISTANT_PERSONAS`, config-driven) et de pourquoi son absence de
maîtrise mènerait à inventer des capacités agentiques inexistantes.

**Critère éliminatoire :** conceptualiser le pont sans référence
correcte au système de personas réel.

## Cas 3 — Distinguer intention future et état actuel

Un candidat rédige une proposition de roadmap produit pour ce pont,
avec des jalons ("Phase 1 : mapping Skill ID ↔ ADL", "Phase 2 : API de
qualification"). Le correcteur doit vérifier que cette roadmap reste
clairement qualifiée comme une proposition hypothétique de travail
futur, jamais comme un état actuel ou un chantier déjà entamé.

**Attendu :** chaque phase de la roadmap est explicitement présentée
au conditionnel ou au futur, avec un rappel clair qu'aucune de ces
phases n'a débuté dans le code observé.

**Critère éliminatoire :** présenter une phase de roadmap comme
partiellement ou totalement réalisée aujourd'hui.
