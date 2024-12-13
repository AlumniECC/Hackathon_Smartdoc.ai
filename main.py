import streamlit as st
from config.globals import GOOGLE_API_KEY, SPEAKER_TYPES, initial_prompt
from rag_architecture.inital_vector import initialize_faiss_index
from rag_architecture.response import generate_response
from llama_parser.markdown_content import load_markdown
from google_vision_api.text_content import load_text  # Exemple : pour Google Vision

def main():
    """
    Application RAG : Rapports sur la Solvabilité et la Situation Financière
    """
    # Configuration de la page Streamlit
    st.set_page_config(
        page_title="RAG - Rapports sur la Solvabilité",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Initialisation des variables de session
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = [initial_prompt]
    if 'selected_text' not in st.session_state:
        st.session_state.selected_text = None
    if 'vector_index' not in st.session_state:
        st.session_state.vector_index = None

    # Barre latérale
    with st.sidebar:
        st.title("📊 RAG - Solvabilité & Situation Financière")
        st.button('Effacer l’historique', on_click=lambda: st.session_state.update(chat_history=[initial_prompt]))

        # Détection des changements dans les sources principales
        prev_source_type = st.session_state.get("selected_source_type", None)

        # Sélection de la source principale
        st.subheader("Choisissez la source principale :")
        use_llama_parser = st.checkbox("Rapport Llama Parser", key="llama_parser_checkbox")
        use_google_vision = st.checkbox("Rapport Google Vision API", key="google_vision_checkbox")

        if use_llama_parser and not use_google_vision:
            st.session_state.selected_source_type = "Llama Parser"
            st.success("Source : Llama Parser sélectionnée.")
        elif use_google_vision and not use_llama_parser:
            st.session_state.selected_source_type = "Google Vision API"
            st.success("Source : Google Vision API sélectionnée.")
        elif use_llama_parser and use_google_vision:
            st.warning("Veuillez sélectionner une seule source principale.")
            st.session_state.selected_source_type = None
        else:
            st.warning("Aucune source principale sélectionnée.")
            st.session_state.selected_source_type = None

        # Réinitialisation de l'index vectoriel si la source principale change
        if prev_source_type != st.session_state.get("selected_source_type"):
            st.session_state.vector_index = None

        # Sélection des sous-sources
        if st.session_state.selected_source_type:
            st.subheader("Choisissez la compagnie d'assurance :")
            axa = st.checkbox("AXA", key="axa_checkbox")
            allianz = st.checkbox("Allianz", key="allianz_checkbox")
            covea = st.checkbox("Covéa", key="covea_checkbox")
            camca = st.checkbox("Groupe CAMCA", key="camca_checkbox")

            selected_subsources = []
            if axa:
                selected_subsources.append("AXA")
            if allianz:
                selected_subsources.append("Allianz")
            if covea:
                selected_subsources.append("Covéa")
            if camca:
                selected_subsources.append("Groupe CAMCA")

            if len(selected_subsources) == 1:
                st.session_state.selected_text = f"{st.session_state.selected_source_type} - {selected_subsources[0]}"
                st.success(f"Source finale sélectionnée : {st.session_state.selected_text}")
            elif len(selected_subsources) > 1:
                st.warning("Veuillez sélectionner une seule compagnie d'assurance.")
                st.session_state.selected_text = None
            else:
                st.warning("Aucune compagnie d'assurance sélectionnée.")
                st.session_state.selected_text = None

        # Initialisation de l'index vectoriel
        if st.session_state.selected_text and not st.session_state.vector_index:
            if st.session_state.selected_source_type == "Llama Parser":
                print("Llama Parser")
                text_data = load_markdown(st.session_state.selected_text)
            elif st.session_state.selected_source_type == "Google Vision API":
                print("Google Vision API")
                text_data = load_text(st.session_state.selected_text)
            else:
                text_data = None

            if text_data:
                st.session_state.vector_index = initialize_faiss_index(text_data)
                st.success("Index vectoriel initialisé avec succès !")


    # Interface principale
    st.header("💬Chatbot - Rapports Solvabilité & Situation Financière")
    if not st.session_state.selected_text:
        st.warning("Veuillez sélectionner une source principale et une sous-source dans la barre latérale.")
        return

    # Interface de chat
    st.write("Posez vos questions sur le rapport sélectionné :")
    prompt = st.chat_input("Entrez une question :", key="user_input")
    if prompt:
        with st.spinner("Génération de la réponse..."):
            response_text = generate_response(prompt, st.session_state.vector_index, GOOGLE_API_KEY)
            st.session_state.chat_history.append({"role": SPEAKER_TYPES.USER, "content": prompt})
            st.session_state.chat_history.append({"role": SPEAKER_TYPES.BOT, "content": response_text})

        # Affichage des messages de chat
        for message in st.session_state.chat_history:
            if message["role"] == SPEAKER_TYPES.USER:
                st.chat_message(SPEAKER_TYPES.USER, avatar="👤").write(message["content"])
            else:
                st.chat_message(SPEAKER_TYPES.BOT, avatar="📊").write(message["content"])

    # Add footer for additional information or credits
    st.markdown("""
    <hr>
    <div style="text-align: center;">
        <small>Hackathon_Smartdoc.ai | Equipe 2 Christian, Daniel, Harouna </small>
    </div>
    """, unsafe_allow_html=True)

# Lancement de l'application
if __name__ == "__main__":
    main()