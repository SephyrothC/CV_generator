"""
Module de condensation intelligente pour CV 1 page
"""
from typing import Dict, List, Any


# Règles de condensation pour tenir sur 1 page
CONDENSATION_RULES = {
    "summary": {
        "max_sentences": 2,
        "max_words": 40
    },
    "strength_points": {
        "max_count": 3,
        "max_words_per_point": 12
    },
    "experiences": {
        "max_count": 2,  # 2 expériences principales
        "bullets_per_exp": 4,  # 4 bullets max par expérience
        "bullet_max_words": 15  # 15 mots max par bullet
    },
    "projects": {
        "max_count": 2,  # 2 projets highlights uniquement
        "bullets_per_project": 3,
        "bullet_max_words": 12
    },
    "skills": {
        "max_per_category": 10,
        "max_total_displayed": 8  # Top 8 skills dans la sidebar
    },
    "interests": 5,  # Top 5 centres d'intérêt
    "technologies": {
        "max_per_section": 6  # Max 6 badges tech par section
    },
    "certifications": {
        "max_count": 2  # Maximum 2 certifications
    }
}


def condense_text(text: str, max_words: int) -> str:
    """
    Condense un texte à un nombre maximum de mots

    Args:
        text: Texte à condenser
        max_words: Nombre maximum de mots

    Returns:
        str: Texte condensé
    """
    words = text.split()
    if len(words) <= max_words:
        return text
    return ' '.join(words[:max_words]) + '...'


def condense_summary(summary: str) -> str:
    """
    Condense le résumé professionnel à 2-3 phrases courtes

    Args:
        summary: Résumé original

    Returns:
        str: Résumé condensé
    """
    rules = CONDENSATION_RULES["summary"]

    # Séparer en phrases
    sentences = [s.strip() + '.' for s in summary.split('.') if s.strip()]

    # Garder les premières phrases
    condensed_sentences = sentences[:rules["max_sentences"]]
    condensed = ' '.join(condensed_sentences)

    # Vérifier la longueur totale
    if len(condensed.split()) > rules["max_words"]:
        condensed = condense_text(condensed, rules["max_words"])

    return condensed


def condense_achievements(achievements: List[str], max_count: int, max_words: int) -> List[str]:
    """
    Condense une liste de réalisations

    Args:
        achievements: Liste des réalisations
        max_count: Nombre maximum de réalisations
        max_words: Mots maximum par réalisation

    Returns:
        List[str]: Réalisations condensées
    """
    # Limiter le nombre
    condensed = achievements[:max_count]

    # Condenser chaque réalisation
    condensed = [condense_text(achievement, max_words) for achievement in condensed]

    return condensed


def condense_experiences(experiences: List[Dict], max_count: int = None) -> List[Dict]:
    """
    Condense les expériences professionnelles

    Args:
        experiences: Liste des expériences
        max_count: Nombre maximum d'expériences (par défaut selon RULES)

    Returns:
        List[Dict]: Expériences condensées
    """
    rules = CONDENSATION_RULES["experiences"]
    max_count = max_count or rules["max_count"]

    # Limiter le nombre d'expériences
    condensed_exps = []
    for exp in experiences[:max_count]:
        exp_copy = exp.copy()

        # Condenser les achievements
        exp_copy["achievements"] = condense_achievements(
            exp.get("achievements", []),
            rules["bullets_per_exp"],
            rules["bullet_max_words"]
        )

        # Limiter les technologies
        if "technologies" in exp_copy:
            exp_copy["technologies"] = exp_copy["technologies"][:CONDENSATION_RULES["technologies"]["max_per_section"]]

        condensed_exps.append(exp_copy)

    return condensed_exps


def condense_projects(projects: List[Dict], max_count: int = None) -> List[Dict]:
    """
    Condense les projets en gardant uniquement les highlights

    Args:
        projects: Liste des projets
        max_count: Nombre maximum de projets (par défaut selon RULES)

    Returns:
        List[Dict]: Projets condensés
    """
    rules = CONDENSATION_RULES["projects"]
    max_count = max_count or rules["max_count"]

    # Prioriser les projets avec highlights=True
    highlighted = [p for p in projects if p.get("highlights", False)]
    non_highlighted = [p for p in projects if not p.get("highlights", False)]

    # Prendre d'abord les highlights, puis les autres si besoin
    selected = (highlighted + non_highlighted)[:max_count]

    # Condenser chaque projet
    condensed_projects = []
    for proj in selected:
        proj_copy = proj.copy()

        # Condenser les achievements
        proj_copy["achievements"] = condense_achievements(
            proj.get("achievements", []),
            rules["bullets_per_project"],
            rules["bullet_max_words"]
        )

        # Limiter les technologies
        if "technologies" in proj_copy:
            proj_copy["technologies"] = proj_copy["technologies"][:CONDENSATION_RULES["technologies"]["max_per_section"]]

        # Condenser la description
        if "description" in proj_copy:
            proj_copy["description"] = condense_text(proj_copy["description"], 20)

        condensed_projects.append(proj_copy)

    return condensed_projects


def condense_skills(skills: Dict[str, List], max_per_category: int = None) -> Dict[str, List]:
    """
    Condense les compétences par catégorie

    Args:
        skills: Dict de compétences par catégorie
        max_per_category: Max par catégorie

    Returns:
        Dict: Compétences condensées
    """
    rules = CONDENSATION_RULES["skills"]
    max_per_category = max_per_category or rules["max_per_category"]

    condensed = {}
    for category, skill_list in skills.items():
        condensed[category] = skill_list[:max_per_category]

    return condensed


def get_top_skills(skills: Dict[str, List], count: int = 8) -> List[str]:
    """
    Extrait les top N compétences toutes catégories confondues

    Args:
        skills: Dict de compétences par catégorie
        count: Nombre de compétences à retourner

    Returns:
        List[str]: Top compétences
    """
    all_skills = []

    # Prioriser certaines catégories
    priority_categories = ["frontend", "backend", "devops", "database"]

    # Ajouter d'abord les compétences des catégories prioritaires
    for category in priority_categories:
        if category in skills:
            all_skills.extend(skills[category][:3])  # Top 3 par catégorie prioritaire

    # Compléter avec les autres catégories
    for category, skill_list in skills.items():
        if category not in priority_categories:
            all_skills.extend(skill_list[:2])

    # Retourner les N premiers (dédupliqués)
    seen = set()
    unique_skills = []
    for skill in all_skills:
        skill_name = skill.get("name") if isinstance(skill, dict) else skill
        if skill_name not in seen:
            seen.add(skill_name)
            unique_skills.append(skill_name)

    return unique_skills[:count]


def condense_cv_data(profile_data: Dict[str, Any], selected_exp_ids: List[str], selected_proj_ids: List[str]) -> Dict[str, Any]:
    """
    Condense toutes les données du CV pour tenir sur 1 page

    Args:
        profile_data: Données complètes du profil
        selected_exp_ids: IDs des expériences sélectionnées
        selected_proj_ids: IDs des projets sélectionnés

    Returns:
        Dict: Données condensées
    """
    condensed = {}

    # Informations personnelles (inchangées)
    condensed["personal_info"] = profile_data.get("personal_info", {})

    # Condenser le résumé s'il existe
    if "summary" in condensed["personal_info"]:
        condensed["personal_info"]["summary"] = condense_summary(
            condensed["personal_info"]["summary"]
        )

    # Filtrer et condenser les expériences
    all_experiences = profile_data.get("experiences", [])
    selected_experiences = [exp for exp in all_experiences if exp.get("id") in selected_exp_ids]
    condensed["experiences"] = condense_experiences(selected_experiences)

    # Filtrer et condenser les projets
    all_projects = profile_data.get("projects", [])
    selected_projects = [proj for proj in all_projects if proj.get("id") in selected_proj_ids]
    condensed["projects"] = condense_projects(selected_projects)

    # Condenser les compétences
    condensed["skills"] = condense_skills(profile_data.get("skills", {}))

    # Limiter les langues (garder toutes, mais format compact)
    condensed["languages"] = profile_data.get("languages", [])

    # Limiter les centres d'intérêt
    condensed["interests"] = profile_data.get("interests", [])[:CONDENSATION_RULES["interests"]]

    # Limiter les certifications
    condensed["certifications"] = profile_data.get("certifications", [])[:CONDENSATION_RULES["certifications"]["max_count"]]

    # Formation (garder toutes)
    condensed["education"] = profile_data.get("education", [])

    return condensed
