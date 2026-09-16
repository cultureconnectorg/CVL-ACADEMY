import { Suspense, lazy, useEffect, useState } from "react";
import { BrowserRouter, Routes, Route, Navigate, Outlet } from "react-router-dom";
import "@/App.css";
import "@/index.css";
import "@/cvln-cinematic.css";

import { AuthProvider, useAuth } from "@/lib/auth.jsx";
import { I18nProvider } from "@/lib/i18n.jsx";
import { fetchLegalAcceptance, peekLegalAcceptance } from "@/lib/legalGateCache";
import { Toaster } from "@/components/ui/sonner";
import Layout from "@/components/Layout";
import LegalFooter from "@/components/LegalFooter";
import CookieConsent from "@/components/CookieConsent";
import PublicDiscoveryLayout from "@/components/PublicDiscoveryLayout";
import SpatialWorldFrame from "@/components/spatial/SpatialWorldFrame.jsx";
import ErrorBoundary from "@/components/ErrorBoundary.jsx";
import { RouteTransition, sectionKeyFor } from "@/lib/RouteTransition";
import { useScrollRestoration } from "@/lib/useScrollRestoration";
import { ForgotPassword, ResetPassword, VerifyEmail } from "@/pages/AuthRecovery";

const LandingSpatial = lazy(() => import("@/pages/LandingSpatial"));
const Pricing = lazy(() => import("@/pages/Pricing"));
const Onboarding = lazy(() => import("@/pages/Onboarding"));
const Dashboard = lazy(() => import("@/pages/Dashboard"));
const Formations = lazy(() => import("@/pages/Formations"));
const FormationDetail = lazy(() => import("@/pages/FormationDetail"));
const ModuleJourney = lazy(() => import("@/pages/ModuleJourney"));
const Missions = lazy(() => import("@/pages/Missions"));
const Badges = lazy(() => import("@/pages/Badges"));
const FrekProfile = lazy(() => import("@/pages/FrekProfile"));
const Roadmap = lazy(() => import("@/pages/Roadmap"));
const Wallet = lazy(() => import("@/pages/Wallet"));
const Skills = lazy(() => import("@/pages/Skills"));
const Certifications = lazy(() => import("@/pages/Certifications"));
const LegalHub = lazy(() => import("@/pages/LegalHub"));
const LegalAcceptance = lazy(() => import("@/pages/LegalAcceptance"));
const AdminDashboard = lazy(() => import("@/pages/admin/AdminDashboard"));
const StakeholderAccessPanel = lazy(() => import("@/pages/admin/StakeholderAccessPanel"));
const TrainerDashboard = lazy(() => import("@/pages/trainer/TrainerDashboard"));
const JuryDashboard = lazy(() => import("@/pages/jury/JuryDashboard"));
const StakeholderPortal = lazy(() => import("@/pages/stakeholder/StakeholderPortal"));
const StakeholderClaim = lazy(() => import("@/pages/stakeholder/StakeholderClaim"));

// RECONCILE-2 Groupe 4 (2026-09-14) — the 17 pages r35l31 built but never
// routed on this branch (RECONCILE-1 imported the files verbatim; wiring
// them was explicitly deferred to this group). Each gets the guard its own
// backend contract actually requires — see docs/reconciliation/
// RECONCILE_2_DECISIONS.md's Groupe 4 section for the per-page justification.
const CanonicalFormations = lazy(() => import("@/pages/CanonicalFormations"));
const CanonicalFormationDetail = lazy(() => import("@/pages/CanonicalFormationDetail"));
const CanonicalModuleView = lazy(() => import("@/pages/CanonicalModuleView"));
const CanonicalKltFormations = lazy(() => import("@/pages/CanonicalKltFormations"));
const CanonicalKltFormationDetail = lazy(() => import("@/pages/CanonicalKltFormationDetail"));
const CanonicalKltModuleView = lazy(() => import("@/pages/CanonicalKltModuleView"));
const CanonicalKorFormations = lazy(() => import("@/pages/CanonicalKorFormations"));
const CanonicalKorFormationDetail = lazy(() => import("@/pages/CanonicalKorFormationDetail"));
const CanonicalKorModuleView = lazy(() => import("@/pages/CanonicalKorModuleView"));
const CanonicalFrkFormations = lazy(() => import("@/pages/CanonicalFrkFormations"));
const CanonicalFrkFormationDetail = lazy(() => import("@/pages/CanonicalFrkFormationDetail"));
const CanonicalFrkModuleView = lazy(() => import("@/pages/CanonicalFrkModuleView"));
const EcosystemBuilder = lazy(() => import("@/pages/EcosystemBuilder"));
const Offers = lazy(() => import("@/pages/Offers"));
const ProfessionalPublicProfile = lazy(() => import("@/pages/ProfessionalPublicProfile"));
const ExpertWorkspace = lazy(() => import("@/pages/ExpertWorkspace"));
const ProfessionalWorkspace = lazy(() => import("@/pages/admin/ProfessionalWorkspace"));

const ADMIN_ROLES = ["admin", "super_admin", "founder"];
const TRAINER_ROLES = ["trainer", ...ADMIN_ROLES];
const JURY_ROLES = ["jury", "corrector", ...ADMIN_ROLES];

function PageFallback() {
  return <div className="p-10 text-[--cvln-ink-2]">…</div>;
}

function ScrollRestoration() {
  useScrollRestoration();
  return null;
}

function GateFailure({ sessionExpired = false, onRetry, onLogout }) {
  return (
    <main
      className="min-h-[60vh] px-6 py-16 md:px-12"
      data-testid="legal-gate-error"
      role="alert"
    >
      <div className="mx-auto max-w-xl rounded-3xl border border-black/10 bg-white p-7 text-[--cvln-ink] shadow-sm">
        <div className="text-xs font-bold uppercase tracking-[0.2em] text-[--cvln-orange]">
          {sessionExpired ? "Session expirée" : "Service momentanément indisponible"}
        </div>
        <h1 className="mt-3 font-display text-3xl font-black tracking-tight">
          {sessionExpired
            ? "Reconnecte-toi pour continuer."
            : "Impossible de vérifier ton accès pour le moment."}
        </h1>
        <p className="mt-3 text-sm leading-6 text-[--cvln-ink-2]">
          {sessionExpired
            ? "Ta session n’est plus valide. Aucune donnée de parcours n’a été modifiée."
            : "CVLN Academy ne transforme plus une panne technique en demande d’acceptation juridique. Réessaie lorsque le service répond à nouveau."}
        </p>
        <div className="mt-6 flex flex-wrap gap-3">
          {sessionExpired ? (
            <button type="button" className="btn-primary" onClick={onLogout}>
              Se reconnecter
            </button>
          ) : (
            <button type="button" className="btn-primary" onClick={onRetry} data-testid="legal-gate-retry">
              Réessayer
            </button>
          )}
        </div>
      </div>
    </main>
  );
}

function LegalGuard({ children }) {
  const { user, loading, logout } = useAuth();
  const userId = user?.id || null;
  // LegalGuard is mounted per-<Route>, so React Router remounts it on every
  // navigation between protected pages. Seed from the session cache (see
  // legalGateCache.js) so a navigation within the freshness window renders
  // straight to "accepted"/"required" instead of a network round trip behind
  // a blocking "checking" render every single time.
  const [state, setState] = useState(() => {
    const cached = peekLegalAcceptance(userId);
    if (!cached) return "checking";
    return cached.accepted ? "accepted" : "required";
  });
  const [retryKey, setRetryKey] = useState(0);

  useEffect(() => {
    let alive = true;
    if (loading) return undefined;
    if (!userId) {
      setState("anonymous");
      return undefined;
    }

    const cached = peekLegalAcceptance(userId);
    if (cached) {
      setState(cached.accepted ? "accepted" : "required");
      return undefined;
    }

    setState("checking");
    fetchLegalAcceptance(userId)
      .then((result) => {
        if (!alive) return;
        setState(result.accepted ? "accepted" : "required");
      })
      .catch((error) => {
        if (!alive) return;
        const status = error?.response?.status;
        setState(status === 401 ? "session_expired" : "unavailable");
      });

    return () => {
      alive = false;
    };
  }, [userId, loading, retryKey]);

  if (loading || state === "checking") return null;
  if (!user || state === "anonymous") return <Navigate to="/" replace />;
  if (state === "session_expired") {
    return (
      <GateFailure
        sessionExpired
        onLogout={() => {
          logout();
          window.location.assign("/login");
        }}
      />
    );
  }
  if (state === "unavailable") {
    return <GateFailure onRetry={() => setRetryKey((value) => value + 1)} />;
  }
  if (state === "required") return <Navigate to="/legal/accept" replace />;
  return children;
}

// ACA-0015/ACA-0016 — `Layout` used to be mounted here, per-route, by
// every `Authenticated` instance (a fresh element tree per `<Route>`
// match, remounting sidebar/AcademyBackdrop/mentor dock on every
// in-section navigation — see `LayoutRoute` below for the fix). Now
// purely an auth/role/legal-acceptance guard; Layout itself is hoisted
// to the one shared `LayoutRoute` that wraps this component's callers.
function Authenticated({ children, roles }) {
  const { user, loading } = useAuth();
  if (loading) return null;
  if (!user) return <Navigate to="/" replace />;
  if (roles && !roles.includes(user.role)) return <Navigate to="/dashboard" replace />;
  return <LegalGuard>{children}</LegalGuard>;
}

function Protected({ children, roles }) {
  const { user, loading } = useAuth();
  if (loading) return null;
  if (!user) return <Navigate to="/" replace />;
  if (!user.onboarding_completed) return <Navigate to="/onboarding" replace />;
  return <Authenticated roles={roles}>{children}</Authenticated>;
}

function PublicOrMember({ children }) {
  const { user, loading } = useAuth();
  if (loading) return null;
  if (!user) return <PublicDiscoveryLayout>{children}</PublicDiscoveryLayout>;
  if (!user.onboarding_completed) return <Navigate to="/onboarding" replace />;
  return <Authenticated>{children}</Authenticated>;
}

// ACA-0015/ACA-0016 — the real Outlet-based layout route
// (SPATIAL_H1_INTEGRATION_PLAN.md's own REPLACE-BLOCKED item; see
// RouteTransition.jsx's own module docstring, which has documented
// this exact structure since it was authorized, 2026-09-08 — this is
// that promotion finally wired into the route tree it always
// described). Every authenticated-shell route below nests under this
// one `<Route>`, so the SAME mounted `Layout` instance (sidebar,
// AcademyBackdrop, mentor dock) persists across an in-section
// navigation instead of each route wrapping a fresh one.
//
// `Layout` still only renders for a real session: an anonymous visitor
// on a `PublicOrMember` route (e.g. /formations, /roadmap) must keep
// getting `PublicDiscoveryLayout`, which `PublicOrMember` already wraps
// itself below this Outlet — rendering `Layout` here too for that case
// would double-wrap. This mirrors exactly what `Authenticated` decided
// per-route before this promotion: Layout only when `user` exists.
function LayoutRoute() {
  const { user } = useAuth();
  const content = (
    <RouteTransition>
      <Outlet />
    </RouteTransition>
  );
  return user ? <Layout>{content}</Layout> : content;
}

function App() {
  const [cookieManagerToken, setCookieManagerToken] = useState(0);

  return (
    <I18nProvider>
      <AuthProvider>
        <BrowserRouter>
          <ScrollRestoration />
          <SpatialWorldFrame>
            <ErrorBoundary>
            <Suspense fallback={<PageFallback />}>
              <RouteTransition keyFor={sectionKeyFor}>
                <Routes>
                  <Route path="/" element={<LandingSpatial />} />
                  <Route path="/login" element={<LandingSpatial authMode="login" />} />
                  <Route path="/register" element={<LandingSpatial authMode="register" />} />
                  <Route path="/forgot-password" element={<ForgotPassword />} />
                  <Route path="/reset-password" element={<ResetPassword />} />
                  <Route path="/verify-email" element={<VerifyEmail />} />
                  <Route path="/pricing" element={<Pricing />} />
                  {/* RECONCILE-2 Groupe 4: PUBLIC_ROUTED — GET /api/professional/public/{frek_id}
                      is a dedicated, deliberately unauthenticated backend route (see
                      api/professional_profile.py); a 404 there already covers "unknown FREK-ID"
                      and "exists but private" identically, so this page needs no auth wrapper. */}
                  <Route path="/id/:frekId" element={<ProfessionalPublicProfile />} />
                  {/* RECONCILE-2 Groupe 4: INTERNAL_ROUTED — governance_advanced.expert_workspace
                      authenticates via its own X-CVLN-Expert-Key header, never an Academy
                      session (external experts have no Academy account); the page's own form
                      is the real access gate, so it gets no Protected/Authenticated wrapper. */}
                  <Route path="/expert" element={<ExpertWorkspace />} />
                  <Route path="/legal/accept" element={<LegalAcceptance />} />
                  <Route path="/legal/:slug" element={<LegalHub />} />
                  <Route path="/onboarding" element={<LegalGuard><Onboarding /></LegalGuard>} />
                  <Route
                    path="/stakeholder/claim/:code"
                    element={
                      <Authenticated>
                        <StakeholderClaim />
                      </Authenticated>
                    }
                  />
                  {/* ACA-0015/ACA-0016 — every route below shares the one
                      mounted `Layout` instance via `LayoutRoute`, instead of
                      each wrapping a fresh one. */}
                  <Route element={<LayoutRoute />}>
                    <Route
                      path="/partner"
                      element={
                        <Authenticated>
                          <StakeholderPortal expectedType="partner" />
                        </Authenticated>
                      }
                    />
                    <Route
                      path="/institution"
                      element={
                        <Authenticated>
                          <StakeholderPortal expectedType="institution" />
                        </Authenticated>
                      }
                    />
                    <Route path="/dashboard" element={<Protected><Dashboard /></Protected>} />
                    <Route path="/roadmap" element={<PublicOrMember><Roadmap /></PublicOrMember>} />
                    <Route path="/formations" element={<PublicOrMember><Formations /></PublicOrMember>} />
                    <Route path="/formations/:code" element={<PublicOrMember><FormationDetail /></PublicOrMember>} />
                    <Route path="/formations/:fc/modules/:mc" element={<Protected><ModuleJourney /></Protected>} />
                    {/* RECONCILE-2 Groupe 4: AUTHENTICATED_ROUTED — the canonical curriculum
                        routers (canonical/frk_canonical/kor_canonical/klt_canonical) are all
                        gated with require_legal_acceptance in api/__init__.py (Groupe 1), unlike
                        the legacy Formations/FormationDetail above (deliberately public,
                        ACA-0009) — so these stay behind the authenticated-only guard, not the
                        hybrid public-discovery one, to match what the backend actually requires. */}
                    <Route path="/canonical" element={<Protected><CanonicalFormations /></Protected>} />
                    <Route path="/canonical/:formationCode" element={<Protected><CanonicalFormationDetail /></Protected>} />
                    <Route path="/canonical/:formationCode/:moduleCode" element={<Protected><CanonicalModuleView /></Protected>} />
                    <Route path="/kiltikonet-canonical" element={<Protected><CanonicalKltFormations /></Protected>} />
                    <Route path="/kiltikonet-canonical/:formationCode" element={<Protected><CanonicalKltFormationDetail /></Protected>} />
                    <Route path="/kiltikonet-canonical/:formationCode/:moduleCode" element={<Protected><CanonicalKltModuleView /></Protected>} />
                    <Route path="/kora-canonical" element={<Protected><CanonicalKorFormations /></Protected>} />
                    <Route path="/kora-canonical/:formationCode" element={<Protected><CanonicalKorFormationDetail /></Protected>} />
                    <Route path="/kora-canonical/:formationCode/:moduleCode" element={<Protected><CanonicalKorModuleView /></Protected>} />
                    <Route path="/frek-canonical" element={<Protected><CanonicalFrkFormations /></Protected>} />
                    <Route path="/frek-canonical/:formationCode" element={<Protected><CanonicalFrkFormationDetail /></Protected>} />
                    <Route path="/frek-canonical/:formationCode/:moduleCode" element={<Protected><CanonicalFrkModuleView /></Protected>} />
                    <Route path="/missions" element={<PublicOrMember><Missions /></PublicOrMember>} />
                    <Route path="/badges" element={<PublicOrMember><Badges /></PublicOrMember>} />
                    <Route path="/frek-profile" element={<PublicOrMember><FrekProfile /></PublicOrMember>} />
                    {/* RECONCILE-2 Groupe 4: AUTHENTICATED_ROUTED — GET /ecosystem-builder/me is
                        a "me"-scoped, per-user endpoint; there is no anonymous view. */}
                    <Route path="/ecosystem-builder" element={<Protected><EcosystemBuilder /></Protected>} />
                    <Route path="/wallet" element={<PublicOrMember><Wallet /></PublicOrMember>} />
                    {/* RECONCILE-2 Groupe 4: AUTHENTICATED_ROUTED, with a documented discrepancy —
                        Offers.js's own docstring describes GET /commerce/offers as "real, public
                        and fully tested"; that was true on r35l31 before Groupe 1's reconciled
                        api/__init__.py put `commerce` in the same require_legal_acceptance-gated
                        group as everything else (no domain in that 53-router import was exempted
                        without a specific reason — see RECONCILE_1_REPORT.md). The route now
                        actually requires login, so it is routed accordingly rather than routed as
                        public against a contract the backend no longer honors. Whether the
                        catalogue should be reopened to anonymous visitors (matching Formations'
                        own public-discovery precedent) is a product decision for the Founder, not
                        one to guess at here — flagged NEEDS_REVIEW in RECONCILE_2_DECISIONS.md. */}
                    <Route path="/offers" element={<Protected><Offers /></Protected>} />
                    <Route path="/skills" element={<PublicOrMember><Skills /></PublicOrMember>} />
                    <Route path="/certifications" element={<PublicOrMember><Certifications /></PublicOrMember>} />
                    <Route
                      path="/trainer"
                      element={<Protected roles={TRAINER_ROLES}><TrainerDashboard /></Protected>}
                    />
                    <Route
                      path="/jury"
                      element={<Protected roles={JURY_ROLES}><JuryDashboard /></Protected>}
                    />
                    <Route
                      path="/admin"
                      element={<Protected roles={ADMIN_ROLES}><AdminDashboard /></Protected>}
                    />
                    <Route
                      path="/admin/stakeholders"
                      element={
                        <Protected roles={ADMIN_ROLES}>
                          <div className="px-6 md:px-12 py-10 max-w-4xl">
                            <StakeholderAccessPanel />
                          </div>
                        </Protected>
                      }
                    />
                    {/* RECONCILE-2 Groupe 4: INTERNAL_ROUTED — same ADMIN_ROLES gate as every
                        other admin surface above. */}
                    <Route
                      path="/admin/professional-workspace"
                      element={<Protected roles={ADMIN_ROLES}><ProfessionalWorkspace /></Protected>}
                    />
                  </Route>
                  <Route path="*" element={<Navigate to="/" replace />} />
                </Routes>
              </RouteTransition>
            </Suspense>
            </ErrorBoundary>
          </SpatialWorldFrame>
          <LegalFooter onManageCookies={() => setCookieManagerToken((n) => n + 1)} />
          <CookieConsent manageToken={cookieManagerToken} />
        </BrowserRouter>
        <Toaster position="top-right" richColors />
      </AuthProvider>
    </I18nProvider>
  );
}

export default App;
