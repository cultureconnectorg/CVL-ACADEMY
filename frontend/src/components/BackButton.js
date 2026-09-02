import { Link, useNavigate } from "react-router-dom";
import { NavArrowLeft } from "iconoir-react";
import { useI18n } from "@/lib/i18n.jsx";

/**
 * Consistent back navigation. Prefers going back in history; if history has
 * only the initial entry (e.g. deep-link), falls back to `fallbackTo`.
 */
export default function BackButton({ to = null, label = null, fallbackTo = "/dashboard", testId = "back-button" }) {
  const { t } = useI18n();
  const nav = useNavigate();
  const canGoBack = window.history.length > 1;
  const resolvedLabel = label ?? t("onboarding_p.back");

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
        <NavArrowLeft width={16} height={16} /> {resolvedLabel}
      </Link>
    );
  }

  return (
    <button
      data-testid={testId}
      onClick={onClick}
      className="inline-flex items-center gap-1 text-sm text-[--cvln-ink-2] hover:text-[--cvln-orange] transition mb-6"
    >
      <NavArrowLeft width={16} height={16} /> {resolvedLabel}
    </button>
  );
}
