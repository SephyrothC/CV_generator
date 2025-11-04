"""
Détection des couleurs de marque d'entreprise
"""
from typing import Dict, Tuple


class ColorMatcher:
    """Détecte et suggère des couleurs de marque pour les entreprises"""

    # Base de données de couleurs d'entreprises connues
    COMPANY_COLORS = {
        # Tech
        "google": {"primary": "#4285f4", "secondary": "#34a853"},
        "microsoft": {"primary": "#00a4ef", "secondary": "#7fba00"},
        "apple": {"primary": "#000000", "secondary": "#a6a6a6"},
        "amazon": {"primary": "#ff9900", "secondary": "#232f3e"},
        "meta": {"primary": "#0081fb", "secondary": "#00c6ff"},
        "facebook": {"primary": "#1877f2", "secondary": "#42b72a"},
        "airbnb": {"primary": "#ff5a5f", "secondary": "#00a699"},
        "uber": {"primary": "#000000", "secondary": "#ffffff"},
        "spotify": {"primary": "#1db954", "secondary": "#191414"},
        "netflix": {"primary": "#e50914", "secondary": "#221f1f"},
        "linkedin": {"primary": "#0077b5", "secondary": "#00a0dc"},
        "twitter": {"primary": "#1da1f2", "secondary": "#14171a"},
        "slack": {"primary": "#611f69", "secondary": "#e01e5a"},
        "dropbox": {"primary": "#0061ff", "secondary": "#0d2481"},

        # Finance
        "paypal": {"primary": "#003087", "secondary": "#009cde"},
        "stripe": {"primary": "#635bff", "secondary": "#0a2540"},
        "revolut": {"primary": "#0075eb", "secondary": "#000000"},

        # French Tech
        "blablacar": {"primary": "#00aff5", "secondary": "#003d7a"},
        "doctolib": {"primary": "#0596de", "secondary": "#004d7a"},
        "ovh": {"primary": "#123f6d", "secondary": "#00b1e7"},
        "deezer": {"primary": "#ef5466", "secondary": "#181818"},
        "leboncoin": {"primary": "#ff6e14", "secondary": "#004d3c"},
        "vinted": {"primary": "#09b1ba", "secondary": "#13151a"},

        # Autres
        "ibm": {"primary": "#054ada", "secondary": "#000000"},
        "oracle": {"primary": "#f80000", "secondary": "#000000"},
        "salesforce": {"primary": "#00a1e0", "secondary": "#032d60"},
        "sap": {"primary": "#0073e7", "secondary": "#000000"},
        "adobe": {"primary": "#ff0000", "secondary": "#000000"},
    }

    # Couleurs par défaut selon le domaine
    DEFAULT_COLORS = {
        "tech": {"primary": "#2563eb", "secondary": "#1e40af"},
        "finance": {"primary": "#059669", "secondary": "#047857"},
        "healthcare": {"primary": "#0891b2", "secondary": "#0e7490"},
        "education": {"primary": "#7c3aed", "secondary": "#6d28d9"},
        "retail": {"primary": "#dc2626", "secondary": "#b91c1c"},
        "marketing": {"primary": "#db2777", "secondary": "#be185d"},
        "consulting": {"primary": "#0f766e", "secondary": "#115e59"},
        "default": {"primary": "#1e293b", "secondary": "#475569"},
    }

    def get_company_colors(self, company_name: str) -> Dict[str, str]:
        """
        Retourne les couleurs d'une entreprise

        Args:
            company_name: Nom de l'entreprise

        Returns:
            Dict avec primary et secondary colors
        """
        # Normaliser le nom de l'entreprise
        normalized_name = company_name.lower().strip()

        # Recherche directe
        if normalized_name in self.COMPANY_COLORS:
            return self.COMPANY_COLORS[normalized_name]

        # Recherche partielle (si le nom contient une entreprise connue)
        for company_key, colors in self.COMPANY_COLORS.items():
            if company_key in normalized_name or normalized_name in company_key:
                return colors

        # Retourner les couleurs par défaut
        return self.DEFAULT_COLORS["default"]

    def get_colors_by_industry(self, keywords: list[str]) -> Dict[str, str]:
        """
        Suggère des couleurs selon l'industrie basée sur des mots-clés

        Args:
            keywords: Liste de mots-clés de l'offre

        Returns:
            Dict avec primary et secondary colors
        """
        keywords_lower = [k.lower() for k in keywords]

        # Mapping de mots-clés vers industries
        industry_keywords = {
            "tech": ["software", "développement", "code", "api", "cloud", "devops"],
            "finance": ["banque", "finance", "fintech", "paiement", "trading"],
            "healthcare": ["santé", "médical", "healthcare", "pharma"],
            "education": ["éducation", "formation", "learning", "enseignement"],
            "retail": ["e-commerce", "retail", "vente", "commerce"],
            "marketing": ["marketing", "publicité", "communication", "digital"],
            "consulting": ["conseil", "consulting", "stratégie", "advisory"],
        }

        # Déterminer l'industrie
        for industry, industry_kw in industry_keywords.items():
            if any(kw in " ".join(keywords_lower) for kw in industry_kw):
                return self.DEFAULT_COLORS.get(industry, self.DEFAULT_COLORS["default"])

        return self.DEFAULT_COLORS["default"]

    def suggest_colors(
        self,
        company_name: str,
        keywords: list[str] = None
    ) -> Dict[str, str]:
        """
        Suggère les meilleures couleurs pour le CV

        Args:
            company_name: Nom de l'entreprise
            keywords: Mots-clés optionnels de l'offre

        Returns:
            Dict avec primary et secondary colors
        """
        # Essayer d'abord avec le nom de l'entreprise
        colors = self.get_company_colors(company_name)

        # Si couleurs par défaut et qu'on a des keywords, essayer par industrie
        if colors == self.DEFAULT_COLORS["default"] and keywords:
            colors = self.get_colors_by_industry(keywords)

        return colors

    @staticmethod
    def validate_hex_color(color: str) -> bool:
        """Valide qu'une couleur est au format hexadécimal"""
        if not color.startswith("#"):
            return False
        if len(color) != 7:
            return False
        try:
            int(color[1:], 16)
            return True
        except ValueError:
            return False
