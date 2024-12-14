def load_markdown(assureur):
    # Dictionnaire associant chaque assureur à son chemin d'accès
    file_paths = {
        "Llama Parser - AXA": "llama_parser/markdown/axa_parsed_output.md",
        "Llama Parser - Allianz": "llama_parser/markdown/allianz_parsed_output.md",
        "Llama Parser - Covéa": "llama_parser/markdown/covea_parsed_output.md",
        "Llama Parser - Groupe CAMCA": "llama_parser/markdown/groupe_camca_parsed_output.md"
    }

    # Vérification si l'assureur sélectionné est valide
    if assureur not in file_paths:
        raise ValueError(f"Assureur non reconnu: {assureur}. Options valides: {list(file_paths.keys())}")

    # Lecture du fichier Markdown
    file_path = file_paths[assureur]
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        return text
    except FileNotFoundError:
        raise FileNotFoundError(f"Le fichier {file_path} n'a pas été trouvé.")
    except Exception as e:
        raise Exception(f"Erreur lors de la lecture du fichier: {str(e)}")