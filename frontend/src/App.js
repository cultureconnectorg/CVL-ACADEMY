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
const EcosystemBuilder = lazy(() => import("@/pages/EcosystemBuilder"));
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
const ProfessionalWorkspace = lazy(() => import("@/pages/admin/ProfessionalWorkspace"));
const TrainerDashboard = lazy(() => import("@/pages/trainer/TrainerDashboard"));
const JuryDashboard = lazy(() => import("@/pages/jury/JuryDashboard"));

const ADMIN_ROLES = ["admin", "super_admin", "founder"];
const TRAINER_ROLES = ["trainer", ...ADMIN_ROLES];
const JURY_ROLES = ["jury", ...ADMIN_ROLES];

function PageFallback() {
  return <div className="p-10 text-[--cvln-ink-2]">…</div>;
}

function ScrollRestoration() {
  useScrollRestoration();
  return null;
}

function LayoutRoute() {
  return (
    <Layout>
      <RouteTransition>
        <Outlet />
      </RouteTransition>
    </Layout>
  );
}

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
            <RouteTransition keyFor={sectionKeyFor}>
              <Routes>
                <Route path="/" element={<Landing />} />
                <Route path="/onboarding" element={<Onboarding />} />

                <Route element={<LayoutRoute />}>
                  <Route path="/formations" element={<Formations />} />
                  <Route path="/formations/:code" element={<FormationDetail />} />
                  <Route path="/offers" element={<Offers />} />
                  <Route path="/id/:frekId" element={<ProfessionalPublicProfile />} />

                  <Route element={<ProtectedRoute />}>
                    <Route path="/dashboard" element={<Dashboard />} />
                    <Route path="/roadmap" element={<Roadmap />} />
                    <Route path="/formations/:fc/modules/:mc" element={<ModuleJourney />} />
                    <Route path="/missions" element={<Missions />} />
                    <Route path="/badges" element={<Badges />} />
                    <Route path="/frek-profile" element={<FrekProfile />} />
                    <Route path="/ecosystem-builder" element={<EcosystemBuilder />} />
                    <Route path="/wallet" element={<Wallet />} />
                    <Route path="/skills" element={<Skills />} />
                    <Route path="/certifications" element={<Certifications />} />
                    <Route path="/canonical" element={<CanonicalFormations />} />
                    <Route path="/canonical/:formationCode" element={<CanonicalFormationDetail />} />
                    <Route path="/canonical/:formationCode/:moduleCode" element={<CanonicalModuleView />} />
                    <Route path="/kiltikonet-canonical" element={<CanonicalKltFormations />} />
                    <Route path="/kiltikonet-canonical/:formationCode" element={<CanonicalKltFormationDetail />} />
                    <Route path="/kiltikonet-canonical/:formationCode/:moduleCode" element={<CanonicalKltModuleView />} />
                    <Route path="/kora-canonical" element={<CanonicalKorFormations />} />
                    <Route path="/kora-canonical/:formationCode" element={<CanonicalKorFormationDetail />} />
                    <Route path="/kora-canonical/:formationCode/:moduleCode" element={<CanonicalKorModuleView />} />
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
                    <Route path="/admin/professional-workspace" element={<ProfessionalWorkspace />} />
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
