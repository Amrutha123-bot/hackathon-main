#we retrieve the relevent vectors based on the question and the vector stored in the database
#user question - retrieval service - relevant chunks(top K) - prompt service - final prompt(context+question) - llm service - gemini/ai response - RAG service - API response
#based on the user query we will return the most relevant chunks from the vector store
#I/P - user question - O/P - list of documents (relevant chunks)
#dependency -vector service(don't know whether it is Chroma or FAISS or even the embeddings-abstraction), settings.py
#this module will use the retriever from the vector service
import logging
from typing import List
from langchain_core.documents import Document
from services.vector_service import VectorService

logger = logging.getLogger(__name__)

class RetrievalService:

    def __init__(self):
        self.vector_service = VectorService()

    def retrieve_documents(self, query: str)-> List[Document]:#even empty list can be returned
        try:
            retriever = self.vector_service.get_retriever()
            relevant_documents = retriever.invoke(query)#no direct retrieve method from langchain
            logger.info(f"Retrieved {len(relevant_documents)} documents for the query: {query}")
            return relevant_documents
        except Exception as e:
            logger.error(f"Error retrieving documents for query '{query}': {e}")
            raise