import { Component } from "react";

// No ErrorBoundary existed anywhere in the app (confirmed by a dedicated
// audit — zero componentDidCatch/getDerivedStateFromError in the whole
// frontend/src tree). Every route below this one is behind React.lazy()
// (see App.js's lazy() imports) — a stale open tab whose index.html still
// references a previous deploy's content-hashed chunk filenames throws a
// real, uncaught error the moment it tries to lazy-load a page after that
// chunk has been replaced by a newer Vercel deployment. With no boundary,
// that single throw unmounted the entire React tree with no recovery path,
// on any route, including the two-line LandingSpatial wrapper on "/",
// "/login" and "/register".
//
// A stale chunk reference is self-healing: reloading the page always fetches
// the current index.html (service-worker.js serves navigations network-first),
// which references the current deployment's real chunk filenames. So a
// first-time chunk failure reloads once automatically; a `sessionStorage`
// guard stops that from becoming a reload loop if the real cause is
// something else (e.g. actually offline) — the second failure falls through
// to a manual, dismissible fallback instead.
const CHUNK_ERROR_PATTERN = /ChunkLoadError|Loading chunk|dynamically imported module|Importing a module script failed/i;
const RELOAD_GUARD_KEY = "cvln_error_boundary_reload_attempted";

export default class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
    this.handleRetry = this.handleRetry.bind(this);
  }

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  componentDidCatch(error) {
    const message = String(error?.message || error || "");
    if (CHUNK_ERROR_PATTERN.test(message)) {
      let alreadyAttempted = false;
      try {
        alreadyAttempted = sessionStorage.getItem(RELOAD_GUARD_KEY) === "1";
        if (!alreadyAttempted) sessionStorage.setItem(RELOAD_GUARD_KEY, "1");
      } catch {
        // sessionStorage unavailable (private mode) — fall through to the
        // manual fallback below rather than risk an unguarded reload loop.
        alreadyAttempted = true;
      }
      if (!alreadyAttempted) {
        window.location.reload();
        return;
      }
    }
    // eslint-disable-next-line no-console
    console.error("CVLN Academy — unhandled render error:", error);
  }

  handleRetry() {
    try {
      sessionStorage.removeItem(RELOAD_GUARD_KEY);
    } catch {
      // best-effort only
    }
    window.location.reload();
  }

  render() {
    if (!this.state.hasError) return this.props.children;
    return (
      <main
        className="min-h-[60vh] flex items-center justify-center px-6 py-16 md:px-12"
        data-testid="app-error-boundary"
        role="alert"
      >
        <div className="mx-auto max-w-xl rounded-3xl border border-black/10 bg-white p-7 text-[--cvln-ink] shadow-sm">
          <div className="text-xs font-bold uppercase tracking-[0.2em] text-[--cvln-orange]">
            Un problème est survenu
          </div>
          <h1 className="mt-3 font-display text-3xl font-black tracking-tight">
            CVLN Academy n'a pas pu afficher cette page.
          </h1>
          <p className="mt-3 text-sm leading-6 text-[--cvln-ink-2]">
            Aucune donnée de ton parcours n'a été perdue. Recharge la page pour réessayer.
          </p>
          <div className="mt-6 flex flex-wrap gap-3">
            <button type="button" className="btn-primary" onClick={this.handleRetry} data-testid="app-error-boundary-retry">
              Recharger
            </button>
          </div>
        </div>
      </main>
    );
  }
}
