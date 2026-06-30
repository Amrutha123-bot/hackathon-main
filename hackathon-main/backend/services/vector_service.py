#responsibility - create, load(existing) and manage the vector database
#retrieve vectors based on the question and the vector stored in the database
#input are the chunked docs and the embedding model
#output is the chroma vector store object
#dependencies - chromaDB, embedding service, settings.py
#public methods - create_vector, load_vector, get_retriver - other services has ntg to do with the chroma 
#vector service is the first service which depends on the other services
#incremental indexing - addition of a new doc to the existing doc instead of rebuilding from the start
#dependecy injection - the code in the file decides which model need to be used not constructor, obj is received from outside (but VectorService doesn't care who is providing that service)
#composition - to create an embedding we create an obj but we don't know which model we use 0 so we do it in constructor
#If someone asks:
# Why didn't you use dependency injection?
# You can answer:
# "For this project, I chose composition because there is a single embedding service implementation and it keeps the design simpler. However, I designed the service boundaries so the project can be refactored to dependency injection later if multiple embedding providers or testing requirements grow."
import logging
from services.embedding_service import EmbeddingService
logger=logging.getLogger(__name__)

class VectorService:

    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.vector_store = None #if we have no DB then we create if only we need and then after that we will reuse the same

    def create_vector_store(self):
        #to create vectors if they don't exist or else use cache
        pass

    def load_vector_store(self):
        #to load the existing vector DB
        pass

    def add_documents(self):
        #to add docs in btw so that no need to start and rebuild the whole process to add 1 more doc
        pass
    
    def get_retriever(self):
        #to retriver relevant chunks
        pass