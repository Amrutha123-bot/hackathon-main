#chunk is converted into embedding vectors (text to numbers)
#so from the chunked docs -> generate embeddings -> embedded docs - the concept of sematic search - choosing relevant chunks or vectors
#embedding service - provide or configure the embedding model --- vector service - use that model to create and store embeddings
#instead of including the model in the code we can import it so that we can easily change it in future to hugging face or gemini embeddings or voyage ai etc
#during development let's use local embedding model (hugging face) and in production (gemini) 
#we are using a hybrid embedding model

#we shouldn't care if huggingface, gemini, openai this is called as ABSTRACTION
import logging
from config.settings import (EMBEDDING_PROVIDER, EMBEDDING_MODEL)
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
#text is converted to vector here
logger=logging.getLogger(__name__)
#this embedding model doesn't store embeddings it only generates them. Initializing it once avoids repeated obj creation, reduces overhead and allows the same obj instance to be used throughout the lifetime of the application- storing is done by vector database
class EmbeddingService:
    #we are caching configuration inside the object
    def __init__(self):
        self.provider = EMBEDDING_PROVIDER#creator of embedding model - the service
        self.model_name = EMBEDDING_MODEL#which model should that provider use
        self.embedding_model = None
        
    def get_embedding_model(self):

        try:
            logger.info(f"Initializing {self.provider} embedding model")
            if self.embedding_model is not None:
                return self.embedding_model#returning the existing model if present
            
            else:#the FACTORY PATTERN - creates diff objects based on the config like openai or azure etc - based on the configuration appropriate embedding model will be created
                if self.provider == 'huggingface':
                    self.embedding_model=HuggingFaceEmbeddings(model_name=self.model_name)
                    return self.embedding_model
                elif self.provider == "gemini":
                    self.embedding_model=GoogleGenerativeAIEmbeddings(model=self.model_name)
                    return self.embedding_model
                else:
                    raise ValueError(f"Unsupported embedding provider: {self.provider}")
        except Exception as e:
                logger.error(f"Failed to initialize embedding model: {e}")
