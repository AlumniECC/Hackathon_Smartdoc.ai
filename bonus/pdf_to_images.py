import os
from pdf2image import convert_from_path

def pdf_to_images(pdf_dir="bonus/pdf", output_dir="bonus/images", dpi=200):
    """Convertit tous les PDF d'un dossier en images, une image par page."""
    print("[INFO] Début de la conversion des PDF en images...")

    # Créer le dossier de sortie s'il n'existe pas
    os.makedirs(output_dir, exist_ok=True)

    # Parcourir les fichiers PDF dans le dossier
    for pdf_file in os.listdir(pdf_dir):
        if pdf_file.endswith(".pdf"):
            pdf_path = os.path.join(pdf_dir, pdf_file)
            pdf_name = os.path.splitext(pdf_file)[0]
            pdf_output_dir = os.path.join(output_dir, pdf_name)
            os.makedirs(pdf_output_dir, exist_ok=True)

            print(f"[INFO] Traitement du fichier PDF : {pdf_path}")
            pages = convert_from_path(pdf_path, dpi=dpi)

            # Convertir chaque page en image
            for i, page in enumerate(pages):
                img_path = os.path.join(pdf_output_dir, f"page_{i + 1}.png")
                if os.path.exists(img_path):
                    print(f"[INFO] Image déjà existante : {img_path}, elle ne sera pas recréée.")
                    continue
                page.save(img_path, "PNG")
                print(f"[INFO] Image sauvegardée : {img_path}")

    print("[INFO] Conversion des PDF en images terminée.")

if __name__ == "__main__":
    import sys
    pdf_dir = sys.argv[1] if len(sys.argv) > 1 else "bonus/pdf"
    pdf_to_images(pdf_dir)
