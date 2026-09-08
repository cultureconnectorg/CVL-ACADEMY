import { Suspense, lazy } from "react";
import { BrowserRouter, Routes, Route, Navigate, Outlet } from "react-router-dom";
import "@/App.css";
import "@/index.css";

import { AuthProvider, useAuth } from "@/lib/auth.jsx";
import { I18nProvider } from "@/lib/i18n.jsx";
import { Toaster } from "@/components/ui/sonner";
import Layout from "@/components/Layout";
import { RouteTransition, sectionKeyFor } from "@/lib/RouteTransition";
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
const ProfessionalPublicProfile = lazy(() => import("@/pages/ProfessionalPublicProfile"));
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

// ACA-0015/ACA-0016 — Layout promoted to a real Outlet-based layout
// route (SPATIAL_H1_INTEGRATION_PLAN.md's own REPLACE-BLOCKED item,
// unblocked by explicit Founder authorization 2026-09-08): every route
// nested under this one renders through the SAME mounted `Layout`
// instance (sidebar/AcademyBackdrop/mentor dock never unmount on an
// in-section navigation), instead of each route wrapping its own fresh
// `<Layout>` (the pre-ACA-0015 `Protected` pattern this replaces). The
// inner `RouteTransition` (raw-pathname-keyed, same component App.js's
// outer instance uses) is what actually crossfades the page content;
// `Layout` itself never re-keys.
function LayoutRoute() {
  return (
    <Layout>
      <RouteTransition>
        <Outlet />
      </RouteTransition>
    </Layout>
  );
}

// The same auth/onboarding/role guard `Protected` already ran, but
// rendering `<Outlet/>` on success instead of `<Layout>{children}</Layout>`
// — Layout is now supplied once by the parent `LayoutRoute`, not by
// this guard. Every redirect (`/`, `/onboarding`, `/dashboard`) is
// byte-identical to `Protected`'s own.
function ProtectedRoute({ roles }) {
  const { user, loading } = useAuth();
  if (loading) return null;
  if (!user) return <Navigate to="/" replace />;
  if (!user.onboarding_completed) return <Navigate to="/onboarding" replace />;
  if (roles && !roles.includes(user.role)) return <Navigate to="/dashboard" replace />;
  return <Outlet />;
}

function App() {
  return (
    <I18nProvider>
      <AuthProvider>
        <BrowserRouter>
          <ScrollRestoration />
          <Suspense fallback={<PageFallback />}>
            {/* ACA-0016 — keyed by section (Landing/Onboarding vs. everything
                else), not the raw pathname: this outer instance now only
                re-keys crossing that boundary, so `LayoutRoute` below stays
                mounted across every in-section navigation. The inner
                RouteTransition inside `LayoutRoute` (raw-pathname-keyed)
                is what crossfades the actual page content in that case. */}
            <RouteTransition keyFor={sectionKeyFor}>
              <Routes>
                <Route path="/" element={<Landing />} />
                <Route path="/onboarding" element={<Onboarding />} />

                {/* Every route below renders through the one, persistent
                    `Layout` instance `LayoutRoute` mounts — sidebar,
                    AcademyBackdrop, mentor dock never remount navigating
                    between any of them (ACA-0015/ACA-0016). */}
                <Route element={<LayoutRoute />}>
                  {/* ACA-0009 — public formation discovery: catalogue +
                      detail are real pages a signed-out visitor can browse
                      (backend already supports this via
                      get_current_user_optional — api/formations.py). No
                      auth guard on these three; only the module *content*
                      route below still requires a session. */}
                  <Route path="/formations" element={<Formations />} />
                  <Route path="/formations/:code" element={<FormationDetail />} />
                  {/* ACA-0025/W-FUNNEL-2 "Conversion" — the real DECIDED_V1
                      commercial catalogue (`GET /commerce/offers`) is public,
                      same PUBLIC_DISCOVERY=TRUE logic as /formations; only
                      the CTA behavior (honest BLOCKED_EXTERNAL, never a fake
                      purchase) is gated inside the page itself. */}
                  <Route path="/offers" element={<Offers />} />
                  {/* ACA-0028 — the public identity surface: a real,
                      explicit-opt-in-only page (GET /api/professional/
                      public/{frek_id} — off-by-default, see services/
                      professional_profile.py). No auth guard, same
                      PUBLIC_DISCOVERY logic as /formations//offers. */}
                  <Route path="/id/:frekId" element={<ProfessionalPublicProfile />} />

                  <Route element={<ProtectedRoute />}>
                    <Route path="/dashboard" element={<Dashboard />} />
                    <Route path="/roadmap" element={<Roadmap />} />
                    <Route path="/formations/:fc/modules/:mc" element={<ModuleJourney />} />
                    <Route path="/missions" element={<Missions />} />
                    <Route path="/badges" element={<Badges />} />
                    <Route path="/frek-profile" element={<FrekProfile />} />
                    <Route path="/wallet" element={<Wallet />} />
                    <Route path="/skills" element={<Skills />} />
                    <Route path="/certifications" element={<Certifications />} />
                    {/* ACA-0006 — canonical FMS runtime binding, read-only
                        pages, separate from the legacy /formations tree. */}
                    <Route path="/canonical" element={<CanonicalFormations />} />
                    <Route path="/canonical/:formationCode" element={<CanonicalFormationDetail />} />
                    <Route path="/canonical/:formationCode/:moduleCode" element={<CanonicalModuleView />} />
                    {/* "Branchage complet de Kiltikonet" (2026-09-04) —
                        canonical Kiltikonet runtime binding, separate tree. */}
                    <Route path="/kiltikonet-canonical" element={<CanonicalKltFormations />} />
                    <Route path="/kiltikonet-canonical/:formationCode" element={<CanonicalKltFormationDetail />} />
                    <Route path="/kiltikonet-canonical/:formationCode/:moduleCode" element={<CanonicalKltModuleView />} />
                    {/* RAIL 2 — "Master -> Runtime Academy" (2026-09-06) —
                        canonical KORA runtime binding, separate tree. */}
                    <Route path="/kora-canonical" element={<CanonicalKorFormations />} />
                    <Route path="/kora-canonical/:formationCode" element={<CanonicalKorFormationDetail />} />
                    <Route path="/kora-canonical/:formationCode/:moduleCode" element={<CanonicalKorModuleView />} />
                    {/* "raccorder ces corpus au même runtime/funnel Academy"
                        (Founder, 2026-09-07) — canonical FREK runtime
                        binding, separate tree. First of the 16 markdown-
                        only Master 2D domains connected to the real runtime. */}
                    <Route path="/frek-canonical" element={<CanonicalFrkFormations />} />
                    <Route path="/frek-canonical/:formationCode" element={<CanonicalFrkFormationDetail />} />
                    <Route path="/frek-canonical/:formationCode/:moduleCode" element={<CanonicalFrkModuleView />} />
                  </Route>

                  <Route element={<ProtectedRoute roles={TRAINER_ROLES} />}>
                    <Route path="/trainer" element={<TrainerDashboard />} />
                  </Route>
                  <Route element={<ProtectedRoute roles={JURY_ROLES} />}>
                    <Route path="/jury" element={<JuryDashboard />} />
                  </Route>
                  <Route element={<ProtectedRoute roles={ADMIN_ROLES} />}>
                    <Route path="/admin" element={<AdminDashboard />} />
                  </Route>
                </Route>

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
