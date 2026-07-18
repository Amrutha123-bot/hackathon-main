# #pip install fastapi uvicorn python-multipart\
# #the web server - react runs browser and the backend runs on a server
# #we need a bridge to connect the browser and the server - API
# import os
# from fastapi import (FastAPI, UploadFile, File)
# from services.ingestion_service import IngestionService
# from services.rag_service import RAGService
# from config.settings import (DOCUMENT_DIRECTORY, SUPPORTED_EXTENSIONS, UPLOAD_DIRECTORY)
# import logging
# from fastapi.middleware.cors import CORSMiddleware
# from schema.request import QuestionRequest
# from schema.response import (UploadResponse, QuestionResponse, HealthResponse)
# from typing import List
# import shutil#to copy the uploaded contents

# logger = logging.getLogger(__name__)

# app=FastAPI()#obj of web application
# ingestion_service = IngestionService()
# rag_service = RAGService()
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[
#         "http://localhost:5173",
#     ],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
# @app.get("/", response_model=HealthResponse)
# def home():
#     logger.info("Health check endpoint called.")
#     return { "message": "Insurance RAG API is running."}
# #how does FastAPI know which python function to execute when there are some 100s of function - we have decorators(request, function to be executed)

# @app.post("/upload", response_model=UploadResponse)#list of docs coming from the request of post method
# def upload_documents(files: List[UploadFile]= File(...)):#simply save the uploaded files
#     logger.info(f"Received {len(files)} files for upload.")
#     os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)
#     uploaded_files = []
#     failed_files = []
#     for file in files:
#         try:
#             filename=file.filename
#             extension = os.path.splitext(filename)[1].lower()
#             if extension not in SUPPORTED_EXTENSIONS:
#                 logger.warning(f"File type not supported: {filename}")
#                 failed_files.append(filename)
#                 continue
#             destination = os.path.join(UPLOAD_DIRECTORY, filename)
#             with open(destination, "wb") as buffer:
#                 shutil.copyfileobj(file.file, buffer)#save all the files before uploading them in the directory
#             uploaded_files.append(filename)
#         except Exception as e:
#             logger.error(f"Failed to save {filename}: {e}")
#             failed_files.append(filename)
#             continue
#     if not uploaded_files:
#         return {
#             "message": "No valid files were uploaded.",
#             "uploaded_files": [],
#             "failed_files": failed_files
#         }
#     if uploaded_files:
#         try:
#             ingestion_service.ingest_documents(UPLOAD_DIRECTORY)
#         except Exception as e:
#             logger.error(f"Error during document ingestion: {e}")
#             raise
#     logger.info(
#         f"Successfully uploaded {len(uploaded_files)} file(s). "
#         f"Failed: {len(failed_files)}."
#     )
#     return {
#         "message": "Upload completed successfully.",
#         "uploaded_files": uploaded_files,
#         "failed_files": failed_files
#     }


# # request = QuestionRequest(...)    #question will be received from the http request by FASTAPI
# @app.post("/ask", response_model=QuestionResponse)
# #receive req-extract questio - epty? - yes (error) - no - RAGService.answer_question() - return answer
# def ask_question(request: QuestionRequest):#as the input is in the form of jso n

#     ques = request.question.strip()
#     if not ques:
#         logger.error(f"Enter a question.")
#         return {
#                 "message": "Please enter a valid question."
#             }
#     logger.info(f"Received question: {ques}")
#     try:
#         ans=rag_service.answer_question(ques)
#         logger.info("Question answered successfully.")
#         logger.info(ans)
#     except Exception as e:
#         logger.error(f"Error in generating response: {e}")
#         raise
#     return {
#                 "question": ques,
#                 "answer": ans
#         }


# # React

# # ↓

# # POST /upload

# # ↓

# # FastAPI

# # ↓

# # UploadFile object

# # ↓
# # validate and then save and continue till all the other files are saved then ingestion
# # Save into uploaded_docs/

# # ↓

# # IngestionService

# # ↓

# # PDFService

# # ↓

# # ChunkService

# # ↓

# # VectorService


import os
import shutil
import logging
from typing import List

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import langchain_community
# from services.ingestion_service import IngestionService
# from services.rag_service import RAGService
from services.chunk_service import ChunkService
from config.settings import (
    DOCUMENT_DIRECTORY,
    SUPPORTED_EXTENSIONS,
    UPLOAD_DIRECTORY,
)

from schema.request import QuestionRequest
from schema.response import (
    UploadResponse,
    QuestionResponse,
    HealthResponse,
)

# -------------------- Logging --------------------

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("STEP 1: Import complete")

# -------------------- FastAPI --------------------

app = FastAPI()

logger.info("STEP 2: FastAPI created")

# -------------------- Startup --------------------

@app.on_event("startup")
async def startup_event():
    logger.info("STEP 5: FastAPI startup event")

# -------------------- Services --------------------

logger.info("Creating IngestionService...")
# ingestion_service = IngestionService()
logger.info("STEP 3: IngestionService created")

logger.info("Creating RAGService...")
# rag_service = RAGService()
logger.info("STEP 4: RAGService created")

# -------------------- CORS --------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://your-frontend.onrender.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------- Health --------------------

@app.get("/", response_model=HealthResponse)
def home():
    logger.info("Health check endpoint called.")
    return {
        "message": "Insurance RAG API is running."
    }

# -------------------- Upload --------------------

@app.post("/upload", response_model=UploadResponse)
def upload_documents(files: List[UploadFile] = File(...)):
    logger.info(f"Received {len(files)} files for upload.")

    os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

    uploaded_files = []
    failed_files = []

    for file in files:
        try:
            filename = file.filename
            extension = os.path.splitext(filename)[1].lower()

            if extension not in SUPPORTED_EXTENSIONS:
                logger.warning(f"Unsupported file: {filename}")
                failed_files.append(filename)
                continue

            destination = os.path.join(UPLOAD_DIRECTORY, filename)

            with open(destination, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            uploaded_files.append(filename)

        except Exception as e:
            logger.exception(f"Failed to save {filename}")
            failed_files.append(filename)

    if not uploaded_files:
        return {
            "message": "No valid files were uploaded.",
            "uploaded_files": [],
            "failed_files": failed_files,
        }

    try:
        ingestion_service = IngestionService()
        ingestion_service.ingest_documents(UPLOAD_DIRECTORY)

    except Exception:
        logger.exception("Document ingestion failed")
        raise

    return {
        "message": "Upload completed successfully.",
        "uploaded_files": uploaded_files,
        "failed_files": failed_files,
    }

# -------------------- Ask --------------------

@app.post("/ask", response_model=QuestionResponse)
def ask_question(request: QuestionRequest):

    question = request.question.strip()

    if not question:
        return {
            "message": "Please enter a valid question."
        }

    logger.info(f"Received question: {question}")

    try:
        rag_service = RAGService()
        answer = rag_service.answer_question(question)

    except Exception:
        logger.exception("Error generating answer")
        raise

    return {
        "question": question,
        "answer": answer,
    }