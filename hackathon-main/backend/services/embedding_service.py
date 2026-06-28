#chunk is converted into embedding vectors (text to numbers)
#so from the chunked docs -> generate embeddings -> embedded docs - the concept of sematic search - choosing relevant chunks or vectors
#embedding service - provide or configure the embedding model --- vector service - use that model to create and store embeddings
#instead of including the model in the code we can import it so that we can easily change it in future to hugging face or gemini embeddings or voyage ai etc
#during development let's use local embedding model (hugging face) and in production (gemini) 
#we are using a hybrid embedding model

#we shouldn't care if huggingface, gemini, openai this is called as ABSTRACTION
class EmbeddingService:
    
    def __init__(self):
        pass
    def get_embedding_model(self):
        pass