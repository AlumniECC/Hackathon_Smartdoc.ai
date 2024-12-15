# Chat with SFCR documents

Cette application fournit une interface de chat interactive pour explorer et interroger des documents textuels à l'aide des modèles Gemini de Google Generative AI. Conçue pour gérer jusqu'à quatre fichiers texte simultanément, l'application permet des conversations intelligentes et contextuelles, simplifiant la recherche d'informations et l'analyse documentaire.  

## Fonctionnalités  

L'application s'appuie sur les modèles SOTA Gemini de Google Generative AI, incluant Gemini Pro, Pro Vision et Ultra. Elle prend en charge le téléversement de plusieurs documents (jusqu'à 4 fichiers) et les transforme en indices vectoriels à l'aide de LlamaIndex. Le moteur de chat personnalisé interagit avec les documents, offrant des réglages configurables pour la créativité (température), la limite de tokens et d'autres paramètres. L'interface interactive Streamlit facilite l'utilisation, permettant de téléverser des fichiers, de configurer des paramètres et de discuter avec les documents.  

## Fonctionnement  

L'application suit un processus clair :  
1. **Configuration initiale** : L'application initialise les clés API, les modèles GEMINI et les indices vectoriels.  
2. **Téléversement de documents** : Les utilisateurs téléversent des fichiers texte via la barre latérale (sidebar). Ces fichiers sont segmentés en blocs et indexés pour permettre une recherche et un traitement efficaces.  
3. **Chat interactif** : Les utilisateurs posent des questions ou demandent des informations à partir des documents téléversés, et le système génère des réponses basées sur la similarité sémantique et l'inférence des modèles.  
4. **Ajustements en temps réel** : Les paramètres des modèles et le contexte des conversations peuvent être modifiés dynamiquement pour affiner les réponses.  

## Aperçu technique  

L'application est construite avec Streamlit pour l'interface interactive, utilise le SDK de Google Generative AI pour interagir avec les modèles Gemini et exploite LlamaIndex pour le traitement et l'indexation des documents. Les documents sont divisés en blocs de 512 tokens (avec un chevauchement de 50 tokens) pour une intégration et une requête optimales. Les embeddings sont générés à l'aide des modèles d'intégration de Gemini pour une représentation sémantique précise. De plus, un système de journalisation intégré enregistre les activités de l'application et les erreurs pour faciliter le débogage.  

## Configuration
Les paramètres de l'application sont définis dans la classe AppConfig :

Taille des blocs : 512 tokens (par défaut)
Limite de tokens : 1024 tokens par réponse
Température : 0,3 (valeur par défaut pour la créativité)
Fichier de journalisation : app.log

## Déploiement avec Docker  
1- Construisez l'image Docker :
```bash 
docker build -t rag .
```
2- Exécutez le conteneur Docker :
```bash
docker run -p 5000:5000 rag
```

3 - Accédez à l'application via votre navigateur à l'adresse suivante :
```bash
http://localhost:5000
```


