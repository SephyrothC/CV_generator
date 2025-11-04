"""
Analyseur d'offres d'emploi avec IA (Ollama - local et gratuit)
"""
import os
from typing import Dict, Any
from dotenv import load_dotenv
from .models import JobOffer
from .ollama_client import OllamaClient

load_dotenv()


class JobOfferAnalyzer:
    """Analyse les offres d'emploi avec l'IA locale (Ollama)"""

    def __init__(self, model: str = None):
        """
        Initialise l'analyseur avec Ollama

        Args:
            model: Nom du modèle Ollama (défaut: qwen2.5:7b)
        """
        # Récupérer le modèle depuis .env ou utiliser le défaut
        self.model = model or os.getenv("OLLAMA_MODEL", "qwen2.5:7b")
        self.client = OllamaClient(model=self.model)

    def analyze_job_offer(self, job_text: str) -> JobOffer:
        """
        Analyse une offre d'emploi et extrait les informations clés

        Args:
            job_text: Texte complet de l'offre d'emploi

        Returns:
            JobOffer: Offre analysée avec compétences, technologies, etc.
        """

        # Prompt optimisé pour les modèles locaux (plus direct et structuré)
        system = """Tu es un expert en analyse d'offres d'emploi. Ta mission est d'extraire des informations structurées.
Réponds UNIQUEMENT avec du JSON valide, sans texte avant ou après."""

        prompt = f"""OFFRE D'EMPLOI :
{job_text}

TÂCHE : Extrais les informations suivantes au format JSON strict :

{{
  "company": "nom de l'entreprise (si mentionné, sinon 'Non spécifié')",
  "position": "titre exact du poste",
  "description": "description courte du poste en 2-3 phrases maximum",
  "required_skills": ["compétence obligatoire 1", "compétence obligatoire 2", ...],
  "preferred_skills": ["compétence souhaitée 1", "compétence souhaitée 2", ...],
  "technologies": ["technologie/outil 1", "technologie/outil 2", ...],
  "keywords": ["mot-clé important 1", "mot-clé important 2", ...]
}}

RÈGLES IMPORTANTES :
- required_skills : Compétences techniques obligatoires (5-8 maximum)
- preferred_skills : Compétences souhaitées ou bonus (3-5 maximum)
- technologies : Technologies, langages, frameworks, outils spécifiques
- keywords : Mots-clés importants (soft skills, domaines, certifications)
- Si une information n'est pas dans l'offre, mets une liste vide []
- Réponds UNIQUEMENT avec le JSON, rien d'autre"""

        try:
            # Générer et parser le JSON automatiquement
            job_data = self.client.generate_json(
                prompt=prompt,
                system=system,
                temperature=0.1,  # Bas pour plus de cohérence
                max_tokens=2000
            )

            # Créer l'objet JobOffer
            return JobOffer(**job_data)

        except ValueError as e:
            raise ValueError(f"❌ Erreur de parsing JSON : {e}")
        except Exception as e:
            raise Exception(f"❌ Erreur lors de l'analyse de l'offre : {e}")

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
