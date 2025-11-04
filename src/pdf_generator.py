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
        Prépare les données pour le template

        Args:
            profile: Profil complet
            customized_cv: CV personnalisé

        Returns:
            Dict: Données pour le template
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

        # Préparer les données
        return {
            "personal_info": profile.personal_info,
            "custom_summary": customized_cv.custom_summary,
            "strengths": customized_cv.strengths,
            "selected_skills": customized_cv.selected_skills,
            "experiences": selected_experiences,
            "projects": selected_projects,
            "education": profile.education,
            "languages": profile.languages,
            "certifications": profile.certifications if profile.certifications else [],
            "interests": profile.interests if profile.interests else [],
            "colors": customized_cv.colors,
        }

    def list_available_templates(self) -> list[str]:
        """Liste tous les templates disponibles"""
        templates = []
        for file in self.templates_dir.glob("*.html"):
            templates.append(file.stem)
        return templates
