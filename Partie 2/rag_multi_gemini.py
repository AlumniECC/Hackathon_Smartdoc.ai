import logging
import sys
import os
import time
import streamlit as st
from dataclasses import dataclass

import google.generativeai as genai
from llama_index.core import Settings, VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms.gemini import Gemini
from llama_index.embeddings.gemini import GeminiEmbedding

@dataclass
class AppConfig:
    """Configuration class for application settings"""
    CHUNK_SIZE: int = 512
    CHUNK_OVERLAP: int = 50
    TOP_K_RESULTS: int = 5
    MAX_TOKENS: int = 1024
    DEFAULT_TEMPERATURE: float = 0.3
    LOG_FILE: str = 'app.log'

    # Latest Gemini Models
    GEMINI_MODELS = {
        "Gemini Pro": "gemini-1.0-pro",
        "Gemini Pro Vision": "gemini-1.0-pro-vision-latest",
        "Gemini 1.5 Pro": "gemini-1.5-pro-latest",
        "Gemini Ultra": "gemini-1.0-ultra"
    }

class DocumentChatApp:
    def __init__(self):
        """Initialize the Streamlit Document Chat Application"""
        # Configure logging
        self._setup_logging()
        
        # Validate API Key
        self._validate_api_key()
        
        # Initialize Google Generative AI
        self._initialize_genai()
        
        # Initialize documents list
        self.documents = []

    def _setup_logging(self):
        """Configure logging with file and stream handlers"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(AppConfig.LOG_FILE),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)

    def _validate_api_key(self):
        self.GOOGLE_API_KEY = 'AIzaSyBwVOCO3mhnYtsK--CZsdmjeXbcX2IkGPU'

    def _initialize_genai(self):
        """Configure Google Generative AI"""
        try:
            genai.configure(api_key=self.GOOGLE_API_KEY)
        except Exception as e:
            self.logger.error(f"Failed to configure Generative AI: {e}")
            st.error(f"API Configuration Error: {e}")
            st.stop()

    def _initialize_models(self, selected_model):
        try:
            model_name = f"models/{AppConfig.GEMINI_MODELS.get(selected_model, 'gemini-1.0-pro')}"
            
            self.llm = Gemini(
                model=model_name,
                api_key=self.GOOGLE_API_KEY,
                temperature=st.session_state.temperature,
                max_tokens=AppConfig.MAX_TOKENS
            )
            
            self.embed_model = GeminiEmbedding(
                api_key=self.GOOGLE_API_KEY,
                model_name="models/embedding-001"
            )
        except Exception as e:
            self.logger.error(f"Model initialization error: {e}")
            st.error(f"Failed to initialize models: {e}")
            st.stop()

    def _load_local_documents(self, selected_files):
        """Load documents directly from the txt_files directory based on user selection."""
        self.documents = []
        txt_dir = "txt_files"
        if not os.path.exists(txt_dir):
            st.error("Text directory not found. Please ensure txt_files directory is present.")
            return []
        
        # Utiliser les fichiers sélectionnés par l'utilisateur
        input_files = [os.path.join(txt_dir, f) for f in selected_files]

        try:
            reader = SimpleDirectoryReader(input_files=input_files)
            self.documents = reader.load_data()

            if not self.documents:
                st.warning("No documents were loaded. Please check the selected files.")
            
            return self.documents
        except Exception as e:
            self.logger.error(f"Document loading error: {e}")
            st.error(f"Failed to load documents: {e}")
            return []

    def _create_vector_index(self):
        """Create vector index from loaded documents"""
        try:
            return VectorStoreIndex.from_documents(
                self.documents, 
                chunk_size=AppConfig.CHUNK_SIZE, 
                chunk_overlap=AppConfig.CHUNK_OVERLAP
            )
        except Exception as e:
            self.logger.error(f"Vector index creation error: {e}")
            st.error(f"Failed to create vector index: {e}")
            return None

    def _initialize_chat_engine(self, vector_index):
        """Initialize chat engine with vector index"""
        try:
            return vector_index.as_chat_engine(
                similarity_top_k=AppConfig.TOP_K_RESULTS
            )
        except Exception as e:
            self.logger.error(f"Chat engine initialization error: {e}")
            st.error(f"Failed to initialize chat engine: {e}")
            return None

    def run(self):
        """Run the Streamlit application"""
        # Set page configuration
        st.set_page_config(page_title="Multi-Doc Gemini Chat", page_icon="📄")
        
        # Create main title
        st.title('Chat with SFCR docs')
        
        # Setup sidebar
        self._setup_sidebar()
        
        # Initialize session state
        self._initialize_session_state()
        
        # Process selected documents
        self._process_local_documents()
        
        # Display chat history
        self._display_chat_history()
        
        # Handle user input
        self._process_user_input()

    def _setup_sidebar(self):
        """Configure sidebar with application settings"""
        st.sidebar.header('Chat Configuration')
        
        # Model selection dropdown
        st.session_state.selected_model = st.sidebar.selectbox(
            'Select Gemini Model',
            list(AppConfig.GEMINI_MODELS.keys()),
            index=0
        )
        
        # Temperature slider
        st.session_state.temperature = st.sidebar.slider(
            'Temperature', 
            min_value=0.0, 
            max_value=1.0, 
            value=AppConfig.DEFAULT_TEMPERATURE,
            step=0.1
        )
        
        st.sidebar.write("Select between 1 and 4 documents from the image:")

        txt_dir = "txt_files"
        if os.path.exists(txt_dir):
            available_files = [f for f in os.listdir(txt_dir) if f.endswith(".txt")]
        else:
            available_files = []

        st.session_state.selected_files = st.sidebar.multiselect(
            "Select documents",
            options=available_files,
            help="Select between 1 and 4 documents."
        )

        # Clear conversation button
        if st.sidebar.button('Clear Conversation'):
            st.session_state.messages = []
            st.session_state.conversation_context = None
            st.session_state.vector_index = None

    def _initialize_session_state(self):
        """Initialize or reset session state variables"""
        if "messages" not in st.session_state:
            st.session_state.messages = []
        if "conversation_context" not in st.session_state:
            st.session_state.conversation_context = None
        if "vector_index" not in st.session_state:
            st.session_state.vector_index = None
        if "selected_model" not in st.session_state:
            st.session_state.selected_model = "Gemini Pro"
        if "temperature" not in st.session_state:
            st.session_state.temperature = AppConfig.DEFAULT_TEMPERATURE
        if "selected_files" not in st.session_state:
            st.session_state.selected_files = []

    def _process_local_documents(self):
        """Process local documents based on user selection and create vector index"""
        selected_files = st.session_state.selected_files
        
        # Vérifier le nombre de fichiers sélectionnés
        if selected_files:
            if len(selected_files) > 4:
                st.warning("You selected more than 4 documents. Only the first 4 will be considered.")
                selected_files = selected_files[:4]
        else:
            st.info("Please select at least one document.")
            return
        
        documents = self._load_local_documents(selected_files)
        
        if documents:
            # Initialize models
            self._initialize_models(st.session_state.selected_model)
            
            # Configure settings
            Settings.llm = self.llm
            Settings.embed_model = self.embed_model
            Settings.chunk_size = AppConfig.CHUNK_SIZE
            Settings.chunk_overlap = AppConfig.CHUNK_OVERLAP
            
            # Create vector index
            st.session_state.vector_index = self._create_vector_index()
            
            # Initialize chat engine
            if st.session_state.vector_index:
                st.session_state.chat_engine = self._initialize_chat_engine(st.session_state.vector_index)
                st.sidebar.success(f"{len(documents)} documents loaded successfully!")
        else:
            st.sidebar.error("Failed to load the selected documents. Please try again.")

    def _display_chat_history(self):
        """Display previous chat messages"""
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    def _process_user_input(self):
        """Process and respond to user input"""
        # Check if chat engine is ready
        if not hasattr(st.session_state, 'chat_engine') or not st.session_state.chat_engine:
            st.info("Please select and load documents to start chatting.")
            return

        if prompt := st.chat_input("Ask me anything about the selected documents!"):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Generate and display assistant response
            with st.chat_message("assistant"):
                response = st.write_stream(self._response_generator(prompt))
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})

    def _response_generator(self, prompt):
        """Generate streaming response for the given prompt"""
        try:
            # Query chat engine
            response = st.session_state.chat_engine.query(prompt)
            
            # Check for empty response
            if not response or not str(response).strip():
                yield "I couldn't find a relevant response. Could you rephrase your question?"
                return
            
            # Stream response words
            for word in str(response).split():
                yield word + " "
                time.sleep(0.05)
        
        except Exception as e:
            self.logger.error(f"Response generation error: {e}")
            yield f"An error occurred: {e}"

def main():
    """Main application entry point"""
    try:
        app = DocumentChatApp()
        app.run()
    except Exception as e:
        st.error(f"Application initialization error: {e}")
        logging.error(f"Unhandled application error: {e}")

if __name__ == "__main__":
    main()

