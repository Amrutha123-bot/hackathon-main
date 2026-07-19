from pydantic import BaseModel
from typing import List

class UploadResponse(BaseModel):
    message: str
    uploaded_files: List[str]
    failed_files: List[str]
    collection_name: str


class QuestionResponse(BaseModel):
    question: str
    answer: str

class HealthResponse(BaseModel):
    message: str