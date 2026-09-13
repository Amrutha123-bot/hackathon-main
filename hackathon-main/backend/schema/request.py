from pydantic import BaseModel
from typing import List


class QuestionRequest(BaseModel):

    question: str

    document_ids: List[str]