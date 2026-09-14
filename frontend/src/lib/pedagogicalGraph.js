/**
 * Spatial Learning — the pedagogical graph (RAIL 3, "Finir Spatial
 * Learning", Founder instruction 2026-09-07).
 *
 * Doctrine this module exists to serve, verbatim: "l'espace se
 * réorganise autour de l'intention, le savoir avance vers toi à mesure
 * que tu avances vers lui." Concretely: every spatial primitive already
 * built (`lib/spatial/attention.js`'s continuous distance model,
 * `lib/spatial/physics.js`'s spring targets, the environmental
 * signature) needs a real `distance` number per object. Before this
 * module, nothing on any real page ever computed that number from real
 * data — Roadmap.js used a bare array index, Dashboard.js used no
 * spatial primitive at all. This module is the single place that
 * number gets computed, from real server truth only.
 *
 * DERIVED, NOT STORED, NEVER A SECOND PROGRESSION LOGIC — same
 * discipline as `lifecycleState.js`, extended from "which lifecycle
 * labels apply" to "how far is each real object from the learner's
 * current intention." Every function here is pure: given the exact
 * response shapes already fetched by `Dashboard.js`/`Roadmap.js`
 * (`/user/learning-path`, `/missions`, `/badges/mine`,
 * `/skills/mine`, `/qualifications/mine`), it computes distances and
 * groupings. It never recomputes `progress_pct`, `is_unlocked`,
 * `eligible`, or `stade` — those numbers are read verbatim from the
 * server and never re-derived here, so there is structurally no way
 * for the spatial layer to disagree with the domain layer about "how
 * far along is this learner." `pedagogicalGraph.test.js`'s own
 * `test_never_recomputes_progress_pct` asserts this, not just by
 * convention (same pattern `lifecycleState.test.js` already
 * established for its own invariant).
 *
 * "Intention" (mission's own word) = the server's own `next_action`
 * from `/user/learning-path` (`lx.py`'s real recommendation engine,
 * already computed server-side) when present, falling back to the
 * learner's declared `metier_vise` pole. Never guessed client-side.
 *
 * Distance convention (matches `lib/spatial/attention.js`'s existing
 * units — same index-like scale `physics.js`/`attentionWeight` already
 * expect): 0 = exactly the object intention currently points at:
 * ascending integers = real, disclosed reasons to be farther (own-pole
 * in-progress, own-pole complete, other-pole unlocked, other-pole
 * locked) — never an arbitrary layout position.
 */

export const GRAPH_DISTANCE = Object.freeze({
  INTENTION: 0, // exactly the next_action's formation/module, or the featured+eligible mission
  OWN_POLE_ACTIVE: 1, // own pole, unlocked, not the exact next action, not yet complete
  OWN_POLE_LOCKED: 1, // own pole but a prior module still gates it — same proximity as ACTIVE: it's still "where the learner is heading"
  OWN_POLE_COMPLETE: 2, // own pole, already 100% — real, but no longer where attention belongs
  OTHER_POLE_UNLOCKED: 2, // real expansion opportunity (mirrors lifecycleState's EXPANDING signal)
  OTHER_POLE_LOCKED: 3, // real, but the farthest a formation can honestly be
});

/** `next_action.formation_code`, or `metier_vise` when the learner has
 * nothing actionable yet (e.g. every own-pole formation locked) — never
 * `null` silently; the caller decides how to render "no intention yet." */
export function deriveIntentionPoleCode(learningPath) {
  if (!learningPath) return null;
  if (learningPath.next_action?.formation_code) {
    const code = learningPath.next_action.formation_code;
    const all = [...(learningPath.own_pole ?? []), ...(learningPath.other_poles ?? [])];
    const formation = all.find((f) => f.code === code);
    return formation?.pole ?? learningPath.metier_vise ?? null;
  }
  return learningPath.metier_vise ?? null;
}

/** One graph node per real formation in `learning-path`'s own two
 * lists — `distance` derived only from fields the server already
 * computed (`is_recommended`, `is_unlocked`, `progress_pct`), plus
 * whether this exact formation is the `next_action`'s target. */
export function deriveFormationNodes(learningPath) {
  if (!learningPath) return [];
  const nextCode = learningPath.next_action?.formation_code ?? null;
  const all = [...(learningPath.own_pole ?? []), ...(learningPath.other_poles ?? [])];

  return all.map((f) => {
    let distance;
    if (f.code === nextCode) {
      distance = GRAPH_DISTANCE.INTENTION;
    } else if (f.is_recommended) {
      distance =
        f.progress_pct >= 100 ? GRAPH_DISTANCE.OWN_POLE_COMPLETE : GRAPH_DISTANCE.OWN_POLE_ACTIVE;
    } else {
      distance = f.is_unlocked
        ? GRAPH_DISTANCE.OTHER_POLE_UNLOCKED
        : GRAPH_DISTANCE.OTHER_POLE_LOCKED;
    }
    return {
      code: f.code,
      name: f.name,
      pole: f.pole,
      poleColor: f.pole_color,
      progressPct: f.progress_pct,
      isUnlocked: f.is_unlocked,
      isRecommended: f.is_recommended,
      isIntention: f.code === nextCode,
      distance,
    };
  });
}

/** One node per real mission — `eligible` is read verbatim (Rail 2's
 * `api/missions.py::list_missions` computed field, itself derived from
 * real `Qualification` rows, never re-derived here). `featured`/`urgent`
 * are the mission's own real `status_type`. */
export function deriveMissionNodes(missions) {
  return (missions ?? []).map((m) => {
    let distance;
    if (m.eligible === false) {
      distance = GRAPH_DISTANCE.OTHER_POLE_LOCKED;
    } else if (m.status_type === "featured" || m.status_type === "urgent") {
      distance = GRAPH_DISTANCE.INTENTION;
    } else {
      distance = GRAPH_DISTANCE.OWN_POLE_ACTIVE;
    }
    return {
      code: m.code,
      title: m.title,
      pole: m.pole,
      ccReward: m.cc_reward,
      eligible: m.eligible !== false, // a mission predating required_qualification_codes has no `eligible` key at all -> open to everyone, per Rail 2's own default
      statusType: m.status_type,
      distance,
    };
  });
}

/** Real proof objects only — badges already earned + qualifications
 * already issued (Rail 2's `Qualification`, sha256-hashed, never a
 * count fabricated from something else). Certifications passed are the
 * caller's own concern if it also fetches `/certifications/attempts/
 * mine`; this function only combines what it's given. */
export function deriveEvidence({ badges, qualifications } = {}) {
  return {
    badges: badges ?? [],
    qualifications: qualifications ?? [],
    totalCount: (badges?.length ?? 0) + (qualifications?.length ?? 0),
  };
}

/**
 * The one entry point a component should call. Combines the above into
 * one graph object; never fetches anything itself (see
 * `usePedagogicalGraph.js` for the fetching half) so it stays testable
 * with plain fixtures, same tier as `lifecycleState.test.js`.
 *
 * @param {Object} signals - same shape `usePedagogicalGraph` returns as
 *   `signals`: { learningPath, missions, badges, qualifications, skills }
 */
export function buildPedagogicalGraph(signals = {}) {
  const { learningPath, missions, badges, qualifications, skills } = signals;
  return {
    intentionPole: deriveIntentionPoleCode(learningPath),
    nextAction: learningPath?.next_action ?? null,
    formationNodes: deriveFormationNodes(learningPath),
    missionNodes: deriveMissionNodes(missions),
    evidence: deriveEvidence({ badges, qualifications }),
    skills: skills ?? [],
  };
}
