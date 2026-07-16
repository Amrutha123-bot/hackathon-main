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
        

    def answer_question(self, query: str)-> str:
        try:
            logger.info("Loading the response...")
            greetings = [
            "hi",
            "hello",
            "hey",
            "good morning",
            "good afternoon",
            "good evening"
        ]
            if query.lower().strip() in greetings:
                return ("Hello! 👋 I'm your Insurance Document Assistant.\n\n"
        "Upload an insurance document and ask me questions about its coverage, waiting periods, claims, exclusions, and more.")
            documents = self.retrieval_service.retrieve_documents(query)
            prompt = self.prompt_service.build_prompt(documents, query)
            answer = self.llm_service.generate_response(prompt)
            return answer
        except Exception as e:
            logger.error(f"Error during loading the response: {e}")
            raise
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