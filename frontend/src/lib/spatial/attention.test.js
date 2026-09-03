import {
  ATTENTION_TIERS,
  attentionWeight,
  attentionTier,
  computeDepthStyle,
  predictNextIndex,
  createAutofocusGuard,
} from "./attention";

describe("attention.js", () => {
  test("exactly one PRIMARY_ATTENTION across a sweep of continuous distances", () => {
    // simulate a live physics position sweeping from 0 to 4 in small
    // steps, computing the tier for 7 candidate objects at each moment —
    // exactly one must read PRIMARY at every sampled instant.
    for (let position = 0; position <= 4; position += 0.13) {
      const tiers = [0, 1, 2, 3, 4, 5, 6].map((i) => attentionTier(i - position));
      const primaries = tiers.filter((t) => t === ATTENTION_TIERS.PRIMARY);
      expect(primaries.length).toBe(1);
    }
  });

  test("deterministic priority: same distance always yields the same tier", () => {
    expect(attentionTier(0)).toBe(ATTENTION_TIERS.PRIMARY);
    expect(attentionTier(0)).toBe(attentionTier(0));
    expect(attentionTier(1)).toBe(attentionTier(1));
    expect(attentionTier(5)).toBe(ATTENTION_TIERS.LATENT);
  });

  test("weight is 1 at distance 0 and monotonically decreasing with |distance|", () => {
    expect(attentionWeight(0)).toBe(1);
    expect(attentionWeight(1)).toBeLessThan(attentionWeight(0));
    expect(attentionWeight(2)).toBeLessThan(attentionWeight(1));
    expect(attentionWeight(-2)).toBeCloseTo(attentionWeight(2), 10); // symmetric
  });

  test("computeDepthStyle: active object is fully sharp/opaque, far object is receded", () => {
    const active = computeDepthStyle(0);
    const far = computeDepthStyle(5);
    expect(active.blur).toBe(0);
    expect(active.opacity).toBeCloseTo(1, 2);
    expect(active.tier).toBe(ATTENTION_TIERS.PRIMARY);
    expect(far.blur).toBeGreaterThan(0);
    expect(far.blur).toBeLessThanOrEqual(1.3); // H0.10's calibrated ceiling
    expect(far.opacity).toBeLessThan(active.opacity);
    expect(far.ariaHidden).toBe(true);
    expect(active.ariaHidden).toBe(false);
  });

  test("computeDepthStyle: mobile narrows perspective (weaker rotateY/Z than desktop)", () => {
    const desktop = computeDepthStyle(2, { mobile: false });
    const mobile = computeDepthStyle(2, { mobile: true });
    expect(Math.abs(mobile.rotateY)).toBeLessThan(Math.abs(desktop.rotateY));
    expect(Math.abs(mobile.translateZ)).toBeLessThan(Math.abs(desktop.translateZ));
  });

  test("predictNextIndex: only active during REPEATED/FAST_REPEAT with a real direction", () => {
    expect(predictNextIndex(5, 2, "STOPPED", 1)).toBe(-1);
    expect(predictNextIndex(5, 2, "SINGLE", 1)).toBe(-1);
    expect(predictNextIndex(5, 2, "REPEATED", 0)).toBe(-1);
    expect(predictNextIndex(5, 2, "REPEATED", 1)).toBe(3);
    expect(predictNextIndex(5, 2, "FAST_REPEAT", -1)).toBe(1);
  });

  test("predictNextIndex: never predicts past a real boundary", () => {
    expect(predictNextIndex(5, 4, "FAST_REPEAT", 1)).toBe(-1); // already last
    expect(predictNextIndex(5, 0, "FAST_REPEAT", -1)).toBe(-1); // already first
  });

  test("autofocus guard: applies when no explicit intent lands before resolution", () => {
    const guard = createAutofocusGuard();
    let applied = false;
    const req = guard.request(() => {
      applied = true;
    });
    req.resolve();
    expect(applied).toBe(true);
  });

  test("autofocus guard: STALE_AUTOFOCUS_REQUEST discarded by a newer request", () => {
    const guard = createAutofocusGuard();
    let firstApplied = false;
    let secondApplied = false;
    const first = guard.request(() => {
      firstApplied = true;
    });
    const second = guard.request(() => {
      secondApplied = true;
    });
    first.resolve(); // superseded, must not apply
    second.resolve();
    expect(firstApplied).toBe(false);
    expect(secondApplied).toBe(true);
  });

  test("autofocus guard: LATEST_EXPLICIT_USER_INTENT_WINS — explicit choice after the request discards it", () => {
    const guard = createAutofocusGuard();
    let applied = false;
    const req = guard.request(() => {
      applied = true;
    });
    guard.noteExplicitIntent(); // user acted explicitly after the request was made
    req.resolve();
    expect(applied).toBe(false);
  });

  test("autofocus guard: an explicit intent BEFORE the request does not block it", () => {
    const guard = createAutofocusGuard();
    guard.noteExplicitIntent();
    let applied = false;
    const req = guard.request(() => {
      applied = true;
    });
    req.resolve();
    expect(applied).toBe(true);
  });
});
