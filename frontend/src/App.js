import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import "@/App.css";
import "@/index.css";

import { AuthProvider, useAuth } from "@/lib/auth.jsx";
import { I18nProvider } from "@/lib/i18n.jsx";
import { Toaster } from "@/components/ui/sonner";

import Landing from "@/pages/Landing";
import Dashboard from "@/pages/Dashboard";
import Formations from "@/pages/Formations";
import FormationDetail from "@/pages/FormationDetail";
import Missions from "@/pages/Missions";
import Badges from "@/pages/Badges";
import FrekProfile from "@/pages/FrekProfile";
import Roadmap from "@/pages/Roadmap";
import Layout from "@/components/Layout";

function Protected({ children }) {
  const { user, loading } = useAuth();
  if (loading) return null;
  if (!user) return <Navigate to="/" replace />;
  return <Layout>{children}</Layout>;
}

function App() {
  return (
    <I18nProvider>
      <AuthProvider>
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<Landing />} />
            <Route path="/dashboard" element={<Protected><Dashboard /></Protected>} />
            <Route path="/roadmap" element={<Protected><Roadmap /></Protected>} />
            <Route path="/formations" element={<Protected><Formations /></Protected>} />
            <Route path="/formations/:code" element={<Protected><FormationDetail /></Protected>} />
            <Route path="/missions" element={<Protected><Missions /></Protected>} />
            <Route path="/badges" element={<Protected><Badges /></Protected>} />
            <Route path="/frek-profile" element={<Protected><FrekProfile /></Protected>} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </BrowserRouter>
        <Toaster position="top-right" richColors />
      </AuthProvider>
    </I18nProvider>
  );
}

export default App;
