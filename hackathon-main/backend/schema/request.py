from pydantic import BaseModel

class QuestionRequest(BaseModel):
    question: str
    collection_name: str