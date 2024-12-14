import os
import cv2
import numpy as np
from PIL import Image
import pytesseract
from pytesseract import Output
import pandas as pd

def process_table_image(input_path="bonus/cropped_images/Rapport-SFCR-Groupe-CAMCA-2022/page_10_1.png", output_dir="bonus/extracted_tables"):
    """Traiter une image contenant un tableau segmenté et reconstruire les données."""
    print(f"[INFO] Chargement de l'image : {input_path}...")
    
    # Charger l'image
    cropped_image = Image.open(input_path)
    cropped_image_cv = np.array(cropped_image)

    # Convertir en niveaux de gris
    gray = cv2.cvtColor(cropped_image_cv, cv2.COLOR_RGB2GRAY)

    # Appliquer une binarisation
    _, binary = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY_INV)

    # Identifier les lignes verticales
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 30))
    vertical_lines = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)

    # Trouver les contours des lignes verticales
    contours, _ = cv2.findContours(vertical_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Annoter l'image pour marquer les colonnes
    marked_image = cropped_image_cv.copy()
    vertical_line_width_threshold = 1  # Ajustez ce seuil pour détecter les colonnes plus finement
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if w < vertical_line_width_threshold:  # Ignorer les lignes trop épaisses
            cv2.line(marked_image, (x, 0), (x, marked_image.shape[0]), (0, 0, 0), 2)

    # Sauvegarder l'image marquée
    marked_image_pil = Image.fromarray(marked_image)
    marked_output_path = os.path.join(output_dir, "Rapport-SFCR-Groupe-CAMCA-2022-page_10_1.png")
    os.makedirs(output_dir, exist_ok=True)
    marked_image_pil.save(marked_output_path)
    print(f"[INFO] Image avec colonnes marquées sauvegardée dans {marked_output_path}.")

    # Ré-appliquer l'OCR
    print("[INFO] Ré-application de l'OCR sur l'image marquée...")
    config = "--psm 6 --oem 3"
    ext_df = pytesseract.image_to_data(marked_image_pil, output_type=Output.DATAFRAME, config=config)

    # Nettoyer les données OCR
    ext_df = ext_df.dropna(subset=["text"])
    ext_df = ext_df[ext_df["text"].str.strip() != ""]

    if ext_df.empty:
        print("[INFO] Aucun texte détecté dans le tableau.")
        return

    # Regrouper les lignes pour reconstruire le tableau
    reconstructed_lines = []
    line_groups = ext_df.groupby(["block_num", "par_num", "line_num"], sort=False)
    for (block, par, line), group in line_groups:
        line_text = " ".join(word for _, word in group.sort_values("left")["text"].items())
        reconstructed_lines.append(line_text)

    # Convertir les lignes en DataFrame
    reconstructed_df = pd.DataFrame({"line": reconstructed_lines})
    print("[INFO] Tableau reconstruit (ligne par ligne) :")
    print(reconstructed_df)

    # Sauvegarder en CSV
    csv_path = os.path.join(output_dir, "Rapport-SFCR-Groupe-CAMCA-2022-page_10_1.csv")
    reconstructed_df.to_csv(csv_path, index=False)
    print(f"[INFO] Tableau sauvegardé dans {csv_path}.")

if __name__ == "__main__":
    import sys
    input_path = sys.argv[1] if len(sys.argv) > 1 else "bonus/cropped_images/Rapport-SFCR-Groupe-CAMCA-2022/page_10_1.png"
    process_table_image(input_path)
