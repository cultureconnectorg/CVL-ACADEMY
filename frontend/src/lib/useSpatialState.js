import { useReducer } from "react";
import { SPATIAL_STATES, spatialStateReducer } from "@/lib/spatial-state";

/**
 * React binding for `spatialStateReducer` (see spatial-state.js for the
 * full DOMAIN_STATE != SPATIAL_STATE rationale). Returns `[state, dispatch]`
 * exactly like `useReducer` — `dispatch` takes one of `SPATIAL_EVENTS`,
 * never a raw state name, so a component can only ever move through the
 * modeled IDLE -> FOCUS -> APPROACH -> ENTER -> ACTIVE -> CONTEXT ->
 * RETURN -> IDLE graph, never jump arbitrarily.
 *
 * W1-D foundation only — not imported by any page yet.
 */
export function useSpatialState(initial = SPATIAL_STATES.IDLE) {
  return useReducer(spatialStateReducer, initial);
}
