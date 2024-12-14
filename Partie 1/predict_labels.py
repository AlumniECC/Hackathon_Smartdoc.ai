import xgboost as xgb
import joblib
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
import os
import sys

# Définir le dossier source par défaut ou celui donné en argument
input_folder = sys.argv[1] if len(sys.argv) > 1 else "data/csv"
output_folder = "data/csv_model"

# Créer le dossier de sortie s'il n'existe pas
os.makedirs(output_folder, exist_ok=True)

# Chargement du pipeline (scaler, pca)
print("Chargement du pipeline (scaler, pca)...")
scaler = joblib.load('classification/classifier/weights/scaler.pkl')
pca = joblib.load('classification/classifier/weights/pca.pkl')

pipeline = Pipeline([
    ('scaler', scaler),
    ('pca', pca)
])

# Chargement du modèle XGBoost sauvegardé au format JSON
print("Chargement du modèle XGBoost...")
bst_loaded = xgb.Booster()
bst_loaded.load_model("classification/classifier/weights/xgboost_classifier.json")

# Mapping des cibles
target_mapping = {
    0: "inutile",
    1: "paragraphe",
    2: "titre"
}

def map_prediction(prediction_encoded):
    return target_mapping.get(prediction_encoded, "Classe inconnue")

# Parcourir les fichiers CSV dans le dossier spécifié
for csv_file in os.listdir(input_folder):
    if csv_file.endswith(".csv"):
        csv_path = os.path.join(input_folder, csv_file)
        print(f"Traitement du fichier : {csv_path}")
        
        # Lecture du CSV
        df = pd.read_csv(csv_path, decimal=",")
        
        # Conserver la colonne text de côté
        text_col = df['text']

        # Suppression des colonnes non désirées (et 'text' pour la prédiction)
        columns_dropped = ['id', 'num_page', 'text', 'pos_y', 'y0', 'area']
        df_pred = df.drop(columns=[col for col in columns_dropped if col in df.columns], errors='ignore')

        # Définition de l'ordre final des colonnes pour la prédiction
        columns_pred = ['width', 'height', 'chars', 'char_size', 'pos_x', 'aspect', 'layout', 'x0', 'x1', 'y1']
        df_pred = df_pred[columns_pred]

        # Encodage de la colonne 'layout' si elle n'est pas numérique
        if df_pred['layout'].dtype == object:
            le = LabelEncoder()
            df_pred['layout'] = le.fit_transform(df_pred['layout'])

        # Transformation des données via le pipeline
        print("Application des transformations (scaler, PCA)...")
        X_transformed = pipeline.transform(df_pred)

        X_transformed = pd.DataFrame(X_transformed)

        # Création du DMatrix pour XGBoost
        dmatrix = xgb.DMatrix(X_transformed)

        # Prédiction
        print("Prédiction en cours...")
        y_pred_proba = bst_loaded.predict(dmatrix)
        y_pred = np.argmax(y_pred_proba, axis=1)

        # Reconstitution du DataFrame final
        final_df = df.copy()  # Reprendre les colonnes initiales
        final_df['label'] = [map_prediction(p) for p in y_pred]  # Ajouter les prédictions dans 'label'

        # Sauvegarder le fichier dans le dossier de sortie
        output_path = os.path.join(output_folder, f"predicted_{csv_file}")
        final_df.to_csv(output_path, index=False, decimal=",")
        print(f"Fichier de sortie enregistré : {output_path}")
