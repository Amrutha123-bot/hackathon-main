#pip install fastapi uvicorn python-multipart\
#the web server - react runs browser and the backend runs on a server
#we need a bridge to connect the browser and the server - API
import os
from fastapi import FastAPI, UploadFile, File
from services.ingestion_service import IngestionService
from services.rag_service import RAGService
from config.settings import (DOCUMENT_DIRECTORY, SUPPORTED_FILE_TYPES, UPLOAD_DIRECTORY)
import logging
from typing import List
import shutil#to copy the uploaded contents

logger = logging.getLogger(__name__)

app=FastAPI()#obj of web application
ingestion_service = IngestionService()
rag_service = RAGService()

@app.get("/")
def home():
    logger.info("Health check endpoint called.")
    return { "message": "Insurance RAG API is running."}
#how does FastAPI know which python function to execute when there are some 100s of function - we have decorators(request, function to be executed)

@app.post("/upload")#list of docs coming from the request of post method
def upload_documents(files: List[UploadFile]=File(...)):#simply save the uploaded files
    logger.info(f"Received {len(files)} files for upload.")
    uploaded_files = []
    failed_files = []
    for file in files:
        try:
            filename=file.filename
            extension = os.path.splitext(filename)[1].lower()
            if extension not in SUPPORTED_FILE_TYPES:
                logger.warning(f"File type not supported: {filename}")
                failed_files.append(filename)
                continue
            destination = os.path.join(UPLOAD_DIRECTORY, filename)
            with open(destination, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)#for saving
            uploaded_files.append(filename)
        except Exception:
            failed_files.append(filename)
            return {
                "message": "No valid files were uploaded",
            }
    if uploaded_files:
        ingestion_service.ingest_documents(UPLOAD_DIRECTORY)
    return {
        "message": "Upload completed successfully.",
        "uploaded_files": uploaded_files,
        "failed_files": failed_files
    }
        



# React

# ↓

# POST /upload

# ↓

# FastAPI

# ↓

# UploadFile object

# ↓
# validate and then save and continue till all the other files are saved then ingestion
# Save into uploaded_docs/

# ↓

# IngestionService

# ↓

# PDFService

# ↓

# ChunkService

# ↓

# VectorService