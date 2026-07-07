#to centralise the configurable values instead of hardcoding in the main module
#so that in this way there is no need to change the whole module 
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150
SUPPORTED_FILE_TYPES = ['.pdf', '.docx', '.txt']
UPLOAD_DIRECTORY = "uploaded_docs"
VECTOR_DB_PATH = './vector_store'
EMBEDDING_PROVIDER = "huggingface"
EMBEDDING_MODEL= "BAAI/bge-small-en-v1.5"#good semantic retrival quality, light enough for local development, popular for production RAG systems, faster than very large embedding models
LLM_PROVIDER = 'gemini'
LLM_MODEL = 'gemini-2.5-pro'
TEMPERATURE = 2
MAX_OUTPUT_TOKEN = 3
VECTOR_DB_PROVIDER = 'chroma'
SEARCH_TYPE = 'similarity'
TOP_K = 5 #best 5 chunks
SYSTEM_PROMPT = """
========================================
SYSTEM INSTRUCTIONS
========================================

You are an AI assistant specialized in insurance documents.

Answer ONLY using the provided document context.

Do not make assumptions.

If the answer is unavailable, clearly state:
"I could not find this information in the uploaded documents."

Always cite the source document and page number whenever possible.

========================================
DOCUMENT CONTEXT
========================================

<Document 1>

<Document 2>

...

========================================
USER QUESTION
========================================

<question>

========================================
RESPONSE FORMAT
========================================

Answer:

Sources:
"""
