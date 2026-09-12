import { Link, NavLink } from "react-router-dom";
import { Leaf } from "iconoir-react";

const PUBLIC_DISCOVERY_NAV = [
  ["/formations", "Formations"],
  ["/roadmap", "Parcours"],
  ["/missions", "Missions"],
  ["/skills", "Skills"],
  ["/certifications", "Certifications"],
  ["/badges", "Badges"],
  ["/wallet", "Wallet"],
  ["/frek-profile", "FREK-ID"],
  ["/pricing", "Tarifs"],
];

export default function PublicDiscoveryLayout({ children }) {
  return (
    <div className="min-h-screen bg-[--cvln-bg] text-[--cvln-ink]" data-testid="public-discovery-layout">
      <header className="sticky top-0 z-40 border-b border-black/5 bg-white/90 backdrop-blur-xl">
        <div className="mx-auto flex max-w-7xl items-center gap-5 px-6 py-4 md:px-12">
          <Link to="/" className="flex items-center gap-3 shrink-0" aria-label="CVLN Academy — Accueil">
            <span className="inline-flex h-9 w-9 items-center justify-center rounded-full bg-[--cvln-orange] text-white">
              <Leaf width={17} height={17} />
            </span>
            <span className="font-display font-black tracking-[0.08em]">CVLN <span className="text-[--cvln-orange]">ACADEMY</span></span>
          </Link>

          <nav className="hidden lg:flex flex-1 items-center gap-1 overflow-x-auto" aria-label="Découvrir CVLN Academy">
            {PUBLIC_DISCOVERY_NAV.map(([to, label]) => (
              <NavLink
                key={to}
                to={to}
                className={({ isActive }) => `rounded-full px-3 py-2 text-xs font-semibold transition ${isActive ? "bg-black text-white" : "text-[--cvln-ink-2] hover:bg-black/5 hover:text-[--cvln-ink]"}`}
              >
                {label}
              </NavLink>
            ))}
          </nav>

          <div className="ml-auto flex items-center gap-2 shrink-0">
            <Link to="/login" className="btn-outline text-sm">Se connecter</Link>
            <Link to="/register" className="btn-primary text-sm">Rejoindre</Link>
          </div>
        </div>
      </header>
      <main>{children}</main>
    </div>
  );
}
