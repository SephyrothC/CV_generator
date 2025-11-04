"""
Adaptateur IA pour la personnalisation du CV (Ollama - local et gratuit)
"""
import os
from typing import List, Dict, Any
from dotenv import load_dotenv
from .models import Profile, JobOffer, CustomizedCV
from .ollama_client import OllamaClient

load_dotenv()


class CVPersonalizer:
    """Personnalise le CV en fonction de l'offre d'emploi avec l'IA locale (Ollama)"""

    def __init__(self, model: str = None):
        """
        Initialise le personnalisateur avec Ollama

        Args:
            model: Nom du modèle Ollama (défaut: qwen2.5:7b)
        """
        # Récupérer le modèle depuis .env ou utiliser le défaut
        self.model = model or os.getenv("OLLAMA_MODEL", "qwen2.5:7b")
        self.client = OllamaClient(model=self.model)

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

        # Prompt optimisé pour les modèles locaux (plus direct et structuré)
        system = """Tu es un expert en optimisation de CV et recrutement.
Tu dois analyser un profil candidat et une offre d'emploi, puis personnaliser le CV pour maximiser les chances.
Réponds UNIQUEMENT avec du JSON valide, sans texte avant ou après."""

        prompt = f"""PROFIL DU CANDIDAT :
{profile_summary}

OFFRE D'EMPLOI CIBLÉE :
- Entreprise : {job_offer.company}
- Poste : {job_offer.position}
- Description : {job_offer.description}
- Compétences requises : {', '.join(job_offer.required_skills)}
- Compétences préférées : {', '.join(job_offer.preferred_skills)}
- Technologies : {', '.join(job_offer.technologies)}
- Mots-clés : {', '.join(job_offer.keywords)}

TÂCHE : Génère une personnalisation complète au format JSON strict :

{{
  "selected_experiences": ["id_exp1", "id_exp2"],
  "selected_projects": ["id_proj1", "id_proj2"],
  "selected_skills": ["compétence1", "compétence2", "compétence3", ...],
  "strengths": [
    "Point fort 1 aligné avec le poste",
    "Point fort 2 démontrant la pertinence",
    "Point fort 3 mettant en valeur l'expérience",
    "Point fort 4 soulignant une qualité unique"
  ],
  "custom_summary": "Résumé professionnel personnalisé de 2-3 phrases qui met en avant les points les plus pertinents pour ce poste spécifique.",
  "colors": {{"primary": "#1a73e8", "secondary": "#34a853"}}
}}

RÈGLES IMPORTANTES :
1. selected_experiences : Choisis les 2-3 IDs d'expériences LES PLUS pertinentes (max 3)
   - Utilise EXACTEMENT les IDs du profil (exp1, exp2, exp3, etc.)
   - Priorise celles qui correspondent aux technologies/compétences requises

2. selected_projects : Choisis les 2-3 IDs de projets LES PLUS alignés (max 3)
   - Utilise EXACTEMENT les IDs du profil (proj1, proj2, proj3, etc.)
   - Priorise ceux qui démontrent les compétences recherchées

3. selected_skills : Liste 6-10 compétences prioritaires pour ce poste
   - Utilise EXACTEMENT les noms de compétences du profil
   - Priorise celles mentionnées dans l'offre

4. strengths : 3-4 points forts concrets et mesurables
   - Phrases courtes et percutantes
   - Liés directement au poste visé
   - Mettent en avant la valeur ajoutée

5. custom_summary : Résumé professionnel personnalisé
   - 2-3 phrases maximum
   - Met en avant les points forts pour CE poste
   - Mentionne l'expérience et les compétences clés

6. colors : Couleurs professionnelles en hexadécimal
   - primary : couleur principale (si entreprise connue, utilise sa couleur de marque)
   - secondary : couleur secondaire complémentaire

IMPORTANT : Réponds UNIQUEMENT avec le JSON, rien d'autre."""

        try:
            # Générer et parser le JSON automatiquement
            customization_data = self.client.generate_json(
                prompt=prompt,
                system=system,
                temperature=0.2,  # Un peu plus créatif pour le résumé
                max_tokens=2500
            )

            # Créer l'objet CustomizedCV
            return CustomizedCV(
                job_offer=job_offer,
                template="modern",
                **customization_data
            )

        except ValueError as e:
            raise ValueError(f"❌ Erreur de parsing JSON : {e}")
        except Exception as e:
            raise Exception(f"❌ Erreur lors de la personnalisation : {e}")

    def _prepare_profile_summary(self, profile: Profile) -> str:
        """Prépare un résumé concis du profil pour l'IA"""

        # Expériences (format compact)
        experiences_text = "\nEXPÉRIENCES PROFESSIONNELLES :\n"
        for exp in profile.experiences:
            experiences_text += f"\n[ID: {exp.id}]\n"
            experiences_text += f"• Poste : {exp.position} @ {exp.company}\n"
            experiences_text += f"• Période : {exp.start_date} - {'Présent' if exp.current else exp.end_date}\n"
            experiences_text += f"• Technologies : {', '.join(exp.technologies)}\n"
            # Limiter à 3 réalisations principales
            experiences_text += f"• Réalisations principales :\n"
            for achievement in exp.achievements[:3]:
                experiences_text += f"  - {achievement}\n"

        # Compétences (format compact par catégorie)
        skills_text = "\nCOMPÉTENCES PAR CATÉGORIE :\n"
        for category, skills in profile.skills.items():
            skill_names = [f"{s.name} ({s.level}, {s.years} ans)" for s in skills]
            skills_text += f"• {category.upper()} : {', '.join(skill_names)}\n"

        # Projets (format compact)
        projects_text = "\nPROJETS NOTABLES :\n"
        for proj in profile.projects:
            projects_text += f"\n[ID: {proj.id}]\n"
            projects_text += f"• Nom : {proj.name}\n"
            projects_text += f"• Rôle : {proj.role}\n"
            projects_text += f"• Description : {proj.description}\n"
            projects_text += f"• Technologies : {', '.join(proj.technologies)}\n"
            # Limiter à 2 réalisations
            if proj.achievements:
                projects_text += f"• Réalisations : {'; '.join(proj.achievements[:2])}\n"

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
        # TODO: Implémenter la reformulation des expériences avec Ollama
        pass
