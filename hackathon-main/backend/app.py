import os
import shutil
import tempfile
import logging
from typing import List
import uuid
from pathlib import Path
from supabase import Client
from auth.auth_dependency import (get_current_user, get_user_supabase_client)

from fastapi import FastAPI, UploadFile
from fastapi import File
from fastapi.middleware.cors import CORSMiddleware
# import langchain_community
from fastapi import HTTPException
from fastapi import Depends
from auth.auth_dependency import get_current_user
from services.ingestion_service import IngestionService
from services.rag_service import RAGService
from services.storage_service import StorageService

from services.document_service import DocumentService
# import langchain
from config.settings import (
    SUPPORTED_EXTENSIONS
)
from services.supabase_service import SupabaseService
from schema.request import QuestionRequest
from schema.response import (
    UploadResponse,
    QuestionResponse,
    HealthResponse,
)
from fastapi.middleware.cors import CORSMiddleware

# -------------------- Logging --------------------

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ingestion_service = IngestionService()

logger.info("All services initialized.")

# -------------------- FastAPI --------------------

app = FastAPI()
logger.info("STEP 2: FastAPI created")
# -------------------- CORS --------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# -------------------- Startup --------------------

@app.on_event("startup")
async def startup_event():
    logger.info("STEP 5: FastAPI startup event")

# -------------------- Services --------------------

# logger.info("Creating IngestionService...")
# ingestion_service = IngestionService()
# logger.info("STEP 3: IngestionService created")

# logger.info("Creating RAGService...")
# rag_service = RAGService()
# logger.info("STEP 4: RAGService created")


@app.get("/me")
def get_me(user=Depends(get_current_user)):
    return {
        "id": str(user.id),
        "email": user.email
    }
# -------------------- Health --------------------

@app.get("/", response_model=HealthResponse)
def home():
    logger.info("Health check endpoint called.")
    return {
        "message": "Insurance RAG API is running."
    }

# -------------------- Upload --------------------
@app.post("/upload", response_model=UploadResponse)
def upload_documents(
    files: List[UploadFile] = File(...),
    user=Depends(get_current_user),
    supabase: Client = Depends(get_user_supabase_client)
):
    document_service = DocumentService(supabase)
    supabase_service = SupabaseService()

    storage_service = StorageService(
        supabase_service.get_storage_client()
    )

    logger.info(
        "Received %d files for upload.",
        len(files)
    )

    logger.info(
        "Authenticated user: %s",
        user.id
    )

    uploaded_files = []
    failed_files = []

    collection_name = f"policy_{uuid.uuid4().hex}"

    for file in files:

        filename = Path(file.filename).name

        try:
            extension = Path(filename).suffix.lower()

            if extension not in SUPPORTED_EXTENSIONS:

                logger.warning(
                    "Unsupported file: %s",
                    filename
                )

                failed_files.append(filename)
                continue

            existing_documents = (
                document_service.get_document_by_filename(
                    user_id=str(user.id),
                    filename=filename
                )
            )

            if existing_documents:

                logger.warning(
                    "Duplicate file rejected: %s",
                    filename
                )

                failed_files.append(filename)
                continue

            # -----------------------------------------
            # Generate document ID before storage upload
            # -----------------------------------------

            document_id = str(uuid.uuid4())

            storage_path = (
                f"{user.id}/{document_id}/{filename}"
            )

            # -----------------------------------------
            # Save temporarily
            # -----------------------------------------

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=extension
            ) as temporary_file:

                temporary_path = temporary_file.name

                shutil.copyfileobj(
                    file.file,
                    temporary_file
                )

           

            # -----------------------------------------
            # Upload to Supabase Storage
            # -----------------------------------------

            content_type = file.content_type

            storage_service.upload_file(
                file_path=temporary_path,
                storage_path=storage_path,
                content_type=content_type
            )

            # -----------------------------------------
            # Remove temporary upload
            # -----------------------------------------

            os.remove(temporary_path)

            uploaded_files.append({
                "filename": filename,
                "storage_path": storage_path,
                "document_id": document_id
            })

            logger.info(
                "Uploaded '%s' to Storage.",
                filename
            )

        except Exception:

            logger.exception(
                "Failed to upload file: %s",
                filename
            )

            failed_files.append(filename)

    if not uploaded_files:

        return {
            "message": "No valid files were uploaded.",
            "uploaded_files": [],
            "failed_files": failed_files,
            "collection_name": ""
        }

    try:

        result = ingestion_service.ingest_documents(
            collection_name=collection_name,
            uploaded_files=uploaded_files,
            user_id=str(user.id),
            supabase=supabase
        )

    except Exception:

        logger.exception(
            "Document ingestion failed."
        )

        raise HTTPException(
            status_code=500,
            detail="Document ingestion failed."
        )

    return {
        "message": "Upload completed successfully.",
        "uploaded_files": [
            file["filename"]
            for file in uploaded_files
        ],
        "failed_files": (
            failed_files +
            result["failed_files"]
        ),
        "collection_name": collection_name
    }
# -------------------- Documents --------------------

@app.get("/documents")
def get_documents(user=Depends(get_current_user), supabase: Client = Depends(get_user_supabase_client)):
    try:
        document_service = DocumentService(supabase)
        documents = document_service.get_all_documents()

        return {
            "documents": documents
        }

    except Exception:
        logger.exception("Failed to fetch documents")
        raise

@app.delete("/documents/file/{document_id}")
def delete_file(
    document_id: str,
    user=Depends(get_current_user),
    supabase: Client = Depends(get_user_supabase_client)
):
    try:
        document_service = DocumentService(supabase)

        supabase_service = SupabaseService()

        storage_service = StorageService(
            supabase_service.get_storage_client()
        )

        document = document_service.get_document_by_id(
            document_id
        )

        if not document:
            raise HTTPException(
                status_code=404,
                detail="Document not found."
            )

        filename = document["filename"]
        collection_name = document["collection_name"]

        logger.info(
            f"Deleting file '{filename}' "
            f"from collection '{collection_name}'"
        )

        # Delete the physical uploaded file
        storage_service.delete_file(
            document["storage_path"]
        )

        # Delete document metadata.
        # Its document_chunks are automatically deleted
        # through ON DELETE CASCADE.
        document_service.delete_document_by_id(
            document_id
        )

        return {
            "message": "Document deleted successfully.",
            "filename": filename
        }

    except HTTPException:
        raise

    except Exception:
        logger.exception(
            "Failed to delete document."
        )

        raise HTTPException(
            status_code=500,
            detail="Failed to delete document."
        )

    
@app.delete("/documents/{collection_name}")
def delete_document(
    collection_name: str,
    user=Depends(get_current_user),
    supabase: Client = Depends(get_user_supabase_client)
):
    try:
        document_service = DocumentService(supabase)

        documents = document_service.get_documents_by_collection(
            collection_name
        )

        if not documents:
            raise HTTPException(
                status_code=404,
                detail="Collection not found."
            )

        logger.info(
            f"Deleting knowledge base '{collection_name}' "
            f"containing {len(documents)} document(s)."
        )

        # Delete physical uploaded files
        for document in documents:
            filepath = document["storage_path"]

            if os.path.exists(filepath):
                os.remove(filepath)

                logger.info(
                    f"Deleted file: {filepath}"
                )

        # Delete document metadata.
        # document_chunks are automatically deleted
        # because of ON DELETE CASCADE.
        for document in documents:
            document_service.delete_document_by_id(
                document["id"]
            )

        return {
            "message": "Knowledge base deleted successfully."
        }

    except HTTPException:
        raise

    except Exception:
        logger.exception(
            "Failed to delete knowledge base."
        )

        raise HTTPException(
            status_code=500,
            detail="Failed to delete knowledge base."
        )
    
@app.post("/ask", response_model=QuestionResponse)
def ask_question(
    request: QuestionRequest,
    user=Depends(get_current_user),
    supabase: Client = Depends(get_user_supabase_client)
):

    question = request.question.strip()
    document_ids = request.document_ids

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Please enter a valid question."
        )

    if not document_ids:
        raise HTTPException(
            status_code=400,
            detail="At least one document must be selected."
        )

    logger.info(f"Received question: {question}")

    try:
        document_service = DocumentService(supabase)

        # Verify that every selected document belongs
        # to the authenticated user.
        verified_documents = []

        for document_id in document_ids:

            document = document_service.get_document_by_id(
                document_id
            )

            if not document:
                raise HTTPException(
                    status_code=404,
                    detail=f"Document not found: {document_id}"
                )

            verified_documents.append(document)

        logger.info(
            f"Verified {len(verified_documents)} selected documents."
        )

        rag_service = RAGService(supabase)

        result = rag_service.answer_question(
            query=question,
            document_ids=document_ids
        )

        return {
            "question": question,
            "answer": result["answer"],
            "citations": result["citations"]
        }

    except HTTPException:
        raise

    except Exception:
        logger.exception("Error generating answer")

        raise HTTPException(
            status_code=500,
            detail="Failed to generate answer."
        )