# CVE-04 — Banque N2 (cas appliqués)

## Cas N2-1 — Re-dérivation inutile de N et CHL

Un stagiaire tente de recalculer `N_i,c` et `CHL_integrated` en
détail dans sa réponse sur la formule CES, au lieu de les citer par
référence. Corrige.

**Critères de notation:** rappelle que ces deux composantes sont
pleinement dérivées ailleurs (§3.2, §3.3, enseignées en CVE-07 et via
CVE-09/CVE-28) et doivent être citées par référence dans CVE-04, jamais
re-dérivées — c'est une discipline anti-duplication du corpus (règle
§26). Pas d'élimination automatique ici (ce n'est pas une invention),
mais note réduite pour duplication de contenu.

## Cas N2-2 — Poids non normalisés proposés

Un manager propose des poids `w_a,c` qui ne somment pas à 1 pour
"donner plus d'importance à l'engagement." Corrige.

**Critères de notation:** cite la contrainte réelle (`Σ_a w_a,c = 1`,
`w_a,c ≥ 0`) et explique qu'un ajustement de poids reste possible mais
doit respecter cette contrainte de normalisation — sinon `CVI_i,c`
perd son interprétation de moyenne pondérée. Élimination si le
candidat valide des poids non normalisés.

## Cas N2-3 — Confusion entre CES et ρ

Un collègue demande d'expliquer "en détail" le rôle exact de `ρ_c`
dans le cadre de CVE-04. Corrige le périmètre.

**Critères de notation:** répond au niveau littératie attendu de
CVE-04 (`ρ_c` est l'exposant/paramètre d'élasticité de substitution
dans la formule CES) et renvoie explicitement vers CVE-05 pour
l'analyse approfondie (cas spéciaux, statut d'hypothèse H2) — jamais
dupliquer ce contenu ici.
