# 📄 CV Generator AI - Version Locale Gratuite

Générateur automatique de CV personnalisés qui s'adapte aux offres d'emploi LinkedIn grâce à l'intelligence artificielle **locale et 100% gratuite** avec **Ollama** !

## ✨ Nouveauté : IA Locale et Gratuite !

Ce projet utilise **Ollama**, une solution d'IA locale qui vous permet de :
- ✅ **Utilisation illimitée** - Aucune limite, aucun coût
- ✅ **Confidentialité totale** - Vos données restent sur votre machine
- ✅ **Pas de clé API** - Aucune inscription requise
- ✅ **Hors ligne** - Fonctionne sans connexion Internet (après installation)

## 🎯 Fonctionnalités

- ✨ **Analyse automatique** des offres d'emploi avec IA locale (Ollama)
- 🎨 **Personnalisation intelligente** du CV en fonction du poste
- 📝 **2 templates professionnels** (Modern & Professional)
- 🎨 **Détection automatique** des couleurs de marque de l'entreprise
- 📄 **Génération PDF** haute qualité (compatible ATS)
- 🖥️ **Interface web intuitive** avec Streamlit
- ⚡ **100% gratuit et illimité**

## 🚀 Installation

### 1. Prérequis

- Python 3.9 ou supérieur
- pip (gestionnaire de paquets Python)

### 2. Installer Ollama

**macOS / Linux :**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Windows :**
Téléchargez l'installateur depuis : https://ollama.com/download

### 3. Télécharger le modèle d'IA

Une fois Ollama installé, téléchargez le modèle recommandé :

```bash
ollama pull qwen2.5:7b
```

> **Pourquoi qwen2.5:7b ?** Excellent pour l'extraction structurée de données (JSON), rapide, et fonctionne bien en français et anglais.

**Modèles alternatifs :**
```bash
# Plus léger (plus rapide, moins précis)
ollama pull qwen2.5:3b

# Alternative
ollama pull llama3.1:8b
```

### 4. Installer le projet CV Generator

```bash
# Cloner le repository
git clone https://github.com/SephyrothC/CV_generator
cd CV_generator

# Créer un environnement virtuel (recommandé)
python -m venv venv

# Activer l'environnement
# Sur Windows
venv\Scripts\activate

# Sur macOS/Linux
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
```

### 5. Configuration (optionnel)

Le fichier `.env` n'est plus obligatoire ! Mais si vous voulez changer de modèle :

```bash
cp .env.example .env
# Éditez .env si vous voulez utiliser un autre modèle
```

## 📖 Utilisation

### 1. Lancer Ollama

Dans un premier terminal, lancez Ollama :

```bash
ollama serve
```

> **Note :** Laissez ce terminal ouvert pendant l'utilisation

### 2. Préparer votre profil

Éditez le fichier `data/profile.json` avec vos informations (un exemple complet est fourni).

### 3. Lancer l'application

Dans un second terminal :

```bash
streamlit run app.py
```

L'application s'ouvrira automatiquement dans votre navigateur (http://localhost:8501)

### 4. Workflow

1. **Vérifiez le statut Ollama** (dans la sidebar) - doit être vert ✅
2. **Chargez votre profil** (clic dans la sidebar)
3. **Collez l'offre LinkedIn** (description complète)
4. **Analysez avec l'IA** (extraction automatique) - ~5-15 secondes
5. **Personnalisez** (sélection intelligente) - ~10-20 secondes
6. **Ajustez** (résumé, points forts, couleurs)
7. **Générez le PDF** final

## 🎨 Templates disponibles

- **Modern** : Design moderne avec sidebar colorée (idéal pour tech/créatif)
- **Professional** : Design classique et élégant (parfait pour corporate)

## 🤖 Modèles d'IA Recommandés

| Modèle | Taille | Vitesse | Précision | Usage RAM | Recommandé pour |
|--------|--------|---------|-----------|-----------|-----------------|
| `qwen2.5:7b` | 4.7 GB | ⚡⚡⚡ | ⭐⭐⭐⭐⭐ | ~8 GB | **Recommandé** - Meilleur équilibre |
| `qwen2.5:3b` | 2.0 GB | ⚡⚡⚡⚡ | ⭐⭐⭐⭐ | ~4 GB | Machines avec peu de RAM |
| `llama3.1:8b` | 4.7 GB | ⚡⚡⚡ | ⭐⭐⭐⭐ | ~8 GB | Alternative fiable |
| `mistral:7b` | 4.1 GB | ⚡⚡⚡ | ⭐⭐⭐ | ~6 GB | Autre option |

### Changer de modèle

```bash
# Télécharger un autre modèle
ollama pull llama3.1:8b

# Il apparaîtra automatiquement dans le sélecteur de l'interface
```

## ⚡ Performances

**Temps de réponse moyens (qwen2.5:7b) :**
- **Avec GPU** (NVIDIA) : 2-5 secondes
- **Avec CPU** (moderne) : 5-15 secondes par requête

Ollama utilise automatiquement votre GPU s'il est disponible (NVIDIA avec CUDA).

## 📊 Exemple d'utilisation

### Offre d'emploi exemple

```
Développeur Full Stack Senior - Google
Paris, France

Nous recherchons un développeur Full Stack Senior passionné.

Compétences requises :
- React, TypeScript, Node.js
- PostgreSQL, Redis
- Docker, AWS
- 5+ ans d'expérience

Compétences appréciées :
- GraphQL, Microservices, CI/CD
```

L'IA va automatiquement :
- Extraire "Google" comme entreprise
- Identifier les technologies (React, Node.js, etc.)
- Sélectionner vos expériences avec ces technologies
- Créer un résumé adapté

## 🐛 Résolution de problèmes

### ❌ "Ollama n'est pas disponible"

**Solution :**
```bash
# Vérifier qu'Ollama est installé
ollama --version

# Lancer Ollama
ollama serve

# Dans un autre terminal, vérifier la connexion
curl http://localhost:11434
```

### ❌ "Le modèle n'est pas installé"

**Solution :**
```bash
# Lister les modèles installés
ollama list

# Télécharger le modèle
ollama pull qwen2.5:7b
```

### ⏱️ Réponses trop lentes

**Solutions :**
1. Utilisez un modèle plus léger : `ollama pull qwen2.5:3b`
2. Vérifiez si votre GPU est utilisé : `ollama ps`
3. Fermez les applications gourmandes en mémoire

### 🔧 JSON invalides

**Solutions :**
1. Le modèle `qwen2.5:7b` est le meilleur pour le JSON
2. Assurez-vous d'utiliser la dernière version d'Ollama
3. Réessayez - parfois le modèle échoue aléatoirement

### Erreur lors de la génération du PDF

- **Linux** : `sudo apt-get install libpango-1.0-0 libpangoft2-1.0-0`
- **macOS** : `brew install pango`
- **Windows** : Installez GTK+ Runtime

## 💡 Conseils d'utilisation

### Profil de base
- ✅ Soyez exhaustif : ajoutez TOUTES vos expériences et compétences
- ✅ Soyez précis : utilisez des verbes d'action et des chiffres
- ✅ Respectez le format JSON

### Offres d'emploi
- ✅ Copiez le texte complet de l'offre LinkedIn
- ✅ Incluez la description, les compétences et les qualifications
- ✅ Plus l'offre est détaillée, meilleure sera la personnalisation

### Performances
- ✅ La première requête est souvent plus lente (chargement du modèle)
- ✅ Les requêtes suivantes sont plus rapides (modèle en cache)
- ✅ Sur GPU, c'est 5-10x plus rapide qu'en CPU

## 📁 Structure du projet

```
CV_generator/
├── data/
│   └── profile.json          # Votre profil complet
├── templates/
│   ├── modern.html           # Template moderne
│   └── professional.html     # Template professionnel
├── generated/                 # CV générés (PDF et HTML)
├── src/
│   ├── ollama_client.py      # Client Ollama
│   ├── analyzer.py           # Analyse d'offres avec IA
│   ├── ai_adapter.py         # Personnalisation avec IA
│   ├── pdf_generator.py      # Génération de PDF
│   ├── color_matcher.py      # Détection couleurs entreprise
│   ├── profile_manager.py    # Gestion du profil
│   └── models.py             # Modèles de données
├── app.py                     # Application Streamlit
├── requirements.txt           # Dépendances Python
├── .env.example              # Exemple de configuration
└── README.md                 # Ce fichier
```

## ❓ FAQ

**Q : Est-ce vraiment gratuit ?**
R : Oui ! 100% gratuit et illimité. Aucun coût, aucune inscription.

**Q : Mes données sont-elles privées ?**
R : Absolument ! Tout fonctionne en local sur votre machine. Aucune donnée n'est envoyée sur Internet.

**Q : Puis-je utiliser sans Internet ?**
R : Oui, une fois Ollama et le modèle installés, tout fonctionne hors ligne.

**Q : Quelle est la différence avec Claude/ChatGPT ?**
R : Les modèles locaux sont moins "intelligents" mais largement suffisants pour cette tâche. Et c'est gratuit !

**Q : Combien de CV puis-je générer ?**
R : Illimité ! Aucune restriction.

**Q : Mon GPU sera-t-il utilisé ?**
R : Oui, Ollama détecte et utilise automatiquement les GPU NVIDIA (avec CUDA).

## 🔄 Comparaison : Avant vs Maintenant

| Aspect | Avant (API Anthropic) | Maintenant (Ollama) |
|--------|----------------------|---------------------|
| Coût | ~$0.01-0.05 par CV | **Gratuit** |
| Limite | Selon crédit API | **Illimité** |
| Vitesse | ~2-3 secondes | 5-15 secondes (CPU) |
| Confidentialité | Données envoyées à Anthropic | **100% local** |
| Internet requis | Oui | Non (après installation) |
| Installation | Simple | Nécessite Ollama |

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Signaler des bugs
- Proposer des améliorations
- Ajouter de nouveaux templates
- Tester d'autres modèles Ollama

## 📝 Licence

Ce projet est sous licence MIT. Utilisez-le librement !

## 🙏 Remerciements

- [Ollama](https://ollama.com) pour la plateforme d'IA locale
- [Qwen Team](https://qwenlm.github.io/) pour les excellents modèles
- [Streamlit](https://streamlit.io) pour le framework web
- [WeasyPrint](https://weasyprint.org) pour la génération PDF

---

**💚 100% Gratuit • 🔒 100% Privé • ⚡ 100% Local**

**Bonne génération de CV ! 🚀**
