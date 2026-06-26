#raw - text converted into chunk 
#the pdf_service .py module is gonna return the list of documents
#we are gonna return the chunks in the form of list of docs
#split and then return the list of docs contiaining the chunks so both the input and the output are list of docs

#so larget docs into small and meaningful chunks
#why do we need to use it because to get a ans related to one specific part we are not sending the gemini the whole doc but only the part related to that part
#more pages - more chunks - but we are gonna send only relevant 3 to 5 chunks - so high improvement

#decide the type of splitting - 1000 chars or each sentence or recursiveTextSplitter 

#recursiveTextSplitter - smart way - priority- nextline, . , , we use langchain to do that

from langchain.text_splitter import RecursiveCharacterTextSplitter
from config.settings import (CHUNK_SIZE, CHUNK_OVERLAP)#instead of creating a splitter every time use the splitter in the
from typing import List
from langchain_core.documents import Document
import logging

logger  = logging.getLogger(__name__)
"""
    Split LangChain Document objects into smaller semantic chunks
    while preserving metadata.
"""
class ChunkService:
    #each and every time the obj of this class is created automatically this splitting values will be loaded like we are creating a splitter
    def __init__(self):#the splitter

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size = CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP
        )

    #they only care about giving input and chunking happens but not how
    def split_documents(self, documents: List[Document]) -> List[Document]:
        
        if not documents:
            logger.warning("No documents to split.")
            return list()
        
        logger.info(f"Splitting {len(documents)} documents...")
        chunks = self.splitter.split_documents(documents)
        logger.info(f"Generated {len(chunks)} chunks.")
        return chunks