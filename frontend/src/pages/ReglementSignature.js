import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { CheckCircle, Erase, PenTablet, ShieldCheck } from "iconoir-react";
import { api } from "@/lib/api";
import { useAuth } from "@/lib/auth.jsx";
import { toast } from "sonner";

const VERSION = "2.0-2026-09";
const CONTENT_HASH = "cvln-academy-reglement-v2-2026-09";

const SECTIONS = [
  ["1. Objet et principes", "Le règlement fixe les règles de santé, sécurité, discipline, intégrité, création, numérique et professionnalisation applicables au parcours CVLN Academy."],
  ["2. Champ d’application", "Il s’applique en présentiel, à distance, en studio, en régie, sur plateau, chez un partenaire et dans les environnements numériques de formation."],
  ["3. Admission et dossier", "Les informations et pièces fournies doivent être exactes. Les prérequis, objectifs, modalités et critères d’évaluation sont communiqués pour chaque formation."],
  ["4. Assiduité et ponctualité", "Présence, émargement, horaires, retards, absences, décrochage et abandon doivent refléter la réalité du parcours et respecter les règles du financeur lorsqu’il y en a un."],
  ["5. Évaluations et intégrité", "Fraude, substitution de personne, plagiat, fabrication de preuves ou appropriation du travail d’autrui sont interdits."],
  ["6. Intelligence artificielle", "L’IA peut assister le travail lorsqu’elle est autorisée. L’apprenant reste responsable du résultat et ne doit pas l’utiliser pour falsifier, usurper, contourner une évaluation ou divulguer des informations confidentielles."],
  ["7. Studio audio et musique", "L’accès au studio se fait uniquement dans les créneaux autorisés. Sessions, stems, masters, presets et exports doivent être organisés et sauvegardés selon les consignes."],
  ["8. Audiovisuel et tournage", "Les consignes de plateau, d’électricité, d’éclairage, de circulation et de sécurité doivent être respectées. Les rushes et contenus non publiés restent confidentiels lorsqu’ils le sont."],
  ["9. Matériel", "Le matériel ne peut être déplacé, prêté, démonté, reconfiguré ou sorti sans autorisation. Toute perte, casse ou anomalie doit être signalée immédiatement."],
  ["10. Numérique et cybersécurité", "Les comptes sont personnels. Les accès non autorisés, le partage d’identifiants, l’extraction abusive de données et l’exposition de secrets techniques sont interdits."],
  ["11. Propriété intellectuelle", "La participation à CVLN Academy n’emporte pas cession automatique des droits de l’apprenant. Les contributions, crédits et splits doivent être clarifiés lorsque nécessaire."],
  ["12. Image, voix et captation", "Une captation pédagogique et une exploitation promotionnelle sont deux finalités distinctes et sont encadrées séparément lorsque nécessaire."],
  ["13. Données personnelles", "Les données d’inscription, d’assiduité, d’évaluation et de financement sont accessibles uniquement aux personnes et partenaires habilités."],
  ["14. Comportement, harcèlement et VSS", "Violence, menace, harcèlement, discrimination, intimidation et représailles sont interdits. Le contexte artistique ne supprime jamais l’exigence de consentement."],
  ["15. Santé, sécurité et urgences", "Les consignes d’évacuation, incendie, premiers secours et sécurité des sites doivent être respectées. Tout accident ou presque-accident doit être signalé."],
  ["16. Accessibilité", "Les besoins d’aménagement peuvent être signalés afin d’étudier des adaptations raisonnables compatibles avec les objectifs de la formation."],
  ["17. Intervenants, invités et partenaires", "Aucun invité ou prestataire n’accède à un espace contrôlé sans autorisation. Les projets clients doivent clarifier rôles, livrables, droits et confidentialité."],
  ["18. Réclamations", "Toute difficulté administrative, pédagogique, technique, relationnelle ou de sécurité peut faire l’objet d’une réclamation formelle et traçable."],
  ["19. Discipline", "Toute mesure disciplinaire doit être proportionnée et respecter les garanties prévues par le droit applicable. Les sanctions pécuniaires disciplinaires sont interdites."],
  ["20. Représentation", "Lorsque les dispositions légales sont applicables, l’organisme met en place la représentation des stagiaires ou apprentis selon les règles en vigueur."],
  ["21. Financeurs et preuves", "Les preuves de présence et de réalisation doivent être authentiques, datées et rattachables au parcours. Les obligations du financeur s’ajoutent au parcours lorsqu’elles sont applicables."],
  ["22. Version et entrée en vigueur", "Chaque version est identifiée et datée. Une évolution substantielle peut entraîner une nouvelle demande d’acceptation."],
];

export default function ReglementSignature() {
  const { user } = useAuth();
  const nav = useNavigate();
  const canvasRef = useRef(null);
  const drawingRef = useRef(false);
  const lastPointRef = useRef(null);
  const [accepted, setAccepted] = useState(false);
  const [hasSignature, setHasSignature] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [checking, setChecking] = useState(true);

  useEffect(() => {
    api.get("/reglement/status")
      .then(({ data }) => {
        if (data.signed) nav(user?.onboarding_completed ? "/dashboard" : "/onboarding", { replace: true });
      })
      .finally(() => setChecking(false));
  }, [nav, user?.onboarding_completed]);

  const pointFromEvent = (event) => {
    const canvas = canvasRef.current;
    const rect = canvas.getBoundingClientRect();
    return {
      x: ((event.clientX - rect.left) / rect.width) * canvas.width,
      y: ((event.clientY - rect.top) / rect.height) * canvas.height,
    };
  };

  const begin = (event) => {
    event.preventDefault();
    drawingRef.current = true;
    lastPointRef.current = pointFromEvent(event);
    event.currentTarget.setPointerCapture?.(event.pointerId);
  };

  const draw = (event) => {
    if (!drawingRef.current) return;
    event.preventDefault();
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");
    const next = pointFromEvent(event);
    const last = lastPointRef.current || next;
    ctx.lineWidth = 4;
    ctx.lineCap = "round";
    ctx.lineJoin = "round";
    ctx.strokeStyle = "#111111";
    ctx.beginPath();
    ctx.moveTo(last.x, last.y);
    ctx.lineTo(next.x, next.y);
    ctx.stroke();
    lastPointRef.current = next;
    setHasSignature(true);
  };

  const end = (event) => {
    drawingRef.current = false;
    lastPointRef.current = null;
    event.currentTarget.releasePointerCapture?.(event.pointerId);
  };

  const clearSignature = () => {
    const canvas = canvasRef.current;
    canvas.getContext("2d").clearRect(0, 0, canvas.width, canvas.height);
    setHasSignature(false);
  };

  const submit = async () => {
    if (!accepted || !hasSignature) return;
    setSubmitting(true);
    try {
      const signaturePng = canvasRef.current.toDataURL("image/png");
      await api.post("/reglement/sign", {
        accepted: true,
        signer_name: user.display_name,
        signature_png: signaturePng,
        version: VERSION,
        content_hash: CONTENT_HASH,
      });
      toast.success("Règlement signé. Ton parcours peut commencer.");
      nav(user.onboarding_completed ? "/dashboard" : "/onboarding", { replace: true });
    } catch (error) {
      toast.error(error?.response?.data?.detail || "Impossible d’enregistrer la signature");
    } finally {
      setSubmitting(false);
    }
  };

  if (checking) return null;

  return (
    <div className="min-h-screen bg-white noise" data-testid="reglement-signature-page">
      <header className="border-b border-black/5 px-6 md:px-16 py-6 flex items-center justify-between gap-4">
        <div>
          <div className="text-xs mono uppercase tracking-[0.25em] font-bold text-[--cvln-orange]">CVLN Academy</div>
          <div className="font-display font-black text-xl mt-1">Avant de commencer ton parcours</div>
        </div>
        <div className="text-xs mono text-[--cvln-ink-2]">Règlement V2.0</div>
      </header>

      <main className="max-w-5xl mx-auto px-6 py-10 md:py-14">
        <div className="grid lg:grid-cols-[1.25fr_.75fr] gap-8 items-start">
          <section>
            <div className="text-xs uppercase tracking-[0.25em] font-bold text-[--cvln-orange]">Lecture</div>
            <h1 className="font-display font-black text-4xl md:text-5xl tracking-tighter mt-2">Règlement intérieur & Student Handbook</h1>
            <p className="text-[--cvln-ink-2] mt-4 max-w-2xl">Lis les règles essentielles. Elles encadrent ton parcours, tes créations, l’usage des studios, du matériel, des outils numériques et la vie collective.</p>

            <div className="mt-8 max-h-[58vh] overflow-y-auto rounded-3xl border border-black/10 bg-white p-5 md:p-7 space-y-6" data-testid="reglement-scroll">
              {SECTIONS.map(([title, body]) => (
                <article key={title}>
                  <h2 className="font-display font-bold text-lg">{title}</h2>
                  <p className="text-sm leading-6 text-[--cvln-ink-2] mt-1">{body}</p>
                </article>
              ))}
              <div className="rounded-2xl bg-[#FFF3EC] p-4 text-sm leading-6">
                <strong>Important :</strong> le règlement ne remplace pas les contrats, conventions, autorisations image/voix, politique de confidentialité ou chartes techniques applicables à une formation précise.
              </div>
            </div>
          </section>

          <aside className="lg:sticky lg:top-6 cvln-card p-6 md:p-7">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-[#FFF3EC] flex items-center justify-center text-[--cvln-orange]"><ShieldCheck /></div>
              <div>
                <div className="font-display font-bold text-xl">Signature obligatoire</div>
                <div className="text-xs text-[--cvln-ink-2]">{user.display_name} · {user.frek_id}</div>
              </div>
            </div>

            <label className="mt-6 flex items-start gap-3 cursor-pointer">
              <input
                data-testid="reglement-accept"
                type="checkbox"
                checked={accepted}
                onChange={(e) => setAccepted(e.target.checked)}
                className="mt-1 h-5 w-5 accent-[--cvln-orange]"
              />
              <span className="text-sm leading-6">J’ai lu le règlement intérieur CVLN Academy V2.0 et je m’engage à le respecter pendant mon parcours.</span>
            </label>

            <div className="mt-6">
              <div className="flex items-center justify-between gap-3 mb-2">
                <div className="text-xs mono uppercase tracking-wider font-bold">Signe avec ton doigt ou ta souris</div>
                <button type="button" onClick={clearSignature} className="text-xs flex items-center gap-1 text-[--cvln-ink-2] hover:text-[--cvln-ink]">
                  <Erase width={14} height={14} /> Effacer
                </button>
              </div>
              <canvas
                ref={canvasRef}
                width={900}
                height={240}
                data-testid="reglement-signature-pad"
                onPointerDown={begin}
                onPointerMove={draw}
                onPointerUp={end}
                onPointerCancel={end}
                onPointerLeave={(e) => drawingRef.current && end(e)}
                className="w-full h-44 rounded-2xl border-2 border-dashed border-black/15 bg-[#FAFAF8] cursor-crosshair"
                style={{ touchAction: "none" }}
                aria-label="Zone de signature manuscrite"
              />
              <div className="mt-2 text-xs text-[--cvln-ink-2] flex items-center gap-1"><PenTablet width={14} height={14} /> Signature manuscrite numérique enregistrée avec la version du règlement.</div>
            </div>

            <button
              type="button"
              data-testid="reglement-sign-submit"
              onClick={submit}
              disabled={!accepted || !hasSignature || submitting}
              className="btn-primary w-full mt-6 disabled:opacity-40 disabled:cursor-not-allowed"
            >
              {submitting ? "Enregistrement…" : "Signer et commencer"}
              <CheckCircle width={18} height={18} className="ml-2" />
            </button>

            <p className="mt-4 text-[11px] leading-5 text-[--cvln-ink-2]">La validation enregistre ton identité de compte, la version du règlement, la date, la signature et une empreinte technique de la signature pour conserver une preuve cohérente.</p>
          </aside>
        </div>
      </main>
    </div>
  );
}
