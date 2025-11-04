# 🚀 Guide de Démarrage Rapide

Ce guide vous permet de lancer le générateur de CV en 5 minutes !

## ⚡ Installation Express

```bash
# 1. Installer les dépendances
pip install -r requirements.txt

# 2. Configurer la clé API
cp .env.example .env
# Éditez .env et ajoutez : ANTHROPIC_API_KEY=votre_clé_api

# 3. Lancer l'application
streamlit run app.py
```

## 📝 Premier CV en 3 Étapes

### 1. Personnalisez votre profil

Éditez `data/profile.json` avec vos informations :
- Informations personnelles
- Expériences professionnelles
- Compétences
- Projets
- Formation

### 2. Trouvez une offre LinkedIn

Copiez le texte complet d'une offre d'emploi LinkedIn (description + compétences requises).

### 3. Générez votre CV

1. Ouvrez l'application dans votre navigateur (http://localhost:8501)
2. Cliquez sur "📂 Charger le profil" dans la barre latérale
3. Collez l'offre d'emploi dans la zone de texte
4. Cliquez sur "🔍 Analyser l'offre"
5. Cliquez sur "✨ Personnaliser avec l'IA"
6. Ajustez si nécessaire (résumé, couleurs, etc.)
7. Cliquez sur "📄 Générer PDF"

**C'est tout !** Votre CV personnalisé est prêt. 🎉

## 💡 Exemple d'offre à tester

```
Développeur Full Stack Senior - Google
Paris, France

Nous recherchons un développeur Full Stack Senior passionné pour rejoindre notre équipe.

Responsabilités :
- Développer et maintenir des applications web
- Collaborer avec l'équipe produit
- Participer aux code reviews

Compétences requises :
- React, TypeScript
- Node.js, Express
- PostgreSQL
- Docker, AWS
- 5+ ans d'expérience

Compétences appréciées :
- GraphQL
- Microservices
- CI/CD
```

Copiez-collez cet exemple dans l'application pour tester !

## 🎨 Templates Disponibles

- **Modern** : Design moderne avec sidebar colorée (recommandé pour tech)
- **Professional** : Design classique et élégant (recommandé pour corporate)

Changez de template dans la barre latérale avant de générer le PDF.

## ❓ Problèmes Courants

### "ANTHROPIC_API_KEY non trouvée"
👉 Créez le fichier `.env` et ajoutez votre clé API Anthropic.

### Erreur lors de l'installation de WeasyPrint
**Sur Linux :**
```bash
sudo apt-get install libpango-1.0-0 libpangoft2-1.0-0
```

**Sur macOS :**
```bash
brew install pango
```

**Sur Windows :**
Téléchargez GTK+ Runtime depuis : https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer

## 📚 Plus d'Infos

- Documentation complète : voir [README.md](README.md)
- Structure du profil : voir [data/profile.json](data/profile.json)
- Templates : voir [templates/](templates/)

## 🎯 Prochaines Étapes

1. ✅ Générez votre premier CV
2. 📝 Personnalisez votre profil avec vos vraies informations
3. 🎨 Testez les différents templates
4. 🔍 Essayez avec plusieurs offres d'emploi
5. 🎨 Personnalisez les couleurs selon vos préférences

---

**Besoin d'aide ?** Consultez le [README.md](README.md) complet ou ouvrez une issue sur GitHub.
