import { useEffect, useState } from "react";
import { NavLink, useLocation, useNavigate } from "react-router-dom";
import {
  HomeAlt,
  Compass,
  GraduationCap,
  Bookmark,
  Medal1st,
  Fingerprint,
  LogOut,
  Leaf,
  Wallet as WalletIcon,
  Sparks,
  ShieldCheck,
  ShieldSearch,
  PeopleTag,
  Settings,
  Building,
} from "iconoir-react";
import { useAuth } from "@/lib/auth.jsx";
import { useI18n } from "@/lib/i18n.jsx";
import { api } from "@/lib/api";
import MentorPanel from "@/components/MentorPanel";
import { isPedagogicalContext } from "@/lib/mentorPresence";
import { captureRouteDepth, restoreRouteDepth } from "@/lib/depthMemory";

const STUDENT_NAV = [
  { to: "/dashboard", key: "dashboard", Icon: HomeAlt },
  { to: "/roadmap", key: "roadmap", Icon: Compass },
  { to: "/formations", key: "formations", Icon: GraduationCap },
  { to: "/missions", key: "missions", Icon: Bookmark },
  { to: "/badges", key: "badges", Icon: Medal1st },
  { to: "/skills", key: "skills", Icon: Sparks },
  { to: "/certifications", key: "certifications", Icon: ShieldCheck },
  { to: "/wallet", key: "wallet", Icon: WalletIcon },
  { to: "/frek-profile", key: "frek_profile", Icon: Fingerprint },
];

const STAFF_NAV = [
  { to: "/trainer", key: "trainer_space", Icon: PeopleTag, roles: ["trainer", "admin", "super_admin", "founder"] },
  { to: "/jury", key: "jury_space", Icon: ShieldSearch, roles: ["jury", "corrector", "admin", "super_admin", "founder"] },
  { to: "/admin", key: "admin_cms", Icon: Settings, roles: ["admin", "super_admin", "founder"] },
  { to: "/admin/stakeholders", label: "Accès partenaires", Icon: Building, roles: ["admin", "super_admin", "founder"] },
];

export default function Layout({ children }) {
  const { user, logout } = useAuth();
  const { t } = useI18n();
  const nav = useNavigate();
  const location = useLocation();
  const [stakeholder, setStakeholder] = useState(null);

  useEffect(() => {
    let alive = true;
    if (!user?.id) return undefined;
    api
      .get("/stakeholders/me")
      .then((response) => {
        if (alive) setStakeholder(response.data.membership);
      })
      .catch(() => {
        if (alive) setStakeholder(null);
      });
    return () => {
      alive = false;
    };
  }, [user?.id, user?.org_id]);

  const stakeholderNav = stakeholder
    ? [{
        to: stakeholder.stakeholder_type === "institution" ? "/institution" : "/partner",
        label: stakeholder.stakeholder_type === "institution" ? "Institution" : "Partenaire",
        Icon: Building,
      }]
    : [];

  const navItems = [
    ...STUDENT_NAV,
    ...stakeholderNav,
    ...STAFF_NAV.filter((item) => item.roles.includes(user?.role)),
  ];

  const mentorAvailable = isPedagogicalContext(location.pathname);

  useEffect(() => {
    restoreRouteDepth(location.pathname);
    return () => captureRouteDepth(location.pathname);
  }, [location.pathname]);

  return (
    <div className="cvln-app-shell" data-testid="app-layout">
      <header className="cvln-app-topbar" data-testid="sidebar">
        <NavLink to="/dashboard" className="cvln-wordmark shrink-0" aria-label="CVLN Academy">
          <div className="cvln-wordmark-mark" aria-hidden="true">
            <Leaf width={17} height={17} />
          </div>
          <div className="hidden sm:block">
            <div className="font-display font-black tracking-[0.1em] text-base leading-none">CVLN</div>
            <div className="text-[8px] tracking-[0.22em] text-white/50 mt-1">ACADEMY</div>
          </div>
        </NavLink>

        <nav data-testid="sidebar-nav" aria-label="Navigation principale">
          {navItems.map(({ to, key, label, Icon }) => {
            const testId = key || to.replace(/^\//, "").replace(/\//g, "-");
            return (
              <NavLink
                key={to}
                to={to}
                data-testid={`nav-${testId}`}
                data-active={location.pathname === to || location.pathname.startsWith(`${to}/`) ? "true" : "false"}
              >
                <Icon width={16} height={16} />
                <span>{label || t(key)}</span>
              </NavLink>
            );
          })}
        </nav>

        <div className="flex items-center gap-2 shrink-0">
          <div className="hidden xl:block text-right mr-1">
            <div className="text-[9px] uppercase tracking-[.2em] text-white/40">{user?.frek_id}</div>
            <div className="text-xs text-white/75 max-w-[130px] truncate">{user?.display_name}</div>
          </div>
          <button
            data-testid="logout-btn"
            onClick={() => {
              logout();
              nav("/");
            }}
            className="w-10 h-10 rounded-full border border-white/10 bg-white/5 inline-flex items-center justify-center text-white/60 hover:text-white hover:bg-white/10 transition"
            aria-label={t("logout")}
          >
            <LogOut width={16} height={16} />
          </button>
        </div>
      </header>

      <main className="cvln-app-main">
        <div className="fade-in">{children}</div>
      </main>

      {mentorAvailable && <MentorPanel />}
    </div>
  );
}
