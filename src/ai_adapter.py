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

        # Prompt optimisé pour CONDENSATION 1 PAGE
        system = """Tu es un expert en optimisation de CV. Le CV DOIT tenir sur 1 PAGE.
CONDENSE au maximum tout en gardant l'essentiel.
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

TÂCHE : CV 1 PAGE - CONDENSÉ et IMPACTANT. Génère ce JSON :

{{
  "selected_experiences": ["id_exp1", "id_exp2"],
  "selected_projects": ["id_proj1", "id_proj2"],
  "selected_skills": ["compétence1", "compétence2", ...8 max],
  "strengths": [
    "Point fort détaillé 1 avec CHIFFRES et technologies spécifiques (1-2 lignes complètes)",
    "Point fort détaillé 2 avec MÉTRIQUES quantifiées et preuves concrètes (1-2 lignes)",
    "Point fort détaillé 3 avec RÉALISATIONS mesurables et impact (1-2 lignes)"
  ],
  "custom_summary": "Résumé ULTRA-COURT de 2 phrases maximum (40 mots max). Direct et percutant.",
  "colors": {{"primary": "#1a73e8", "secondary": "#34a853"}}
}}

RÈGLES STRICTES pour CV 1 PAGE :
1. selected_experiences : SEULEMENT 2 expériences (pas 3!)
   - Utilise EXACTEMENT les IDs du profil (exp1, exp2, etc.)
   - Priorise celles qui correspondent aux compétences requises

2. selected_projects : SEULEMENT 2 projets (pas 3!)
   - Utilise EXACTEMENT les IDs du profil (proj1, proj2, proj3, etc.)
   - Priorise ceux qui démontrent les compétences recherchées

3. selected_skills : 8 compétences MAXIMUM (idéalement 6-8)
   - Utilise EXACTEMENT les noms de compétences du profil
   - Priorise celles mentionnées dans l'offre
   - PAS PLUS de 8 pour garder l'espace limité

4. strengths : 3 points forts DÉTAILLÉS et QUANTIFIÉS (1-2 lignes chacun)
   - OBLIGATOIRE : inclure des CHIFFRES/MÉTRIQUES (15+, 25%, 200+, x2, etc.)
   - Mentionner des TECHNOLOGIES SPÉCIFIQUES du profil
   - Donner des PREUVES concrètes (projets nommés, réalisations, présentations)
   - Exemples : "Expert cybersécurité avec 15+ scénarios OWASP développés, présentés devant 200+ professionnels"

5. custom_summary : 2 phrases MAXIMUM (40 mots total)
   - Résumé ultra-court et percutant
   - Met en avant les points forts pour CE poste
   - PAS de détails superflus - condensé au maximum

6. colors : Couleurs professionnelles en hexadécimal
   - primary : couleur principale (si entreprise connue, utilise sa couleur de marque)
   - secondary : couleur secondaire complémentaire

EXEMPLES DE BONS ATOUTS (À IMITER) :
✅ "Expert cybersécurité avec 15+ scénarios OWASP développés, présentés devant 200+ professionnels lors de OpenESIEA, incluant détection XSS et injection SQL avec architecture Docker sécurisée"
✅ "Développeur polyvalent maîtrisant C/C++/Python/TypeScript avec 10+ projets open-source sur GitHub (500+ stars), optimisation -25% consommation énergétique sur systèmes embarqués temps réel"
✅ "Lead technique sur projets collaboratifs avec mise en place CI/CD complète (GitHub Actions, Docker, tests automatisés), réduction -40% bugs production, contribution active communauté open-source"

EXEMPLES DE MAUVAIS ATOUTS (À ÉVITER) :
❌ "Expert en cybersécurité" → Trop vague, pas de preuves
❌ "Développeur polyvalent" → Pas de technologies mentionnées
❌ "Bonne maîtrise de Docker" → Pas de métriques ni contexte

CRITIQUE : Les atouts DOIVENT être LONGS (1-2 lignes), DÉTAILLÉS et inclure des CHIFFRES obligatoirement !

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
