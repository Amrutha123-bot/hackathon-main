#read the pdf
#extract text
#clean text

#input is the insurance pdf file
#the output is the raw text file

import os
import logging
from datetime import datetime
# from pydoc import doc

from click import File
from langchain_community.document_loaders import (TextLoader, UnstructuredPDFLoader, UnstructuredWordDocumentLoader)

from dataclasses import dataclass
from typing import List
from langchain_core.documents import Document
logger = logging.getLogger(__name__)

@dataclass
class DocumentLoadResult:
    documents: List[Document]
    failed_files: List[str]
    total_loaded: int

class PDFService:
    def get_loader(self, file_path: str):
     #unstructured pdf loader#the word doc loader#the text loader
        extension = os.path.splitext(file_path)[1].lower()
        if(extension == '.pdf'):
            return UnstructuredPDFLoader(file_path)
        elif extension == '.docx':
            return UnstructuredWordDocumentLoader(file_path)
        elif extension == '.txt':
            return TextLoader(file_path)
        logger.warning(f"Unsupported file type: {extension}. ")
        return None

    def load_documents(self,directory_path: str,strict_mode: bool = False) -> DocumentLoadResult:
        #try to search for the doc if not found edrror rises#call loader function to load the doc -> add metadata -> store in doc list
        documents = []
        failed_files = []
        if not os.path.exists(directory_path):
            raise FileNotFoundError(f"Directory not found: {directory_path}")
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)#to construct the file path
                loader = self.get_loader(file_path)
                if loader is None:
                    failed_files.append(file_path)
                    continue
                try:
                    docs=loader.load() #to lad the doc and then use it for text extraction -> doc objects
                    for doc in docs:
                        extension = os.path.splitext(file)[1].lower() #metadata is used to know where actually is the answer came from like to get the source
                        doc.metadata['source']=file
                        doc.metadata['file_type']=extension
                        doc.metadata['file_path']=file_path
                        doc.metadata['loaded_at']=datetime.now().isoformat()
                    documents.append(docs)
                except Exception as e:
                    logger.error(f"Error loading file {file_path}: {e}")
                    failed_files.append(file_path)

                    if strict_mode:
                        raise
        return DocumentLoadResult(documents=documents, failed_files=failed_files, total_loaded=len(documents))
    
#to test the module 1 code
pdf_service = PDFService()
result = pdf_service.load_documents('path/to/your/directory', strict_mode=False)
print(result.total_loaded)
print(result.failed_files)

for doc in result.documents:
    print(doc.metadata)