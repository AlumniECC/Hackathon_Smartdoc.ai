from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter


def initialize_faiss_index(text):
    # Split text
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=100000, chunk_overlap=200)
    texts = text_splitter.split_text(text)
    
    # Create embeddings
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    
    # Create FAISS vector store
    vectorstore = FAISS.from_texts(texts, embeddings)
    
    return vectorstore