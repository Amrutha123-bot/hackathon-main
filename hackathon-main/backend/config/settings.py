#to centralise the configurable values instead of hardcoding in the main module
#so that in this way there is no need to change the whole module 
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150
SUPPORTED_FILE_TYPES = ['.pdf', '.docx', '.txt']
# UPLOAD_DIRECTORY = 
VECTOR_DB_PATH = './vector_store'
EMBEDDING_PROVIDER = "huggingface"
EMBEDDING_MODEL= "BAAI/bge-small-en-v1.5"#good semantic retrival quality, light enough for local development, popular for production RAG systems, faster than very large embedding models
LLM_PROVIDER = 'gemini'
LLM_MODEL = 'gemini-2.5-pro'
VECTOR_DB_PROVIDER = 'chroma'
SEARCH_TYPE = 'similarity'
TOP_K = 5
