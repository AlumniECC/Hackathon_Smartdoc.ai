def load_text(assureur):
    # Dictionnaire associant chaque assureur à son chemin d'accès
    file_paths = {
        "Google Vision API - AXA": "google_vision_api/text/axa-output-1-to-71_report.txt",
        "Google Vision API - Allianz": "google_vision_api/text/allianz-1-to-94_report.txt",
        "Google Vision API - Covéa": "google_vision_api/text/covea-output-1-to-98_report.txt",
        "Google Vision API - Groupe CAMCA": "google_vision_api/text/camca-output-1-to-49_report.txt"
    }

    # Vérification si l'assureur sélectionné est valide
    if assureur not in file_paths:
        raise ValueError(f"Assureur non reconnu: {assureur}. Options valides: {list(file_paths.keys())}")

    # Lecture du fichier texte
    file_path = file_paths[assureur]
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        return text
    except FileNotFoundError:
        raise FileNotFoundError(f"Le fichier {file_path} n'a pas été trouvé.")
    except Exception as e:
        raise Exception(f"Erreur lors de la lecture du fichier: {str(e)}")
