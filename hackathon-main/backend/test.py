from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    groq_api_key=os.getenv("GROQ_API_KEY")
)
GROQ_API_KEY=os.getenv("GROQ_API_KEY")

print(llm.invoke("Hello"))
print("GROQ_API_KEY loaded:", GROQ_API_KEY is not None)
print("GROQ_API_KEY prefix:", GROQ_API_KEY[:10] if GROQ_API_KEY else "None")

from fastapi import UploadFile
print(UploadFile)