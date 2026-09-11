import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { ArrowRight, Leaf } from "iconoir-react";
import { toast } from "sonner";
import { api } from "@/lib/api";
import { useAuth } from "@/lib/auth.jsx";

const destinationForRole = (role) => {
  if (role === "partner") return "/partner";
  if (role === "institution") return "/institution";
  if (role === "trainer") return "/trainer";
  if (role === "jury") return "/jury";
  if (["admin", "super_admin", "founder"].includes(role)) return "/admin";
  return "/onboarding";
};

export default function Invite() {
  const { code } = useParams();
  const { register } = useAuth();
  const navigate = useNavigate();
  const [invite, setInvite] = useState(null);
  const [error, setError] = useState(null);
  const [busy, setBusy] = useState(false);
  const [form, setForm] = useState({
    display_name: "",
    email: "",
    password: "",
  });

  useEffect(() => {
    let alive = true;
    api.get(`/invitations/${code}`)
      .then(({ data }) => {
        if (!alive) return;
        setInvite(data);
        setForm((prev) => ({ ...prev, email: data.email || prev.email }));
      })
      .catch((err) => alive && setError(err?.response?.data?.detail || "Invitation invalide"));
    return () => { alive = false; };
  }, [code]);

  const submit = async (e) => {
    e.preventDefault();
    setBusy(true);
    try {
      const user = await register({
        ...form,
        lang: "fr",
        invite_code: code,
      });
      toast.success("Invitation acceptée");
      navigate(destinationForRole(user.role), { replace: true });
    } catch (err) {
      toast.error(err?.response?.data?.detail || "Impossible d’accepter l’invitation");
    } finally {
      setBusy(false);
    }
  };

  if (error) {
    return <div className="min-h-screen grid place-items-center px-6"><div className="cvln-card p-8 max-w-lg w-full">{error}</div></div>;
  }
  if (!invite) return null;

  return (
    <div className="min-h-screen grid place-items-center px-6 py-12 bg-[--cvln-bg-warm]" data-testid="invite-page">
      <div className="cvln-card p-8 md:p-10 max-w-xl w-full">
        <div className="flex items-center gap-2">
          <div className="w-9 h-9 rounded-full bg-[--cvln-orange] flex items-center justify-center">
            <Leaf className="text-white" width={18} height={18} />
          </div>
          <div className="font-display font-black text-lg">CVLN <span className="text-[--cvln-orange]">Academy</span></div>
        </div>
        <div className="text-xs uppercase tracking-[0.22em] font-bold text-[--cvln-orange] mt-8">Invitation sécurisée</div>
        <h1 className="font-display font-black text-3xl tracking-tight mt-2">Rejoindre {invite.org_name || "CVLN Academy"}</h1>
        <p className="text-sm text-[--cvln-ink-2] mt-2">Rôle attribué par CVLN : <strong>{invite.role}</strong></p>

        <form onSubmit={submit} className="space-y-4 mt-8">
          <div>
            <label className="text-xs font-semibold text-[--cvln-ink-2]">Nom affiché</label>
            <input required minLength={1} maxLength={80} value={form.display_name} onChange={(e) => setForm({ ...form, display_name: e.target.value })} className="mt-1 w-full bg-white border border-black/10 rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-[--cvln-orange]" />
          </div>
          <div>
            <label className="text-xs font-semibold text-[--cvln-ink-2]">Email</label>
            <input required type="email" value={form.email} readOnly={Boolean(invite.email)} onChange={(e) => setForm({ ...form, email: e.target.value })} className="mt-1 w-full bg-white border border-black/10 rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-[--cvln-orange] disabled:opacity-60" />
          </div>
          <div>
            <label className="text-xs font-semibold text-[--cvln-ink-2]">Mot de passe</label>
            <input required type="password" minLength={6} value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} className="mt-1 w-full bg-white border border-black/10 rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-[--cvln-orange]" />
          </div>
          <button type="submit" disabled={busy} className="btn-primary w-full disabled:opacity-60">
            Accepter et créer mon espace <ArrowRight width={18} height={18} className="ml-2" />
          </button>
        </form>
      </div>
    </div>
  );
}
