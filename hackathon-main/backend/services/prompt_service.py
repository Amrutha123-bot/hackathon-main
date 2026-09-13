#retrieved docs + user query -> prompt -> llm ->response
#i/o - List[Docs] -retrieved aand  use query 
#o/p - prompt(string)
import logging
from typing import List
from langchain_core.documents import Document
from config.settings import SYSTEM_PROMPT

logger = logging.getLogger(__name__)
#when 
class PromptService:
    
#receive List of docs -> create empty list -> loop through every doc -> read page_content -> read metadata -> format nicely -> append to list -> join everything in one string -> return
    def format_context(self, documents: List[Document]) -> str:

        formatted_chunks = []

        for document in documents:

            content = document.page_content
            metadata = document.metadata

            source = metadata.get("source", "Unknown")
            page = metadata.get("page", "Unknown")

            if not content.strip():
                continue

            formatted_chunk = f"""
    SOURCE INFORMATION
    --------------------------
    Filename: {source}
    Page: {page}

    CONTENT
    --------------------------
    {content}
    """

            formatted_chunks.append(formatted_chunk)

        return "\n\n".join(formatted_chunks)
    def build_prompt(self, documents: List[Document], query: str) -> str:
        try:
            system_prompt = SYSTEM_PROMPT
            context = self.format_context(documents)

            logger.info("========== PROMPT CONTEXT ==========")
            logger.info(context)
            logger.info("====================================")

            prompt = f"""
    SYSTEM INSTRUCTIONS
    -------------------

    {system_prompt}

    DOCUMENT CONTEXT
    -------------------

    {context}

    USER QUESTION
    -------------------

    {query}

    RESPONSE
    -------------------
    """
            return prompt

        except Exception as e:
            logger.error(f"Error in generating the prompt: {e}")
            raise
