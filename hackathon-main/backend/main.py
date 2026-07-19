#this file only needs ingestion service and the RAG service

import logging 
from services.ingestion_service import IngestionService
from services.rag_service import RAGService
from config.settings import VECTOR_STORE_PATH

logger = logging.getLogger(__name__)

def main():
    try: 
        ingestion_service = IngestionService()
        rag_service = RAGService()
        logger.info("Starting document ingestion...")
        ingestion_service.ingest_documents(VECTOR_STORE_PATH)
        logger.info("Knowledge base is ready.")
        while True:
            query=input("\nAsk Your question: ").strip()#to remove leading and trailing spaces so it is easy for comparisons
            if not query:
                print("Please enter a question...")
                continue
            if query.lower() in ["exit", 'quit']:
                print("GoodBye!")
                break
            try:
                ans=rag_service.answer_question(query)
                print("\nAnswer: ")
                print(ans)
            except Exception as e:
                logger.error(f"Error generating response: {e}")
    except Exception as e:
        logger.error(f"Error in the pipeline: {e}")
            

if __name__ == "__main__":
    main()


# Start Program

# ↓

# Create IngestionService

# ↓

# Create RAGService

# ↓

# Ingest uploaded documents

# ↓

# while True

# ↓

# Ask user for question

# ↓

# If "exit"

# ↓

# Break

# ↓

# Generate answer

# ↓

# Print answer

# ↓

# Repeat