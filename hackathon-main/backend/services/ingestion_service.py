#read all PDFs, chunk them and build the vector DB like connecting the pdf service-chunk service-vector service
#instead of writing this load, split and vector creation multiple times just create a function and use this
#i/o - the policy pdf doc, o/p - the relevant chunk docs
#main purpose is to build the vector store database and not to return the content in it or u can return a summary saying that these many docs, chunks are successfully inserted
import logging
import os
import tempfile

from services.document_loader_service import DocumentLoaderService
from services.chunk_service import ChunkService
from services.vector_service import VectorService
from services.document_service import DocumentService
from services.storage_service import StorageService
from services.supabase_service import SupabaseService

logger = logging.getLogger(__name__)


class IngestionService:

    def __init__(self):
        self.document_loader = DocumentLoaderService()
        self.chunk_service = ChunkService()

    def ingest_documents(
        self,
        collection_name: str,
        uploaded_files: list[dict],
        user_id: str,
        supabase
    ):
        document_service = DocumentService(supabase)
        vector_service = VectorService(supabase)
        supabase_service = SupabaseService()

        storage_service = StorageService(
            supabase_service.get_storage_client()
        )

        created_documents = []

        try:
            # -----------------------------------------
            # 1. Create document metadata
            # -----------------------------------------

            for uploaded_file in uploaded_files:

                filename = uploaded_file["filename"]
                storage_path = uploaded_file["storage_path"]

                existing_documents = (
                    document_service.get_document_by_filename(
                        user_id=user_id,
                        filename=filename
                    )
                )

                if existing_documents:
                    raise ValueError(
                        f"Document '{filename}' already exists."
                    )

                document = document_service.add_document(
                    user_id=user_id,
                    filename=filename,
                    filepath=storage_path,
                    collection_name=collection_name,
                    document_id=uploaded_file["document_id"]
                )

                created_documents.append(document)

            logger.info(
                "Created metadata for %d documents.",
                len(created_documents)
            )

            # -----------------------------------------
            # 2. Download files temporarily
            # -----------------------------------------

            all_documents = []
            failed_files = []

            with tempfile.TemporaryDirectory() as temp_directory:

                for uploaded_file, document in zip(
                    uploaded_files,
                    created_documents
                ):

                    filename = uploaded_file["filename"]
                    storage_path = uploaded_file["storage_path"]

                    try:
                        file_bytes = storage_service.download_file(
                            storage_path
                        )
                        logger.info(
                            "Bytes received for '%s': %d",
                            filename,
                            len(file_bytes)
                        )

                        temporary_path = os.path.join(
                            temp_directory,
                            filename
                        )

                        with open(
                            temporary_path,
                            "wb"
                        ) as temporary_file:
                            temporary_file.write(file_bytes)
                        logger.info(
                                "Temporary file size for '%s': %d bytes",
                                filename,
                                os.path.getsize(temporary_path)
                        )

                        load_result = (
                            self.document_loader.load_file(
                                temporary_path
                            )
                        )

                        # Make sure the original filename is preserved.
                        for loaded_document in load_result.documents:
                            loaded_document.metadata["source"] = filename

                        all_documents.extend(
                            load_result.documents
                        )

                        failed_files.extend(
                            load_result.failed_files
                        )

                    except Exception:
                        logger.exception(
                            "Failed to process file: %s",
                            filename
                        )
                        failed_files.append(filename)

                # -----------------------------------------
                # 3. Validate loaded content
                # -----------------------------------------

                if not all_documents:
                    raise ValueError(
                        "No readable content found in uploaded files."
                    )

                # -----------------------------------------
                # 4. Create chunks
                # -----------------------------------------

                chunks = self.chunk_service.split_documents(
                    all_documents
                )

                if not chunks:
                    raise ValueError(
                        "No chunks were created from the documents."
                    )

                # -----------------------------------------
                # 5. Map filenames → document IDs
                # -----------------------------------------

                document_ids_by_filename = {
                    document["filename"]: document["id"]
                    for document in created_documents
                }

                # -----------------------------------------
                # 6. Generate embeddings + save chunks
                # -----------------------------------------

                saved_chunks = vector_service.add_chunks(
                    chunks=chunks,
                    document_ids_by_filename=document_ids_by_filename
                )

            logger.info(
                "Successfully ingested %d documents and %d chunks.",
                len(created_documents),
                len(saved_chunks)
            )

            return {
                "documents": created_documents,
                "chunks": saved_chunks,
                "failed_files": failed_files
            }

        except Exception:

            logger.exception(
                "Document ingestion failed. Rolling back metadata."
            )

                        # -----------------------------------------
            # Roll back Storage uploads
            # -----------------------------------------

            for uploaded_file in uploaded_files:

                try:
                    storage_service.delete_file(
                        uploaded_file["storage_path"]
                    )

                except Exception:
                    logger.exception(
                        "Failed to rollback Storage file: %s",
                        uploaded_file["storage_path"]
                    )

            # Roll back database metadata
            for document in created_documents:

                try:
                    document_service.delete_document_by_id(
                        document["id"]
                    )

                except Exception:

                    logger.exception(
                        "Failed to rollback document %s",
                        document["id"])

            raise