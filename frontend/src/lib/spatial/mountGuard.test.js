import { waitForElement } from "./mountGuard";

describe("mountGuard.js — waitForElement (ACA-0015 mount-detection guard)", () => {
  test("resolves immediately when the element already exists", async () => {
    document.body.innerHTML = '<div data-testid="already-here"></div>';
    const el = await waitForElement('[data-testid="already-here"]', { timeoutMs: 100 });
    expect(el).not.toBeNull();
    expect(el.getAttribute("data-testid")).toBe("already-here");
  });

  test("resolves once the element is added asynchronously (real mount race)", async () => {
    document.body.innerHTML = "<div></div>";
    const promise = waitForElement('[data-testid="arrives-late"]', { timeoutMs: 1000 });

    // Simulate a destination page's own async data-fetch-then-render,
    // same real race the docstring names — the anchor genuinely isn't
    // there yet when the observer starts watching.
    setTimeout(() => {
      const el = document.createElement("div");
      el.setAttribute("data-testid", "arrives-late");
      document.body.appendChild(el);
    }, 30);

    const found = await promise;
    expect(found).not.toBeNull();
    expect(found.getAttribute("data-testid")).toBe("arrives-late");
  });

  test("resolves null after timeoutMs if the anchor never appears", async () => {
    document.body.innerHTML = "<div></div>";
    const found = await waitForElement('[data-testid="never-appears"]', { timeoutMs: 50 });
    expect(found).toBeNull();
  });

  test("scoped to a `root` element — a match outside root is never found", async () => {
    document.body.innerHTML =
      '<div id="scope"></div><div data-testid="outside-scope"></div>';
    const scope = document.getElementById("scope");
    const found = await waitForElement('[data-testid="outside-scope"]', {
      root: scope,
      timeoutMs: 50,
    });
    expect(found).toBeNull();
  });

  test("a match found inside root resolves, ignoring an identical selector outside it", async () => {
    document.body.innerHTML = '<div id="scope"></div>';
    const scope = document.getElementById("scope");
    const inside = document.createElement("div");
    inside.setAttribute("data-testid", "dup");
    scope.appendChild(inside);
    const outside = document.createElement("div");
    outside.setAttribute("data-testid", "dup");
    document.body.appendChild(outside);

    const found = await waitForElement('[data-testid="dup"]', { root: scope, timeoutMs: 50 });
    expect(found).toBe(inside);
  });

  test("never rejects, never throws — always settles to an Element or null", async () => {
    document.body.innerHTML = "";
    await expect(
      waitForElement('[data-testid="anything"]', { timeoutMs: 10 })
    ).resolves.toBeNull();
  });
});
