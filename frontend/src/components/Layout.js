import { NavLink, useLocation, useNavigate } from "react-router-dom";
import {
  HomeAlt, Compass, GraduationCap, Bookmark, Medal1st,
  Fingerprint, LogOut, Leaf, Language, Wallet as WalletIcon,
  Sparks, ShieldCheck, ShieldSearch, PeopleTag, Settings,
} from "iconoir-react";
import { useAuth } from "@/lib/auth.jsx";
import { useI18n, LANGS } from "@/lib/i18n.jsx";
import MentorPanel from "@/components/MentorPanel";
import { isPedagogicalContext } from "@/lib/mentorPresence";

const STUDENT_NAV = [
  { to: "/dashboard",       key: "dashboard",       Icon: HomeAlt },
  { to: "/roadmap",         key: "roadmap",         Icon: Compass },
  { to: "/formations",      key: "formations",      Icon: GraduationCap },
  { to: "/missions",        key: "missions",        Icon: Bookmark },
  { to: "/badges",          key: "badges",          Icon: Medal1st },
  { to: "/skills",          key: "skills",          Icon: Sparks },
  { to: "/certifications",  key: "certifications",  Icon: ShieldCheck },
  { to: "/wallet",          key: "wallet",          Icon: WalletIcon },
  { to: "/frek-profile",    key: "frek_profile",    Icon: Fingerprint },
];

const STAFF_NAV = [
  { to: "/trainer", key: "trainer_space", Icon: PeopleTag,   roles: ["trainer", "admin", "super_admin", "founder"] },
  { to: "/jury",    key: "jury_space",    Icon: ShieldSearch, roles: ["jury", "admin", "super_admin", "founder"] },
  { to: "/admin",   key: "admin_cms",     Icon: Settings,    roles: ["admin", "super_admin", "founder"] },
];

export default function Layout({ children }) {
  const { user, logout } = useAuth();
  const { t, lang, setLang } = useI18n();
  const nav = useNavigate();
  const location = useLocation();
  const NAV = [...STUDENT_NAV, ...STAFF_NAV.filter((item) => item.roles.includes(user?.role))];
  // MENTOR = CONTEXTUAL_PRESENCE (W3-C): the FAB/panel only mounts where a
  // pedagogical context justifies it — never a permanent floating chatbot
  // on every screen. See mentorPresence.js for the exact, deliberately
  // conservative scope.
  const mentorAvailable = isPedagogicalContext(location.pathname);

  return (
    <div className="min-h-screen flex" data-testid="app-layout">
      {/* Sidebar */}
      <aside
        className="hidden md:flex flex-col w-64 shrink-0 px-6 py-8 border-r border-black/5 bg-white sticky top-0 h-screen"
        data-testid="sidebar"
      >
        <div className="flex items-center gap-2 mb-10">
          <div className="w-9 h-9 rounded-full bg-[--cvln-orange] flex items-center justify-center">
            <Leaf className="text-white" width={18} height={18} />
          </div>
          <div className="font-display font-black text-[19px] tracking-tight leading-none">
            CVLN <span className="text-[--cvln-orange]">Academy</span>
          </div>
        </div>

        <nav className="flex flex-col gap-1" data-testid="sidebar-nav">
          {NAV.map(({ to, key, Icon }) => (
            <NavLink
              key={to} to={to}
              data-testid={`nav-${key}`}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition
                 ${isActive
                   ? "bg-[--cvln-forest] text-white"
                   : "text-[--cvln-ink-2] hover:bg-[--cvln-bg-warm] hover:text-[--cvln-ink]"}`
              }
            >
              <Icon width={18} height={18} />
              {t(key)}
            </NavLink>
          ))}
        </nav>

        <div className="mt-auto pt-6 border-t border-black/5 flex flex-col gap-3">
          {/* FREK-ID card */}
          <div className="rounded-2xl bg-[--cvln-bg-warm] p-4">
            <div className="text-[11px] uppercase tracking-[0.2em] text-[--cvln-ink-2] font-semibold">FREK-ID</div>
            <div className="mono text-lg mt-1 font-semibold" data-testid="frek-id-badge">{user?.frek_id}</div>
            <div className="text-sm text-[--cvln-ink-2] truncate">{user?.display_name}</div>
          </div>
          {/* Lang toggle */}
          <div className="flex items-center gap-1 px-1" data-testid="lang-toggle">
            <Language width={14} height={14} className="text-[--cvln-ink-2]" />
            {LANGS.map((l) => (
              <button
                key={l.code}
                data-testid={`lang-${l.code}`}
                onClick={() => setLang(l.code)}
                className={`text-xs px-2 py-1 rounded-full font-semibold transition
                  ${lang === l.code ? "bg-[--cvln-orange] text-white" : "text-[--cvln-ink-2] hover:text-[--cvln-ink]"}`}
              >
                {l.label}
              </button>
            ))}
          </div>
          <button
            data-testid="logout-btn"
            onClick={() => { logout(); nav("/"); }}
            className="flex items-center gap-2 text-sm text-[--cvln-ink-2] hover:text-[--cvln-orange] transition px-3 py-2"
          >
            <LogOut width={16} height={16} /> {t("logout")}
          </button>
        </div>
      </aside>

      {/* Main */}
      <main className="flex-1 min-w-0">
        {/* Mobile header */}
        <div className="md:hidden flex items-center justify-between px-5 py-4 border-b border-black/5 bg-white sticky top-0 z-30">
          <div className="font-display font-black tracking-tight">
            CVLN <span className="text-[--cvln-orange]">Academy</span>
          </div>
          <div className="mono text-sm text-[--cvln-ink-2]">{user?.frek_id}</div>
        </div>
        <div className="fade-in">{children}</div>
      </main>

      {mentorAvailable && <MentorPanel />}
    </div>
  );
}
