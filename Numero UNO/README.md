# README: Hackathon SmartDoc.ai
## L'Équipe 1 : Número UNO 
- Imad Assouabi
- Adam Ammour

En tant qu'élèves en première année cycle ingénieur centralien intéréssé par la data science et l'IA, nous avons saisi l'occasion de ce hackathon pour se plonger dans le monde de la data science, découvrir et affiner nos compétences. Nous aimerons par ailleurs remercier Imad Zaoug, Marouane Maamar ainsi que la communauté ECC Alumni et le club Centrale Tech pour leur travail acharné afin de réussir ce hackathon dans sa première édition.  
Noua avons essayé d'appliquer les notions acquises dans les workshops et de faire un effort pour implémenter des nouvelles techniques afin de répondre aux différents défis des trois parties de ce hackathon.   

  ---  
# Partie 1 (nettoyage et traitement des rapports SFCR) :
## Méthode 1 (Positions OCR) :  
Étapes principales :  
  
### 1. Analyse de l’output de produce_brut() :
   
- Étudier les colonnes du fichier Excel produit.

- Identifier les attributs pertinents pour détecter les bas de pages, les hauts de pages, les tableaux, etc.

### 2. Détection des contenus inutiles :  

- Analyser les motifs récurrents pour les bas de pages/hauts de pages (ex. : numéros de pages, titres répétitifs, mentions légales, etc.).  

- Identifier les caractéristiques des contenus de tableaux (position, alignement, etc.).

### 3. Identification des paragraphes et titres :  

- Détecter les paragraphes basés sur leur longueur, ponctuation, ou structure textuelle.  

- Reconnaître les titres grâce à des indices comme :  

  **Style** : texte en majuscules, gras ou souligné.  
  
  **Position** : titres souvent alignés à gauche/centre ou au début d’une section.

### 4. Labélisation des données :  

Ajouter une colonne "Label" et assigner les valeurs :  

- **Inutile** : pour les contenus détectés comme bas de page/haut de page/tableaux.  

- **Paragraphe** : pour les blocs de texte continus.  

- **Titre** : pour les blocs identifiés comme des titres.

## Méthode 2 (approche hybride incluant un modèle NLP) :  
### Description :  

Il s'agit de la combinaison de la segmentation visuelle (positions OCR) avec un modèle NLP pour comprendre la structure et le contexte des données dans les tableaux.  

#### Étapes :
- Utiliser les métadonnées (positions) pour segmenter les blocs formant les tableaux.  

- Passer chaque ligne dans un modèle NLP (BERT) pour comprendre sémantiquement les en-têtes, les catégories, et les relations.  

- Reconstruiser le tableau dans un format structuré.

#### Avantages :  
  
- Prendre en compte à la fois les aspects visuels et textuels.  

- Gérer mieux les tableaux contenant des relations complexes.
#### Analyse :  
- Vision (métadonnées OCR) :
Permet de capturer les relations visuelles essentielles pour les tableaux.
Exploite les positions (pos_x, pos_y), les tailles, et les alignements pour reconstruire des relations complexes.
- NLP :
À travers un modèle pré-entraîné Hugging Face, on ajoutera une compréhension contextuelle et sémantique des blocs textuels (par ex., différencier les titres des colonnes des données).
**Gestion des Cas Complexes :**
- Colonnes fusionnées ou titres imbriqués : Gérés grâce à une combinaison d’alignement visuel et de classification NLP.  
- Tableaux désorganisés ou mal alignés : Les métadonnées OCR permettent de détecter et regrouper les blocs liés, même s’ils ne sont pas strictement alignés.
#### Contraintes rencontrées :  
Ce modeèle NLP de Hugging Face utilisé en fait nécessite un fine-tuning, donc nous avons essayé de l'entraîner sur une database contenant les deux colonnes `text` et `label`; nous avons choisi de travailler avec la dataframe générée par la première méthode.  
```python 
# Charger le modèle avec le bon nombre de labels
model = DistilBertForSequenceClassification.from_pretrained("distilbert-base-uncased", num_labels=3)
import os
os.environ["WANDB_DISABLED"] = "true"
# Définir les arguments d'entraînement
training_args = TrainingArguments(
    output_dir="./results",          # Répertoire pour sauvegarder les modèles
    eval_strategy="epoch",    # Évaluer à chaque epoch
    learning_rate=2e-5,             # Taux d'apprentissage
    per_device_train_batch_size=16, # Batch size pour entraînement
    per_device_eval_batch_size=16,  # Batch size pour validation
    num_train_epochs=3,             # Nombre d'epochs
    weight_decay=0.01,              # Regularisation L2
    logging_dir="./logs",           # Répertoire pour logs
    logging_steps=10                # Logs tous les 10 pas
)

# Configurer le Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset
)

# Entraîner le modèle
trainer.train()

# Sauvegarder le modèle fine-tuné
model.save_pretrained("./fine_tuned_distilbert")
tokenizer.save_pretrained("./fine_tuned_distilbert")
print("Modèle fine-tuné sauvegardé !")
```
  ---

# Partie Bonus (Extraction des tableaux à partir des rapports PDF) :  
## Méthode 1 (avec API Viaion) : 
### Éxplication de l'approche :  
#### Extraction des tableaux depuis un PDF :  
- Le programme utilise `pdfplumber` pour extraire chaque page du fichier PDF.  
- Chaque page est convertie en une image avec pdfplumber et ensuite en niveaux de gris à l'aide d'OpenCV.  
- La détection des contours des tableaux s'effectue avec des opérations morphologiques (cv2.erode, cv2.dilate) et l'algorithme Canny Edge Detection.  
- Les tableaux détectés sont extraits sous forme de "Régions d'Intérêt" (ROI).  

  
#### Reconnaissance optique de caractères (OCR) :  

- `pytesseract` est utilisé pour lire le texte contenu dans chaque tableau extrait. Le paramètre --psm 6 indique à Tesseract de traiter l'image en tant que tableau structuré.  
- Le texte extrait est divisé ligne par ligne et converti en listes pour structurer les données.  

#### Conversion en DataFrames :  

- Chaque tableau est transformé en un DataFrame Pandas avec pd.DataFrame.  
- Les petits blocs (moins de 50 pixels en largeur et 20 en hauteur) sont ignorés pour éviter les faux positifs.    

#### Affichage des résultats :  

- Les DataFrames extraits sont simplement affichés dans la console.

## Méthode 2 (avec la bibliothèque PdfPlumbe) : 


#### Explication du Code

##### Fonction `extract_tables_with_pdfplumber`
- **Objectif** : Extraire les tableaux d'un fichier PDF sous forme de **DataFrames** en utilisant la bibliothèque `pdfplumber`.
- **Étapes** :
  1. Le fichier PDF est ouvert avec `pdfplumber`.
  2. Chaque page est parcourue pour détecter les tableaux grâce à la méthode `extract_tables`.
  3. Chaque tableau extrait est transformé en **DataFrame**.
  4. Les DataFrames sont ajoutés à une liste pour être retournés.


##### Bloc Principal (`__main__`)
- **Objectif** : Exécuter la fonction et afficher les résultats.
- **Vérifications** :
  - Si le fichier PDF existe, le programme procède à l'extraction.
  - Sinon, un message d'erreur est affiché pour signaler l'absence du fichier.
- **Affichage** :
  - Chaque **DataFrame extrait** est affiché sur la console avec un index, ce qui permet une identification facile des tableaux.


#### Analyse du Code

##### 1. Utilisation de `pdfplumber`
- La bibliothèque `pdfplumber` est **très efficace** pour extraire les tableaux des fichiers PDF.
- Elle détecte automatiquement les tableaux structurés et les retourne sous forme de **liste de listes**, ce qui est idéal pour la manipulation en Python.


##### 2. DataFrames avec Pandas
- Les tableaux extraits sont convertis en **DataFrames Pandas**.
- **Avantages** :
  - Pandas permet une **manipulation simple** des données pour des tâches comme le nettoyage, le filtrage ou l'agrégation.
  - Les DataFrames sont facilement exploitables pour des analyses avancées ou des visualisations.

  

##### 3. Simplicité et Modularité
- Le code est bien structuré avec :
  - Une fonction principale dédiée à l'extraction.
  - Un bloc d'exécution clair qui gère les entrées et les résultats.
- **Extensibilité** :
  - Ce code peut être facilement étendu pour inclure d'autres fonctionnalités comme le nettoyage des données extraites ou leur exportation vers différents formats (ex : CSV, Excel).

  ---

# Partie 2 (Architecture RAG pour les rapports SFCR) :
## Aperçu de l'Architecture

### 1. **Choix du modèle de langage (LLM)**

Nous avons sélectionné GPT-4 pour les raisons suivantes :

- **Performance :** Excellente capacité à comprendre et générer des réponses à des requêtes financières complexes.
- **Compréhension contextuelle :** Gère de grands contextes, ce qui est crucial pour les documents SFCR.
- **Facilité d'intégration :** Pris en charge par des API fiables, permettant une intégration transparente dans le pipeline.

### 2. **Stratégie de découpage des documents**

Pour assurer un traitement efficace des documents SFCR volumineux :

- **Méthode :** Utilisation de `RecursiveCharacterTextSplitter` avec une taille de segment de 800 caractères et un chevauchement de 100 caractères.
- **Objectif :** Conserver la cohérence sémantique tout en optimisant la recherche et la génération.

### 3. **Modèle d'embedding**

Pour la vectorisation, les embeddings OpenAI ont été utilisés en raison de leur :

- **Haute précision :** Capture efficacement les nuances sémantiques.
- **Compatibilité :** S'intègre parfaitement avec FAISS pour le stockage des vecteurs.

### 4. **Moteur de recherche vectorielle : FAISS**

FAISS (Facebook AI Similarity Search) est utilisé pour l'indexation et la récupération des vecteurs :

- **Scalabilité :** Gestion efficace des ensembles de données volumineux.
- **Rapidité :** Recherches de similarité quasi-instantanées.

---

## Fonctionnalités clés

### **Fonctionnalité hors ligne**

Pour permettre une exécution hors ligne, le système prend en charge des alternatives open-source comme Sentence-BERT pour les embeddings et un modèle de réponse basé sur les transformers Hugging Face.

#### Mise en œuvre

1. Remplacer les embeddings basés sur l'API OpenAI par Sentence-BERT.
2. Utiliser le `pipeline` de Hugging Face pour les tâches de questions-réponses.

### **Fonctionnalités avancées de recherche**

Améliorez l'expérience utilisateur avec :

- **Filtrage sémantique :** Permettre un filtrage par sujets, sections ou mots-clés.
- **Correspondance par mots-clés :** Combiner la compréhension sémantique avec la précision basée sur les mots-clés.

### **Téléchargement et analyse des PDFs**

Permettre le téléchargement direct des rapports SFCR au format PDF en utilisant des bibliothèques comme `pdfplumber` pour extraire le contenu textuel.

#### Exemple de code

```python
import pdfplumber

def parse_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        text = "\n".join(page.extract_text() for page in pdf.pages)
    return text
```

### **Visualisations interactives**

Ajoutez des visualisations dynamiques pour l'exploration des données :

- **Tableaux de bord Plotly :** Visualiser les ratios de solvabilité, les indicateurs de risque et les tendances.
- **Mise en évidence des récupérations :** Utilisez des surlignages colorés pour afficher les segments de texte pertinents.

#### Exemple de code

```python
import plotly.express as px

def visualize_solvent_ratios(data):
    fig = px.bar(data, x='Year', y='Solvency Ratio', title='Ratios de solvabilité au fil du temps')
    fig.show()
```

## Explicabilité

Inclure des explications pour les réponses récupérées :

- Mettre en évidence les segments de texte spécifiques utilisés dans la réponse.
- Afficher les scores de confiance pour les récupérations et les prédictions.

---

## Fonctionnalités principales

### 1. **Chatbot interactif**

L'application permet aux utilisateurs de :

- Télécharger des rapports SFCR (PDF ou texte).
- Poser des questions spécifiques liées aux risques financiers, aux ratios de solvabilité ou à la performance de l'entreprise.
- Recevoir des réponses détaillées avec le texte source référencé.

#### Étapes

1. Lancez l'application Streamlit avec :
   ```bash
   streamlit run main.py
   ```
2. Téléchargez un document SFCR.
3. Saisissez une question dans la boîte de texte (par exemple : "Quels sont les ratios de solvabilité ?").
4. Visualisez la réponse avec le texte source récupéré.

### 2. **Exemples de questions**

- *Quels sont les principaux risques identifiés dans le SFCR ?*
- *Quels sont les ratios de solvabilité rapportés ?*
- *Décrivez la stratégie de gestion des risques mentionnée dans le document.*
- *Quel est le résumé des performances financières pour l'année ?*

### 3. **Visualisations interactives**

Après le traitement du document, les utilisateurs peuvent visualiser des graphiques, tendances et indicateurs clés.

- **Graphiques en barres :** Afficher les ratios de solvabilité sur plusieurs années.
- **Graphiques circulaires :** Montrer les catégories de distribution des risques.

### 4. **Comparaison des approches**

Démontrez la supériorité de l'implémentation actuelle :

- Comparez la précision des réponses et la latence par rapport aux modèles de référence.
- Présentez des exemples de récupération à partir de systèmes concurrents (si disponibles).

#### Métriques de comparaison

- Précision de récupération.
- Latence (temps de réponse).
- Scores de satisfaction utilisateur.

---

## Tests

### 1. **Tests unitaires**

Créez des cas de test pour le découpage, l'analyse PDF et les fonctionnalités du pipeline :

```python
import unittest
from rag_pipeline import chunk_document
from pdf_parser import parse_pdf

class TestPipeline(unittest.TestCase):
    def test_chunk_size(self):
        text = "Exemple de texte " * 50
        chunks = chunk_document(text, chunk_size=100, chunk_overlap=20)
        self.assertTrue(all(len(chunk) <= 100 for chunk in chunks))

    def test_parse_pdf(self):
        text = parse_pdf('sample_report.pdf')
        self.assertTrue(len(text) > 0)

if __name__ == "__main__":
    unittest.main()
```

Exécutez les tests :

```bash
python -m unittest discover -s tests
```

---

## Conclusion

Ce projet fournit une architecture RAG robuste adaptée aux rapports SFCR. Il intègre des fonctionnalités hors ligne, des options de recherche avancées, l'analyse de PDFs et des visualisations interactives, garantissant une solution complète et conviviale.

### Principaux avantages

1. **Fonctionnalité hors ligne :** Fonctionne sans API externes grâce à Sentence-BERT et aux transformers Hugging Face.
2. **Recherche avancée :** Permet une récupération sémantique et basée sur les mots-clés pour une précision accrue.
3. **Explicabilité :** Fournit des réponses transparentes en montrant les segments source.
4. **Analyse PDF :** Simplifie le flux de travail avec des téléchargements directs.
5. **Visualisations :** Améliore les insights grâce à des graphiques dynamiques.
