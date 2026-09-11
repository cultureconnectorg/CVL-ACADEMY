import { useEffect, useMemo, useRef, useState } from "react";
import { Link, Navigate, useNavigate } from "react-router-dom";
import { CheckCircle, Erase } from "iconoir-react";
import { api } from "@/lib/api";
import { useAuth } from "@/lib/auth.jsx";
import { toast } from "sonner";

export default function LegalAcceptance() {
  const { user, loading } = useAuth();
  const nav = useNavigate();
  const canvasRef = useRef(null);
  const drawingRef = useRef(false);
  const lastPointRef = useRef(null);

  const [requirements, setRequirements] = useState(null);
  const [checked, setChecked] = useState({});
  const [signerName, setSignerName] = useState("");
  const [hasSignature, setHasSignature] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [loadError, setLoadError] = useState("");

  useEffect(() => {
    if (!user) return;
    setSignerName((name) => name || user.display_name || "");
    api.get("/legal/requirements")
      .then(({ data }) => {
        setRequirements(data);
        if (data.accepted) {
          nav(user.onboarding_completed ? "/dashboard" : "/onboarding", { replace: true });
        }
      })
      .catch((e) => setLoadError(e?.response?.data?.detail || "Impossible de charger les documents juridiques."));
  }, [user, nav]);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const resize = () => {
      const rect = canvas.getBoundingClientRect();
      const dpr = Math.max(1, window.devicePixelRatio || 1);
      const snapshot = hasSignature ? canvas.toDataURL("image/png") : null;
      canvas.width = Math.round(rect.width * dpr);
      canvas.height = Math.round(rect.height * dpr);
      const ctx = canvas.getContext("2d");
      ctx.scale(dpr, dpr);
      ctx.lineWidth = 2.2;
      ctx.lineCap = "round";
      ctx.lineJoin = "round";
      ctx.strokeStyle = "#111111";
      if (snapshot) {
        const img = new Image();
        img.onload = () => ctx.drawImage(img, 0, 0, rect.width, rect.height);
        img.src = snapshot;
      }
    };
    resize();
    window.addEventListener("resize", resize);
    return () => window.removeEventListener("resize", resize);
  }, [requirements, hasSignature]);

  const allChecked = useMemo(() => {
    if (!requirements?.documents?.length) return false;
    return requirements.documents.every((doc) => checked[doc.id]);
  }, [requirements, checked]);

  if (loading) return null;
  if (!user) return <Navigate to="/" replace />;

  const point = (event) => {
    const canvas = canvasRef.current;
    const rect = canvas.getBoundingClientRect();
    return { x: event.clientX - rect.left, y: event.clientY - rect.top };
  };

  const startDrawing = (event) => {
    drawingRef.current = true;
    lastPointRef.current = point(event);
    event.currentTarget.setPointerCapture?.(event.pointerId);
  };

  const draw = (event) => {
    if (!drawingRef.current) return;
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");
    const next = point(event);
    const prev = lastPointRef.current || next;
    ctx.beginPath();
    ctx.moveTo(prev.x, prev.y);
    ctx.lineTo(next.x, next.y);
    ctx.stroke();
    lastPointRef.current = next;
    setHasSignature(true);
  };

  const stopDrawing = () => {
    drawingRef.current = false;
    lastPointRef.current = null;
  };

  const clearSignature = () => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    setHasSignature(false);
  };

  const submit = async () => {
    if (!requirements || !allChecked || !hasSignature || !signerName.trim()) return;
    setSubmitting(true);
    try {
      const documents = Object.fromEntries(requirements.documents.map((doc) => [doc.id, doc.version]));
      const signature_data_url = canvasRef.current.toDataURL("image/png");
      const { data } = await api.post("/legal/accept", {
        documents,
        signature_data_url,
        signer_name: signerName.trim(),
      });
      toast.success(`Accord enregistré · ${data.bundle_version}`);
      nav(user.onboarding_completed ? "/dashboard" : "/onboarding", { replace: true });
    } catch (e) {
      const detail = e?.response?.data?.detail;
      toast.error(typeof detail === "string" ? detail : detail?.message || "Impossible d’enregistrer l’accord.");
      if (e?.response?.status === 409) window.location.reload();
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <main className="min-h-screen bg-white px-6 py-10 text-[--cvln-ink] md:px-16" data-testid="legal-acceptance-page">
      <div className="mx-auto max-w-4xl">
        <Link to="/legal/reglement-academy" className="text-sm font-semibold text-[--cvln-orange]">Consulter le centre juridique</Link>
        <div className="mt-8 rounded-3xl border border-black/10 p-6 md:p-10">
          <div className="text-xs font-bold uppercase tracking-[0.22em] text-[--cvln-orange]">Avant de commencer ton parcours</div>
          <h1 className="mt-3 font-display text-4xl font-black tracking-tight md:text-5xl">Accord Academy</h1>
          <p className="mt-4 max-w-2xl text-[--cvln-ink-2]">
            Lis les documents applicables, confirme chaque point puis signe dans le cadre avec ton doigt ou ta souris. CVLN Academy conservera la version signée et une preuve technique horodatée.
          </p>

          {loadError && <div className="mt-6 rounded-2xl bg-red-50 p-4 text-sm text-red-900">{loadError}</div>}
          {!requirements && !loadError && <div className="mt-8 text-sm text-[--cvln-ink-2]">Chargement…</div>}

          {requirements && (
            <>
              <div className="mt-8 rounded-2xl bg-black/[0.03] p-4 text-xs text-[--cvln-ink-2]">
                Bundle juridique <strong className="text-[--cvln-ink]">{requirements.bundle_version}</strong>. Une nouvelle version substantielle pourra nécessiter une nouvelle acceptation.
              </div>

              <div className="mt-6 space-y-3">
                {requirements.documents.map((doc) => (
                  <label key={doc.id} className="flex cursor-pointer items-start gap-3 rounded-2xl border border-black/10 p-4 hover:border-black/25">
                    <input
                      type="checkbox"
                      checked={!!checked[doc.id]}
                      onChange={(e) => setChecked((c) => ({ ...c, [doc.id]: e.target.checked }))}
                      className="mt-1 h-5 w-5 accent-[--cvln-orange]"
                      data-testid={`legal-check-${doc.id}`}
                    />
                    <span className="flex-1 text-sm leading-6">
                      {doc.mode === "accept" ? "J’accepte" : "J’atteste avoir pris connaissance de"}{" "}
                      <Link
                        to={doc.url}
                        target="_blank"
                        rel="noreferrer"
                        className="font-semibold text-[--cvln-orange] underline underline-offset-2"
                        onClick={(e) => e.stopPropagation()}
                      >
                        {doc.label}
                      </Link>
                      <span className="ml-2 font-mono text-[11px] text-[--cvln-ink-2]">v{doc.version}</span>
                    </span>
                  </label>
                ))}
              </div>

              <div className="mt-8">
                <label htmlFor="signer-name" className="text-sm font-semibold">Nom du signataire</label>
                <input
                  id="signer-name"
                  value={signerName}
                  onChange={(e) => setSignerName(e.target.value)}
                  maxLength={120}
                  className="mt-2 w-full rounded-2xl border-2 border-black/10 px-4 py-3 focus:border-[--cvln-orange] focus:outline-none"
                  autoComplete="name"
                />
              </div>

              <div className="mt-6">
                <div className="mb-2 flex items-center justify-between gap-3">
                  <div>
                    <div className="text-sm font-semibold">Signature</div>
                    <div className="mt-1 text-xs text-[--cvln-ink-2]">Signe avec ton doigt, un stylet, un trackpad ou une souris.</div>
                  </div>
                  <button type="button" onClick={clearSignature} className="btn-outline text-xs" disabled={!hasSignature}>
                    <Erase width={15} className="mr-1" /> Effacer
                  </button>
                </div>
                <canvas
                  ref={canvasRef}
                  className="h-44 w-full touch-none rounded-2xl border-2 border-dashed border-black/20 bg-white"
                  onPointerDown={startDrawing}
                  onPointerMove={draw}
                  onPointerUp={stopDrawing}
                  onPointerCancel={stopDrawing}
                  onPointerLeave={stopDrawing}
                  aria-label="Zone de signature"
                  data-testid="legal-signature-canvas"
                />
              </div>

              <div className="mt-6 rounded-2xl bg-amber-50 p-4 text-xs leading-5 text-amber-950">
                La signature graphique complète la preuve électronique mais ne remplace pas, à elle seule, l’identité du compte, la version des documents, l’horodatage et l’empreinte de preuve enregistrés côté serveur.
              </div>

              <button
                type="button"
                onClick={submit}
                disabled={!allChecked || !hasSignature || !signerName.trim() || submitting}
                className="btn-primary mt-8 w-full justify-center disabled:cursor-not-allowed disabled:opacity-40 md:w-auto"
                data-testid="legal-accept-submit"
              >
                <CheckCircle width={18} className="mr-2" />
                {submitting ? "Enregistrement…" : "Signer et commencer mon parcours"}
              </button>
            </>
          )}
        </div>
      </div>
    </main>
  );
}
