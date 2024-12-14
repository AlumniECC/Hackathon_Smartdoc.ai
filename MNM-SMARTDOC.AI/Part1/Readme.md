# Extraction et Analyse de Données OCR

Ce projet utilise des données OCR (Reconnaissance Optique de Caractères) pour extraire des informations textuelles et les organiser sous forme de DataFrame. Le fichier JSON source contient des données structurées issues d'un processus OCR.

## Fonctionnalités principales

1. *Extraction de données :*
   - Chargement de fichiers JSON contenant les résultats OCR.
   - Extraction de texte et de caractéristiques géométriques (dimensions, positions, etc.).

2. *Prétraitement des données :*
   - Calcul des caractéristiques telles que la largeur, la hauteur, l'aire, et le ratio d'aspect des éléments textuels.

3. *Organisation des données :*
   - Structuration des données extraites dans un DataFrame pour une analyse ultérieure.

4. *Export des résultats :*
   - Sauvegarde des données traitées dans un fichier CSV.

## Prérequis

- Python 3.x
- Librairies Python nécessaires :
  - pandas
  - numpy
  - scikit-learn
  - json

Installez les dépendances avec la commande suivante :
bash
pip install pandas numpy scikit-learn


## Utilisation

1. *Charger un fichier JSON :*
   - Placez vos fichiers JSON dans le dossier data/ocr.

2. *Exécuter le Notebook :*
   - Lancez les cellules pour traiter un fichier JSON spécifique. Exemple :
     python
     produce_brut("allianz-1-to-94")
     

3. *Exporter les résultats :*
   - Les données traitées seront sauvegardées dans un fichier CSV :
     python
     produce_brut("allianz-1-to-94").to_csv("dataframe.csv", index=False, encoding='utf-8')
     
   - Vous pouvez ensuite télécharger ou analyser le fichier dataframe.csv.

## Structure du projet


|-- data/
|   |-- ocr/
|       |-- [fichiers JSON sources]
|-- notebook.ipynb
|-- README.md


## Auteurs

Ce projet a été conçu pour extraire et structurer les données OCR d'une manière standardisée et accessible. Vous êtes libre de le modifier et de l'améliorer selon vos besoins.
