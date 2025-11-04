"""
Gestionnaire de profil utilisateur
"""
import json
from pathlib import Path
from typing import Optional
from .models import Profile


class ProfileManager:
    """Gestionnaire pour charger et sauvegarder les profils"""

    def __init__(self, profile_path: str = "data/profile.json"):
        self.profile_path = Path(profile_path)
        self._profile: Optional[Profile] = None

    def load_profile(self) -> Profile:
        """Charge le profil depuis le fichier JSON"""
        if not self.profile_path.exists():
            raise FileNotFoundError(f"Fichier de profil non trouvé: {self.profile_path}")

        with open(self.profile_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self._profile = Profile(**data)
        return self._profile

    def save_profile(self, profile: Profile) -> None:
        """Sauvegarde le profil dans le fichier JSON"""
        self.profile_path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.profile_path, 'w', encoding='utf-8') as f:
            json.dump(profile.model_dump(), f, indent=2, ensure_ascii=False)

        self._profile = profile

    def get_profile(self) -> Profile:
        """Retourne le profil en cache ou le charge"""
        if self._profile is None:
            return self.load_profile()
        return self._profile

    def get_all_skills(self) -> list[str]:
        """Retourne toutes les compétences du profil"""
        profile = self.get_profile()
        all_skills = []
        for category_skills in profile.skills.values():
            all_skills.extend([skill.name for skill in category_skills])
        return all_skills

    def get_skills_by_level(self, min_level: str = "intermediate") -> list[str]:
        """Retourne les compétences selon le niveau minimum"""
        level_order = {"beginner": 0, "intermediate": 1, "advanced": 2, "expert": 3}
        min_level_value = level_order.get(min_level, 1)

        profile = self.get_profile()
        skills = []
        for category_skills in profile.skills.values():
            for skill in category_skills:
                if level_order.get(skill.level, 0) >= min_level_value:
                    skills.append(skill.name)
        return skills

    def search_experiences_by_technology(self, technology: str) -> list[dict]:
        """Recherche les expériences qui utilisent une technologie"""
        profile = self.get_profile()
        matching_exps = []

        for exp in profile.experiences:
            if technology.lower() in [tech.lower() for tech in exp.technologies]:
                matching_exps.append(exp.model_dump())

        return matching_exps

    def search_projects_by_technology(self, technology: str) -> list[dict]:
        """Recherche les projets qui utilisent une technologie"""
        profile = self.get_profile()
        matching_projects = []

        for project in profile.projects:
            if technology.lower() in [tech.lower() for tech in project.technologies]:
                matching_projects.append(project.model_dump())

        return matching_projects
