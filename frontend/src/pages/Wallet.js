import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { Coins, Medal1st, AppleWallet, CardWallet } from "iconoir-react";
import { toast } from "sonner";
import { api } from "@/lib/api";
import { useAuth } from "@/lib/auth.jsx";
import { useI18n } from "@/lib/i18n.jsx";

export default function Wallet() {
  const { t } = useI18n();
  const { user } = useAuth();
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(Boolean(user));

  const TXN_LABELS = {
    badge_earned: t("wallet_p.txn_badge_earned"),
    jcc_earned: t("wallet_p.txn_jcc_earned"),
    token_earned: t("wallet_p.txn_token_earned"),
    reward_redeemed: t("wallet_p.txn_reward_redeemed"),
    payment: t("wallet_p.txn_payment"),
  };

  useEffect(() => {
    if (!user) {
      setSummary(null);
      setLoading(false);
      return;
    }
    setLoading(true);
    api
      .get("/wallet/me")
      .then((r) => setSummary(r.data))
      .catch(() => toast.error(t("wallet_p.load_error")))
      .finally(() => setLoading(false));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [user]);

  const openPass = async (provider) => {
    if (!user) return;
    try {
      const { data } = await api.get(`/wallet/pass/${provider}`);
      toast.info(data.note || t("wallet_p.pass_ready"));
      console.log(`${provider} Academy mini-wallet pass payload`, data.payload);
    } catch {
      toast.error(t("wallet_p.pass_unavailable"));
    }
  };

  if (loading) return <div className="p-10 text-[--cvln-ink-2]">…</div>;

  if (!user) {
    return (
      <div className="px-6 md:px-12 py-10 max-w-6xl" data-testid="wallet-page" data-public="true">
        <div className="text-xs uppercase tracking-[0.25em] font-bold text-[--cvln-orange]">CVLN Academy · Wallet</div>
        <h1 className="font-display font-black text-4xl md:text-5xl tracking-tighter mt-2">Une économie liée aux preuves, pas un solde public.</h1>
        <p className="text-[--cvln-ink-2] mt-4 max-w-2xl">Le Wallet Academy relie crédits, récompenses, badges et droits d’accès. Les soldes, transactions, paiements et passes restent strictement privés et ne sont chargés qu’après authentification.</p>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-5 mt-10">
          <div className="cvln-card p-6"><Coins width={22} height={22} className="text-[--cvln-orange]" /><h2 className="font-display font-bold text-xl mt-4">Crédits & récompenses</h2><p className="text-sm text-[--cvln-ink-2] mt-2">Les actions validées peuvent alimenter les unités prévues par l’écosystème Academy.</p></div>
          <div className="cvln-card p-6"><Medal1st width={22} height={22} className="text-[--cvln-orange]" /><h2 className="font-display font-bold text-xl mt-4">Badges reliés</h2><p className="text-sm text-[--cvln-ink-2] mt-2">Les preuves acquises restent liées à l’identité et au parcours du membre.</p></div>
          <div className="cvln-card p-6"><CardWallet width={22} height={22} className="text-[--cvln-orange]" /><h2 className="font-display font-bold text-xl mt-4">Paiement protégé</h2><p className="text-sm text-[--cvln-ink-2] mt-2">Aucun historique ni moyen de paiement n’est exposé dans cette vue publique.</p></div>
        </div>
        <div className="mt-8 flex flex-wrap gap-3">
          <Link to="/register" className="btn-primary">Créer mon Wallet Academy</Link>
          <Link to="/badges" className="btn-outline">Découvrir les badges</Link>
        </div>
      </div>
    );
  }

  const account = summary?.account;

  return (
    <div className="px-6 md:px-12 py-10 max-w-5xl" data-testid="wallet-page">
      <div className="text-xs uppercase tracking-[0.25em] font-bold text-[--cvln-orange]">CVLN Academy · Mini-wallet</div>
      <h1 className="font-display font-black text-4xl tracking-tighter mt-2">{t("wallet_p.title")}</h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 md:gap-6 mt-8">
        <div className="cvln-card p-6" data-testid="wallet-jcc">
          <div className="flex items-center justify-between"><div className="text-xs uppercase tracking-[0.2em] font-bold text-[--cvln-ink-2]">JCC</div><Coins width={18} height={18} className="text-[--cvln-orange]" /></div>
          <div className="mt-2 font-display font-black text-5xl tracking-tighter">{account?.jcc_balance ?? 0}</div>
        </div>
        <div className="cvln-card p-6" data-testid="wallet-tokens"><div className="text-xs uppercase tracking-[0.2em] font-bold text-[--cvln-ink-2]">Tokens</div><div className="mt-2 font-display font-black text-5xl tracking-tighter">{account?.token_balance ?? 0}</div></div>
        <div className="cvln-card p-6" data-testid="wallet-badges">
          <div className="flex items-center justify-between"><div className="text-xs uppercase tracking-[0.2em] font-bold text-[--cvln-ink-2]">{t("wallet_p.badges_linked")}</div><Medal1st width={18} height={18} className="text-[--cvln-orange]" /></div>
          <div className="mt-2 font-display font-black text-5xl tracking-tighter">{account?.badges?.length ?? 0}</div>
        </div>
      </div>

      <div className="flex flex-wrap gap-3 mt-6">
        <button className="btn-outline" data-testid="apple-wallet-btn" onClick={() => openPass("apple")}><AppleWallet width={16} height={16} className="mr-2" /> Apple Wallet</button>
        <button className="btn-outline" data-testid="google-wallet-btn" onClick={() => openPass("google")}><CardWallet width={16} height={16} className="mr-2" /> Google Wallet</button>
      </div>

      <div className="cvln-card p-6 mt-8" data-testid="wallet-history">
        <h3 className="font-display font-bold text-xl tracking-tight mb-4">{t("wallet_p.history")}</h3>
        {(!summary?.recent_transactions || summary.recent_transactions.length === 0) ? (
          <div className="text-sm text-[--cvln-ink-2]">{t("wallet_p.no_transactions")}</div>
        ) : (
          <div className="space-y-2">
            {summary.recent_transactions.map((tx) => (
              <div key={tx.id} className="flex items-center justify-between px-4 py-3 rounded-xl border border-black/5" data-testid={`wallet-txn-${tx.id}`}>
                <div><div className="text-sm font-semibold">{TXN_LABELS[tx.type] || tx.type}</div><div className="text-xs text-[--cvln-ink-2]">{tx.description}</div></div>
                <div className="text-sm font-bold text-[--cvln-orange] whitespace-nowrap">{tx.amount >= 0 ? "+" : ""}{tx.amount} {tx.currency.toUpperCase()}</div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
