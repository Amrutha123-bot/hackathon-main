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

    def __init__(self):
        self.retrieval_service= RetrievalService()
        self.prompt_service=    PromptService()
        self.llm_service= LLMService()
        

    def answer_question(self, query: str) -> str:
        logger.info("Step 1: Entered answer_question")

        greetings = [
            "hi", "hello", "hey",
            "good morning", "good afternoon", "good evening"
        ]

        if query.lower().strip() in greetings:
            return "Hello!"

        logger.info("Step 2: Retrieving documents")
        documents = self.retrieval_service.retrieve_documents(query)

        logger.info(f"Step 3: Retrieved {len(documents)} documents")

        logger.info("Step 4: Building prompt")
        prompt = self.prompt_service.build_prompt(documents, query)

        logger.info("Step 5: Calling LLM")
        answer = self.llm_service.generate_response(prompt)

        logger.info("Step 6: Answer generated successfully")

        return answer
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
#         │
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