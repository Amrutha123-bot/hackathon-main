import os
from dotenv import load_dotenv

load_dotenv()

#to centralise the configurable values instead of hardcoding in the main module
#so that in this way there is no need to change the whole module 
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150
SUPPORTED_FILE_TYPES = ['.pdf', '.docx', '.txt']
UPLOAD_DIRECTORY = "uploaded_docs"
VECTOR_STORE_PATH = './vector_store'
EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "gemini")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "gemini-embedding-001")
LLM_PROVIDER = os.getenv("LLM_PROVIDER", 'groq')
LLM_MODEL = os.getenv("LLM_MODEL", "openai/gpt-oss-120b")

TEMPERATURE = 0.2
MAX_OUTPUT_TOKEN = 512
VECTOR_DB_PROVIDER = 'chroma'
SEARCH_TYPE = 'similarity'
TOP_K = 5 #best 5 chunks
SUPPORTED_EXTENSIONS = {'.pdf', '.docx', '.txt'}
SYSTEM_PROMPT = """
========================================
GROUNDING RULES
========================================

Answer the user's question ONLY using the information provided in the
DOCUMENT CONTEXT.

Do not use outside knowledge.

Do not invent, assume, or hallucinate facts, filenames, page numbers,
policy details, or sources.

If the answer cannot be found in the DOCUMENT CONTEXT, clearly say that
the information was not found in the provided documents.

SOURCE RULES:
- The DOCUMENT CONTEXT contains the only valid sources.
- In the Sources section, mention ONLY files and page numbers that actually
  appear in the DOCUMENT CONTEXT.
- Never mention a filename that does not appear in the DOCUMENT CONTEXT.
- Never invent a page number.
- Do not cite documents that were not retrieved.
- If multiple retrieved chunks come from the same file, list that file only
  once with the relevant page numbers.

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
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES = 60