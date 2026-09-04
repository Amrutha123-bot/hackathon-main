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
from chromadb import PersistentClient
from config.settings import (VECTOR_STORE_PATH, SEARCH_TYPE, TOP_K) #to keep the created vector DB persistencef
logger=logging.getLogger(__name__)
#a langchain model converts the embedding model and chunks into a vector database which is Chroma.from_documents
#chroma internally has the vector+original chunk+metadata stored in a DB
class VectorService:

    def __init__(self):
        self.embedding_service = EmbeddingService()#composition - VectorService doesn't know how embeddings work
        self.vector_stores = {} #if we have no DB then we create if only we need and then after that we will reuse the same
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
    def create_vector_store(
    self,
    documents: List[Document],
    collection_name: str
):

        if collection_name in self.vector_stores:
            return self.vector_stores[collection_name]

        embedding_model = self.embedding_service.get_embedding_model()

        logger.info(
            f"Creating vector store for collection: {collection_name}"
        )

        vector_store = Chroma.from_documents(
            documents=documents,
            embedding=embedding_model,
            persist_directory=self.db_path,
            collection_name=collection_name
        )

        self.vector_stores[collection_name] = vector_store

        logger.info(
            f"Created collection {collection_name} "
            f"with {vector_store._collection.count()} chunks"
        )

        return vector_store
        
#when we ask question - load embedding model even it is present in the create vector function - query vector - run similarity search - relevant chunks 
#to load the existing vector DB
    def load_vector_store(self, collection_name: str):
        logger.info(f"Loading collection: {collection_name}")
        logger.info(f"Vector DB path: {self.db_path}")

        if collection_name in self.vector_stores:
            logger.info(f"Using cached collection: {collection_name}")
            return self.vector_stores[collection_name]

        embedding_model = self.embedding_service.get_embedding_model()

        if not os.path.exists(self.db_path):
            raise FileNotFoundError(
                f"Vector store path {self.db_path} does not exist."
            )

        vector_store = Chroma(
            persist_directory=self.db_path,
            embedding_function=embedding_model,
            collection_name=collection_name
        )

        logger.info(
            f"Loaded Chroma collection: {collection_name}"
        )
        logger.info(
        f"ACTUAL CHROMA COLLECTION: {vector_store._collection.name}"
    )
        logger.info(
            f"Chroma collection count: {vector_store._collection.count()}"
        )

        self.vector_stores[collection_name] = vector_store

        return vector_store        
#receive chunked documents - load existing vector store - add docs - persist changes - return updated vector store
    def add_documents(self, documents: List[Document], collection_name: str):
        #to add docs in btw so that no need to start and rebuild the whole process to add 1 more doc
        try:
            vector_store = self.load_vector_store(collection_name)
            vector_store.add_documents(documents)
            logger.info(f"Added {len(documents)} documents to the vector store.")
            return vector_store
        except Exception as e:
            logger.error(f"Error adding documents to vector store: {e}")
            raise
#handles embedding questions - similarity search - return the top matches
#so here we are just gonna create the search engine
    def get_retriever(self, collection_name: str):
        vector_store = self.load_vector_store(collection_name)
        return vector_store.as_retriever(
        search_type=SEARCH_TYPE,
        search_kwargs={"k": TOP_K}
    )

    def delete_collection(self, collection_name: str):
        try:
            client = PersistentClient(path=self.db_path)

            client.delete_collection(collection_name)

            if collection_name in self.vector_stores:
                del self.vector_stores[collection_name]

            logger.info(
                f"Deleted Chroma collection: {collection_name}"
            )

            return True

        except Exception as e:
            logger.error(
                f"Failed to delete collection {collection_name}: {e}"
            )
            return False

    def delete_documents_by_file(self, collection_name: str, filename: str):
        try:
            vector_store = self.load_vector_store(collection_name)

            vector_store._collection.delete(
                where={"source": filename}
            )

            logger.info(
                f"Deleted chunks for file '{filename}' "
                f"from collection '{collection_name}'"
            )

            return True

        except FileNotFoundError:
            logger.warning(
                f"Vector store not found for collection "
                f"'{collection_name}'. Skipping vector deletion."
            )
            return False

        except Exception as e:
            logger.error(f"Failed to delete file chunks: {e}")
            raise
    
#vector service will build the retriever 