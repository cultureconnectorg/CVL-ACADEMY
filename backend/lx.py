"""CVLN Academy Learning Experience v2.

Transforms each raw module into a 7-phase learning journey and provides
unlock rules for sequential progression.

Phases:
  1. hook          — narrative to spark motivation
  2. objectives    — clear learning outcomes
  3. course        — main content (video placeholder + long-form text)
  4. workshop      — guided step-by-step exercise
  5. deliverable   — user submits written proof of work
  6. quiz          — validation quiz (existing 8-Q template)
  7. mini_mission  — real-world commitment attached to the module

A module is `validated` only when ALL phases are completed:
  - hook_viewed_at set
  - objectives_viewed_at set
  - course_progress_pct >= 80
  - workshop_viewed_at set
  - deliverable_submitted_at set (text >= 250 chars)
  - quiz_passed = True (score >= 0.8)
  - mini_mission_committed_at set
"""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple

STADE_LABEL = {
    "graine": "🌱 Graine",
    "pousse": "🌿 Pousse",
    "racine": "🌳 Racine",
    "branches": "🌲 Branches",
    "arbre": "🦅 Arbre",
    "foret": "🌳🌳 Forêt",
}

DELIVERABLE_MIN_CHARS = 250

# Signals that get emitted when a module reaches full validation. FREK-WORK is
# always emitted; the module's specific signal (WORK / SCORE / LINK / CERT /
# CONTRIB) is emitted in addition.


def _course_content_md(mod: Dict) -> str:
    """Auto-generated long-form course content in Markdown.

    Real videos/PDFs will be produced by CVLN Academy Studio and injected
    via /api/modules/{fc}/{mc}/content (P1 hook — see routes).
    """
    name = mod["name"]
    hook = mod.get("hook", "")
    deliverable = mod.get("deliverable", "")
    stade = mod.get("stade", "graine")
    stade_label = STADE_LABEL.get(stade, stade)

    return f"""## 1. Le contexte caribéen

Nous démarrons par le cas concret : **{hook}**. Ce n'est pas un exemple pédagogique
inventé : c'est une réalité que tu vas croiser dans ton parcours CVLN. Ancre-toi
dans ce contexte avant d'aborder la théorie.

## 2. La théorie appliquée

Ce module ({stade_label}) t'apprend à maîtriser : **{name}**. Trois piliers :

- **Le fondement** — pourquoi ce sujet est central dans l'écosystème CVLN
- **La méthode** — les gestes précis à reproduire
- **Les pièges** — ce que la doctrine CVLN évite explicitement

## 3. Démonstration

Un intervenant CVLN te montre pas-à-pas comment produire : **{deliverable}**.
La vidéo (production CVLN Academy Studio, à venir) sera injectée ici via le
gestionnaire de contenu.

En attendant la vidéo, lis attentivement ces 5 points-clés :

1. Comprends l'intention avant l'exécution
2. Repère les 2-3 éléments non-négociables du livrable
3. Note tes questions au fur et à mesure
4. Prends 15 minutes de recul avant de te lancer
5. Prépare ton environnement de production (fichier, outils, références)

## 4. Récap et transition

Une fois cette lecture terminée, passe à l'**atelier guidé** — c'est là que tu
transformes la théorie en compétence. Prends ton temps : c'est la partie qui te
donne le savoir-faire réel."""


def _workshop_steps(mod: Dict) -> List[Dict]:
    deliverable = mod.get("deliverable", "livrable prévu")
    return [
        {
            "n": 1,
            "action": "Préparer ton espace de travail",
            "detail": (
                "5 min — ferme les distractions, ouvre un doc vierge, "
                "note la date et le code du module en en-tête."
            ),
        },
        {
            "n": 2,
            "action": "Reformuler l'objectif du livrable dans tes mots",
            "detail": f"10 min — écris en 3 lignes ce que « {deliverable} » signifie POUR TOI, dans ton contexte.",
        },
        {
            "n": 3,
            "action": "Structurer le squelette",
            "detail": "15 min — pose 3 à 5 sections claires, sans encore rédiger le contenu détaillé.",
        },
        {
            "n": 4,
            "action": "Produire une première version brute",
            "detail": "30-60 min — remplis chaque section sans t'auto-censurer. C'est ton V0.",
        },
        {
            "n": 5,
            "action": "Prendre du recul et itérer",
            "detail": (
                "15 min — relis à voix haute, corrige uniquement ce qui te choque, "
                "garde les imperfections mineures."
            ),
        },
    ]


def _deliverable_spec(mod: Dict) -> str:
    deliverable = mod.get("deliverable", "livrable prévu")
    signal = mod.get("frek_signal", "FREK-WORK").split(" ")[0]
    return (
        f"Rends ici ton livrable : **{deliverable}**.\n\n"
        f"Format attendu : texte structuré (min. {DELIVERABLE_MIN_CHARS} caractères) "
        "avec au minimum : intention, méthode utilisée, résultat produit, et 3 apprentissages "
        f"personnels. Ton dépôt sera archivé dans FREK et générera un signal {signal}."
    )


def _mini_mission(mod: Dict) -> str:
    name = mod["name"]
    return (
        f"Dans les 7 prochains jours, applique « {name} » sur un cas réel de ton entourage "
        "(un artiste, un événement, un projet culturel de ton territoire). "
        "Écris en 3 lignes ce que tu as fait et ce qui a changé — c'est ton passage "
        "de la théorie au terrain."
    )


def enrich_module(mod: Dict) -> Dict:
    """Return the raw module doc augmented with the LX v2 phase definitions."""
    return {
        **mod,
        "phases": {
            "hook": {
                "title": "Le déclencheur",
                "narrative": (
                    f"**{mod.get('hook', '')}**\n\n"
                    "Ce module s'ouvre sur un cas caribéen concret. Prends 5 minutes "
                    "pour t'imprégner du contexte. Note ta première réaction — c'est "
                    "cette énergie qui va guider tout ton apprentissage."
                ),
            },
            "objectives": {
                "title": "Ce que tu sauras faire à la fin",
                "items": [
                    f"Comprendre en profondeur : {mod['name']}",
                    f"Maîtriser les gestes clés du stade {STADE_LABEL.get(mod.get('stade','graine'), 'graine')}",
                    f"Produire de façon autonome : {mod.get('deliverable', '')}",
                    f"Émettre un signal {mod.get('frek_signal', 'FREK-WORK').split(' ')[0]} archivé dans ton FREK-ID",
                ],
            },
            "course": {
                "title": "Le cours — théorie & démonstration",
                "video_placeholder": {
                    "note": "Vidéo produite par CVLN Academy Studio (à venir).",
                    "duration_min": max(8, int(mod.get("duration_h", 4)) * 4),
                },
                "reading_min": max(10, int(mod.get("duration_h", 4)) * 3),
                "content_md": _course_content_md(mod),
            },
            "workshop": {
                "title": "L'atelier guidé",
                "estimated_min": max(45, int(mod.get("duration_h", 4)) * 15),
                "steps": _workshop_steps(mod),
            },
            "deliverable": {
                "title": "Ton livrable",
                "spec_md": _deliverable_spec(mod),
                "expected": mod.get("deliverable", ""),
                "min_chars": DELIVERABLE_MIN_CHARS,
            },
            "quiz": {
                "title": "Quiz de validation",
                "passing_score": 0.8,
                "questions_count": 8,
                "attempts_allowed": "illimité (mais chaque tentative < 80% te renvoie au cours)",
            },
            "mini_mission": {
                "title": "Mini-mission terrain",
                "brief": _mini_mission(mod),
            },
        },
    }


# ---------------- PROGRESS / STATUS ----------------

EMPTY_PROGRESS = {
    "hook_viewed_at": None,
    "objectives_viewed_at": None,
    "course_progress_pct": 0,
    "workshop_viewed_at": None,
    "deliverable_text": None,
    "deliverable_submitted_at": None,
    "quiz_passed": False,
    "quiz_score": 0.0,
    "quiz_attempts": 0,
    "mini_mission_committed_at": None,
}


def prereqs_before_quiz_ready(progress: Dict) -> Tuple[bool, List[str]]:
    """Returns (ready, list_of_missing_phase_keys) — quiz can only be taken
    when hook + objectives + course(>=80) + workshop + deliverable are done."""
    missing: List[str] = []
    if not progress.get("hook_viewed_at"):
        missing.append("hook")
    if not progress.get("objectives_viewed_at"):
        missing.append("objectives")
    if int(progress.get("course_progress_pct", 0)) < 80:
        missing.append("course")
    if not progress.get("workshop_viewed_at"):
        missing.append("workshop")
    if not progress.get("deliverable_submitted_at"):
        missing.append("deliverable")
    return (not missing, missing)


def compute_status(progress: Optional[Dict]) -> str:
    """Derive module status from the progress doc (or from None if never touched)."""
    if not progress:
        return "available"
    if progress.get("quiz_passed") and progress.get("mini_mission_committed_at"):
        return "validated"
    if progress.get("quiz_passed"):
        return "awaiting_mini_mission"
    ready, _ = prereqs_before_quiz_ready(progress)
    if ready:
        return "ready_for_quiz"
    # Any activity started?
    if (
        progress.get("hook_viewed_at")
        or progress.get("objectives_viewed_at")
        or int(progress.get("course_progress_pct", 0)) > 0
    ):
        return "in_progress"
    return "available"


def phase_completion_flags(progress: Optional[Dict]) -> Dict[str, bool]:
    p = progress or {}
    return {
        "hook": bool(p.get("hook_viewed_at")),
        "objectives": bool(p.get("objectives_viewed_at")),
        "course": int(p.get("course_progress_pct", 0)) >= 80,
        "workshop": bool(p.get("workshop_viewed_at")),
        "deliverable": bool(p.get("deliverable_submitted_at")),
        "quiz": bool(p.get("quiz_passed")),
        "mini_mission": bool(p.get("mini_mission_committed_at")),
    }


# ---------------- UNLOCK RULES ----------------


def is_module_unlocked(
    formation_doc: Dict, module_code: str, user_progress_by_module: Dict[str, Dict]
) -> bool:
    """A module is unlocked if it's the first one OR the previous one is validated."""
    modules = formation_doc.get("modules", [])
    codes = [m["code"] for m in modules]
    if module_code not in codes:
        return False
    idx = codes.index(module_code)
    if idx == 0:
        return True
    prev_code = codes[idx - 1]
    prev_progress = user_progress_by_module.get(prev_code)
    return compute_status(prev_progress) == "validated"


def is_formation_unlocked(
    user_metier_vise: Optional[str],
    formation_doc: Dict,
    all_pole_formations: List[Dict],
    user_progress_by_module: Dict[str, Dict],
) -> Tuple[bool, str]:
    """A formation is unlocked if:
      - it belongs to the user's chosen pole (metier_vise), sequentially: first
        of the pole is open; next ones open when the prior one is >=50% validated.
      - OR the user has fully validated their first pole formation (unlocks
        cross-pole exploration).

    Returns (unlocked, reason_locked_message).
    """
    pole = formation_doc.get("pole")
    if not user_metier_vise:
        return (True, "")  # no onboarding yet — leave everything open

    # Sequence within same pole
    sorted_pole = sorted(
        [f for f in all_pole_formations if f["pole"] == pole],
        key=lambda x: x["code"],
    )
    pole_codes = [f["code"] for f in sorted_pole]
    if formation_doc["code"] not in pole_codes:
        return (True, "")

    idx = pole_codes.index(formation_doc["code"])
    if pole == user_metier_vise:
        if idx == 0:
            return (True, "")
        prev = sorted_pole[idx - 1]
        prev_mods = [m["code"] for m in prev.get("modules", [])]
        if not prev_mods:
            return (True, "")
        validated = sum(
            1
            for c in prev_mods
            if compute_status(user_progress_by_module.get(c)) == "validated"
        )
        pct = validated / len(prev_mods)
        if pct >= 0.5:
            return (True, "")
        return (
            False,
            f"Débloquée quand tu auras validé 50% de {prev['code']} "
            f"({validated}/{len(prev_mods)} modules à ce jour).",
        )
    else:
        # Other poles — first formation of each other pole unlocks when the
        # user has fully validated one of their own pole's formations.
        # Check any formation of their own pole is fully validated:
        own_pole = [f for f in all_pole_formations if f["pole"] == user_metier_vise]
        has_any_full = False
        for f in own_pole:
            mods = [m["code"] for m in f.get("modules", [])]
            if not mods:
                continue
            if all(
                compute_status(user_progress_by_module.get(c)) == "validated"
                for c in mods
            ):
                has_any_full = True
                break
        if idx == 0 and has_any_full:
            return (True, "")
        if idx == 0:
            return (
                False,
                f"Termine 1 formation de ton pôle {user_metier_vise} pour "
                "débloquer les autres pôles.",
            )
        # Non-first of other pole: needs the previous one in same pole
        prev_code = pole_codes[idx - 1]
        return (False, f"Débloquée après {prev_code}.")
