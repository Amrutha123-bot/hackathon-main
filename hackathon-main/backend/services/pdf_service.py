#read the pdf
#extract text
#clean text

#input is the insurance pdf file
#the output is the raw text file

import os
import logging
from datetime import datetime
# from pydoc import doc

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
        pdf_service = PDFService()
        loader = pdf_service.get_loader("")
     #unstructured pdf loader
     #the word doc loader
     #the text loader

    def load_documents(
        self,
        directory_path: str,
        strict_mode: bool = False
    ) -> DocumentLoadResult:
        pass

documents = []
failed_files = []