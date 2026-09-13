#chunk is converted into embedding vectors (text to numbers)
#so from the chunked docs -> generate embeddings -> embedded docs - the concept of sematic search - choosing relevant chunks or vectors
#embedding service - provide or configure the embedding model --- vector service - use that model to create and store embeddings
#instead of including the model in the code we can import it so that we can easily change it in future to hugging face or gemini embeddings or voyage ai etc
#during development let's use local embedding model (hugging face) and in production (gemini) 
#we are using a hybrid embedding model

#we shouldn't care if huggingface, gemini, openai this is called as ABSTRACTION
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from config.settings import (
    EMBEDDING_PROVIDER,
    EMBEDDING_MODEL,
    EMBEDDING_DIMENSION
)

class EmbeddingService:

    def __init__(self):
        self.provider = EMBEDDING_PROVIDER
        self.model_name = EMBEDDING_MODEL
        self.dimension = EMBEDDING_DIMENSION
        self.embedding_model = None

    def get_embedding_model(self):

        if self.embedding_model is not None:
            return self.embedding_model

        if self.provider == "gemini":

            self.embedding_model = GoogleGenerativeAIEmbeddings(
                model=self.model_name,
                output_dimensionality=self.dimension
            )

            return self.embedding_model

        raise ValueError(
            f"Unsupported embedding provider: {self.provider}"
        )