"""
Adaptateur IA pour la personnalisation du CV
"""
import os
import json
from typing import List, Dict, Any
from anthropic import Anthropic
from dotenv import load_dotenv
from .models import Profile, JobOffer, CustomizedCV

load_dotenv()


class CVPersonalizer:
    """Personnalise le CV en fonction de l'offre d'emploi avec l'IA"""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY non trouvée. Ajoutez-la dans le fichier .env")

        self.client = Anthropic(api_key=self.api_key)
        self.model = os.getenv("AI_MODEL", "claude-3-5-sonnet-20241022")

    def personalize_cv(self, profile: Profile, job_offer: JobOffer) -> CustomizedCV:
        """
        Personnalise le CV en fonction de l'offre d'emploi

        Args:
            profile: Profil complet de l'utilisateur
            job_offer: Offre d'emploi analysée

        Returns:
            CustomizedCV: CV personnalisé avec sélections et adaptations
        """

        # Préparer les données du profil pour l'IA
        profile_summary = self._prepare_profile_summary(profile)

        prompt = f"""Tu es un expert en recrutement et en optimisation de CV.

Voici le profil complet d'un candidat :
{profile_summary}

Voici l'offre d'emploi ciblée :
- Entreprise: {job_offer.company}
- Poste: {job_offer.position}
- Description: {job_offer.description}
- Compétences requises: {', '.join(job_offer.required_skills)}
- Compétences préférées: {', '.join(job_offer.preferred_skills)}
- Technologies: {', '.join(job_offer.technologies)}
- Mots-clés: {', '.join(job_offer.keywords)}

Ta mission : personnaliser le CV pour maximiser les chances d'obtenir un entretien.

Génère un objet JSON avec :
1. selected_experiences: Liste des IDs des 2-3 expériences les plus pertinentes (max 3)
2. selected_projects: Liste des IDs des 2-3 projets les plus pertinents (max 3)
3. selected_skills: Liste de 6-10 compétences les plus pertinentes du candidat
4. strengths: Liste de 3-4 points forts/atouts adaptés au poste (phrases courtes et percutantes)
5. custom_summary: Un résumé personnalisé de 2-3 phrases qui met en avant ce qui correspond au poste
6. colors: Objet avec "primary" et "secondary" (couleurs hex de la marque si connue, sinon couleurs professionnelles neutres)

IMPORTANT:
- Sélectionne UNIQUEMENT les expériences, projets et compétences qui existent dans le profil
- Les IDs doivent correspondre exactement aux IDs du profil
- Priorise la pertinence par rapport à l'offre
- Les points forts doivent être concrets et liés au poste
- Le résumé doit être personnalisé pour ce poste spécifique

Réponds UNIQUEMENT avec un objet JSON valide :
{{
  "selected_experiences": ["exp1", "exp2"],
  "selected_projects": ["proj1", "proj2"],
  "selected_skills": ["skill1", "skill2", "skill3", ...],
  "strengths": ["Point fort 1", "Point fort 2", "Point fort 3"],
  "custom_summary": "Résumé personnalisé...",
  "colors": {{"primary": "#1a73e8", "secondary": "#34a853"}}
}}"""

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=2500,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            # Extraire le texte de la réponse
            response_text = message.content[0].text

            # Parser le JSON
            customization_data = json.loads(response_text)

            # Créer l'objet CustomizedCV
            return CustomizedCV(
                job_offer=job_offer,
                template="modern",
                **customization_data
            )

        except json.JSONDecodeError as e:
            raise ValueError(f"Erreur de parsing JSON : {e}\nRéponse : {response_text}")
        except Exception as e:
            raise Exception(f"Erreur lors de la personnalisation : {e}")

    def _prepare_profile_summary(self, profile: Profile) -> str:
        """Prépare un résumé du profil pour l'IA"""

        # Expériences
        experiences_text = "\n\nEXPÉRIENCES:\n"
        for exp in profile.experiences:
            experiences_text += f"- ID: {exp.id}\n"
            experiences_text += f"  Poste: {exp.position} chez {exp.company}\n"
            experiences_text += f"  Technologies: {', '.join(exp.technologies)}\n"
            experiences_text += f"  Réalisations: {'; '.join(exp.achievements[:3])}\n"

        # Compétences
        skills_text = "\n\nCOMPÉTENCES:\n"
        for category, skills in profile.skills.items():
            skills_text += f"{category.upper()}: "
            skills_text += ", ".join([f"{s.name} ({s.level})" for s in skills]) + "\n"

        # Projets
        projects_text = "\n\nPROJETS:\n"
        for proj in profile.projects:
            projects_text += f"- ID: {proj.id}\n"
            projects_text += f"  Nom: {proj.name}\n"
            projects_text += f"  Technologies: {', '.join(proj.technologies)}\n"
            projects_text += f"  Description: {proj.description}\n"

        return experiences_text + skills_text + projects_text

    def refine_experience_descriptions(
        self,
        profile: Profile,
        job_offer: JobOffer,
        experience_ids: List[str]
    ) -> Dict[str, List[str]]:
        """
        Reformule les descriptions d'expériences pour mieux correspondre au poste
        (Fonctionnalité bonus - peut être ajoutée plus tard)
        """
        # TODO: Implémenter la reformulation des expériences
        pass
