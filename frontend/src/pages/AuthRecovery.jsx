import { useEffect, useState } from "react";
import { Link, useNavigate, useSearchParams } from "react-router-dom";
import { toast } from "sonner";

import { api } from "@/lib/api";

function Shell({ title, subtitle, children }) {
  return (
    <main className="min-h-screen flex items-center justify-center px-6 py-12 bg-[--cvln-bg] text-[--cvln-ink]">
      <section className="w-full max-w-md rounded-3xl border border-white/10 bg-black/20 p-6 md:p-8 backdrop-blur-xl">
        <p className="text-xs uppercase tracking-[0.22em] text-[--cvln-ink-2]">CVLN Academy</p>
        <h1 className="mt-3 text-2xl font-semibold">{title}</h1>
        {subtitle ? <p className="mt-2 text-sm text-[--cvln-ink-2]">{subtitle}</p> : null}
        <div className="mt-6">{children}</div>
        <div className="mt-6 text-sm text-[--cvln-ink-2]">
          <Link to="/login" className="underline underline-offset-4">Retour à la connexion</Link>
        </div>
      </section>
    </main>
  );
}

export function ForgotPassword() {
  const [email, setEmail] = useState("");
  const [busy, setBusy] = useState(false);
  const [sent, setSent] = useState(false);

  async function submit(event) {
    event.preventDefault();
    setBusy(true);
    try {
      await api.post("/auth/forgot-password", { email });
      setSent(true);
      toast.success("Si ce compte existe, les instructions ont été préparées.");
    } catch (error) {
      toast.error(error?.response?.data?.detail || "Impossible de lancer la réinitialisation.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <Shell title="Mot de passe oublié" subtitle="Saisis l’adresse e-mail de ton compte CVLN Academy.">
      {sent ? (
        <p className="text-sm">Demande enregistrée. Vérifie ton canal de récupération configuré.</p>
      ) : (
        <form onSubmit={submit} className="space-y-4">
          <label className="block text-sm">
            E-mail
            <input
              type="email"
              required
              autoComplete="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="mt-2 w-full rounded-xl border border-white/15 bg-black/20 px-4 py-3 outline-none"
            />
          </label>
          <button disabled={busy} className="w-full rounded-xl border border-white/15 px-4 py-3 disabled:opacity-50">
            {busy ? "Envoi…" : "Réinitialiser mon mot de passe"}
          </button>
        </form>
      )}
    </Shell>
  );
}

export function ResetPassword() {
  const [params] = useSearchParams();
  const navigate = useNavigate();
  const token = params.get("token") || "";
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");
  const [busy, setBusy] = useState(false);

  async function submit(event) {
    event.preventDefault();
    if (!token) return toast.error("Lien de réinitialisation invalide.");
    if (password.length < 6) return toast.error("Le mot de passe doit contenir au moins 6 caractères.");
    if (password !== confirm) return toast.error("Les mots de passe ne correspondent pas.");
    setBusy(true);
    try {
      await api.post("/auth/reset-password", { token, new_password: password });
      toast.success("Mot de passe modifié.");
      navigate("/login", { replace: true });
    } catch (error) {
      toast.error(error?.response?.data?.detail || "Lien invalide ou expiré.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <Shell title="Nouveau mot de passe" subtitle="Choisis un nouveau mot de passe pour ton compte.">
      {!token ? (
        <p className="text-sm">Ce lien ne contient aucun jeton de réinitialisation.</p>
      ) : (
        <form onSubmit={submit} className="space-y-4">
          <label className="block text-sm">Nouveau mot de passe
            <input type="password" minLength={6} required autoComplete="new-password" value={password} onChange={(e) => setPassword(e.target.value)} className="mt-2 w-full rounded-xl border border-white/15 bg-black/20 px-4 py-3 outline-none" />
          </label>
          <label className="block text-sm">Confirmer
            <input type="password" minLength={6} required autoComplete="new-password" value={confirm} onChange={(e) => setConfirm(e.target.value)} className="mt-2 w-full rounded-xl border border-white/15 bg-black/20 px-4 py-3 outline-none" />
          </label>
          <button disabled={busy} className="w-full rounded-xl border border-white/15 px-4 py-3 disabled:opacity-50">{busy ? "Validation…" : "Mettre à jour"}</button>
        </form>
      )}
    </Shell>
  );
}

export function VerifyEmail() {
  const [params] = useSearchParams();
  const token = params.get("token") || "";
  const [state, setState] = useState(token ? "checking" : "invalid");

  useEffect(() => {
    let alive = true;
    if (!token) return undefined;
    api.post("/auth/verify-email", { token })
      .then(() => alive && setState("verified"))
      .catch(() => alive && setState("error"));
    return () => { alive = false; };
  }, [token]);

  const copy = {
    checking: ["Vérification en cours", "Nous validons ton adresse e-mail."],
    verified: ["Adresse e-mail vérifiée", "Ton compte CVLN Academy est maintenant vérifié."],
    invalid: ["Lien invalide", "Aucun jeton de vérification n’a été fourni."],
    error: ["Vérification impossible", "Ce lien est invalide, expiré ou a déjà été utilisé."],
  }[state];

  return (
    <Shell title={copy[0]} subtitle={copy[1]}>
      {state === "verified" ? <Link to="/dashboard" className="inline-block rounded-xl border border-white/15 px-4 py-3">Continuer</Link> : null}
    </Shell>
  );
}
