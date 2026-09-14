import { api } from "./api";
import { fetchLegalAcceptance, invalidateLegalAcceptance, peekLegalAcceptance } from "./legalGateCache";

jest.mock("./api", () => ({ api: { get: jest.fn() } }));

describe("legalGateCache", () => {
  beforeEach(() => {
    invalidateLegalAcceptance();
    api.get.mockReset();
  });

  test("peek is empty until a check has resolved", () => {
    expect(peekLegalAcceptance("user-1")).toBeNull();
  });

  test("fetch hits the network once, then peek/fetch serve the cached answer", async () => {
    api.get.mockResolvedValue({ data: { accepted: true, bundle_version: "v3" } });

    const first = await fetchLegalAcceptance("user-1");
    expect(first).toEqual({ accepted: true });
    expect(api.get).toHaveBeenCalledTimes(1);

    expect(peekLegalAcceptance("user-1")).toEqual({ accepted: true });

    const second = await fetchLegalAcceptance("user-1");
    expect(second).toEqual({ accepted: true });
    expect(api.get).toHaveBeenCalledTimes(1); // still 1 -- served from cache
  });

  test("concurrent callers for the same user dedupe into a single request", async () => {
    let resolveRequest;
    api.get.mockReturnValue(
      new Promise((resolve) => {
        resolveRequest = resolve;
      })
    );

    const p1 = fetchLegalAcceptance("user-1");
    const p2 = fetchLegalAcceptance("user-1");
    expect(api.get).toHaveBeenCalledTimes(1);

    resolveRequest({ data: { accepted: false } });
    const [r1, r2] = await Promise.all([p1, p2]);
    expect(r1).toEqual({ accepted: false });
    expect(r2).toEqual({ accepted: false });
  });

  test("a different user is never served the first user's cached answer", async () => {
    api.get.mockResolvedValue({ data: { accepted: true } });
    await fetchLegalAcceptance("user-1");

    expect(peekLegalAcceptance("user-2")).toBeNull();
    api.get.mockResolvedValueOnce({ data: { accepted: false } });
    const other = await fetchLegalAcceptance("user-2");
    expect(other).toEqual({ accepted: false });
    expect(api.get).toHaveBeenCalledTimes(2);
  });

  test("a failed check is never cached as accepted -- the next call re-hits the network", async () => {
    api.get.mockRejectedValueOnce(new Error("boom"));
    await expect(fetchLegalAcceptance("user-1")).rejects.toThrow("boom");
    expect(peekLegalAcceptance("user-1")).toBeNull();

    api.get.mockResolvedValueOnce({ data: { accepted: true } });
    const retried = await fetchLegalAcceptance("user-1");
    expect(retried).toEqual({ accepted: true });
    expect(api.get).toHaveBeenCalledTimes(2);
  });

  test("invalidateLegalAcceptance forces the next fetch back to the network", async () => {
    api.get.mockResolvedValue({ data: { accepted: true } });
    await fetchLegalAcceptance("user-1");
    expect(api.get).toHaveBeenCalledTimes(1);

    invalidateLegalAcceptance();
    expect(peekLegalAcceptance("user-1")).toBeNull();

    await fetchLegalAcceptance("user-1");
    expect(api.get).toHaveBeenCalledTimes(2);
  });
});
