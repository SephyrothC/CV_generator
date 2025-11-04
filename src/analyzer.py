"""
Analyseur d'offres d'emploi avec IA
"""
import os
import json
from typing import Dict, Any
from anthropic import Anthropic
from dotenv import load_dotenv
from .models import JobOffer

load_dotenv()


class JobOfferAnalyzer:
    """Analyse les offres d'emploi avec l'IA"""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY non trouvée. Ajoutez-la dans le fichier .env")

        self.client = Anthropic(api_key=self.api_key)
        self.model = os.getenv("AI_MODEL", "claude-3-5-sonnet-20241022")

    def analyze_job_offer(self, job_text: str) -> JobOffer:
        """
        Analyse une offre d'emploi et extrait les informations clés

        Args:
            job_text: Texte complet de l'offre d'emploi

        Returns:
            JobOffer: Offre analysée avec compétences, technologies, etc.
        """

        prompt = f"""Analyse cette offre d'emploi et extrais les informations suivantes au format JSON :

- company: Nom de l'entreprise
- position: Titre du poste
- description: Description courte du poste (2-3 phrases max)
- required_skills: Liste des compétences requises (hard skills)
- preferred_skills: Liste des compétences préférées/bonus
- technologies: Liste des technologies, langages, frameworks mentionnés
- keywords: Mots-clés importants pour le poste (soft skills, domaines, etc.)

Offre d'emploi :
{job_text}

Réponds UNIQUEMENT avec un objet JSON valide, sans texte avant ou après.
Format attendu :
{{
  "company": "Nom Entreprise",
  "position": "Titre du poste",
  "description": "Description courte",
  "required_skills": ["skill1", "skill2"],
  "preferred_skills": ["skill3", "skill4"],
  "technologies": ["tech1", "tech2"],
  "keywords": ["keyword1", "keyword2"]
}}"""

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            # Extraire le texte de la réponse
            response_text = message.content[0].text

            # Parser le JSON
            job_data = json.loads(response_text)

            # Créer l'objet JobOffer
            return JobOffer(**job_data)

        except json.JSONDecodeError as e:
            raise ValueError(f"Erreur de parsing JSON : {e}\nRéponse : {response_text}")
        except Exception as e:
            raise Exception(f"Erreur lors de l'analyse de l'offre : {e}")

    def extract_url_content(self, url: str) -> str:
        """
        Extrait le contenu d'une URL LinkedIn (si possible)
        Note: Cette fonctionnalité nécessite du web scraping ou une API
        Pour le MVP, on demandera à l'utilisateur de coller le texte directement
        """
        raise NotImplementedError(
            "L'extraction automatique d'URL n'est pas encore implémentée. "
            "Veuillez copier-coller le texte de l'offre directement."
        )
