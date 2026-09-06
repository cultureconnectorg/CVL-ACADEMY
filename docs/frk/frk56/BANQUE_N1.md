# FRK-56 — Banque N1 (formative, M1→M4)

```
Sourced against real FREK_PROOF_MAPPING headers already carried by
docs/kor/ modules and docs/kor/kor01/skills/EVIDENCE_MODEL.md's own
written rationale, re-read this session.
```

## M1 — header literacy

1. Combien de modules KOR portent un header réel `FREK_PROOF_MAPPING` ?
   (Chaque module `docs/kor/korXX/modules/*.md`, sans exception)
2. Ce header vient-il d'une conception FREK-native ou d'un héritage ?
   (Hérité de `seed_modules.py` pour les modules issus du legacy)

## M2 — READY_FOR_FREK_PROOF rationale

3. Cite la valeur de `READY_FOR_FREK_PROOF` pour les 14 compétences de
   KOR-01. (`FALSE` pour les 14, sans exception)
4. Quelle est la raison exacte donnée par `kor01/skills/
   EVIDENCE_MODEL.md` pour ce `FALSE` généralisé ? (Le stack
   `frek_signal` est réel et utilisé, mais aucune ancre externe
   vérifiable — hash publié, horodatage tiers — n'existe dans
   `fms_canonical`/`klt_canonical`/`frek_core.py` pour aucune
   formation)

## M3 — bridge reuse discipline

5. Ce cas KORA↔FREK doit-il être re-dérivé pour chaque nouveau
   domaine (FMS, KLT, Good Mood) qui a besoin de la même explication ?
   (Non — il doit être réutilisé tel quel, jamais re-dérivé)

## M4 — anti-contamination

6. Le header `FREK_PROOF_MAPPING` documente-t-il une intégration
   technique réelle entre KORA et FREK ? (Non — il documente une
   intention d'émission de signal, pas une intégration technique
   bidirectionnelle)
