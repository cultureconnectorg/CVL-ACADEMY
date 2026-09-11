import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

const STORAGE_KEY = "cvln_cookie_consent_v1";

function readPreference() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
}

function writePreference(choice) {
  const payload = {
    version: 1,
    necessary: true,
    analytics: choice === "all",
    marketing: choice === "all",
    choice,
    decided_at: new Date().toISOString(),
  };
  localStorage.setItem(STORAGE_KEY, JSON.stringify(payload));
  window.dispatchEvent(new CustomEvent("cvln:cookie-consent", { detail: payload }));
  return payload;
}

export default function CookieConsent({ manageToken = 0 }) {
  const [open, setOpen] = useState(false);

  useEffect(() => {
    if (!readPreference()) setOpen(true);
  }, []);

  useEffect(() => {
    if (manageToken > 0) setOpen(true);
  }, [manageToken]);

  if (!open) return null;

  const choose = (choice) => {
    writePreference(choice);
    setOpen(false);
  };

  return (
    <section className="fixed inset-x-4 bottom-4 z-[100] mx-auto max-w-3xl rounded-3xl border border-black/10 bg-white p-5 shadow-2xl md:p-6" role="dialog" aria-modal="true" aria-labelledby="cookie-title">
      <h2 id="cookie-title" className="font-display text-xl font-black">Votre choix, réellement.</h2>
      <p className="mt-2 text-sm leading-6 text-[--cvln-ink-2]">Les traceurs nécessaires restent actifs. Les autres ne doivent être activés qu’après votre accord. Vous pouvez accepter, refuser ou revenir sur votre choix à tout moment.</p>
      <div className="mt-4 flex flex-col gap-2 sm:flex-row">
        <button type="button" onClick={() => choose("all")} className="btn-primary justify-center" data-testid="cookies-accept-all">Tout accepter</button>
        <button type="button" onClick={() => choose("necessary")} className="btn-outline justify-center" data-testid="cookies-refuse">Tout refuser</button>
        <Link to="/legal/cookies" className="btn-outline justify-center">En savoir plus</Link>
      </div>
    </section>
  );
}

export { STORAGE_KEY, readPreference };
