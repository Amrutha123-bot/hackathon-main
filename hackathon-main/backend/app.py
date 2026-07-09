#pip install fastapi uvicorn python-multipart\
#the web server - react runs browser and the backend runs on a server
#we need a bridge to connect the browser and the server - API
import os
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from services.ingestion_service import IngestionService
from services.rag_service import RAGService
from config.settings import (DOCUMENT_DIRECTORY, SUPPORTED_EXTENSIONS, UPLOAD_DIRECTORY)
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
            if extension not in SUPPORTED_EXTENSIONS:
                logger.warning(f"File type not supported: {filename}")
                failed_files.append(filename)
                continue
            destination = os.path.join(UPLOAD_DIRECTORY, filename)
            with open(destination, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)#save all the files before uploading them in the directory
            uploaded_files.append(filename)
        except Exception as e:
            logger.error(f"Failed to save {filename}: {e}")
            failed_files.append(filename)
            continue
    if not uploaded_files:
        return {
            "message": "No valid files were uploaded.",
            "uploaded_files": [],
            "failed_files": failed_files
        }
    if uploaded_files:
        try:
            ingestion_service.ingest_documents(UPLOAD_DIRECTORY)
        except Exception as e:
            logger.error(f"Error during document ingestion: {e}")
            raise
    logger.info(
        f"Successfully uploaded {len(uploaded_files)} file(s). "
        f"Failed: {len(failed_files)}."
    )
    return {
        "message": "Upload completed successfully.",
        "uploaded_files": uploaded_files,
        "failed_files": failed_files
    }

class QuestionRequest(BaseModel):
    question: str
# request = QuestionRequest(...)    #question will be received from the http request by FASTAPI
@app.post("/ask")
#receive req-extract questio - epty? - yes (error) - no - RAGService.answer_question() - return answer
def ask_question(request: QuestionRequest):#as the input is in the form of jso n

    ques = request.question.strip()
    if not ques:
        logger.error(f"Enter a question.")
        return {
                "message": "Please enter a valid question."
            }
    logger.info(f"Received question: {ques}")
    try:
        ans=rag_service.answer_question(ques)
        logger.info("Question answered successfully.")
    except Exception as e:
        logger.error(f"Error in generating response: {e}")
        raise
    return {
                "question": ques,
                "answer": ans
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