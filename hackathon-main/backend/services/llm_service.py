#we talk to llm- receives prompt - send it to gemini - return the answer
#i/p - string o/p - string
#we cache the gemini client instead of loading the model multiple times
#receive prompt - load gemini model - send prompt - receive response - return response
#if provider- gemini - create gemini chat model - store in self.llm - return self.llm
#langchain_google_genai  - has - GoogleGenerativeAIEmbeddings and ChatGoogleGenerativeAI for 2 diff purposes
#u can't invoke the model from model name right but it should be from the client 
import logging 
from config.settings import (LLM_MODEL, LLM_PROVIDER, TEMPERATURE, MAX_OUTPUT_TOKEN)
from langchain_google_genai import ChatGoogleGenerativeAI#(prompt - answer)

logger = logging.getLogger(__name__)
#provider - model name - llm (client object)
class LLMService:

    def __init__(self):
        self.provider = LLM_PROVIDER
        self.model_name = LLM_MODEL
        self.llm = None

    def get_llm(self):
        #creates the API client only once and then cache it and return it
        
        if self.llm is not None:#return the client not the model name(str)
            return self.llm#this is caching
        
        if self.provider=="gemini":
            logger.info("Initialising Gemini LLM...")
            self.llm = ChatGoogleGenerativeAI(model=self.model_name, temperature=TEMPERATURE, max_output_tokens=MAX_OUTPUT_TOKEN)
            return self.llm#has methods like invoke, stream, batch
        elif self.provider=='openai':
            raise NotImplementedError("OpenAI provider is not implemented yet.")
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")
    #send the prompt to gemini and return the response
    #receive prompt - get llm - send prompt - receive response - extract text - return string
    def generate_response(self, prompt: str)->str:
        try:
            if not prompt.strip():
                raise ValueError("Prompt cannot be empty.")
            logger.info("Generating LLM response...")
            llm=self.get_llm()
            response = llm.invoke(prompt)#an ai msg obj is returned AImessage(context="....", response_metadata={....}) but we only need the content but not the metadata
            logger.info("LLM response generated successfully.")
            return response.content
        except Exception as e:
            logger.error(f"Issue during the response: {e}")
            raise
#Prompt (string)
        # │
#         ▼
# get_llm()
#         │
#         ▼
# Gemini Client
#         │
#         ▼
# invoke(prompt)
#         │
#         ▼
# AIMessage Object
#         │
#         ▼
# response.content
#         │
#         ▼
# String