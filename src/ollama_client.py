"""
Client pour interagir avec Ollama (IA locale)
"""
import json
import requests
import re
from typing import Optional, Dict, Any


class OllamaClient:
    """Client pour communiquer avec Ollama en local"""

    def __init__(self, model: str = "qwen2.5:7b", base_url: str = "http://localhost:11434"):
        """
        Initialise le client Ollama

        Args:
            model: Nom du modèle à utiliser (qwen2.5:7b, llama3.1:8b, etc.)
            base_url: URL de base de l'API Ollama
        """
        self.model = model
        self.base_url = base_url.rstrip('/')
        self.generate_url = f"{self.base_url}/api/generate"
        self.chat_url = f"{self.base_url}/api/chat"

    def is_available(self) -> bool:
        """
        Vérifie qu'Ollama est lancé et accessible

        Returns:
            bool: True si Ollama est disponible
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

    def is_model_available(self) -> bool:
        """
        Vérifie que le modèle spécifié est téléchargé

        Returns:
            bool: True si le modèle est disponible
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get('models', [])
                model_names = [m['name'] for m in models]
                return self.model in model_names
            return False
        except requests.exceptions.RequestException:
            return False

    def generate(
        self,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.1,
        max_tokens: int = 2000
    ) -> str:
        """
        Génère une réponse avec Ollama

        Args:
            prompt: Le prompt utilisateur
            system: Instructions système (optionnel)
            temperature: Température de génération (0.0 = déterministe, 1.0 = créatif)
            max_tokens: Nombre maximum de tokens à générer

        Returns:
            str: La réponse générée

        Raises:
            Exception: Si Ollama n'est pas disponible ou erreur de génération
        """
        if not self.is_available():
            raise Exception(
                "❌ Ollama n'est pas disponible. "
                "Assurez-vous qu'Ollama est installé et lancé (commande: 'ollama serve')"
            )

        if not self.is_model_available():
            raise Exception(
                f"❌ Le modèle '{self.model}' n'est pas installé. "
                f"Téléchargez-le avec: ollama pull {self.model}"
            )

        # Construire le prompt complet
        full_prompt = prompt
        if system:
            full_prompt = f"{system}\n\n{prompt}"

        # Paramètres de la requête
        payload = {
            "model": self.model,
            "prompt": full_prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
            }
        }

        try:
            response = requests.post(
                self.generate_url,
                json=payload,
                timeout=120  # 2 minutes max
            )
            response.raise_for_status()

            result = response.json()
            return result.get('response', '').strip()

        except requests.exceptions.Timeout:
            raise Exception("⏱️ Délai d'attente dépassé. Le modèle met trop de temps à répondre.")
        except requests.exceptions.RequestException as e:
            raise Exception(f"❌ Erreur lors de la communication avec Ollama : {e}")

    def extract_json(self, response: str) -> Dict[str, Any]:
        """
        Extrait le JSON d'une réponse, même si du texte l'entoure

        Args:
            response: Réponse brute du modèle

        Returns:
            dict: JSON parsé

        Raises:
            ValueError: Si aucun JSON valide n'est trouvé
        """
        # Essayer de parser directement
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            pass

        # Chercher le premier { et le dernier }
        match = re.search(r'\{.*\}', response, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except json.JSONDecodeError:
                pass

        # Chercher des blocs de code markdown
        match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', response, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                pass

        raise ValueError(
            f"Impossible d'extraire un JSON valide de la réponse.\n"
            f"Réponse reçue : {response[:500]}..."
        )

    def generate_json(
        self,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.1,
        max_tokens: int = 2000
    ) -> Dict[str, Any]:
        """
        Génère une réponse et extrait le JSON automatiquement

        Args:
            prompt: Le prompt utilisateur
            system: Instructions système (optionnel)
            temperature: Température de génération
            max_tokens: Nombre maximum de tokens

        Returns:
            dict: JSON parsé

        Raises:
            Exception: Si erreur de génération ou parsing JSON
        """
        response = self.generate(prompt, system, temperature, max_tokens)
        return self.extract_json(response)

    def list_available_models(self) -> list[str]:
        """
        Liste tous les modèles disponibles localement

        Returns:
            list: Liste des noms de modèles
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get('models', [])
                return [m['name'] for m in models]
            return []
        except requests.exceptions.RequestException:
            return []
