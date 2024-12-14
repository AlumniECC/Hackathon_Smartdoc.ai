

# Hackathon NLP: Analyse des Rapports SFCR avec RAG

## **Description du Projet**
Cette application **Streamlit** exploite une architecture innovante de **RAG (Retrieval-Augmented Generation)** pour analyser efficacement les rapports **SFCR (Solvency and Financial Condition Reports)**. L'objectif est de fournir une solution intuitive pour extraire, analyser, et répondre à des questions en langage naturel basées sur des documents financiers complexes.

### **Points Forts**
- Extraction automatisée de texte depuis des fichiers PDF.
- Traitement optimisé grâce à une segmentation intelligente des textes.
- Indexation rapide via des embeddings sémantiques et une base vectorielle performante.
- Réponses précises et contextualisées générées à l'aide de modèles GPT.

---

## **Fonctionnalités Principales**
1. **Téléchargement de fichiers PDF** :
   - Interface intuitive permettant de télécharger plusieurs documents simultanément.
2. **Extraction de texte** :
   - Conversion précise des documents PDF en texte brut grâce à `PyPDF2`.
3. **Segmentation intelligente des textes** :
   - Découpage des textes en **chunks** (segments) de 1000 caractères avec chevauchement de 200 caractères pour conserver le contexte.
4. **Création d'embeddings sémantiques** :
   - Utilisation des **OpenAI Embeddings** pour représenter chaque chunk sous forme de vecteurs.
5. **Recherche vectorielle** :
   - Identification des chunks pertinents via l'algorithme de similarité de **FAISS**.
6. **Réponses générées par GPT** :
   - Les réponses aux questions sont générées à partir des chunks identifiés et d'un prompt personnalisé.

---

## **Architecture Naïve RAG (Retrieval-Augmented Generation)**
La solution repose sur une approche hybride combinant la recherche d'information (retrieval) et la génération de texte (generation). Voici les étapes détaillées :

### **Étape 1 : Extraction des chunks pertinents**
- Les documents sont convertis en embeddings vectoriels, stockés dans **FAISS**.
- À chaque requête, les chunks les plus similaires sont identifiés.

### **Étape 2 : Augmentation par le contexte**
- Les chunks sélectionnés sont fournis au modèle GPT comme contexte.

### **Étape 3 : Génération des réponses**
- Les réponses sont produites à partir du modèle GPT en utilisant un prompt spécialement conçu.

![Architecture Naïve RAG](Rag.png)


## **Détails Techniques**

### **1. Modèle de Langage (LLM)**
- **Choix : ChatGPT** 
  - Reconnu pour sa capacité à traiter des documents financiers complexes avec une précision exceptionnelle.
  - Sa maîtrise du français en fait un outil adapté pour ce cas d'usage.

### **2. Approche de Chunking Optimisée**
- Le découpage des textes est réalisé via **RecursiveCharacterTextSplitter**, garantissant :
  - Une conservation optimale du contexte.
  - Une continuité dans la recherche de similarités.
  - Une analyse approfondie des sections pertinentes.

### **3. Embeddings Sémantiques**
- Générés par **OpenAI Embeddings**, les vecteurs sémantiques :
  - Capturent les nuances contextuelles et les relations conceptuelles.
  - Identifient efficacement les correspondances complexes dans le contenu.

### **4. Recherche Vectorielle avec FAISS**
- **FAISS (Facebook AI Similarity Search)** optimise la recherche grâce à :
  - Une indexation rapide et efficace, même pour des bases volumineuses.
  - Des temps de requête ultra-rapides (millisecondes).
  - Une utilisation optimisée des ressources système.

---

## **Pipeline de Traitement**
### **Étapes Clés**
1. **Prétraitement** :
   - Extraction de texte, découpage en chunks, et vectorisation.
2. **Recherche Sémantique** :
   - Identification des chunks les plus pertinents à l'aide de FAISS.
3. **Génération Contextuelle** :
   - Création de réponses précises guidées par un prompt personnalisé.



## **Démo Vidéo**
[Démo Vidéo](./DEMO.mp4)



## Prérequis
### 1. **Outils Nécessaires**
- Python 3.9 ou plus.
- Un accès à l'API OpenAI (clé API).
- Bibliothèques Python (listées dans `requirements.txt`).

### 2. **Installation des Dépendances**
Installez les dépendances avec la commande suivante :
```bash
pip install -r requirements.txt
```

### 3. **Configuration de l'environnement (.env)**
Créez un fichier `.env` à la racine du projet et ajoutez-y votre clé API OpenAI :
```plaintext
OPENAI_API_KEY=your_openai_api_key
```
### Pourquoi un fichier `.env` ?
Le fichier `.env` est utilisé pour sécuriser et centraliser la gestion des variables sensibles comme les clés API. En utilisant `dotenv`, l'application charge automatiquement ces variables sans les inclure directement dans le code.

## Lancer l'application
1. **Exécutez l'application Streamlit** :
   ```bash
   streamlit run app.py
   ```
2. **Accédez à l'application** :
   Ouvrez un navigateur et rendez-vous à l'adresse suivante :
   [http://localhost:8501](http://localhost:8501).

## Fonctionnalités de l'application
- **Téléchargement de Fichiers PDF** : Importez plusieurs documents PDF pour analyse.
- **Extraction de Texte** : Le contenu des fichiers est extrait et préparé pour l'analyse.
- **Recherche Sémantique** : Posez des questions sur les documents et obtenez des réponses précises grâce à l'architecture RAG.
- **Visualisation des Résultats** : Les réponses sont présentées directement dans l'interface.

## Structure du Projet
```plaintext
|-- app.py
|-- requirements.txt
|-- .env
|-- faiss_index/ (généré automatiquement pour stocker les embeddings)
```

## Exemples de Fonctionnement
### 1. **Téléchargement de Fichiers**
   - Chargez plusieurs fichiers PDF via la barre latérale.
   - Cliquez sur "Soumettre & Traiter" pour préparer les fichiers.

### 2. **Posez des Questions**
   - Entrez une question dans le champ de texte, par exemple :
     > Quelle est la solvabilité de l'entreprise en 2022 ?
   - Obtenez une réponse basée sur les données extraites.

### 3. **Réinitialisation**
   - Utilisez le bouton "Réinitialiser" pour supprimer les données et recommencer.

## Remarques
- Assurez-vous que vos fichiers PDF sont lisibles et bien formatés.
- Le système utilise FAISS pour la recherche vectorielle et OpenAI pour la génération de texte.

## Ressources
- [Streamlit Documentation](https://docs.streamlit.io/)
- [LangChain Documentation](https://docs.langchain.com/)
- [FAISS Documentation](https://faiss.ai/)
- [OpenAI API](https://platform.openai.com/docs/)

