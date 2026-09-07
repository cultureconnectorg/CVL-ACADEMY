import { Suspense, lazy } from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import "@/App.css";
import "@/index.css";

import { AuthProvider, useAuth } from "@/lib/auth.jsx";
import { I18nProvider } from "@/lib/i18n.jsx";
import { Toaster } from "@/components/ui/sonner";
import Layout from "@/components/Layout";
import { RouteTransition } from "@/lib/RouteTransition";
import { useScrollRestoration } from "@/lib/useScrollRestoration";

const Landing = lazy(() => import("@/pages/Landing"));
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
const Offers = lazy(() => import("@/pages/Offers"));
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
const AdminDashboard = lazy(() => import("@/pages/admin/AdminDashboard"));
const TrainerDashboard = lazy(() => import("@/pages/trainer/TrainerDashboard"));
const JuryDashboard = lazy(() => import("@/pages/jury/JuryDashboard"));

const ADMIN_ROLES = ["admin", "super_admin", "founder"];
const TRAINER_ROLES = ["trainer", ...ADMIN_ROLES];
const JURY_ROLES = ["jury", ...ADMIN_ROLES];

function PageFallback() {
  return <div className="p-10 text-[--cvln-ink-2]">…</div>;
}

// ACA-0023 (scroll slice) — must be inside <BrowserRouter> (useLocation/
// useNavigationType need Router context) and outside <Suspense>/
// <RouteTransition> so it observes every navigation regardless of what
// lazy chunk is or isn't loaded yet. Renders nothing — side-effect only.
function ScrollRestoration() {
  useScrollRestoration();
  return null;
}

function Protected({ children, roles }) {
  const { user, loading } = useAuth();
  if (loading) return null;
  if (!user) return <Navigate to="/" replace />;
  if (!user.onboarding_completed) return <Navigate to="/onboarding" replace />;
  if (roles && !roles.includes(user.role)) return <Navigate to="/dashboard" replace />;
  return <Layout>{children}</Layout>;
}

function App() {
  return (
    <I18nProvider>
      <AuthProvider>
        <BrowserRouter>
          <ScrollRestoration />
          <Suspense fallback={<PageFallback />}>
            <RouteTransition>
              <Routes>
                <Route path="/" element={<Landing />} />
                <Route path="/onboarding" element={<Onboarding />} />
                <Route path="/dashboard" element={<Protected><Dashboard /></Protected>} />
                <Route path="/roadmap" element={<Protected><Roadmap /></Protected>} />
                {/* ACA-0009 — public formation discovery: catalogue + detail
                    are real pages a signed-out visitor can browse (backend
                    already supports this via get_current_user_optional —
                    api/formations.py). Layout itself doesn't require a
                    user, so these render outside <Protected>; only the
                    module *content* route below still requires a session. */}
                <Route path="/formations" element={<Layout><Formations /></Layout>} />
                <Route path="/formations/:code" element={<Layout><FormationDetail /></Layout>} />
                <Route path="/formations/:fc/modules/:mc" element={<Protected><ModuleJourney /></Protected>} />
                <Route path="/missions" element={<Protected><Missions /></Protected>} />
                <Route path="/badges" element={<Protected><Badges /></Protected>} />
                <Route path="/frek-profile" element={<Protected><FrekProfile /></Protected>} />
                <Route path="/wallet" element={<Protected><Wallet /></Protected>} />
                <Route path="/skills" element={<Protected><Skills /></Protected>} />
                <Route path="/certifications" element={<Protected><Certifications /></Protected>} />
                {/* ACA-0025/W-FUNNEL-2 "Conversion" — the real DECIDED_V1
                    commercial catalogue (`GET /commerce/offers`) is public
                    same PUBLIC_DISCOVERY=TRUE logic as /formations; only the
                    CTA behavior (honest BLOCKED_EXTERNAL, never a fake
                    purchase) is gated inside the page itself. */}
                <Route path="/offers" element={<Layout><Offers /></Layout>} />
                {/* ACA-0006 — canonical FMS runtime binding, read-only pages,
                    separate from the legacy /formations tree above. */}
                <Route path="/canonical" element={<Protected><CanonicalFormations /></Protected>} />
                <Route path="/canonical/:formationCode" element={<Protected><CanonicalFormationDetail /></Protected>} />
                <Route path="/canonical/:formationCode/:moduleCode" element={<Protected><CanonicalModuleView /></Protected>} />
                {/* "Branchage complet de Kiltikonet" (2026-09-04) — canonical
                    Kiltikonet runtime binding, read-only pages, separate tree. */}
                <Route path="/kiltikonet-canonical" element={<Protected><CanonicalKltFormations /></Protected>} />
                <Route path="/kiltikonet-canonical/:formationCode" element={<Protected><CanonicalKltFormationDetail /></Protected>} />
                <Route path="/kiltikonet-canonical/:formationCode/:moduleCode" element={<Protected><CanonicalKltModuleView /></Protected>} />
                {/* RAIL 2 — "Master -> Runtime Academy" (2026-09-06) — canonical
                    KORA runtime binding, read-only pages, separate tree. */}
                <Route path="/kora-canonical" element={<Protected><CanonicalKorFormations /></Protected>} />
                <Route path="/kora-canonical/:formationCode" element={<Protected><CanonicalKorFormationDetail /></Protected>} />
                <Route path="/kora-canonical/:formationCode/:moduleCode" element={<Protected><CanonicalKorModuleView /></Protected>} />
                {/* "raccorder ces corpus au même runtime/funnel Academy"
                    (Founder, 2026-09-07) — canonical FREK runtime binding,
                    read-only pages, separate tree. First of the 16 markdown-
                    only Master 2D domains connected to the real runtime. */}
                <Route path="/frek-canonical" element={<Protected><CanonicalFrkFormations /></Protected>} />
                <Route path="/frek-canonical/:formationCode" element={<Protected><CanonicalFrkFormationDetail /></Protected>} />
                <Route path="/frek-canonical/:formationCode/:moduleCode" element={<Protected><CanonicalFrkModuleView /></Protected>} />
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
                <Route path="*" element={<Navigate to="/" replace />} />
              </Routes>
            </RouteTransition>
          </Suspense>
        </BrowserRouter>
        <Toaster position="top-right" richColors />
      </AuthProvider>
    </I18nProvider>
  );
}

export default App;
