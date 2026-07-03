#retrieved docs + user query -> prompt -> llm ->response
#i/o - List[Docs] -retrieved aand  use query 
#o/p - prompt(string)
import logging
from typing import List
from langchain_core.documents import Document

logger = logging.getLogger(__name__)
#when 
class PromptService:
    
#receive List of docs -> create empty list -> loop through every doc -> read page_content -> read metadata -> format nicely -> append to list -> join everything in one string -> return
    def format_context(self, documents: List[Document])->str:
        
        formatted_chunks=[]
        for index, document in enumerate(documents):
            content=document.page_content #as here doc is an obj with page content and metadata(in the form of a dictionary)
            metadata=document.metadata
            source=metadata.get("source", "Unknown")
            page=metadata.get("page", "Unknown")#instead of raising an error when the value is not found or exist we return Unknown using get method
            if not content.strip():
                continue
            formatted_chunk = f"""
            Document {index+1}
            --------------------------
            Source: {source}
            Page: {page}
            Content: 
            {content}
"""
            formatted_chunks.append(formatted_chunk)
        
        return "\n\n".join(formatted_chunks)
    
