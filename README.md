# 📄 CV Generator AI

Générateur automatique de CV personnalisés qui s'adapte aux offres d'emploi LinkedIn grâce à l'intelligence artificielle.

## 🎯 Fonctionnalités

- ✨ **Analyse automatique** des offres d'emploi avec l'IA (Claude API)
- 🎨 **Personnalisation intelligente** du CV en fonction du poste
- 📝 **2 templates professionnels** (Modern & Professional)
- 🎨 **Détection automatique** des couleurs de marque de l'entreprise
- 📄 **Génération PDF** haute qualité (compatible ATS)
- 🖥️ **Interface web intuitive** avec Streamlit
- ⚡ **Workflow rapide** : de l'offre au PDF en quelques minutes

## 🚀 Installation

### Prérequis

- Python 3.9 ou supérieur
- pip (gestionnaire de paquets Python)

### Étapes d'installation

1. **Cloner le repository**
```bash
git clone <votre-repo>
cd CV_generator
```

2. **Créer un environnement virtuel** (recommandé)
```bash
python -m venv venv

# Sur Windows
venv\Scripts\activate

# Sur macOS/Linux
source venv/bin/activate
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Configurer les variables d'environnement**
```bash
# Copier le fichier d'exemple
cp .env.example .env

# Éditer .env et ajouter votre clé API Anthropic
# ANTHROPIC_API_KEY=sk-ant-...
```

### Obtenir une clé API Anthropic (Claude)

1. Créez un compte sur [https://console.anthropic.com](https://console.anthropic.com)
2. Allez dans "API Keys"
3. Créez une nouvelle clé API
4. Copiez la clé dans votre fichier `.env`

> **Note** : Anthropic offre un crédit gratuit pour tester l'API.

## 📖 Utilisation

### 1. Préparer votre profil

Éditez le fichier `data/profile.json` avec vos informations :

```json
{
  "personal_info": {
    "first_name": "Votre Prénom",
    "last_name": "Votre Nom",
    "title": "Votre Titre",
    "email": "votre@email.com",
    ...
  },
  "experiences": [...],
  "skills": {...},
  "projects": [...],
  ...
}
```

Un exemple complet est déjà fourni dans le fichier.

### 2. Lancer l'application

```bash
streamlit run app.py
```

L'application s'ouvrira automatiquement dans votre navigateur (par défaut : http://localhost:8501)

### 3. Workflow

1. **Charger votre profil** (barre latérale)
2. **Coller l'offre d'emploi** LinkedIn
3. **Analyser** l'offre avec l'IA
4. **Personnaliser** : l'IA sélectionne automatiquement les éléments pertinents
5. **Ajuster** si nécessaire (résumé, points forts, couleurs)
6. **Générer le PDF** final

## 📁 Structure du projet

```
CV_generator/
├── data/
│   └── profile.json          # Votre profil complet
├── templates/
│   ├── modern.html           # Template moderne (sidebar colorée)
│   └── professional.html     # Template professionnel (classique)
├── generated/                 # CV générés (PDF et HTML)
├── src/
│   ├── __init__.py
│   ├── models.py             # Modèles de données (Pydantic)
│   ├── profile_manager.py    # Gestion du profil
│   ├── analyzer.py           # Analyse d'offres avec IA
│   ├── ai_adapter.py         # Personnalisation avec IA
│   ├── pdf_generator.py      # Génération de PDF
│   └── color_matcher.py      # Détection couleurs entreprise
├── app.py                     # Application Streamlit
├── requirements.txt           # Dépendances Python
├── .env.example              # Exemple de configuration
└── README.md                 # Ce fichier
```

## 🎨 Templates disponibles

### Modern
- Design moderne avec sidebar colorée
- Informations de contact dans la sidebar
- Mise en page deux colonnes
- Idéal pour les profils tech/créatifs

### Professional
- Design classique et élégant
- Header centré
- Grille de compétences
- Parfait pour les profils corporate

## 🤖 Comment fonctionne l'IA ?

1. **Analyse de l'offre** : Claude extrait automatiquement :
   - Entreprise et poste
   - Compétences requises
   - Technologies mentionnées
   - Mots-clés importants

2. **Personnalisation** : Claude sélectionne :
   - Les 2-3 expériences les plus pertinentes
   - Les 2-3 projets les plus adaptés
   - Les 6-10 compétences à mettre en avant
   - Génère 3-4 points forts personnalisés
   - Crée un résumé sur-mesure

3. **Optimisation** : Le CV généré est :
   - Adapté au poste ciblé
   - Compatible ATS (Applicant Tracking Systems)
   - Visuellement professionnel
   - Limité à 1-2 pages

## 💡 Conseils d'utilisation

### Profil de base
- ✅ Soyez exhaustif : ajoutez TOUTES vos expériences et compétences
- ✅ Soyez précis : utilisez des verbes d'action et des chiffres
- ✅ Gardez le format JSON : respectez la structure du fichier exemple

### Offres d'emploi
- ✅ Copiez le texte complet de l'offre LinkedIn
- ✅ Incluez la description, les compétences et les qualifications
- ✅ Plus l'offre est détaillée, meilleure sera la personnalisation

### Personnalisation
- ✅ Vérifiez toujours les suggestions de l'IA
- ✅ Ajustez le résumé si nécessaire
- ✅ Modifiez les couleurs selon vos préférences
- ✅ Relisez attentivement avant de générer le PDF

## 🔧 Options avancées

### Utiliser un autre modèle d'IA

Éditez le fichier `.env` :

```env
AI_PROVIDER=anthropic
AI_MODEL=claude-3-5-sonnet-20241022
```

### Ajouter de nouvelles entreprises

Éditez `src/color_matcher.py` pour ajouter les couleurs de nouvelles entreprises :

```python
COMPANY_COLORS = {
    "nouvelle_entreprise": {"primary": "#123456", "secondary": "#789abc"},
    ...
}
```

### Créer un nouveau template

1. Créez un nouveau fichier HTML dans `templates/`
2. Utilisez la syntaxe Jinja2 pour les variables
3. Suivez la structure des templates existants

## 📊 Exemples

### Exemple d'offre d'emploi

```
Développeur Full Stack Senior - TechCorp
Paris, France

Nous recherchons un développeur Full Stack Senior pour rejoindre notre équipe...

Compétences requises :
- React, Node.js, TypeScript
- PostgreSQL, Redis
- Docker, AWS
- Expérience en microservices

Compétences appréciées :
- GraphQL
- CI/CD
- Agile/Scrum
```

L'IA va automatiquement :
- Extraire "TechCorp" comme entreprise
- Identifier les technologies (React, Node.js, etc.)
- Sélectionner vos expériences avec ces technologies
- Créer un résumé adapté

## ❓ FAQ

**Q : L'API Anthropic est-elle vraiment gratuite ?**
R : Anthropic offre un crédit de démarrage. Ensuite, le paiement est à l'usage (très faible coût par CV généré).

**Q : Puis-je utiliser une autre IA ?**
R : Oui, le code est modulaire. Vous pouvez adapter `analyzer.py` et `ai_adapter.py` pour utiliser OpenAI, Groq ou Ollama.

**Q : Les CV sont-ils compatibles ATS ?**
R : Oui, les templates utilisent une structure HTML sémantique compatible avec les systèmes de tracking.

**Q : Puis-je modifier les templates ?**
R : Absolument ! Les templates sont en HTML/CSS standard. Personnalisez-les selon vos besoins.

**Q : Combien de CV puis-je générer ?**
R : Illimité ! Chaque CV est sauvegardé avec un nom unique (date + entreprise).

## 🐛 Résolution de problèmes

### Erreur : "ANTHROPIC_API_KEY non trouvée"
- Vérifiez que le fichier `.env` existe
- Vérifiez que la clé API est correcte
- Relancez l'application

### Erreur lors de la génération du PDF
- Vérifiez que WeasyPrint est installé correctement
- Sur Linux : installez les dépendances système (libpango, libcairo)
- Sur Windows : installez GTK+ Runtime

### L'IA ne retourne pas de résultats
- Vérifiez votre connexion Internet
- Vérifiez votre crédit API Anthropic
- Essayez avec une offre plus détaillée

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Signaler des bugs
- Proposer des améliorations
- Ajouter de nouveaux templates
- Améliorer la documentation

## 📝 Licence

Ce projet est sous licence MIT. Utilisez-le librement pour vos besoins personnels ou professionnels.

## 🙏 Remerciements

- [Anthropic](https://www.anthropic.com) pour l'API Claude
- [Streamlit](https://streamlit.io) pour le framework web
- [WeasyPrint](https://weasyprint.org) pour la génération PDF

## 📧 Support

Pour toute question ou suggestion, ouvrez une issue sur GitHub.

---

**Bonne génération de CV ! 🚀**
