import { useEffect, useState } from "react";
import { NavLink, useLocation, useNavigate } from "react-router-dom";
import {
  HomeAlt, Compass, GraduationCap, Bookmark, Medal1st,
  Fingerprint, LogOut, Leaf, Language, Wallet as WalletIcon,
  Sparks, ShieldCheck, ShieldSearch, PeopleTag, Settings,
  Menu, Xmark, CreditCard,
} from "iconoir-react";
import { useAuth } from "@/lib/auth.jsx";
import { useI18n, LANGS } from "@/lib/i18n.jsx";
import MentorPanel from "@/components/MentorPanel";
import AcademyBackdrop from "@/components/AcademyBackdrop";
import { isPedagogicalContext } from "@/lib/mentorPresence";

const STUDENT_NAV = [
  { to: "/dashboard",       key: "dashboard",       Icon: HomeAlt },
  { to: "/roadmap",         key: "roadmap",         Icon: Compass },
  { to: "/formations",      key: "formations",      Icon: GraduationCap },
  { to: "/missions",        key: "missions",        Icon: Bookmark },
  { to: "/badges",          key: "badges",          Icon: Medal1st },
  { to: "/skills",          key: "skills",          Icon: Sparks },
  { to: "/certifications",  key: "certifications",  Icon: ShieldCheck },
  // ACA-0025/W-FUNNEL-2 "Conversion" — the real DECIDED_V1 commercial
  // catalogue, same NAV list every other page uses (desktop sidebar +
  // mobile "more" sheet, see MOBILE_PRIMARY_KEYS below).
  { to: "/offers",          key: "offers",          Icon: CreditCard },
  { to: "/wallet",          key: "wallet",          Icon: WalletIcon },
  { to: "/frek-profile",    key: "frek_profile",    Icon: Fingerprint },
];

const STAFF_NAV = [
  { to: "/trainer", key: "trainer_space", Icon: PeopleTag,   roles: ["trainer", "admin", "super_admin", "founder"] },
  { to: "/jury",    key: "jury_space",    Icon: ShieldSearch, roles: ["jury", "admin", "super_admin", "founder"] },
  { to: "/admin",   key: "admin_cms",     Icon: Settings,    roles: ["admin", "super_admin", "founder"] },
];

// ACA-0022 — mobile global navigation. The sidebar is `hidden md:flex`
// (always was); below md there was no navigation at all besides a
// static header, so a signed-in learner on a phone could only move
// between screens via browser back/forward. This is the real fix, not
// a cosmetic one: a fixed bottom tab bar for the 4 highest-frequency
// destinations, plus a "More" sheet for the rest of STUDENT_NAV and
// every role-gated STAFF_NAV entry the user actually has — same NAV
// list the sidebar already computes, just presented two ways.
const MOBILE_PRIMARY_KEYS = ["dashboard", "roadmap", "formations", "missions"];

export default function Layout({ children }) {
  const { user, logout } = useAuth();
  const { t, lang, setLang } = useI18n();
  const nav = useNavigate();
  const location = useLocation();
  const [mobileMoreOpen, setMobileMoreOpen] = useState(false);
  const NAV = [...STUDENT_NAV, ...STAFF_NAV.filter((item) => item.roles.includes(user?.role))];
  const mobilePrimary = NAV.filter((item) => MOBILE_PRIMARY_KEYS.includes(item.key));
  const mobileMore = NAV.filter((item) => !MOBILE_PRIMARY_KEYS.includes(item.key));
  // MENTOR = CONTEXTUAL_PRESENCE (W3-C): the FAB/panel only mounts where a
  // pedagogical context justifies it — never a permanent floating chatbot
  // on every screen. See mentorPresence.js for the exact, deliberately
  // conservative scope.
  const mentorAvailable = isPedagogicalContext(location.pathname);

  // A route change (tapping a bottom-tab link, or a sheet link) always
  // closes the sheet — it must never survive a navigation.
  useEffect(() => { setMobileMoreOpen(false); }, [location.pathname]);

  useEffect(() => {
    if (!mobileMoreOpen) return;
    const onKey = (e) => { if (e.key === "Escape") setMobileMoreOpen(false); };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [mobileMoreOpen]);

  return (
    <div className="min-h-screen flex" data-testid="app-layout">
      <AcademyBackdrop />
      {/* Sidebar */}
      <aside
        className="hidden md:flex flex-col w-64 shrink-0 px-6 py-8 border-r border-black/5 bg-white sticky top-0 h-screen relative z-10"
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
      <main className="flex-1 min-w-0 relative z-10">
        {/* Mobile header */}
        <div className="md:hidden flex items-center justify-between px-5 py-4 border-b border-black/5 bg-white sticky top-0 z-30">
          <div className="font-display font-black tracking-tight">
            CVLN <span className="text-[--cvln-orange]">Academy</span>
          </div>
          <div className="mono text-sm text-[--cvln-ink-2]">{user?.frek_id}</div>
        </div>
        {/* pb-20 clears the fixed bottom tab bar below (mobile only —
            the bar itself is md:hidden, so this padding is harmless,
            not just unused, once md:pb-0 cancels it above that
            breakpoint). */}
        <div className="fade-in pb-20 md:pb-0">{children}</div>
      </main>

      {/* Mobile bottom tab bar (ACA-0022) — the sidebar's `hidden md:flex`
          counterpart. Same NAV data, curated to the 4 highest-frequency
          destinations + a "More" sheet for the rest, so a phone user can
          always reach every screen the desktop sidebar reaches. */}
      <nav
        className="md:hidden fixed bottom-0 left-0 right-0 z-40 bg-white border-t border-black/5 flex items-stretch"
        data-testid="mobile-nav-bar"
        style={{ paddingBottom: "env(safe-area-inset-bottom)" }}
      >
        {mobilePrimary.map(({ to, key, Icon }) => (
          <NavLink
            key={to}
            to={to}
            data-testid={`mobile-nav-${key}`}
            className={({ isActive }) =>
              `flex-1 flex flex-col items-center justify-center gap-1 py-2.5 text-[10px] font-medium transition
               ${isActive ? "text-[--cvln-forest]" : "text-[--cvln-ink-2]"}`
            }
          >
            <Icon width={20} height={20} />
            {t(key)}
          </NavLink>
        ))}
        <button
          type="button"
          data-testid="mobile-nav-more"
          onClick={() => setMobileMoreOpen(true)}
          aria-expanded={mobileMoreOpen}
          aria-controls="mobile-nav-sheet"
          className="flex-1 flex flex-col items-center justify-center gap-1 py-2.5 text-[10px] font-medium text-[--cvln-ink-2] transition"
        >
          <Menu width={20} height={20} />
          {t("mobile_nav_more")}
        </button>
      </nav>

      {/* "More" sheet — the rest of STUDENT_NAV plus every role-gated
          STAFF_NAV entry this user has, plus lang toggle + logout (the
          sidebar's footer block, mirrored here since it's md:hidden on
          mobile). Backdrop click, the X, or Escape all close it. */}
      {mobileMoreOpen && (
        <div className="md:hidden fixed inset-0 z-50 flex items-end">
          <button
            type="button"
            className="absolute inset-0 bg-black/40"
            data-testid="mobile-nav-sheet-backdrop"
            aria-label={t("mobile_nav_close")}
            onClick={() => setMobileMoreOpen(false)}
          />
          <div
            id="mobile-nav-sheet"
            data-testid="mobile-nav-sheet"
            role="dialog"
            aria-modal="true"
            className="relative w-full max-h-[75vh] overflow-y-auto bg-white rounded-t-3xl p-5 pb-[calc(1.25rem+env(safe-area-inset-bottom))]"
          >
            <div className="flex items-center justify-between mb-4">
              <div className="font-display font-bold text-lg">{t("mobile_nav_more")}</div>
              <button
                type="button"
                data-testid="mobile-nav-sheet-close"
                onClick={() => setMobileMoreOpen(false)}
                aria-label={t("mobile_nav_close")}
                className="w-9 h-9 rounded-full bg-black/5 flex items-center justify-center text-[--cvln-ink-2]"
              >
                <Xmark width={18} height={18} />
              </button>
            </div>

            <div className="grid grid-cols-3 gap-3">
              {mobileMore.map(({ to, key, Icon }) => (
                <NavLink
                  key={to}
                  to={to}
                  data-testid={`mobile-nav-sheet-${key}`}
                  className={({ isActive }) =>
                    `flex flex-col items-center justify-center gap-2 rounded-2xl p-4 text-xs font-medium text-center transition
                     ${isActive ? "bg-[--cvln-forest] text-white" : "bg-[--cvln-bg-warm] text-[--cvln-ink-2]"}`
                  }
                >
                  <Icon width={20} height={20} />
                  {t(key)}
                </NavLink>
              ))}
            </div>

            <div className="mt-5 pt-4 border-t border-black/5 flex items-center justify-between">
              <div className="flex items-center gap-1" data-testid="lang-toggle-mobile">
                <Language width={14} height={14} className="text-[--cvln-ink-2]" />
                {LANGS.map((l) => (
                  <button
                    key={l.code}
                    data-testid={`lang-mobile-${l.code}`}
                    onClick={() => setLang(l.code)}
                    className={`text-xs px-2 py-1 rounded-full font-semibold transition
                      ${lang === l.code ? "bg-[--cvln-orange] text-white" : "text-[--cvln-ink-2]"}`}
                  >
                    {l.label}
                  </button>
                ))}
              </div>
              <button
                type="button"
                data-testid="logout-btn-mobile"
                onClick={() => { setMobileMoreOpen(false); logout(); nav("/"); }}
                className="flex items-center gap-2 text-sm text-[--cvln-ink-2]"
              >
                <LogOut width={16} height={16} /> {t("logout")}
              </button>
            </div>
          </div>
        </div>
      )}

      {mentorAvailable && <MentorPanel />}
    </div>
  );
}
