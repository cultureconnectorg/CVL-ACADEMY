import { Suspense, lazy, useEffect, useState } from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
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
import { RouteTransition } from "@/lib/RouteTransition";
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

const ADMIN_ROLES = ["admin", "super_admin", "founder"];
const TRAINER_ROLES = ["trainer", ...ADMIN_ROLES];
const JURY_ROLES = ["jury", "corrector", ...ADMIN_ROLES];

function PageFallback() {
  return <div className="p-10 text-[--cvln-ink-2]">…</div>;
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

function Authenticated({ children, roles, withLayout = true }) {
  const { user, loading } = useAuth();
  if (loading) return null;
  if (!user) return <Navigate to="/" replace />;
  if (roles && !roles.includes(user.role)) return <Navigate to="/dashboard" replace />;
  const content = withLayout ? <Layout>{children}</Layout> : children;
  return <LegalGuard>{content}</LegalGuard>;
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

function App() {
  const [cookieManagerToken, setCookieManagerToken] = useState(0);

  return (
    <I18nProvider>
      <AuthProvider>
        <BrowserRouter>
          <SpatialWorldFrame>
            <Suspense fallback={<PageFallback />}>
              <RouteTransition>
                <Routes>
                  <Route path="/" element={<LandingSpatial />} />
                  <Route path="/login" element={<LandingSpatial authMode="login" />} />
                  <Route path="/register" element={<LandingSpatial authMode="register" />} />
                  <Route path="/forgot-password" element={<ForgotPassword />} />
                  <Route path="/reset-password" element={<ResetPassword />} />
                  <Route path="/verify-email" element={<VerifyEmail />} />
                  <Route path="/pricing" element={<Pricing />} />
                  <Route path="/legal/accept" element={<LegalAcceptance />} />
                  <Route path="/legal/:slug" element={<LegalHub />} />
                  <Route path="/onboarding" element={<LegalGuard><Onboarding /></LegalGuard>} />
                  <Route
                    path="/stakeholder/claim/:code"
                    element={
                      <Authenticated withLayout={false}>
                        <StakeholderClaim />
                      </Authenticated>
                    }
                  />
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
                  <Route path="/missions" element={<PublicOrMember><Missions /></PublicOrMember>} />
                  <Route path="/badges" element={<PublicOrMember><Badges /></PublicOrMember>} />
                  <Route path="/frek-profile" element={<PublicOrMember><FrekProfile /></PublicOrMember>} />
                  <Route path="/wallet" element={<PublicOrMember><Wallet /></PublicOrMember>} />
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
                  <Route path="*" element={<Navigate to="/" replace />} />
                </Routes>
              </RouteTransition>
            </Suspense>
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
