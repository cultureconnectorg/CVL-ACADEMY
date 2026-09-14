import { useMemo, useState, useCallback, useRef, useEffect } from "react";
import { useNavigate, useLocation, useNavigationType } from "react-router-dom";
import { motion } from "framer-motion";
import { computeDepthStyle } from "@/lib/spatial/attention";
import { createCadenceTracker } from "@/lib/spatial/cadence";
import { createSpatialAudio } from "@/lib/spatial/audio";
import { createHaptics } from "@/lib/spatial/haptics";
import { useDepthPhysics } from "@/lib/useDepthPhysics";
import { useCameraIntent } from "@/lib/useCameraIntent";
import { useReducedMotion } from "@/lib/useReducedMotion";
import { FEATURE_FLAGS } from "@/lib/featureFlags";
import { useI18n } from "@/lib/i18n.jsx";
import { getRailPosition, saveRailPosition } from "@/lib/railPositionRestoration";

/**
 * RAIL 3 ("Finir Spatial Learning", 2026-09-07; corrected same day after
 * "j'ai pas l'impression que c'est au niveau de ce que nous avions
 * commencé" — accurate: the first pass wired only `attention.js`'s
 * static depth formulas behind a fixed-duration tween. This is the real
 * level: every sense channel H0.9/H0.10 built and verified is reused
 * here, unmodified, none of it re-derived —
 *
 *   - `spatial/physics.js` (`makeRailPhysics`, via `useDepthPhysics`) —
 *     the real rAF spring drives each node's depth, not a CSS/Framer
 *     tween. Retarget-safe, velocity-preserving, exactly as H0.9 built.
 *   - `spatial/cadence.js` (`createCadenceTracker`) — classifies real
 *     ArrowLeft/Right timestamps; its `state` throttles the audio engine's
 *     own NAV_MOVE repeat exactly as `audio.js` already expects.
 *   - `spatial/audio.js` / `spatial/haptics.js` — the real 8-event tone
 *     set / 5-pattern vibration set, gated by the pre-existing
 *     `SPATIAL_AUDIO`/`SPATIAL_HAPTICS` flags (declared in
 *     `featureFlags.js` since W-FUNNEL-1, never consumed until now).
 *     Only the events this component has a real, honest source for are
 *     fired: NAV_MOVE (a real rail move), FOCUS_LOCK (the physics spring
 *     actually settling on the focused node), CONFIRM (a real
 *     activation), BLOCKED (hitting the rail edge, or activating a
 *     locked/ineligible node). ENTER_DEPTH/RETURN_DEPTH/CONTEXT_OPEN/
 *     CONTEXT_CLOSE belong to route-level transitions
 *     (`RouteTransition.jsx`'s own topology wiring), not this rail —
 *     left alone rather than given a meaning they don't have here.
 *   - `spatial/attention.js` — unchanged, still the only depth-style
 *     math in the system; this component adds no formula of its own,
 *     only feeds it a continuously-animated (not static) distance.
 *
 * Doctrine this component is the direct, visible proof of: "l'espace se
 * réorganise autour de l'intention, le savoir avance vers toi à mesure
 * que tu avances vers lui" — the intention node (`distance === 0`)
 * renders largest/sharpest/closest; every other real node recedes by
 * exactly how far it really is, and now *moves* there the same way the
 * validated H0.9/H0.10 engine always did.
 *
 * Accessibility invariants inherited unchanged from H0.10: DOM order is
 * the real tab order (not the visual depth order), every node stays a
 * real focusable/activatable element, `prefers-reduced-motion` flattens
 * translateZ/rotateY/large translateX but keeps the tier hierarchy
 * (opacity/saturation/scale) — and, per `useDepthPhysics`'s own
 * contract, still fires FOCUS_LOCK feedback (audio/haptics are not
 * motion) even though the spring itself is skipped.
 *
 * RAIL 4 ("continue les H", 2026-09-07) addendum: activation can also
 * play a real camera-intent flight (`useCameraIntent.js`, ported from
 * H0.8's camera-follow state machine) before navigating — flag-gated
 * (`SPATIAL_CAMERA_INTENT`, default off). **ACA-0015 update
 * (2026-09-08)**: the flight is no longer same-page-only — each item's
 * real `destinationSelector` (FormationDetail's own root testid; the
 * exact same mission's own card on `/missions`) lets `useCameraIntent`
 * continue CROSSING → REVEALING once that real destination anchor
 * actually mounts (`lib/spatial/mountGuard.js`), instead of stopping at
 * FOLLOWING. See that hook's own docstring for the full state contract.
 */
export default function SpatialHub({ formationNodes, missionNodes }) {
  const navigate = useNavigate();
  const location = useLocation();
  const navType = useNavigationType();
  const { t } = useI18n();
  const reduced = useReducedMotion();
  const railRef = useRef(null);

  // One combined, distance-sorted rail — real nodes only, closest first.
  // Distance is the sole ordering key (never a hand-picked position).
  const items = useMemo(() => {
    const formations = (formationNodes ?? []).map((n) => ({
      kind: "formation",
      key: `formation:${n.code}`,
      distance: n.distance,
      title: n.name,
      subtitle: n.poleColor ? n.pole : undefined,
      poleColor: n.poleColor,
      meta: `${n.progressPct}%`,
      progressPct: n.progressPct,
      isUnlocked: n.isUnlocked,
      onActivate: () => navigate(`/formations/${n.code}`),
      // ACA-0015 — the real anchor FormationDetail.js always renders
      // once mounted (its own root, not per-formation — the page has
      // no per-code testid to hand a REVEALING flight a tighter
      // target). Real and load-bearing: e2e already depends on this
      // exact testid (module-journey-navigation.spec.js).
      destinationSelector: '[data-testid="formation-detail"]',
    }));
    const missions = (missionNodes ?? []).map((n) => ({
      kind: "mission",
      key: `mission:${n.code}`,
      distance: n.distance,
      title: n.title,
      subtitle: n.pole,
      meta: `+${n.ccReward} CC`,
      eligible: n.eligible,
      onActivate: () => navigate("/missions"),
      // ACA-0015 — the SAME real mission's own card on the destination
      // list (Missions.js renders `data-testid="mission-${code}"` in
      // both its plain-grid and depth-card treatments) — a genuinely
      // specific shared-element target, not the whole page.
      destinationSelector: `[data-testid="mission-${n.code}"]`,
    }));
    return [...formations, ...missions].sort((a, b) => a.distance - b.distance);
  }, [formationNodes, missionNodes, navigate]);

  // ACA-0023 (camera/rail/focus slice) — a real browser back/forward
  // (POP) into this exact history entry restores whichever real item
  // last had focus here, same axis useScrollRestoration.js's own scope
  // note deferred pending the spatial engine's real production mount
  // (ACA-0014, now done). A saved key that no longer matches a real
  // current item (data changed) is ignored, falling back to the
  // existing distance-0 default — never a stale/fabricated focus.
  const [focusedKey, setFocusedKey] = useState(() => {
    if (navType === "POP") {
      const saved = getRailPosition(location.key);
      if (saved && items.some((i) => i.key === saved.focusedKey)) {
        return saved.focusedKey;
      }
    }
    return items.find((i) => i.distance === 0)?.key ?? items[0]?.key;
  });
  const nodeRefs = useRef({});

  // Companion to the focus restore above: the rail's own horizontal
  // scroll (separate from the page's vertical scroll — already handled
  // by useScrollRestoration.js) — imperative because scrollLeft isn't
  // React state. Runs once, on the same POP arrival the focus restore
  // above already gates on.
  useEffect(() => {
    if (navType !== "POP" || !railRef.current) return;
    const saved = getRailPosition(location.key);
    if (typeof saved?.scrollLeft === "number") {
      railRef.current.scrollLeft = saved.scrollLeft;
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Persist the position at the moment attention genuinely moves to a
  // new item (keyboard arrow, click, or restore itself) — the same
  // granularity a real "where was I" memory needs, without a
  // continuous scroll listener this rail doesn't otherwise need.
  useEffect(() => {
    if (!focusedKey) return;
    saveRailPosition(location.key, {
      focusedKey,
      scrollLeft: railRef.current?.scrollLeft ?? 0,
    });
  }, [focusedKey, location.key]);

  // Real sense channels — one instance for this rail's lifetime, gated
  // by the pre-existing feature flags. Reading the flags inside a ref
  // initializer (not at import time) keeps the "read live" discipline
  // the rest of this codebase already follows for FEATURE_FLAGS.
  const cadenceRef = useRef(null);
  if (!cadenceRef.current) cadenceRef.current = createCadenceTracker();
  const audioRef = useRef(null);
  if (!audioRef.current) {
    audioRef.current = createSpatialAudio({ getCadenceState: () => cadenceRef.current.state });
  }
  audioRef.current.setEnabled(FEATURE_FLAGS.SPATIAL_AUDIO);
  const hapticsRef = useRef(null);
  if (!hapticsRef.current) {
    hapticsRef.current = createHaptics({ isEnabled: () => FEATURE_FLAGS.SPATIAL_HAPTICS });
  }
  // RAIL 4 ("continue les H") — real camera-follow primitives
  // (lib/spatial/cameraFollow.js, ported from H0.8), same-page scope
  // only. See useCameraIntent.js's own docstring for exactly what is
  // and isn't authorized.
  const cameraIntent = useCameraIntent();

  // Roving tabindex: the keyboard handler lives on each real, already-
  // interactive `<button>` (never on the non-interactive wrapper), and
  // moving between items calls real DOM `.focus()` — a roving-tabindex
  // change alone doesn't move focus, only bookkeeping does.
  const moveFocus = useCallback(
    (fromKey, dir) => {
      const idx = items.findIndex((i) => i.key === fromKey);
      if (idx === -1) return;
      const next = dir > 0 ? Math.min(idx + 1, items.length - 1) : Math.max(idx - 1, 0);
      cadenceRef.current.trackInput(dir);
      if (next === idx) {
        // Real rail edge — nothing further that way. BLOCKED, not silence.
        audioRef.current.play("BLOCKED");
        hapticsRef.current.fire("BLOCKED");
        return;
      }
      audioRef.current.play("NAV_MOVE");
      const nextKey = items[next].key;
      setFocusedKey(nextKey);
      nodeRefs.current[nextKey]?.focus();
    },
    [items]
  );

  const activate = useCallback(
    (item) => {
      const blocked =
        (item.kind === "formation" && item.isUnlocked === false) ||
        (item.kind === "mission" && item.eligible === false);
      if (blocked) {
        audioRef.current.play("BLOCKED");
        hapticsRef.current.fire("BLOCKED");
        // Still real navigation — the destination page explains the lock;
        // this rail never fabricates a different behavior than the rest
        // of the app already has for a locked/ineligible destination.
        item.onActivate();
        return;
      }
      audioRef.current.play("CONFIRM");
      hapticsRef.current.fire("CONFIRM");
      if (FEATURE_FLAGS.SPATIAL_CAMERA_INTENT) {
        cameraIntent.fly(nodeRefs.current[item.key], item.onActivate, {
          destinationSelector: item.destinationSelector,
        });
      } else {
        item.onActivate();
      }
    },
    [cameraIntent]
  );

  if (items.length === 0) return null;

  return (
    <div ref={railRef} className="mt-2 mb-10 -mx-2 px-2 overflow-x-auto" data-testid="spatial-hub">
      <h2 className="sr-only">{t("dashboard_p.next_step")}</h2>
      <div className="flex gap-5 pb-4" style={{ perspective: reduced ? "none" : "1400px" }}>
        {items.map((item) => (
          <SpatialNode
            key={item.key}
            item={item}
            reduced={reduced}
            isFocused={item.key === focusedKey}
            registerRef={(el) => {
              nodeRefs.current[item.key] = el;
            }}
            onFocus={() => setFocusedKey(item.key)}
            onActivate={() => activate(item)}
            onArrow={(dir) => moveFocus(item.key, dir)}
            audio={audioRef.current}
            haptics={hapticsRef.current}
          />
        ))}
      </div>
    </div>
  );
}

/** One rail node — owns its own `useDepthPhysics` instance (a real React
 * hook, so it must live in its own component: `items.map()` can't call
 * hooks per-iteration in the parent). FOCUS_LOCK fires from the physics
 * engine's own `onSettle` — the moment the spring (or, reduced-motion,
 * the instant jump) actually arrives — and only when this node is the
 * currently-focused one, read live via the `isFocused` prop closure. */
function SpatialNode({ item, reduced, isFocused, registerRef, onFocus, onActivate, onArrow, audio, haptics }) {
  const distance = useDepthPhysics(item.distance, {
    reduced,
    onSettle: () => {
      if (isFocused) {
        audio.play("FOCUS_LOCK");
        haptics.fire("FOCUS_LOCK");
      }
    },
  });
  const depth = computeDepthStyle(distance, { mobile: false });
  const style = reduced
    ? {
        // Reduced motion: keep the hierarchy signal (opacity/scale/
        // saturation) — drop the perspective/rotation/large-shift
        // motion per the inherited, unchanged accessibility rule.
        opacity: depth.opacity,
        filter: `saturate(${depth.saturate}) contrast(${depth.contrast})`,
        transform: `scale(${Math.max(depth.scale, 0.94)})`,
      }
    : {
        opacity: depth.opacity,
        filter: `saturate(${depth.saturate}) contrast(${depth.contrast}) brightness(${depth.brightness}) blur(${depth.blur}px)`,
        transform: `translate3d(${depth.translateX * 0.4}px, ${depth.translateY}px, ${depth.translateZ}px) rotateY(${depth.rotateY}deg) scale(${depth.scale})`,
        zIndex: depth.zIndex,
        transformStyle: "preserve-3d",
      };

  return (
    <motion.button
      ref={registerRef}
      type="button"
      data-testid={`spatial-hub-node-${item.kind}-${item.key.split(":")[1]}`}
      data-tier={depth.tier}
      aria-hidden={reduced ? undefined : depth.ariaHidden}
      aria-current={item.distance === 0 ? "true" : undefined}
      tabIndex={isFocused ? 0 : -1}
      onFocus={onFocus}
      onClick={onActivate}
      onKeyDown={(e) => {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          onActivate();
        } else if (e.key === "ArrowRight" || e.key === "ArrowLeft") {
          e.preventDefault();
          onArrow(e.key === "ArrowRight" ? 1 : -1);
        }
      }}
      style={style}
      className={`spatial-tile shrink-0 w-56 text-left rounded-2xl p-5 border cursor-pointer
        focus-visible:outline focus-visible:outline-2 focus-visible:outline-[--cvln-orange]
        ${item.distance === 0 ? "border-[--cvln-orange] bg-white shadow-lg" : "border-black/5 bg-white/70"}`}
    >
      <div className="spatial-tile-eyebrow text-[10px] mono uppercase tracking-[0.2em] text-[--cvln-ink-2]">
        {item.kind === "mission" ? "MISSION" : item.subtitle}
      </div>
      <div className="font-display font-bold text-lg tracking-tight mt-1 leading-snug">{item.title}</div>
      {item.kind === "formation" && (
        <div className="mt-3 stage-line">
          <div style={{ width: `${item.progressPct}%`, background: item.poleColor || undefined }} />
        </div>
      )}
      <div className="spatial-tile-meta mt-3 text-xs font-semibold text-[--cvln-orange]">{item.meta}</div>
      {item.kind === "formation" && !item.isUnlocked && (
        <div className="mt-1 text-[10px] text-[--cvln-ink-2] uppercase tracking-wider">🔒</div>
      )}
      {item.kind === "mission" && item.eligible === false && (
        <div className="mt-1 text-[10px] text-[--cvln-ink-2] uppercase tracking-wider">🔒</div>
      )}
    </motion.button>
  );
}
