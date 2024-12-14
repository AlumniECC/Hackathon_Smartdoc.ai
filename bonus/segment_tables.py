import os
import numpy as np
from PIL import Image
from ultralyticsplus import YOLO

def segment_tables(input_path="bonus/images", output_path="bonus/cropped_images"):
    """Segmenter les tableaux dans les images et enregistrer les parties détectées."""
    print("[INFO] Début de la segmentation des tableaux...")

    # Charger le modèle YOLO
    model = YOLO('keremberke/yolov8m-table-extraction')
    model.overrides['conf'] = 0.25
    model.overrides['iou'] = 0.45
    model.overrides['agnostic_nms'] = False
    model.overrides['max_det'] = 1000

    # Vérifier si le chemin d'entrée est un dossier ou un fichier
    if os.path.isdir(input_path):
        pdf_dirs = [os.path.join(input_path, d) for d in os.listdir(input_path) if os.path.isdir(os.path.join(input_path, d))]
    else:
        pdf_dirs = [input_path]

    for pdf_dir in pdf_dirs:
        pdf_name = os.path.basename(pdf_dir)
        output_dir = os.path.join(output_path, pdf_name)
        os.makedirs(output_dir, exist_ok=True)

        for img_file in os.listdir(pdf_dir):
            if img_file.endswith(".png"):
                img_path = os.path.join(pdf_dir, img_file)
                img = Image.open(img_path)

                # Prédiction avec YOLO
                print(f"[INFO] Détection des tableaux dans {img_file}...")
                results = model.predict(img)

                if len(results[0].boxes.data) == 0:
                    print(f"[INFO] Aucun tableau détecté dans {img_file}.")
                    continue

                # Découper les tableaux détectés
                for idx, box in enumerate(results[0].boxes.data.numpy()):
                    x1, y1, x2, y2, _, _ = map(int, box)
                    margin = 10
                    x1, y1, x2, y2 = max(0, x1 - margin), max(0, y1 - margin), min(img.width, x2 + margin), min(img.height, y2 + margin)

                    # Découper l'image
                    cropped_array = np.array(img)[y1:y2, x1:x2]
                    cropped_img = Image.fromarray(cropped_array)

                    # Sauvegarder l'image découpée
                    cropped_img_name = f"{os.path.splitext(img_file)[0]}_{idx + 1}.png"
                    cropped_img_path = os.path.join(output_dir, cropped_img_name)
                    cropped_img.save(cropped_img_path)
                    print(f"[INFO] Tableau sauvegardé : {cropped_img_path}")

    print("[INFO] Segmentation des tableaux terminée.")

if __name__ == "__main__":
    import sys
    input_path = sys.argv[1] if len(sys.argv) > 1 else "bonus/images"
    segment_tables(input_path)
