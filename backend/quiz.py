"""Quiz generator + evaluator.

Uses the "template" from the CVLN Master OS (Bloc 4, quiz bank):
each module always evaluates:
 1. Objectif principal (QCM)
 2. Hook / cas concret (QCM)
 3. Livrable archivé dans FREK (VRAI/FAUX)
 4. Seuil minimum (80%)
 5. Signal FREK émis (QCM)
 6. Langue du livrable (APPLICATION)
 7. Stade attendu (REFLEXION)
 8. Intégration écosystème (INTEGRATION)
"""
from __future__ import annotations

from typing import List, Dict


def build_quiz(module: Dict) -> List[Dict]:
    """Return 8 standardized questions for any module."""
    stade = module.get("stade", "graine")
    stade_label = {
        "graine": "🌱 Graine", "pousse": "🌿 Pousse", "racine": "🌳 Racine",
        "branches": "🌲 Branches", "arbre": "🦅 Arbre", "foret": "🌳🌳 Forêt",
    }[stade]
    deliverable = module.get("deliverable", "livrable prévu")
    hook = module.get("hook", "cas caribéen concret")
    signal = module.get("frek_signal", "FREK-WORK").split(" ")[0]
    name = module["name"]

    return [
        {
            "n": 1, "type": "QCM",
            "question": f"Quel est l'objectif principal du module « {name} » ?",
            "choices": [
                {"id": "A", "text": f"Produire le livrable : {deliverable}", "correct": True},
                {"id": "B", "text": "Regarder une démonstration sans participer", "correct": False},
                {"id": "C", "text": "Obtenir le badge sans validation", "correct": False},
                {"id": "D", "text": "Accumuler des heures sans livrable", "correct": False},
            ],
        },
        {
            "n": 2, "type": "QCM",
            "question": f"Dans le hook « {hook} », quel est le problème mis en scène ?",
            "choices": [
                {"id": "A", "text": "Une situation caribéenne réelle qui illustre l'enjeu", "correct": True},
                {"id": "B", "text": "Une situation fictive inventée pour l'exercice", "correct": False},
                {"id": "C", "text": "Un exemple de succès sans contexte", "correct": False},
                {"id": "D", "text": "Une anecdote sans lien", "correct": False},
            ],
        },
        {
            "n": 3, "type": "VRAI_FAUX",
            "question": f"Le livrable « {deliverable} » est archivé automatiquement dans FREK.",
            "choices": [
                {"id": "VRAI", "text": f"Vrai — chaque livrable génère un signal {signal}", "correct": True},
                {"id": "FAUX", "text": "Faux — le livrable est optionnel", "correct": False},
            ],
        },
        {
            "n": 4, "type": "QCM",
            "question": "Pour valider ce module, quel est le seuil minimum requis ?",
            "choices": [
                {"id": "A", "text": "60%", "correct": False},
                {"id": "B", "text": "70%", "correct": False},
                {"id": "C", "text": "80% — seuil standard CVLN Academy", "correct": True},
                {"id": "D", "text": "100%", "correct": False},
            ],
        },
        {
            "n": 5, "type": "QCM",
            "question": "Quel signal FREK est généré en priorité lors de ce module ?",
            "choices": [
                {"id": "A", "text": f"{signal} — généré à la remise du livrable", "correct": True},
                {"id": "B", "text": "FREK-TIME uniquement — les vidéos regardées", "correct": False},
                {"id": "C", "text": "Aucun signal — FREK est optionnel", "correct": False},
                {"id": "D", "text": "FREK-CERT dès la connexion", "correct": False},
            ],
        },
        {
            "n": 6, "type": "APPLICATION",
            "question": f"Dans quelle langue le livrable « {deliverable} » doit-il être produit ?",
            "choices": [
                {"id": "A", "text": "Français uniquement", "correct": False},
                {"id": "B", "text": "Anglais uniquement", "correct": False},
                {"id": "C", "text": "Français, English ou Kreyòl selon le contexte", "correct": True},
                {"id": "D", "text": "Aucune langue imposée", "correct": False},
            ],
        },
        {
            "n": 7, "type": "REFLEXION",
            "question": f"Ce module appartient au stade « {stade_label} ». Qu'est-ce que cela implique ?",
            "choices": [
                {"id": "A", "text": f"Le stade détermine la complexité et l'autonomie — {stade_label}", "correct": True},
                {"id": "B", "text": "Le stade est indicatif et peut être ignoré", "correct": False},
                {"id": "C", "text": "Tous les stades ont la même difficulté", "correct": False},
                {"id": "D", "text": "Le stade ne concerne que les formateurs", "correct": False},
            ],
        },
        {
            "n": 8, "type": "INTEGRATION",
            "question": "Après avoir produit le livrable, quelle est la prochaine étape dans CVLN ?",
            "choices": [
                {"id": "A", "text": "Archivé dans FREK, génère des CC et alimente le FREK-ID", "correct": True},
                {"id": "B", "text": "Gardé localement sans intégration", "correct": False},
                {"id": "C", "text": "Envoyé par email uniquement", "correct": False},
                {"id": "D", "text": "Aucune intégration — la formation est indépendante", "correct": False},
            ],
        },
    ]


def evaluate(quiz: List[Dict], answers: Dict[str, str]) -> Dict:
    correct = 0
    total = len(quiz)
    for q in quiz:
        picked = answers.get(str(q["n"]))
        for c in q["choices"]:
            if c["id"] == picked and c["correct"]:
                correct += 1
                break
    score = correct / total if total else 0.0
    return {"correct": correct, "total": total, "score": round(score, 3), "passed": score >= 0.8}
