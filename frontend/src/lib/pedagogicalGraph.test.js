import {
  GRAPH_DISTANCE,
  deriveIntentionPoleCode,
  deriveFormationNodes,
  deriveMissionNodes,
  deriveEvidence,
  buildPedagogicalGraph,
} from "./pedagogicalGraph";

describe("pedagogicalGraph.js — deriveIntentionPoleCode", () => {
  test("no learning path -> null, never guessed", () => {
    expect(deriveIntentionPoleCode(null)).toBeNull();
  });

  test("next_action present -> that formation's real pole", () => {
    const learningPath = {
      metier_vise: "KOR",
      own_pole: [{ code: "KOR-01", pole: "KOR" }],
      other_poles: [{ code: "FMS-01", pole: "FMS" }],
      next_action: { formation_code: "FMS-01" },
    };
    expect(deriveIntentionPoleCode(learningPath)).toBe("FMS");
  });

  test("no next_action -> falls back to declared metier_vise", () => {
    expect(
      deriveIntentionPoleCode({ metier_vise: "KOR", own_pole: [], other_poles: [], next_action: null })
    ).toBe("KOR");
  });
});

describe("pedagogicalGraph.js — deriveFormationNodes", () => {
  const learningPath = {
    metier_vise: "KOR",
    next_action: { formation_code: "KOR-01" },
    own_pole: [
      { code: "KOR-01", name: "Podcast Production", pole: "KOR", pole_color: "#F59E0B", progress_pct: 40, is_unlocked: true, is_recommended: true },
      { code: "KOR-02", name: "Storytelling", pole: "KOR", pole_color: "#F59E0B", progress_pct: 0, is_unlocked: false, is_recommended: true },
    ],
    other_poles: [
      { code: "FMS-01", name: "Artist Development", pole: "FMS", pole_color: "#E05A33", progress_pct: 100, is_unlocked: true, is_recommended: false },
      { code: "FMS-02", name: "Music Business", pole: "FMS", pole_color: "#E05A33", progress_pct: 0, is_unlocked: false, is_recommended: false },
    ],
  };

  test("the next_action's own formation gets distance INTENTION (0)", () => {
    const nodes = deriveFormationNodes(learningPath);
    const target = nodes.find((n) => n.code === "KOR-01");
    expect(target.distance).toBe(GRAPH_DISTANCE.INTENTION);
    expect(target.isIntention).toBe(true);
  });

  test("own pole, locked, not the intention -> still OWN_POLE_ACTIVE proximity", () => {
    const nodes = deriveFormationNodes(learningPath);
    const locked = nodes.find((n) => n.code === "KOR-02");
    expect(locked.distance).toBe(GRAPH_DISTANCE.OWN_POLE_ACTIVE);
  });

  test("other pole, unlocked -> OTHER_POLE_UNLOCKED, further than own pole", () => {
    const nodes = deriveFormationNodes(learningPath);
    const other = nodes.find((n) => n.code === "FMS-01");
    expect(other.distance).toBe(GRAPH_DISTANCE.OTHER_POLE_UNLOCKED);
    expect(other.distance).toBeGreaterThan(GRAPH_DISTANCE.INTENTION);
  });

  test("other pole, locked -> the farthest real distance", () => {
    const nodes = deriveFormationNodes(learningPath);
    const farthest = nodes.find((n) => n.code === "FMS-02");
    expect(farthest.distance).toBe(GRAPH_DISTANCE.OTHER_POLE_LOCKED);
  });

  test("never invents a progress_pct different from the server's own value", () => {
    const nodes = deriveFormationNodes(learningPath);
    for (const src of [...learningPath.own_pole, ...learningPath.other_poles]) {
      const node = nodes.find((n) => n.code === src.code);
      expect(node.progressPct).toBe(src.progress_pct); // verbatim, never recomputed
      expect(node.isUnlocked).toBe(src.is_unlocked);
    }
  });

  test("empty learning path -> empty node list, never throws", () => {
    expect(deriveFormationNodes(null)).toEqual([]);
  });
});

describe("pedagogicalGraph.js — deriveMissionNodes", () => {
  test("ineligible mission (Rail 2 gate) -> farthest distance", () => {
    const nodes = deriveMissionNodes([
      { code: "M1", title: "Gated", pole: "KOR", cc_reward: 20, status_type: "featured", eligible: false },
    ]);
    expect(nodes[0].distance).toBe(GRAPH_DISTANCE.OTHER_POLE_LOCKED);
    expect(nodes[0].eligible).toBe(false);
  });

  test("eligible + featured -> distance INTENTION", () => {
    const nodes = deriveMissionNodes([
      { code: "M2", title: "Featured", pole: "KOR", cc_reward: 20, status_type: "featured", eligible: true },
    ]);
    expect(nodes[0].distance).toBe(GRAPH_DISTANCE.INTENTION);
  });

  test("a mission with no eligible key at all (pre-Rail-2 default) reads as open/eligible", () => {
    const nodes = deriveMissionNodes([{ code: "M3", title: "Open", pole: "KOR", cc_reward: 10, status_type: "open" }]);
    expect(nodes[0].eligible).toBe(true);
  });

  test("no missions -> empty array", () => {
    expect(deriveMissionNodes(undefined)).toEqual([]);
  });
});

describe("pedagogicalGraph.js — deriveEvidence", () => {
  test("combines real badges and qualifications, never fabricates a count", () => {
    const evidence = deriveEvidence({
      badges: [{ code: "B1" }],
      qualifications: [{ qualification_code: "QUAL-KOR01-PRODUCTEUR-PODCAST" }],
    });
    expect(evidence.totalCount).toBe(2);
    expect(evidence.badges).toHaveLength(1);
    expect(evidence.qualifications).toHaveLength(1);
  });

  test("no evidence yet -> zero, not undefined", () => {
    expect(deriveEvidence({})).toEqual({ badges: [], qualifications: [], totalCount: 0 });
  });
});

describe("pedagogicalGraph.js — buildPedagogicalGraph", () => {
  test("combines every signal into one graph object", () => {
    const graph = buildPedagogicalGraph({
      learningPath: {
        metier_vise: "KOR",
        next_action: { formation_code: "KOR-01" },
        own_pole: [{ code: "KOR-01", name: "Podcast", pole: "KOR", pole_color: "#F59E0B", progress_pct: 10, is_unlocked: true, is_recommended: true }],
        other_poles: [],
      },
      missions: [{ code: "M1", title: "T", pole: "KOR", cc_reward: 10, status_type: "open", eligible: true }],
      badges: [{ code: "B1" }],
      qualifications: [],
      skills: [{ skill: { id: "KOR01.SKILL.C01" }, state: "acquired" }],
    });
    expect(graph.intentionPole).toBe("KOR");
    expect(graph.formationNodes).toHaveLength(1);
    expect(graph.missionNodes).toHaveLength(1);
    expect(graph.evidence.totalCount).toBe(1);
    expect(graph.skills).toHaveLength(1);
    expect(graph.nextAction.formation_code).toBe("KOR-01");
  });

  test("no signals at all -> a well-formed empty graph, never throws", () => {
    const graph = buildPedagogicalGraph();
    expect(graph.intentionPole).toBeNull();
    expect(graph.formationNodes).toEqual([]);
    expect(graph.missionNodes).toEqual([]);
    expect(graph.evidence.totalCount).toBe(0);
  });
});

// Structural guard, same discipline as lifecycleState.test.js's own
// "never invents a PAID state" test: this module must never compute a
// progress percentage of its own — every numeric progress value in its
// output must trace back verbatim to a `progress_pct`/`eligible` field
// the caller supplied, never a formula involving counts/dates/etc.
describe("pedagogicalGraph.js — never a second progression logic", () => {
  test("formation node progressPct is always identity-equal to the source progress_pct", () => {
    const src = { code: "X", name: "X", pole: "P", pole_color: "#000", progress_pct: 37, is_unlocked: true, is_recommended: true };
    const [node] = deriveFormationNodes({ next_action: null, own_pole: [src], other_poles: [] });
    expect(node.progressPct).toBe(37);
  });
});
