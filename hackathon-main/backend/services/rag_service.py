# question - retrieve chunks - attach chunks to prompt to llm - get answer from llm  - answer to user
#responsibility - coordinate all the services to answer the user questions
#i/p - query of the user o/p - str the final ans
#dependencies - retrieval, chunkservice, prompt service, llm service, the most imp orchestor
#receive query - retrieve relevant docs - build prompt - generate response - return response
import logging

from services.retrieval_service import RetrievalService
from services.prompt_service import PromptService
from services.llm_service import LLMService

logger = logging.getLogger(__name__)


class RAGService:

    def __init__(self, supabase):
        self.retrieval_service = RetrievalService(supabase)
        self.prompt_service = PromptService()
        self.llm_service = LLMService()

    def answer_question(
        self,
        query: str,
        document_ids: list[str] | None = None,
        top_k: int | None = None
    ):

        logger.info("Step 1: Entered answer_question")

        if not query or not query.strip():
            raise ValueError("Question cannot be empty.")

        greetings = [
            "hi",
            "hello",
            "hey",
            "good morning",
            "good afternoon",
            "good evening"
        ]

        if query.lower().strip() in greetings:
            return {
                "answer": "Hello!",
                "citations": []
            }

        logger.info("Step 2: Retrieving relevant chunks")

        documents = self.retrieval_service.retrieve_documents(
            query=query,
            document_ids=document_ids,
            top_k=top_k
        )

        if not documents:
            raise ValueError("No relevant documents found.")

        logger.info(
            "Step 3: Retrieved %d relevant chunks",
            len(documents)
        )

        logger.info("Step 4: Building prompt")

        prompt = self.prompt_service.build_prompt(
            documents,
            query
        )

        logger.info("Step 5: Calling LLM")

        answer = self.llm_service.generate_response(prompt)

        logger.info("Step 6: Answer generated successfully")

        citations = []

        seen = set()

        for document in documents:

            filename = document.metadata.get("source")
            page = document.metadata.get("page")
            document_id = document.metadata.get("document_id")

            if not filename or not document_id:
                continue

            citation_key = (document_id, page)

            if citation_key in seen:
                continue

            seen.add(citation_key)

            citations.append({
                "document_id": document_id,
                "filename": filename,
                "page": page
            })

        return {
            "answer": answer,
            "citations": citations
        }
#multiple independent services to complete a workflow
# User Question
#       │
#       ▼
#  RAGService
#       │
#       ▼
# RetrievalService
#       │
#       ▼
# VectorService
#       │
#       ▼
# EmbeddingService
#       │
#       ▼
# Chroma DB

# Retrieved Documents
#         │but 
#         ▼
# PromptService
#         │
#         ▼
# Prompt
#         │
#         ▼
# LLMService
#         │
#         ▼
# Gemini
#         │
#         ▼
# Final Answer