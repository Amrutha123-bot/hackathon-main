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
from typing import List
import logging
import os
from langchain_core.documents import Document
from services.embedding_service import EmbeddingService
from langchain_chroma import Chroma
from config.settings import (VECTOR_STORE_PATH, SEARCH_TYPE, TOP_K) #to keep the created vector DB persistencef
logger=logging.getLogger(__name__)
#a langchain model converts the embedding model and chunks into a vector database which is Chroma.from_documents
#chroma internally has the vector+original chunk+metadata stored in a DB
class VectorService:

    def __init__(self):
        self.embedding_service = EmbeddingService()#composition - VectorService doesn't know how embeddings work
        self.vector_store = None #if we have no DB then we create if only we need and then after that we will reuse the same
        self.db_path = VECTOR_STORE_PATH

    # def create_vector_store(self):
    #         if self.vector_store is not None:#lazy initialization - only create vector store when needed
    #             return self.vector_store
    #     #guard clause - rest of the function focuses on creating the stored
    #         embedding_model = self.embedding_service.get_embedding_model()#composition - VectorService doesn't know how embeddings work
    #         #in RAG chunk_service = ChunkService()#composition - VectorService doesn't know how chunks work
    #         documents = PDFService().load_documents(directory_path='data')
    #         # chunks = chunk_service.split_documents(documents.documents)#as it is a list of documents 
    #         self.vector_store = Chroma.from_documents(chunks, embedding_model, persist_directory=self.db_path)
    #         return self.vector_store
    def create_vector_store(self, documents: List[Document]):
        if self.vector_store is not None:
            return self.vector_store
        embedding_model = self.embedding_service.get_embedding_model()
        self.vector_store = Chroma.from_documents(documents, embedding_model, persist_directory=self.db_path)
        return self.vector_store
        
#when we ask question - load embedding model even it is present in the create vector function - query vector - run similarity search - relevant chunks 
#to load the existing vector DB
    def load_vector_store(self):
        logger.info(f"Loading vector store from {self.db_path}")
        if self.vector_store is not None:
            return self.vector_store
        embedding_model = self.embedding_service.get_embedding_model()#obj already created in constructor
        if os.path.exists(self.db_path):#to check if this folder exists
            self.vector_store=Chroma(persist_directory=self.db_path, embedding_function=embedding_model)
            logger.info(f"Vector store loaded successfully from {self.db_path}")
            return self.vector_store
        else:
            raise FileNotFoundError(f"Vector store path {self.db_path} does not exist.")
        
#receive chunked documents - load existing vector store - add docs - persist changes - return updated vector store
    def add_documents(self, documents: List[Document]):
        #to add docs in btw so that no need to start and rebuild the whole process to add 1 more doc
        try:
            vector_store = self.load_vector_store()
            vector_store.add_documents(documents)
            logger.info(f"Added {len(documents)} documents to the vector store.")
            return vector_store
        except Exception as e:
            logger.error(f"Error adding documents to vector store: {e}")
            raise
#handles embedding questions - similarity search - return the top matches
#so here we are just gonna create the search engine
    def get_retriever(self):
        if self.vector_store is None:
            return self.load_vector_store().as_retriever(search_type=SEARCH_TYPE, search_kwargs={"k": TOP_K})
        retriever = self.vector_store.as_retriever(search_type=SEARCH_TYPE, search_kwargs={'k': TOP_K})
        return retriever