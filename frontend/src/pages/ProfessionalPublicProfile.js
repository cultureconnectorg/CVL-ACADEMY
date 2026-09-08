import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { api } from "@/lib/api";
import { useI18n } from "@/lib/i18n.jsx";

/** ACA-0028 — the public, unauthenticated identity surface: what
 * `GET /api/professional/public/{frek_id}` returns when (and only
 * when) that learner has explicitly opted in (see
 * `services/professional_profile.py`'s own docstring for the
 * off-by-default privacy contract). A 404 here — unknown FREK-ID or
 * a real one that just isn't public — renders the same honest
 * "not available" state either way, never distinguishing the two. */
export default function ProfessionalPublicProfile() {
  const { frekId } = useParams();
  const { t } = useI18n();
  const [profile, setProfile] = useState(undefined); // undefined = loading
  const [notFound, setNotFound] = useState(false);

  useEffect(() => {
    setProfile(undefined);
    setNotFound(false);
    api
      .get(`/professional/public/${frekId}`)
      .then((r) => setProfile(r.data))
      .catch(() => setNotFound(true));
  }, [frekId]);

  if (notFound) {
    return (
      <div className="px-6 md:px-12 py-16 max-w-3xl text-center" data-testid="professional-public-not-found">
        <div className="font-display font-black text-3xl tracking-tighter">
          {t("professional_profile_p.not_found_title")}
        </div>
        <p className="text-[--cvln-ink-2] mt-3">{t("professional_profile_p.not_found_body")}</p>
        <Link to="/" className="mt-6 inline-block text-[--cvln-orange] font-semibold">
          {t("professional_profile_p.back_home")}
        </Link>
      </div>
    );
  }

  if (!profile) {
    return <div className="px-6 md:px-12 py-16" data-testid="professional-public-loading" />;
  }

  return (
    <div className="px-6 md:px-12 py-10 max-w-4xl" data-testid="professional-public-profile">
      <div className="text-xs uppercase tracking-[0.25em] font-bold text-[--cvln-orange]">
        {t("professional_profile_p.eyebrow")}
      </div>
      <h1 className="font-display font-black text-4xl md:text-5xl tracking-tighter leading-none mt-2">
        {profile.display_name}
      </h1>
      <div className="mono text-lg text-[--cvln-ink-2] mt-1">{profile.frek_id}</div>

      <div className="mt-8 cvln-card p-6">
        <h3 className="font-display font-bold text-xl tracking-tight mb-4">
          {t("professional_profile_p.skills_title")}
        </h3>
        {profile.acquired_skills.length === 0 ? (
          <div className="text-sm text-[--cvln-ink-2]">{t("professional_profile_p.no_skills")}</div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {profile.acquired_skills.map((s) => (
              <div key={s.skill_id} className="p-3 rounded-xl border border-black/10" data-testid={`public-skill-${s.skill_id}`}>
                <div className="mono text-xs text-[--cvln-orange] font-bold">{s.skill_id}</div>
                <div className="text-sm font-semibold">{s.label}</div>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="mt-6 cvln-card p-6">
        <h3 className="font-display font-bold text-xl tracking-tight mb-4">
          {t("professional_profile_p.certs_title")}
        </h3>
        {profile.certifications.length === 0 ? (
          <div className="text-sm text-[--cvln-ink-2]">{t("professional_profile_p.no_certs")}</div>
        ) : (
          <div className="space-y-2">
            {profile.certifications.map((c) => (
              <div
                key={c.certification_code}
                className="flex items-center justify-between p-3 rounded-xl border border-black/10"
                data-testid={`public-cert-${c.certification_code}`}
              >
                <span className="mono font-bold">{c.certification_code}</span>
                <span className="text-sm text-[--cvln-ink-2]">{c.mention}</span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
