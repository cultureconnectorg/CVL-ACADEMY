/** Cheap, synchronous WebGL2/WebGL1 capability probe — no context retained. */
export function webglSupported(win = typeof window !== "undefined" ? window : null) {
  if (!win?.document) return false;
  try {
    const canvas = win.document.createElement("canvas");
    return Boolean(
      win.WebGLRenderingContext &&
        (canvas.getContext("webgl2") || canvas.getContext("webgl") || canvas.getContext("experimental-webgl"))
    );
  } catch {
    return false;
  }
}
