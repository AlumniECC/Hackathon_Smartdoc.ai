# README: Hackathon SmartDoc.ai

## Equipe 2

Ce projet a été réalisé dans le cadre du hackathon SmartDoc.ai, ayant pour objectif principal le traitement de documents financiers au format PDF pour en extraire uniquement les contenus pertinents à l'aide d'outils NLP. Voici une description des étapes réalisées lors de la première partie de cet exercice.

---
<details>
<summary>Premiere partie</summary>

## 1. Traitement des Données OCR

### Fonctionnalités Utilisées :
La fonction **`produce_brut()`** fournie dans le fichier `helper.py` (que l'on a gardé comme telle) a été utilisée telle quelle pour transformer les fichiers JSON obtenus à partir de l'OCR (Google Vision API) en un tableau Excel structurant les blocs textuels extraits des rapports SFCR. Cette fonction constitue la base des analyses effectuées dans les étapes suivantes.

---

## 2. Détection et Labélisation des Contenus

### Objectifs :
L'objectif principal était de classifier automatiquement les blocs textuels extraits des rapports SFCR en trois catégories :
- **Inutile** : Contenus non pertinents comme les bas de page, hauts de page et tableaux.
- **Paragraphe** : Contenus informatifs pertinents pour le corps principal des rapports.
- **Titre** : Grands titres ou sous-titres délimitant les différentes sections des rapports.

### Approche Technique :
Pour cette étape, une fonction nommée **`label_content(df, thresholds=None)`** a été développée dans le fichier `google_vision_api/report_cleaning.ipynb`. Elle repose sur des seuils définis pour différencier les catégories de contenu.

#### Fonctionnement de `label_content()` :
1. **Seuils Utilisés :**
   - Position verticale (`pos_y`) pour les en-têtes et pieds de page.
   - Nombre de caractères (`chars`) pour distinguer titres et paragraphes.
   - Taille des caractères et hauteur des blocs (`char_size`, `height`) pour identifier le contenu des tableaux.

2. **Classification :** Chaque bloc textuel est évalué selon ces seuils pour être classifié en "Inutile", "Titre" ou "Paragraphe". Par exemple :
   - Si la position verticale est proche des bords (haut ou bas de page), il est marqué comme "Inutile".
   - Si le nombre de caractères est très faible, il est marqué comme "Titre".
   - Si le nombre de caractères est élevé, il est considéré comme "Paragraphe".

### Filtrage et Génération des Fichiers Texte :
Une fois la labélisation effectuée, les données inutiles sont filtrées pour ne conserver que les titres et paragraphes pertinents. Le contenu résultant est ensuite sauvegardé dans un fichier texte suivant une organisation claire :
- Les titres et paragraphes sont regroupés par page.
- Une ligne de séparation est ajoutée entre les pages pour une meilleure lisibilité.

#### Exemple de Code :
Le fichier généré est produit à l'aide de la fonction suivante :
```python
# Fonction pour générer un fichier texte organisé
 def generate_text(dataframe, filename):
     with open(filename, 'w', encoding='utf-8') as f:
         current_page = None
         for _, row in dataframe.iterrows():
             if current_page is None or row['num_page'] != current_page:
                 if current_page is not None:
                     f.write("\n" + "="*50 + "\n")  # Séparateur pour une nouvelle page
                 current_page = row['num_page']
                 f.write(f"\nPage {current_page}\n")

             if row['Label'] == 'Titre':
                 f.write(f"\n{row['text']}\n")
             elif row['Label'] == 'Paragraphe':
                 f.write(f"{row['text']}\n")

             f.write("\n")
```

### Résultats :
- **Classification Automatisée :** Les blocs textuels sont correctement identifiés et classés.
- **Fichiers Lisibles :** Les fichiers texte produits sont clairs et organisés par page avec une distinction nette entre les titres et les paragraphes.

### Analyse :
La labélisation a été fait 

---

## Conclusion :
Ces étapes ont permis d'établir une base solide pour l'analyse des rapports SFCR en filtrant efficacement le contenu utile. Les techniques de traitement et de labélisation développées ici préparent à la deuxième partie de l'exercice, centrée sur l'implémentation d'une architecture RAG.

</details>