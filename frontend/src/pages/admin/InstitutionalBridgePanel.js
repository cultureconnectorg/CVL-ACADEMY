import { useEffect, useState } from "react";
import { CheckCircle, WarningTriangle } from "iconoir-react";
import { api } from "@/lib/api";

export default function InstitutionalBridgePanel() {
  const [rows, setRows] = useState([]);
  const [error, setError] = useState(false);

  useEffect(() => {
    api
      .get("/institutional/connectors")
      .then((response) => setRows(response.data))
      .catch(() => setError(true));
  }, []);

  return (
    <div className="cvln-card p-6" data-testid="institutional-bridge-panel">
      <div className="flex items-start justify-between gap-4 mb-4">
        <div>
          <div className="text-xs uppercase tracking-[0.2em] font-bold text-[--cvln-orange]">
            Interopérabilité
          </div>
          <h3 className="font-display font-bold text-xl tracking-tight mt-1">
            CVLN Institutional Bridge
          </h3>
        </div>
        <span className="text-xs font-bold px-3 py-1 rounded-full bg-[--cvln-bg-warm]">
          fail-closed
        </span>
      </div>

      <p className="text-sm text-[--cvln-ink-2] mb-4">
        Capacités réellement disponibles. Une préparation de dossier n&apos;est jamais affichée comme une soumission live.
      </p>

      {error ? (
        <div className="text-sm text-red-700 flex items-center gap-2">
          <WarningTriangle width={16} height={16} />
          Impossible de charger le registre institutionnel.
        </div>
      ) : (
        <div className="space-y-2">
          {rows.map((row) => (
            <div key={row.code} className="px-4 py-3 rounded-xl border border-black/5">
              <div className="flex items-center justify-between gap-3">
                <div className="min-w-0">
                  <div className="text-sm font-semibold truncate">{row.name}</div>
                  <div className="text-xs mono text-[--cvln-ink-2] mt-0.5">
                    {row.connection_mode}
                  </div>
                </div>
                <div className="text-right shrink-0">
                  {row.live_write_implemented ? (
                    <span className="text-xs font-bold text-[--cvln-forest] flex items-center gap-1">
                      <CheckCircle width={14} height={14} /> LIVE
                    </span>
                  ) : (
                    <span className="text-xs font-bold text-amber-700">PREPARE ONLY</span>
                  )}
                </div>
              </div>
              {row.capabilities.length > 0 && (
                <div className="flex flex-wrap gap-1.5 mt-2">
                  {row.capabilities.map((capability) => (
                    <span
                      key={capability}
                      className="text-[10px] mono px-2 py-1 rounded-md bg-[--cvln-bg-warm]"
                    >
                      {capability}
                    </span>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
