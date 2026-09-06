# LAU-01→10 — Banque N1 (formatif)

Réserve `LAU0110.SKILL.*`.

1. Qu'est-ce que le patron "assistant exécutif IA / chief-of-staff"
   (triage d'agenda, synthèse de briefings, coordination
   transverse) et pourquoi est-ce une catégorie de marché réelle et
   actuelle ?
2. Que fait réellement `services/integrations/registry.py` avec
   l'entrée `laurentia` — pourquoi est-ce un stub générique sans
   logique propre ?
3. Le vrai `Laurent.ia` (orchestrateur multi-service réel, agents,
   circuit-breaker, bus d'événements, bridges) est cité comme contexte
   de marché — pourquoi ne doit-il jamais être présenté comme câblé à
   cette Academy ?
4. Pourquoi serait-il une erreur éliminatoire d'affirmer que cette
   Academy dispose d'un assistant exécutif IA fonctionnel ?

## Corrigé indicatif

1. Ce patron répond à un besoin réel de coordination cognitive
   (agenda, priorités, synthèse) via un agent IA — catégorie de
   marché établie, enseignable indépendamment de toute implémentation
   précise.
2. L'entrée `laurentia` dans `registry.py` est un simple nom de
   configuration générique, sans aucune logique métier associée — un
   stub, pas une implémentation.
3. Aucune intégration observée ne relie le vrai `Laurent.ia`
   (substantiel, audité, multi-service) à cette Academy — l'affirmer
   inventerait une capacité inexistante.
4. Cela affirmerait une capacité technique inexistante — contraire à
   la discipline `CAPABILITY_NOT_IMPLEMENTED`/`BLOCKED_PRODUCT_
   DEPENDENCY`.
