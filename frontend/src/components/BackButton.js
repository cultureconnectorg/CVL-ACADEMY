import { Link, useNavigate } from "react-router-dom";
import { NavArrowLeft } from "iconoir-react";

/**
 * Consistent back navigation. Prefers going back in history; if history has
 * only the initial entry (e.g. deep-link), falls back to `fallbackTo`.
 */
export default function BackButton({ to = null, label = "Retour", fallbackTo = "/dashboard", testId = "back-button" }) {
  const nav = useNavigate();
  const canGoBack = window.history.length > 1;

  const onClick = (e) => {
    if (to) return; // let Link handle it
    e.preventDefault();
    if (canGoBack) nav(-1);
    else nav(fallbackTo);
  };

  if (to) {
    return (
      <Link
        to={to}
        data-testid={testId}
        className="inline-flex items-center gap-1 text-sm text-[--cvln-ink-2] hover:text-[--cvln-orange] transition mb-6"
      >
        <NavArrowLeft width={16} height={16} /> {label}
      </Link>
    );
  }

  return (
    <button
      data-testid={testId}
      onClick={onClick}
      className="inline-flex items-center gap-1 text-sm text-[--cvln-ink-2] hover:text-[--cvln-orange] transition mb-6"
    >
      <NavArrowLeft width={16} height={16} /> {label}
    </button>
  );
}
