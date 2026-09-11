import { Link } from "react-router-dom";
import { LEGAL_LINKS } from "@/pages/LegalHub";

export default function LegalFooter({ onManageCookies }) {
  return (
    <footer className="border-t border-black/10 bg-white px-6 py-6 md:px-16" aria-label="Informations juridiques">
      <div className="mx-auto flex max-w-7xl flex-col gap-4 text-xs text-[--cvln-ink-2] md:flex-row md:items-center md:justify-between">
        <div>© {new Date().getFullYear()} CVLN Academy</div>
        <nav className="flex flex-wrap gap-x-4 gap-y-2">
          {LEGAL_LINKS.map(([slug, label]) => (
            <Link key={slug} to={`/legal/${slug}`} className="hover:text-[--cvln-ink]">{label}</Link>
          ))}
          <button type="button" onClick={onManageCookies} className="hover:text-[--cvln-ink]">Gérer mes cookies</button>
        </nav>
      </div>
    </footer>
  );
}
