import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")


def get_pdf_text(pdf_docs):
    """Extracts text from a list of PDF documents."""
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def get_text_chunks(text):
    """Splits a large text into smaller chunks for efficient processing."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_text(text)
    return chunks


def get_vector_store(text_chunks):
    """Creates a vector store from a list of text chunks."""
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")
    return vector_store


def get_conversional_chain():
    """Creates a conversational chain for question answering."""
    prompt_template = """
    Answer the question as detailed as possible from the provided context. If the answer is not available in the context,
    just say "The answer is not available in the context".

    Context:
    {context}

    Question:
    {question}

    Answer:
    """

    model = ChatOpenAI(temperature=0.3, openai_api_key=openai_api_key)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain


def user_input(user_question, processed_pdf_text):
    """Processes user input and generates a response using the conversational chain."""
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question)
    chain = get_conversional_chain()
    context = f"{processed_pdf_text}\n\nQuestion: {user_question}"
    response = chain({"input_documents": docs, "question": user_question, "context": context}, return_only_outputs=True)
    st.write("### Réponse :")
    st.write(response["output_text"])


def main():
    """Main function for the Streamlit app."""
    # Configurer la page
    st.set_page_config(page_title="Hackathon NLP - SFCR Analysis", layout="wide")
    
    # En-tête principal
    st.markdown("<h1 style='text-align: center; color: #4CAF50;'>Hackathon NLP: Analyse des Rapports SFCR</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: gray;'>Traitement automatique des rapports d'assurance avec une architecture RAG</h4>", unsafe_allow_html=True)

    # Champ de question utilisateur
    user_question = st.text_input(
        "Posez une question sur les rapports SFCR téléchargés :",
        placeholder="Exemple : Quelle est la solvabilité de l'entreprise pour 2022 ?",
    )

    if user_question:
        if st.session_state.get("pdf_docs"):
            processed_pdf_text = get_pdf_text(st.session_state["pdf_docs"])
            user_input(user_question, processed_pdf_text)
        else:
            st.error("Veuillez d'abord télécharger des fichiers PDF.")

    # Barre latérale
    with st.sidebar:
        st.title("📄 Gestion des Documents")
        st.markdown(
            """
            Téléchargez vos rapports SFCR pour :
            - Extraire des informations pertinentes
            - Répondre à des questions spécifiques
            - Analyser les données en profondeur
            """
        )
        pdf_docs = st.file_uploader("Téléchargez vos fichiers PDF ici :", type="pdf", accept_multiple_files=True)
        if st.button("Soumettre & Traiter"):
            with st.spinner("Traitement en cours..."):
                raw_text = ""
                text_chunks = []
                for pdf in pdf_docs:
                    pdf_reader = PdfReader(pdf)
                    for page in pdf_reader.pages:
                        raw_text += page.extract_text()
                text_chunks = get_text_chunks(raw_text)
                vector_store = get_vector_store(text_chunks)
                chain = get_conversional_chain()
                st.session_state["pdf_docs"] = pdf_docs
                st.session_state["text_chunks"] = text_chunks
                st.session_state["vector_store"] = vector_store
                st.session_state["chain"] = chain
                st.success("Traitement des rapports SFCR terminé avec succès !")

        if st.button("Réinitialiser"):
            st.session_state["pdf_docs"] = []
            st.session_state["text_chunks"] = []
            st.session_state["vector_store"] = None
            st.session_state["chain"] = None
            st.experimental_rerun()

        if st.session_state.get("pdf_docs"):
            st.subheader("Fichiers Téléchargés :")
            for i, pdf_doc in enumerate(st.session_state["pdf_docs"]):
                st.write(f"{i+1}. {pdf_doc.name}")


    


if __name__ == "__main__":
    main()
