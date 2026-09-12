import { useEffect, useRef } from "react";
import { FEATURE_FLAGS } from "@/lib/featureFlags";
import { SPATIAL_CONTEXT_EVENT } from "@/lib/ContextFrame";
import { createSpatialAudio } from "@/lib/spatial/audio";
import { createHaptics } from "@/lib/spatial/haptics";
import { SPATIAL_CAMERA_EVENT } from "@/lib/spatial/cameraRuntime";
import {
  SPATIAL_SIGNAL_EVENT,
  SPATIAL_SIGNAL_TYPES,
} from "@/lib/spatial/spatialLearningSignals";
import {
  readSpatialSensoryOptIn,
  SPATIAL_SENSORY_PREFERENCE_EVENT,
} from "@/lib/spatial/sensoryPreference";

function feedbackForCamera(kind) {
  if (kind === "LOCK") return { audio: "FOCUS_LOCK", haptic: "FOCUS_LOCK" };
  if (kind === "FOLLOW") return { audio: "ENTER_DEPTH", haptic: "ENTER" };
  if (kind === "RETURN_FOLLOW") return { audio: "RETURN_DEPTH", haptic: "SNAP" };
  return null;
}

function feedbackForSignal(type) {
  if (
    type === SPATIAL_SIGNAL_TYPES.ASSESSMENT_PASSED ||
    type === SPATIAL_SIGNAL_TYPES.MODULE_VALIDATED ||
    type === SPATIAL_SIGNAL_TYPES.MISSION_COMPLETED
  ) {
    return { audio: "CONFIRM", haptic: "CONFIRM" };
  }
  return null;
}

/**
 * Optional sensory projection of already-confirmed Spatial events.
 *
 * Two independent gates must pass before anything fires:
 * 1) deployment feature flag (audio and/or haptics), and
 * 2) explicit learner opt-in stored by sensoryPreference.js.
 *
 * No sound/vibration is emitted for assessment retry: failure remains a calm
 * refocus state, never a punitive sensory event. Hidden tabs are silent.
 */
export default function SpatialSensoryBridge() {
  const audioRef = useRef(null);
  const hapticsRef = useRef(null);
  const optedInRef = useRef(false);

  useEffect(() => {
    if (typeof window === "undefined") return undefined;

    const audio = createSpatialAudio();
    const haptics = createHaptics({
      isEnabled: () => optedInRef.current && FEATURE_FLAGS.SPATIAL_HAPTICS,
    });
    audioRef.current = audio;
    hapticsRef.current = haptics;

    const syncPreference = (enabled = readSpatialSensoryOptIn()) => {
      optedInRef.current = Boolean(enabled);
      audio.setEnabled(Boolean(enabled) && FEATURE_FLAGS.SPATIAL_AUDIO);
    };
    syncPreference();

    const isInteractive = () => document.visibilityState === "visible";
    const fire = (feedback) => {
      if (!feedback || !optedInRef.current || !isInteractive()) return;
      if (FEATURE_FLAGS.SPATIAL_AUDIO && feedback.audio) audio.play(feedback.audio);
      if (FEATURE_FLAGS.SPATIAL_HAPTICS && feedback.haptic) haptics.fire(feedback.haptic);
    };

    const onPreference = (event) => syncPreference(event?.detail?.enabled === true);
    const onCamera = (event) => fire(feedbackForCamera(event?.detail?.kind));
    const onContext = (event) => fire(
      event?.detail?.active
        ? { audio: "CONTEXT_OPEN", haptic: "FOCUS_LOCK" }
        : { audio: "CONTEXT_CLOSE", haptic: "SNAP" },
    );
    const onSignal = (event) => fire(feedbackForSignal(event?.detail?.type));
    const onVisibility = () => {
      if (document.visibilityState !== "visible") audio.setEnabled(false);
      else audio.setEnabled(optedInRef.current && FEATURE_FLAGS.SPATIAL_AUDIO);
    };

    window.addEventListener(SPATIAL_SENSORY_PREFERENCE_EVENT, onPreference);
    window.addEventListener(SPATIAL_CAMERA_EVENT, onCamera);
    window.addEventListener(SPATIAL_CONTEXT_EVENT, onContext);
    window.addEventListener(SPATIAL_SIGNAL_EVENT, onSignal);
    document.addEventListener("visibilitychange", onVisibility);

    return () => {
      audio.setEnabled(false);
      window.removeEventListener(SPATIAL_SENSORY_PREFERENCE_EVENT, onPreference);
      window.removeEventListener(SPATIAL_CAMERA_EVENT, onCamera);
      window.removeEventListener(SPATIAL_CONTEXT_EVENT, onContext);
      window.removeEventListener(SPATIAL_SIGNAL_EVENT, onSignal);
      document.removeEventListener("visibilitychange", onVisibility);
      audioRef.current = null;
      hapticsRef.current = null;
    };
  }, []);

  return null;
}
