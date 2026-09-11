import { useEffect, useRef, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { useAuth } from "@/lib/auth.jsx";

export default function FrekAuthCallback() {
  const [params] = useSearchParams();
  const navigate = useNavigate();
  const { completeFrekLogin } = useAuth();
  const once = useRef(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (once.current) return;
    once.current = true;

    const code = params.get("code");
    const state = params.get("state");
    const providerError = params.get("error");

    if (providerError) {
      setError("Connexion FREK annulée ou refusée.");
      return;
    }
    if (!code || !state) {
      setError("Retour FREK incomplet.");
      return;
    }

    completeFrekLogin(code, state)
      .then((user) => {
        navigate(user.onboarding_completed ? "/dashboard" : "/onboarding", {
          replace: true,
        });
      })
      .catch((err) => {
        setError(err?.response?.data?.detail || "Connexion FREK impossible.");
      });
  }, [completeFrekLogin, navigate, params]);

  return (
    <div className="min-h-screen flex items-center justify-center px-6" data-testid="frek-auth-callback">
      <div className="cvln-card p-8 max-w-md w-full text-center">
        <div className="font-display font-black text-2xl">FREK</div>
        {error ? (
          <>
            <p className="mt-4 text-sm text-red-700">{error}</p>
            <button className="btn-outline mt-6" onClick={() => navigate("/", { replace: true })}>
              Retour
            </button>
          </>
        ) : (
          <p className="mt-4 text-sm text-[--cvln-ink-2]">Connexion à votre identité CVLN…</p>
        )}
      </div>
    </div>
  );
}
