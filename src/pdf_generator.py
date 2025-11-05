"""
Générateur de PDF à partir des templates HTML
"""
import os
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List
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


# ============================================
# FONCTIONS D'ENRICHISSEMENT POUR MODERN_V2
# ============================================

def categorize_technology(tech_name: str) -> str:
    """Catégorise une technologie pour appliquer la bonne couleur de badge"""
    categories = {
        'language': ['Python', 'C', 'C++', 'JavaScript', 'TypeScript', 'Java', 'Bash', 'SQL', 'Go', 'Rust', 'PHP', 'Ruby'],
        'framework': ['React', 'Vue.js', 'Node.js', 'Express', 'FastAPI', 'Next.js', 'Angular', 'Django', 'Flask', 'Spring'],
        'devops': ['Docker', 'Kubernetes', 'CI/CD', 'GitHub Actions', 'Git', 'Linux', 'Nginx', 'Jenkins', 'Terraform', 'Ansible'],
        'security': ['OWASP', 'Security Testing', 'Pentest', 'Burp Suite', 'Cryptography', 'SSL', 'Firewall', 'Metasploit'],
        'database': ['PostgreSQL', 'MySQL', 'MongoDB', 'Redis', 'SQLite', 'Oracle', 'MariaDB', 'Cassandra']
    }

    tech_lower = tech_name.lower()
    for category, keywords in categories.items():
        if any(keyword.lower() in tech_lower for keyword in keywords):
            return category
    return 'other'


def enrich_technologies(technologies: List[str]) -> List[Dict[str, str]]:
    """Enrichit la liste des technologies avec leur catégorie"""
    return [
        {
            'name': tech,
            'category': categorize_technology(tech)
        }
        for tech in technologies
    ]


def prepare_skills_with_levels(profile: Profile, selected_skills: List[str]) -> List[Dict[str, Any]]:
    """Prépare les compétences avec des niveaux de progression visuels"""
    skill_levels = {
        'expert': 95,
        'advanced': 80,
        'intermediate': 60,
        'beginner': 40
    }

    result = []

    # Parcourir toutes les catégories de compétences du profil
    for skill_category in profile.skills:
        for skill in skill_category.skills:
            if skill.name in selected_skills[:8]:
                # Déterminer le niveau (par défaut 'intermediate')
                level_value = 70  # Valeur par défaut

                # Si le skill a un attribut level, l'utiliser
                if hasattr(skill, 'level') and skill.level:
                    level_text = skill.level.lower()
                    level_value = skill_levels.get(level_text, 70)

                result.append({
                    'name': skill.name,
                    'level': level_value
                })

    return result[:8]  # Top 8 seulement


def prepare_languages_with_indicators(profile: Profile) -> List[Dict[str, Any]]:
    """Prépare les langues avec emoji et indicateurs visuels"""
    language_emojis = {
        'Français': '🇫🇷',
        'Anglais': '🇬🇧',
        'Allemand': '🇩🇪',
        'Espagnol': '🇪🇸',
        'Coréen': '🇰🇷',
        'Italien': '🇮🇹',
        'Chinois': '🇨🇳',
        'Japonais': '🇯🇵',
        'Portugais': '🇵🇹',
        'Russe': '🇷🇺'
    }

    level_dots = {
        'Natif': 5,
        'Courant': 4,
        'Avancé': 4,
        'Intermédiaire': 3,
        'Scolaire': 2,
        'Débutant': 1,
        'C2': 5,
        'C1': 4,
        'B2': 4,
        'B1': 3,
        'A2': 2,
        'A1': 1
    }

    result = []
    for lang in profile.languages:
        lang_name = lang.name
        lang_level = lang.level

        # Extraire le niveau des parenthèses si présent
        level_text = lang_level.split('(')[0].strip()

        result.append({
            'name': lang_name,
            'emoji': language_emojis.get(lang_name, '🌐'),
            'level': lang_level,
            'dots': level_dots.get(level_text, 3)
        })

    return result


def enhance_text_with_metrics(text: str) -> str:
    """Met en surbrillance les chiffres/métriques dans le texte"""
    if not text:
        return text

    # Patterns pour trouver les métriques
    patterns = [
        (r'(\d+\+)', r'<span class="metric-blue">\1</span>'),  # 15+
        (r'(\d+%)', r'<span class="metric-green">\1</span>'),  # 25%
        (r'(\d{2,})', r'<span class="metric-purple">\1</span>'),  # 200
    ]

    result = text
    for pattern, replacement in patterns:
        result = re.sub(pattern, replacement, result)

    return result


def prepare_certifications_with_icons(profile: Profile) -> List[Dict[str, str]]:
    """Ajoute des icônes aux certifications"""
    if not profile.certifications:
        return []

    cert_icons = {
        'TOEIC': '🏆',
        'TOEFL': '🏆',
        'AWS': '☁️',
        'Azure': '☁️',
        'Google': '☁️',
        'Certified': '✅',
        'Formation': '📚',
        'Cybersécurité': '🛡️',
        'Security': '🛡️',
        'OWASP': '🛡️',
        'Cloud': '☁️',
        'DevOps': '⚙️'
    }

    result = []
    for cert in profile.certifications:
        cert_name = cert.name
        icon = '🏅'  # Icône par défaut

        # Trouver l'icône appropriée
        for keyword, emoji in cert_icons.items():
            if keyword.lower() in cert_name.lower():
                icon = emoji
                break

        result.append({
            'name': cert_name,
            'issuer': cert.issuer,
            'date': cert.date if hasattr(cert, 'date') and cert.date else '',
            'icon': icon
        })

    return result


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

        # Détection du template modern_v2 pour enrichissements avancés
        is_modern_v2 = customized_cv.template == "modern_v2"

        if is_modern_v2:
            # Enrichissements spécifiques pour modern_v2
            # Compétences avec barres de progression
            top_skills = prepare_skills_with_levels(profile, customized_cv.selected_skills)

            # Langues avec emojis et indicateurs
            languages_enriched = prepare_languages_with_indicators(profile)

            # Expériences avec technologies catégorisées et métriques en surbrillance
            experiences_enriched = []
            for exp in condensed_experiences[:2]:
                exp_enriched = exp.copy()
                # Enrichir les technologies
                if 'technologies' in exp and exp['technologies']:
                    exp_enriched['technologies'] = enrich_technologies(exp['technologies'])
                else:
                    exp_enriched['technologies'] = []
                # Mettre en surbrillance les métriques dans les achievements
                if 'achievements' in exp:
                    exp_enriched['achievements'] = [
                        enhance_text_with_metrics(ach) for ach in exp['achievements']
                    ]
                experiences_enriched.append(exp_enriched)

            # Projets avec technologies catégorisées et métriques
            projects_enriched = []
            for proj in condensed_projects[:2]:
                proj_enriched = proj.copy()
                # Enrichir les technologies
                if 'technologies' in proj and proj['technologies']:
                    proj_enriched['technologies'] = enrich_technologies(proj['technologies'])
                else:
                    proj_enriched['technologies'] = []
                # Mettre en surbrillance les métriques
                if 'achievements' in proj:
                    proj_enriched['achievements'] = [
                        enhance_text_with_metrics(ach) for ach in proj['achievements']
                    ]
                projects_enriched.append(proj_enriched)

            # Points forts avec métriques en surbrillance
            strengths_enriched = [
                enhance_text_with_metrics(strength) for strength in condensed_strengths
            ]

            # Certifications avec icônes
            certifications_enriched = prepare_certifications_with_icons(profile)

            # Footer items par défaut (peut être personnalisé)
            footer_items = [
                "Disponible immédiatement",
                "Mobilité France/Remote",
                "Open to opportunities"
            ]

            return {
                "personal_info": profile.personal_info,
                "custom_summary": condensed_summary,
                "strengths": strengths_enriched,
                "top_skills": top_skills,  # Compétences avec niveaux
                "selected_skills": condensed_skills,  # Fallback pour autres templates
                "experiences": experiences_enriched,
                "projects": projects_enriched,
                "education": condensed_education,
                "languages": languages_enriched,  # Langues enrichies
                "certifications": certifications_enriched,  # Certifications avec icônes
                "interests": condensed_interests,
                "colors": customized_cv.colors,
                "qr_code_enabled": False,  # À activer si besoin
                "qr_code_path": "",
                "footer_items": footer_items,
            }
        else:
            # Templates classiques (modern, professional)
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
