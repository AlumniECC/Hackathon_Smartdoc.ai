import pandas as pd
import numpy as np
import json
import os
import sys


def produce_brut(json_path):
    with open(json_path, "r", encoding="utf8") as f:
        data = json.load(f)
    pages_content = data["responses"]
    num_page = 0
    rows = []
    for page in pages_content:
        num_page += 1
        if "fullTextAnnotation" not in page:
            continue
        p = page["fullTextAnnotation"]["pages"]
        for e in p:
            blocks = e["blocks"]
            for block in blocks:
                for para in block["paragraphs"]:
                    # Collect text
                    text = ""
                    for word in para["words"]:
                        for symbol in word["symbols"]:
                            if symbol["confidence"] >= 0.8:
                                text += symbol["text"]
                        text += " "
                    # Extract bounding box features
                    x_list = []
                    y_list = []
                    for v in para["boundingBox"]["normalizedVertices"]:
                        x_list.append(v["x"])
                        y_list.append(v["y"])
                    f = {
                        "num_page": num_page,
                        "text": text,
                        "width": max(x_list) - min(x_list),
                        "height": max(y_list) - min(y_list),
                        "area": (max(x_list) - min(x_list))
                        * (max(y_list) - min(y_list)),
                        "chars": len(text),
                        "char_size": (
                            (max(x_list) - min(x_list))
                            * (max(y_list) - min(y_list))
                            / len(text)
                            if len(text) > 0
                            else 0
                        ),
                        "pos_x": (max(x_list) - min(x_list)) / 2.0 + min(x_list),
                        "pos_y": (max(y_list) - min(y_list)) / 2.0 + min(y_list),
                        "aspect": (
                            (max(x_list) - min(x_list)) / (max(y_list) - min(y_list))
                            if (max(y_list) - min(y_list)) > 0
                            else 0
                        ),
                        "layout": (
                            "h"
                            if (max(x_list) - min(x_list)) / (max(y_list) - min(y_list))
                            > 1
                            else "v"
                        ),
                        "x0": x_list[0],
                        "x1": x_list[1],
                        "y0": y_list[0],
                        "y1": y_list[1],
                    }
                    rows.append(f)
    df = pd.DataFrame(rows)
    return df


# Récupérer le dossier contenant les fichiers JSON ou utiliser "data/json" par défaut
input_folder = sys.argv[1] if len(sys.argv) > 1 else "data/json"

# Définir un dossier de sortie fixe : "data/csv"
output_folder = "data/csv"

# Créer le dossier "csv" s'il n'existe pas
os.makedirs(output_folder, exist_ok=True)

# Parcourir les fichiers JSON dans le dossier
for json_file in os.listdir(input_folder):
    if json_file.endswith(".json"):
        json_path = os.path.join(input_folder, json_file)
        try:
            # Transformer le fichier JSON en DataFrame
            df = produce_brut(json_path)

            # Ajouter une colonne "id" au début
            df.insert(0, "id", range(1, len(df) + 1))

            # Ajouter une colonne "label" vide à la fin
            df["label"] = np.nan

            # Sauvegarder le CSV dans le dossier "csv"
            csv_file = os.path.join(
                output_folder, os.path.splitext(json_file)[0] + ".csv"
            )
            
            if os.path.exists(csv_file):
                confirmation = input(f"Le fichier '{csv_file}' existe déjà. Voulez-vous le remplacer ? (oui/non) : ").strip().lower()
                if confirmation != "oui":
                    print(f"Le fichier '{csv_file}' n'a pas été remplacé.")
                    continue
            
            df.to_csv(csv_file, index=False)
            print(f"Fichier CSV généré : {csv_file}")
        except Exception as e:
            print(f"Erreur lors du traitement du fichier {json_file}: {e}")
