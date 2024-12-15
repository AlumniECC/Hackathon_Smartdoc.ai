import os
import pandas as pd
import sys

def csv_to_txt(input_folder="data/csv_model", output_folder="data/txt"):
    # Créer le dossier de sortie s'il n'existe pas
    os.makedirs(output_folder, exist_ok=True)
    
    # Parcourir les fichiers CSV dans le dossier spécifié
    for csv_file in os.listdir(input_folder):
        if csv_file.endswith(".csv"):
            csv_path = os.path.join(input_folder, csv_file)
            print(f"Traitement du fichier : {csv_path}")
            
            try:
                # Lire le fichier CSV
                df = pd.read_csv(csv_path, decimal=",")
                
                # Filtrer les lignes pour ne conserver que "titre" et "paragraphe"
                filtered_df = df[df['label'].isin(['titre', 'paragraphe'])]

                # Vérifier si le DataFrame est vide
                if filtered_df.empty:
                    print(f"Aucun titre ou paragraphe trouvé dans {csv_file}. Fichier ignoré.")
                    continue

                # Ordonner les données par numéro de page
                filtered_df = filtered_df.sort_values(by=['num_page', 'id'])

                # Initialiser une chaîne pour stocker le contenu du fichier TXT
                txt_content = ""
                current_page = None

                # Parcourir les lignes filtrées
                for _, row in filtered_df.iterrows():
                    # Ajouter une séparation de page si nécessaire
                    if row['num_page'] != current_page:
                        current_page = row['num_page']
                        txt_content += f"\n=======page {current_page}=======\n"
                    
                    # Ajouter le texte avec le bon format
                    if row['label'] == 'titre':
                        txt_content += f"# {row['text']}\n"
                    elif row['label'] == 'paragraphe':
                        txt_content += f"{row['text']}\n"

                # Sauvegarder le fichier TXT dans le dossier de sortie
                output_file = os.path.join(output_folder, f"{os.path.splitext(csv_file)[0]}.txt")
                with open(output_file, "w", encoding="utf-8") as txt_file:
                    txt_file.write(txt_content.strip())  # Supprimer les espaces ou retours à la ligne inutiles
                print(f"Fichier txt généré : {output_file}")
            
            except Exception as e:
                print(f"Erreur lors du traitement du fichier {csv_file} : {e}")

# Récupérer le dossier source à partir des arguments ou utiliser "data/csv_model" par défaut
input_folder = sys.argv[1] if len(sys.argv) > 1 else "data/csv_model"
csv_to_txt(input_folder=input_folder)
