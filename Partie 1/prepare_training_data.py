import os
import sys
import pandas as pd

def prepare_training_data(input_folder="data/csv_manual", output_file="training_data.csv"):
    # Vérifier si le dossier existe
    if not os.path.exists(input_folder):
        print(f"Le dossier {input_folder} n'existe pas.")
        sys.exit(1)
    
    # Initialiser une liste pour stocker les DataFrames
    dataframes = []
    
    # Parcourir tous les fichiers CSV dans le dossier
    for csv_file in os.listdir(input_folder):
        if csv_file.endswith(".csv") and csv_file != output_file:
            csv_path = os.path.join(input_folder, csv_file)
            try:
                # Charger le fichier CSV
                df = pd.read_csv(csv_path)
                
                # Filtrer les lignes où la colonne 'label' est remplie
                if "label" in df.columns:
                    filtered_df = df[df["label"].notna()]
                    
                    # Ajouter le DataFrame filtré à la liste
                    dataframes.append(filtered_df)
                else:
                    print(f"Avertissement : Le fichier {csv_file} ne contient pas de colonne 'label'. Ignoré.")
            except Exception as e:
                print(f"Erreur lors de la lecture du fichier {csv_file}: {e}")
    
    # Vérifier si des données ont été chargées
    if not dataframes:
        print("Aucun fichier valide n'a été trouvé ou aucune ligne avec un label n'a été détectée.")
        sys.exit(1)
    
    # Concaténer tous les DataFrames
    final_df = pd.concat(dataframes, ignore_index=True)
    
    # Supprimer les colonnes 'id', 'text' et 'num_page'
    columns_to_drop = ["id", "text", "num_page"]
    final_df = final_df.drop(columns=[col for col in columns_to_drop if col in final_df.columns], errors="ignore")
    
    # Sauvegarder le fichier de sortie
    output_path = os.path.join(input_folder, output_file)
    final_df.to_csv(output_path, index=False)
    print(f"Fichier de données d'entraînement généré : {output_path}")

# Si un argument de dossier est donné, l'utiliser, sinon utiliser le dossier par défaut
input_folder = sys.argv[1] if len(sys.argv) > 1 else "data/csv_manual"
prepare_training_data(input_folder=input_folder)
