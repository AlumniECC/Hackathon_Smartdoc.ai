from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain

def generate_response(question, vector_index, api_key, model_name="gemini-1.5-flash"):
    """
    Génère une réponse à partir de la question et du contexte fourni par l'index vectoriel.
    """
    docs = vector_index.similarity_search(question)
    prompt_template = """
    Tu es un expert en analyse financière spécialisé dans l'interprétation des Rapports sur la Solvabilité et la Situation Financière (RSSF) des entreprises d'assurance. 

    Consignes pour répondre aux questions :

        1. Utilise uniquement les informations présentes dans le contexte fourni.

        2. Structure ta réponse de manière claire et professionnelle :
        - Commence par un résumé concis 
        - Détaille ensuite les points clés
        - Cite précisément les sections ou paragraphes sources

        3. Si la réponse n'est pas disponible dans le contexte, dis explicitement : 
        "Les informations nécessaires pour répondre à cette question ne sont pas présentes dans le rapport."

        4. Pour chaque élément financier :
        - Indique les chiffres exacts 
        - Explique leur signification
        - Contextualise par rapport aux normes du secteur de l'assurance

        5. Sois précis et technique, en utilisant le vocabulaire spécifique à la réglementation Solvabilité 2.

    Contexte:\n{context}\n

    Question:\n{question}\n

    Réponds de manière détaillée et analytique :
    """
    prompt = PromptTemplate(template=prompt_template, input_variables=['context', 'question'])
    model = ChatGoogleGenerativeAI(model=model_name, temperature=0.3, api_key=api_key)
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    response = chain({"input_documents": docs, "question": question}, return_only_outputs=True)
    return response['output_text']
