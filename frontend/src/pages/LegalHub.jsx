import { Link, useParams } from "react-router-dom";

const UPDATED = "11 septembre 2026";

const docs = {
  "mentions-legales": {
    title: "Mentions légales",
    body: (
      <>
        <p>CVLN Academy est un service de formation de l’écosystème CVLN. Les informations d’identification complètes de l’entité juridique exploitante, son adresse, son immatriculation, son directeur de publication, son hébergeur et ses coordonnées doivent être renseignées avant ouverture publique du service.</p>
        <p><strong>Important :</strong> tant que ces informations ne sont pas finalisées, cette page ne doit pas être considérée comme une version juridique définitive.</p>
      </>
    ),
  },
  confidentialite: {
    title: "Politique de confidentialité",
    body: (
      <>
        <p>CVLN Academy traite uniquement les données nécessaires à la création du compte, à l’inscription, au suivi pédagogique, à la sécurité, au support, à la facturation et, lorsque c’est applicable, aux obligations administratives liées à la formation.</p>
        <p>Selon le traitement, la base juridique peut être l’exécution d’un contrat, une obligation légale, l’intérêt légitime de sécurité et d’amélioration du service, ou votre consentement. Vous pouvez exercer les droits prévus par le RGPD : accès, rectification, effacement lorsqu’il est applicable, limitation, opposition, portabilité lorsqu’elle est applicable et retrait du consentement.</p>
        <p>Les durées de conservation, catégories de destinataires, sous-traitants, éventuels transferts hors EEE et coordonnées du contact données personnelles doivent être documentés dans la version de production.</p>
        <p>Les données sensibles ne doivent pas être demandées sans nécessité démontrée. Les décisions pédagogiques ou administratives importantes ne doivent pas être déléguées à une IA sans contrôle humain approprié.</p>
      </>
    ),
  },
  cookies: {
    title: "Cookies et traceurs",
    body: (
      <>
        <p>Les traceurs strictement nécessaires au fonctionnement du service peuvent être utilisés sans consentement lorsque la loi le permet. Les traceurs non nécessaires, notamment publicitaires ou certains outils de mesure, ne doivent être activés qu’après votre choix.</p>
        <p>Vous pouvez accepter ou refuser avec le même niveau de facilité et modifier votre choix à tout moment grâce au bouton « Gérer mes cookies » disponible en bas du site.</p>
        <p>CVLN Academy conserve localement une preuve technique de votre préférence de consentement. Les outils tiers effectivement déployés devront être listés ici avec leur finalité et leur durée.</p>
      </>
    ),
  },
  cgu: {
    title: "Conditions générales d’utilisation",
    body: (
      <>
        <p>L’accès à CVLN Academy suppose un usage loyal du service, le respect des droits des autres utilisateurs, de la propriété intellectuelle, des règles de sécurité, des consignes pédagogiques et des règles applicables aux espaces communautaires.</p>
        <p>Sont notamment interdits : l’usurpation d’identité, la fraude, le contournement des contrôles d’accès, l’extraction abusive de données, l’introduction de code malveillant, le harcèlement, la diffusion de contenus illicites et l’utilisation du service pour porter atteinte aux droits d’un tiers.</p>
        <p>Les modalités de suspension, de résiliation, de responsabilité, de propriété intellectuelle et de règlement des différends doivent être adaptées à l’entité contractante et au statut exact des apprenants avant commercialisation.</p>
      </>
    ),
  },
  "charte-ia": {
    title: "Charte IA & transparence",
    body: (
      <>
        <p>CVLN Academy peut utiliser des systèmes d’intelligence artificielle pour assister la recherche, la recommandation, la création de contenus, le support, l’analyse et certaines tâches pédagogiques. Lorsqu’un utilisateur interagit directement avec une IA, cette interaction doit être signalée clairement lorsqu’elle entre dans le champ des obligations de transparence applicables.</p>
        <p>L’IA n’a pas d’autorité autonome pour prendre une décision engageant définitivement l’admission, la certification, une sanction disciplinaire, une décision financière ou un engagement contractuel au nom de CVLN Academy. Un humain responsable conserve l’autorité sur ces décisions.</p>
        <p>Les contenus générés ou substantiellement manipulés par IA sont identifiés lorsque la réglementation l’exige. Les équipes utilisant l’IA pour le compte de CVLN Academy doivent recevoir une information et une formation adaptées à leur rôle.</p>
      </>
    ),
  },
  "reglement-academy": {
    title: "Règlement & accord Academy",
    body: (
      <>
        <p>Ce document encadre la vie de l’Academy : assiduité, sécurité, respect des personnes et des locaux, utilisation des équipements, propriété intellectuelle, confidentialité, usage responsable de l’IA, fraude, évaluations, sanctions, réclamations et règles applicables aux parcours financés.</p>
        <p>Avant le démarrage effectif d’un parcours, l’apprenant doit pouvoir consulter la version applicable du règlement et des documents contractuels, puis exprimer une acceptation traçable. La preuve doit associer au minimum l’identité du compte, la version du document, la date et l’heure, ainsi que l’action explicite d’acceptation.</p>
        <p>Cette page constitue le point d’accès public. La signature/acceptation probante doit être reliée au parcours d’inscription côté serveur.</p>
      </>
    ),
  },
  accessibilite: {
    title: "Accessibilité",
    body: (
      <>
        <p>CVLN Academy vise un accès utilisable au clavier, des contrastes suffisants, des libellés compréhensibles, une structure sémantique correcte et des alternatives textuelles lorsque nécessaires.</p>
        <p>Le niveau réglementaire applicable, la déclaration d’accessibilité et le mécanisme de signalement doivent être finalisés en fonction du statut juridique et du périmètre exact du service.</p>
      </>
    ),
  },
};

export const LEGAL_LINKS = [
  ["mentions-legales", "Mentions légales"],
  ["confidentialite", "Confidentialité"],
  ["cookies", "Cookies"],
  ["cgu", "CGU"],
  ["charte-ia", "Charte IA"],
  ["reglement-academy", "Règlement Academy"],
  ["accessibilite", "Accessibilité"],
];

export default function LegalHub() {
  const { slug = "mentions-legales" } = useParams();
  const doc = docs[slug] || docs["mentions-legales"];

  return (
    <main className="min-h-screen bg-white text-[--cvln-ink] px-6 py-12 md:px-16">
      <div className="mx-auto max-w-4xl">
        <Link to="/" className="text-sm font-semibold text-[--cvln-orange]">← CVLN Academy</Link>
        <p className="mt-10 text-xs uppercase tracking-[0.22em] text-[--cvln-ink-2]">Centre juridique · version mise à jour le {UPDATED}</p>
        <h1 className="mt-3 font-display text-4xl font-black tracking-tight md:text-6xl">{doc.title}</h1>
        <div className="mt-8 space-y-5 text-base leading-7 text-[--cvln-ink-2]">{doc.body}</div>
        <div className="mt-12 border-t border-black/10 pt-8">
          <h2 className="font-display text-xl font-bold">Documents associés</h2>
          <div className="mt-4 flex flex-wrap gap-3">
            {LEGAL_LINKS.map(([key, label]) => (
              <Link key={key} to={`/legal/${key}`} className="rounded-full border border-black/10 px-4 py-2 text-sm hover:border-black/30">{label}</Link>
            ))}
          </div>
        </div>
        <p className="mt-10 rounded-2xl bg-amber-50 p-4 text-sm text-amber-950">Couche de conformité technique. Elle ne remplace pas la validation finale par le conseil juridique de l’entité exploitante, notamment pour l’identité légale, les CGV/contrats de formation, les financeurs, les mineurs et les traitements de données réellement déployés.</p>
      </div>
    </main>
  );
}
