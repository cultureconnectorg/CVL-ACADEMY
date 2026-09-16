import { Component } from "react";

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
        alreadyAttempted = true;
      }
      if (!alreadyAttempted) {
        window.location.reload();
        return;
      }
    }
    console.error("CVLN Academy — unhandled render error:", error);
  }

  handleRetry() {
    try {
      sessionStorage.removeItem(RELOAD_GUARD_KEY);
    } catch {
      // Best-effort cleanup only.
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
            CVLN Academy n&apos;a pas pu afficher cette page.
          </h1>
          <p className="mt-3 text-sm leading-6 text-[--cvln-ink-2]">
            Aucune donnée de ton parcours n&apos;a été perdue. Recharge la page pour réessayer.
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
