#read all PDFs, chunk them and build the vector DB like connecting the pdf service-chunk service-vector service
#instead of writing this load, split and vector creation multiple times just create a function and use this
#i/o - the policy pdf doc, o/p - the relevant chunk docs
#main purpose is to build the vector store database and not to return the content in it or u can return a summary saying that these many docs, chunks are successfully inserted
import logging 
import os
from services.document_loader_service import DocumentLoaderService
from services.chunk_service import ChunkService
from services.vector_service import VectorService
from services.document_service import DocumentService

logger = logging.getLogger(__name__)

class IngestionService:

    def __init__(self):
        self.pdf_service = DocumentLoaderService()
        self.chunk_service = ChunkService()
        self.vector_service = VectorService()
        self.document_service = DocumentService()
    
    def ingest_documents(self, directory_path: str, collection_name: str, uploaded_files: list[str]):#ingestion_service.ingest_documents("data/")
        # documents=self.pdf_service.load_documents(directory_path)
        try:
            logger.info(f"Starting document ingestion from {directory_path}")
            load_result = self.pdf_service.load_documents(directory_path)
            if not load_result.documents:#here document is an obj but not a list
                # logger.error(f"No valid documents were loaded.")
                raise ValueError("No valid documents were loaded.")
            if load_result.failed_files:
                logger.warning(f"Failed to load {len(load_result.failed_files)} file(s).")
            chunks = self.chunk_service.split_documents(load_result.documents)
            try:
                vector_store = self.vector_service.add_documents(chunks, collection_name)
            except FileNotFoundError:
                vector_store = self.vector_service.create_vector_store(chunks, collection_name)
            logger.info(f"Processed {len(load_result.documents)} documents into {len(chunks)} chunks.")
            for filename in uploaded_files:
                filepath = os.path.join(directory_path, filename)
                self.document_service.add_document(filename=filename, filepth=filepath, collection_name=collection_name)
            logger.info(f"Processed {len(load_result.documents)} documents" f"into {len(chunks)} chunks.")
            return vector_store
        except Exception as e:
            logger.error(f"Error during document ingestion: {e}")
            raise


    