#to centralise the configurable values instead of hardcoding in the main module
#so that in this way there is no need to change the whole module 
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150
SUPPORTED_FILE_TYPES = ['.pdf', '.docx', '.txt']
UPLOAD_DIRECTORY = "uploaded_docs"
VECTOR_STORE_PATH = './vector_store'
# EMBEDDING_PROVIDER = "huggingface"
# EMBEDDING_MODEL= "BAAI/bge-small-en-v1.5"#good semantic retrival quality, light enough for local development, popular for production RAG systems, faster than very large embedding models
EMBEDDING_PROVIDER = "gemini"
EMBEDDING_MODEL = "gemini-embedding-001"
LLM_PROVIDER = 'groq'
LLM_MODEL = 'llama-3.3-70b-versatile'

TEMPERATURE = 0.2
MAX_OUTPUT_TOKEN = 512
VECTOR_DB_PROVIDER = 'chroma'
SEARCH_TYPE = 'similarity'
TOP_K = 5 #best 5 chunks
SUPPORTED_EXTENSIONS = {'.pdf', '.docx', '.txt'}
SYSTEM_PROMPT = """
========================================
RESPONSE FORMAT
========================================

Always answer using the following format.

# 📋 Answer

## ✅ Summary

Give a concise 2–3 sentence summary.

---

## 📖 Details

Explain the answer using:
- Bullet points
- Numbered lists
- Tables whenever suitable

Highlight important values using **bold**.

---

## ⚠️ Important Notes

Mention any exceptions, conditions, limits, exclusions or special cases.

---

## 📚 Sources

Mention:
- File Name
- Page Number

Formatting Rules:
- Leave one blank line after every heading.
- Leave one blank line between sections.
- Never write one large paragraph.
- Keep every bullet on a separate line.
- Use tables whenever numerical values are involved.
"""