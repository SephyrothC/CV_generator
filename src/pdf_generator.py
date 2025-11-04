"""
Générateur de PDF à partir des templates HTML
"""
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Any
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML, CSS
from .models import Profile, CustomizedCV
from .condensation import (
    condense_experiences,
    condense_projects,
    condense_summary,
    condense_achievements,
    condense_text,
    CONDENSATION_RULES
)


class PDFGenerator:
    """Génère des CV en PDF à partir de templates HTML"""

    def __init__(self, templates_dir: str = "templates", output_dir: str = "generated"):
        self.templates_dir = Path(templates_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        # Initialiser Jinja2
        self.jinja_env = Environment(
            loader=FileSystemLoader(str(self.templates_dir)),
            autoescape=True
        )

    def generate_cv(
        self,
        profile: Profile,
        customized_cv: CustomizedCV,
        output_filename: str = None
    ) -> str:
        """
        Génère un CV en PDF

        Args:
            profile: Profil complet de l'utilisateur
            customized_cv: CV personnalisé avec sélections
            output_filename: Nom du fichier de sortie (optionnel)

        Returns:
            str: Chemin du fichier PDF généré
        """

        # Préparer les données pour le template
        template_data = self._prepare_template_data(profile, customized_cv)

        # Charger le template
        template_name = f"{customized_cv.template}.html"
        template = self.jinja_env.get_template(template_name)

        # Rendre le HTML
        html_content = template.render(**template_data)

        # Générer le nom de fichier si non fourni
        if output_filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            company_clean = customized_cv.job_offer.company.replace(" ", "_")
            output_filename = f"CV_{profile.personal_info.last_name}_{company_clean}_{timestamp}.pdf"

        # Chemin complet du fichier de sortie
        output_path = self.output_dir / output_filename

        # Générer le PDF avec WeasyPrint
        HTML(string=html_content).write_pdf(output_path)

        return str(output_path)

    def generate_html_preview(
        self,
        profile: Profile,
        customized_cv: CustomizedCV,
        output_filename: str = None
    ) -> str:
        """
        Génère un aperçu HTML du CV (pour prévisualisation)

        Args:
            profile: Profil complet de l'utilisateur
            customized_cv: CV personnalisé avec sélections
            output_filename: Nom du fichier de sortie (optionnel)

        Returns:
            str: Chemin du fichier HTML généré
        """

        # Préparer les données pour le template
        template_data = self._prepare_template_data(profile, customized_cv)

        # Charger le template
        template_name = f"{customized_cv.template}.html"
        template = self.jinja_env.get_template(template_name)

        # Rendre le HTML
        html_content = template.render(**template_data)

        # Générer le nom de fichier si non fourni
        if output_filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            company_clean = customized_cv.job_offer.company.replace(" ", "_")
            output_filename = f"CV_{profile.personal_info.last_name}_{company_clean}_{timestamp}.html"

        # Chemin complet du fichier de sortie
        output_path = self.output_dir / output_filename

        # Écrire le fichier HTML
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        return str(output_path)

    def _prepare_template_data(self, profile: Profile, customized_cv: CustomizedCV) -> Dict[str, Any]:
        """
        Prépare les données pour le template avec condensation pour CV 1 page

        Args:
            profile: Profil complet
            customized_cv: CV personnalisé

        Returns:
            Dict: Données condensées pour le template
        """

        # Filtrer les expériences sélectionnées
        selected_experiences = [
            exp for exp in profile.experiences
            if exp.id in customized_cv.selected_experiences
        ]

        # Filtrer les projets sélectionnés
        selected_projects = [
            proj for proj in profile.projects
            if proj.id in customized_cv.selected_projects
        ]

        # Appliquer la condensation pour tenir sur 1 page
        # Expériences: max 2 avec 4 bullets chacune
        condensed_experiences = condense_experiences(
            [exp.dict() for exp in selected_experiences],
            max_count=2
        )

        # Projets: max 2 avec 3 bullets chacun
        condensed_projects = condense_projects(
            [proj.dict() for proj in selected_projects],
            max_count=2
        )

        # Résumé: max 2 phrases, 40 mots
        condensed_summary = condense_summary(customized_cv.custom_summary)

        # Points forts: max 3-4, condensés à 12 mots max chacun
        strength_rules = CONDENSATION_RULES["strength_points"]
        condensed_strengths = [
            condense_text(strength, strength_rules["max_words_per_point"])
            for strength in customized_cv.strengths[:strength_rules["max_count"]]
        ]

        # Compétences: max 8
        condensed_skills = customized_cv.selected_skills[:CONDENSATION_RULES["skills"]["max_total_displayed"]]

        # Langues: max 4
        condensed_languages = profile.languages[:4] if profile.languages else []

        # Centres d'intérêt: max 5
        condensed_interests = profile.interests[:CONDENSATION_RULES["interests"]] if profile.interests else []

        # Certifications: max 2
        condensed_certifications = (
            profile.certifications[:CONDENSATION_RULES["certifications"]["max_count"]]
            if profile.certifications else []
        )

        # Formation: max 2 (garde les plus récentes)
        condensed_education = profile.education[:2] if profile.education else []

        # Préparer les données condensées
        return {
            "personal_info": profile.personal_info,
            "custom_summary": condensed_summary,
            "strengths": condensed_strengths,
            "selected_skills": condensed_skills,
            "experiences": condensed_experiences,
            "projects": condensed_projects,
            "education": condensed_education,
            "languages": condensed_languages,
            "certifications": condensed_certifications,
            "interests": condensed_interests,
            "colors": customized_cv.colors,
        }

    def list_available_templates(self) -> list[str]:
        """Liste tous les templates disponibles"""
        templates = []
        for file in self.templates_dir.glob("*.html"):
            templates.append(file.stem)
        return templates
