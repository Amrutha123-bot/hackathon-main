#read all PDFs, chunk them and build the vector DB like connecting the pdf service-chunk service-vector service
#instead of writing this load, split and vector creation multiple times just create a function and use this
#i/o - the policy pdf doc, o/p - the relevant chunk docs
#main purpose is to build the vector store database and not to return the content in it or u can return a summary saying that these many docs, chunks are successfully inserted
import logging 
import os
from supabase import Client
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
        # self.document_service = DocumentService() can't be created here because the supabase client belongs to the curr user/request
    
    def ingest_documents(
    self,
    directory_path: str,
    collection_name: str,
    uploaded_files: list[str],
    user_id: str,
    supabase: Client
):
        document_service = DocumentService(supabase)

        try:
            logger.info(
                f"Starting document ingestion for files: {uploaded_files}"
            )

            # -------------------------------------------------
            # 1. Load ONLY the files uploaded in this request
            # -------------------------------------------------
            all_documents = []
            failed_files = []

            for filename in uploaded_files:

                filepath = os.path.join(
                    directory_path,
                    filename
                )

                logger.info(
                    f"Loading uploaded file only: {filepath}"
                )

                load_result = self.pdf_service.load_file(filepath)

                all_documents.extend(
                    load_result.documents
                )

                failed_files.extend(
                    load_result.failed_files
                )

            if not all_documents:
                raise ValueError(
                    "No valid documents were loaded."
                )

            if failed_files:
                logger.warning(
                    f"Failed to load {len(failed_files)} file(s)."
                )

            # -------------------------------------------------
            # 2. Chunk ONLY those uploaded documents
            # -------------------------------------------------
            chunks = self.chunk_service.split_documents(
                all_documents
            )

            # -------------------------------------------------
            # 3. Add ONLY those chunks to user's collection
            # -------------------------------------------------
            try:

                vector_store = self.vector_service.add_documents(
                    chunks,
                    collection_name
                )

            except FileNotFoundError:

                vector_store = self.vector_service.create_vector_store(
                    chunks,
                    collection_name
                )

            logger.info(
                f"Processed {len(all_documents)} documents "
                f"into {len(chunks)} chunks."
            )

            # -------------------------------------------------
            # 4. Store document metadata in Supabase
            # -------------------------------------------------
            for filename in uploaded_files:

                existing_documents=document_service.get_document_by_filename(user_id=user_id, filename=filename)
                if existing_documents:
                    raise ValueError(f"File '{filename}' has already been uploaded." )

                filepath = os.path.join(
                    directory_path,
                    filename
                )

                document_service.add_document(
                    user_id=user_id,
                    filename=filename,
                    filepath=filepath,
                    collection_name=collection_name
                )

            return vector_store

        except Exception as e:

            logger.error(
                f"Error during document ingestion: {e}"
            )

            raise
#request - jwt/user - user.id / user supabase client -ingestion service - document service(manage the metadata) - store the details for each user in the supabase - RLS (makes sures that the files and the collections related to one user is not viewed or accessed by another user)
    