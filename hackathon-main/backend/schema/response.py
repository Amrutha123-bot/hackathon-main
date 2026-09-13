from pydantic import BaseModel
from typing import List

class UploadResponse(BaseModel):
    message: str
    uploaded_files: List[str]
    failed_files: List[str]
    collection_name: str

class Citation(BaseModel):

    document_id: str

    filename: str

    page: int | None

class QuestionResponse(BaseModel):

    question: str

    answer: str

    citations: List[Citation]


class HealthResponse(BaseModel):
    message: str