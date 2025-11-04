# 🚀 Guide de Démarrage Rapide - IA Locale Gratuite !

Ce guide vous permet de lancer le générateur de CV avec **Ollama** (IA locale 100% gratuite) en moins de 10 minutes !

## ⚡ Installation Express

### 1. Installer Ollama

**macOS / Linux :**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Windows :**
Téléchargez depuis [https://ollama.com/download](https://ollama.com/download)

### 2. Télécharger le modèle d'IA

```bash
ollama pull qwen2.5:7b
```

> ⏱️ Premier téléchargement : ~5 minutes (4.7 GB)

### 3. Installer le projet

```bash
# Installer les dépendances Python
pip install -r requirements.txt
```

## 🎯 Lancer l'application

### Terminal 1 : Démarrer Ollama

```bash
ollama serve
```

> 💡 **Laissez ce terminal ouvert** pendant toute l'utilisation

### Terminal 2 : Lancer l'application

```bash
streamlit run app.py
```

L'application s'ouvrira automatiquement à [http://localhost:8501](http://localhost:8501)

## 📝 Premier CV en 4 Étapes

### 1. Vérifiez Ollama ✅

Dans l'interface, la sidebar doit afficher :
```
✅ Ollama actif - 1 modèle(s) disponible(s)
Modèle IA: qwen2.5:7b
```

### 2. Chargez votre profil

- Cliquez sur **"📂 Charger le profil"** dans la sidebar
- Un profil d'exemple est déjà pré-chargé !

### 3. Testez avec cette offre exemple

Copiez-collez cette offre dans la zone de texte :

```
Développeur Full Stack Senior - Google
Paris, France

Nous recherchons un développeur Full Stack Senior passionné pour rejoindre notre équipe produit.

Responsabilités :
- Développer des applications web performantes
- Collaborer avec l'équipe produit et design
- Participer aux code reviews
- Mentorer les développeurs juniors

Compétences requises :
- React, TypeScript
- Node.js, Express
- PostgreSQL
- Docker, AWS
- 5+ ans d'expérience en développement web

Compétences appréciées :
- GraphQL
- Microservices
- CI/CD
- Expérience en équipe Agile
```

### 4. Générez votre CV

1. Cliquez sur **"🔍 Analyser l'offre"** (⏱️ ~10 secondes)
2. Cliquez sur **"✨ Personnaliser avec l'IA"** (⏱️ ~15 secondes)
3. Ajustez si nécessaire (résumé, couleurs, etc.)
4. Cliquez sur **"📄 Générer PDF"**

**🎉 Votre CV personnalisé est prêt !**

## 🎨 Templates Disponibles

Changez de template dans la sidebar :

- **Modern** : Design moderne avec sidebar colorée (parfait pour tech)
- **Professional** : Design classique et élégant (parfait pour corporate)

## ⚡ Performances Attendues

**Temps de traitement (qwen2.5:7b) :**

| Étape | CPU | GPU (NVIDIA) |
|-------|-----|--------------|
| Analyse offre | ~10s | ~3s |
| Personnalisation | ~15s | ~5s |
| Génération PDF | ~2s | ~2s |

> 💡 **Première utilisation** : +5-10s pour charger le modèle en mémoire

## 🔧 Problèmes Courants

### ❌ "Ollama n'est pas disponible"

**Solution rapide :**
```bash
# Terminal 1
ollama serve
```

Puis relancez Streamlit.

### ❌ "Le modèle n'est pas installé"

**Solution :**
```bash
ollama pull qwen2.5:7b
```

### ⏱️ C'est trop lent !

**Solutions :**

1. **Modèle plus léger** (si <8 GB RAM) :
```bash
ollama pull qwen2.5:3b
```

2. **Vérifier si GPU est utilisé** :
```bash
ollama ps
# Si GPU utilisé, vous verrez "GPU: NVIDIA ..."
```

3. **Fermer les applications gourmandes** en mémoire

### 🔧 Réponses bizarres ou JSON invalide

**Solutions :**

1. **Réessayez** - parfois le modèle a besoin d'une 2e tentative
2. **Utilisez qwen2.5:7b** - meilleur pour le JSON structuré
3. **Mettez à jour Ollama** :
```bash
# macOS/Linux
curl -fsSL https://ollama.com/install.sh | sh

# Windows : re-téléchargez l'installateur
```

## 💡 Conseils pour de Meilleurs Résultats

### Pour l'analyse d'offres :
- ✅ Collez **tout le texte** de l'offre (description + compétences)
- ✅ Incluez l'entreprise et le titre du poste
- ✅ Plus c'est détaillé, mieux c'est !

### Pour personnaliser votre profil :
- ✅ Remplissez `data/profile.json` avec **toutes** vos expériences
- ✅ Listez **toutes** vos compétences (l'IA sélectionnera les pertinentes)
- ✅ Ajoutez des **chiffres** et des **résultats mesurables**

### Pour la personnalisation :
- ✅ Vérifiez toujours les suggestions de l'IA
- ✅ Ajustez le résumé selon votre style
- ✅ Modifiez les couleurs si vous préférez

## 🚀 Prochaines Étapes

Une fois que vous avez testé :

1. ✅ **Personnalisez votre profil**
   Éditez `data/profile.json` avec vos vraies informations

2. ✅ **Testez avec vos vraies offres LinkedIn**
   Copiez-collez des offres qui vous intéressent

3. ✅ **Générez plusieurs CV**
   Créez un CV adapté pour chaque candidature !

4. ✅ **Testez les 2 templates**
   Modern vs Professional - voyez ce qui vous convient

5. ✅ **Optimisez les performances**
   Si vous avez un GPU NVIDIA, Ollama l'utilisera automatiquement

## 📊 Modèles Alternatifs

Si `qwen2.5:7b` ne vous convient pas :

```bash
# Plus léger et rapide (mais moins précis)
ollama pull qwen2.5:3b

# Alternative populaire
ollama pull llama3.1:8b

# Pour les machines puissantes
ollama pull qwen2.5:14b
```

Changez de modèle dans le sélecteur de la sidebar.

## ❓ Questions Fréquentes

**Q : C'est vraiment gratuit et illimité ?**
R : Oui ! 100% gratuit, aucune limite, aucun coût caché.

**Q : Mes données CV sont-elles privées ?**
R : Absolument ! Tout reste sur votre machine. Aucune donnée n'est envoyée sur Internet.

**Q : Puis-je utiliser sans Internet ?**
R : Oui, après avoir téléchargé Ollama et le modèle.

**Q : Quelle RAM minimum ?**
R : 8 GB recommandés pour qwen2.5:7b (4 GB si vous utilisez qwen2.5:3b)

**Q : Ça fonctionne sur quel OS ?**
R : Windows, macOS, Linux - tous supportés !

## 📚 Ressources

- **Documentation complète** : [README.md](README.md)
- **Structure du profil** : [data/profile.json](data/profile.json)
- **Ollama** : [https://ollama.com](https://ollama.com)
- **Modèles disponibles** : [https://ollama.com/library](https://ollama.com/library)

---

## 🎯 Récapitulatif - 3 Commandes

```bash
# 1. Installer Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 2. Télécharger le modèle
ollama pull qwen2.5:7b

# 3. Installer le projet
pip install -r requirements.txt
```

**Puis lancez** :
```bash
# Terminal 1
ollama serve

# Terminal 2
streamlit run app.py
```

---

**💚 100% Gratuit • 🔒 100% Privé • ⚡ 100% Local**

**Besoin d'aide ?** Consultez le [README.md](README.md) complet.

**Bonne génération de CV ! 🚀**
