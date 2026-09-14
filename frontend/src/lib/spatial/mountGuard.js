/**
 * Spatial Learning — mount-detection guard (ACA-0015).
 *
 * `cameraFollow.js`'s own docstring names the exact reason its
 * CROSSING/REVEALING phases stayed unused by any production caller:
 * React Router unmounts/remounts pages on navigation, and a destination
 * page (Roadmap, Badges, ...) fetches its own data on mount before
 * rendering the real anchor element a REVEALING flight needs to land
 * on — so a same-frame handoff (the prototype's own single-document-SPA
 * assumption) isn't safely reproducible. That docstring named two
 * prerequisites: (a) promoting `Layout` to a real Outlet-based layout
 * route (done — ACA-0015/ACA-0016's routing restructure) and (b) "a
 * real mount-detection race guard neither built nor verified here."
 * This file is (b).
 *
 * `waitForElement` resolves with the real destination anchor the
 * instant it appears in the DOM after a `navigate()` call — via a real
 * `MutationObserver`, not a fixed-delay guess — and resolves `null`
 * after `timeoutMs` if it never appears (a destination page whose data
 * fetch is slow, or whose anchor genuinely doesn't exist for this
 * learner's real data, e.g. an empty stage list). Never throws, never
 * blocks navigation indefinitely — same "graceful no-op, never fake
 * support" doctrine `audio.js`/`haptics.js` already established for an
 * unsupported browser API; here it's an anchor that unsupported.
 */

/**
 * @param {string} selector a CSS selector for the real destination
 *   anchor (e.g. a `[data-testid="..."]` already rendered by the
 *   destination page — never invented, always an attribute the page
 *   already carries for its own purposes).
 * @param {{ root?: Element, timeoutMs?: number }} [opts]
 * @returns {Promise<Element|null>}
 */
export function waitForElement(selector, opts = {}) {
  const { timeoutMs = 1500 } = opts;
  const root = opts.root || (typeof document !== "undefined" ? document.body : null);

  return new Promise((resolve) => {
    if (!root || typeof MutationObserver === "undefined") {
      // No DOM / no MutationObserver support (e.g. a non-browser test
      // environment) — resolve null rather than throw. A caller already
      // treats null exactly like "anchor never appeared."
      resolve(null);
      return;
    }

    const existing = root.querySelector(selector);
    if (existing) {
      resolve(existing);
      return;
    }

    let settled = false;
    let observer;
    let timer;

    const finish = (result) => {
      if (settled) return;
      settled = true;
      if (observer) observer.disconnect();
      if (timer) clearTimeout(timer);
      resolve(result);
    };

    observer = new MutationObserver(() => {
      const found = root.querySelector(selector);
      if (found) finish(found);
    });
    observer.observe(root, { childList: true, subtree: true });

    timer = setTimeout(() => finish(null), timeoutMs);
  });
}
