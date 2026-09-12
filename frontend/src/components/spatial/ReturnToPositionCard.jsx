import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { ArrowRight } from "iconoir-react";
import {
  armReturnPositionRestore,
  loadReturnPosition,
  resumeHref,
  returnPositionUserKey,
} from "@/lib/returnPosition";

function labelForPath(pathname) {
  if (pathname?.includes("/modules/")) return "Reprendre le module";
  if (pathname?.startsWith("/formations/")) return "Reprendre la formation";
  if (pathname === "/formations") return "Reprendre l’exploration";
  if (pathname === "/roadmap") return "Reprendre la roadmap";
  if (pathname === "/missions") return "Reprendre les missions";
  if (pathname === "/skills") return "Reprendre les compétences";
  if (pathname === "/certifications") return "Reprendre les certifications";
  if (pathname === "/wallet") return "Reprendre le Wallet";
  return "Reprendre là où tu étais";
}

export default function ReturnToPositionCard({ user }) {
  const userKey = useMemo(() => returnPositionUserKey(user), [user]);
  const [snapshot, setSnapshot] = useState(null);

  useEffect(() => {
    setSnapshot(userKey ? loadReturnPosition(userKey) : null);
  }, [userKey]);

  const href = resumeHref(snapshot);
  if (!userKey || !href || snapshot?.pathname === "/dashboard") return null;

  return (
    <div className="mb-6 cvln-card p-5 flex flex-wrap items-center gap-4" data-testid="return-position-card">
      <div className="flex-1 min-w-0">
        <div className="text-[10px] mono uppercase tracking-[0.25em] font-bold text-[--cvln-orange]">
          Continuité Spatial
        </div>
        <div className="font-display font-bold text-xl tracking-tight mt-1">
          {labelForPath(snapshot.pathname)}
        </div>
        <div className="text-xs text-[--cvln-ink-2] mt-1 truncate">
          {snapshot.pathname}
        </div>
      </div>
      <Link
        to={href}
        className="btn-primary"
        data-testid="return-position-open"
        onClick={() => armReturnPositionRestore(userKey)}
      >
        Continuer
        <ArrowRight width={16} height={16} className="ml-2" />
      </Link>
    </div>
  );
}
