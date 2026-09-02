import { Suspense, lazy } from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import "@/App.css";
import "@/index.css";

import { AuthProvider, useAuth } from "@/lib/auth.jsx";
import { I18nProvider } from "@/lib/i18n.jsx";
import { Toaster } from "@/components/ui/sonner";
import Layout from "@/components/Layout";
import { RouteTransition } from "@/lib/RouteTransition";

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
const AdminDashboard = lazy(() => import("@/pages/admin/AdminDashboard"));
const TrainerDashboard = lazy(() => import("@/pages/trainer/TrainerDashboard"));
const JuryDashboard = lazy(() => import("@/pages/jury/JuryDashboard"));

const ADMIN_ROLES = ["admin", "super_admin", "founder"];
const TRAINER_ROLES = ["trainer", ...ADMIN_ROLES];
const JURY_ROLES = ["jury", ...ADMIN_ROLES];

function PageFallback() {
  return <div className="p-10 text-[--cvln-ink-2]">…</div>;
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
          <Suspense fallback={<PageFallback />}>
            <RouteTransition>
              <Routes>
                <Route path="/" element={<Landing />} />
                <Route path="/onboarding" element={<Onboarding />} />
                <Route path="/dashboard" element={<Protected><Dashboard /></Protected>} />
                <Route path="/roadmap" element={<Protected><Roadmap /></Protected>} />
                <Route path="/formations" element={<Protected><Formations /></Protected>} />
                <Route path="/formations/:code" element={<Protected><FormationDetail /></Protected>} />
                <Route path="/formations/:fc/modules/:mc" element={<Protected><ModuleJourney /></Protected>} />
                <Route path="/missions" element={<Protected><Missions /></Protected>} />
                <Route path="/badges" element={<Protected><Badges /></Protected>} />
                <Route path="/frek-profile" element={<Protected><FrekProfile /></Protected>} />
                <Route path="/wallet" element={<Protected><Wallet /></Protected>} />
                <Route path="/skills" element={<Protected><Skills /></Protected>} />
                <Route path="/certifications" element={<Protected><Certifications /></Protected>} />
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
