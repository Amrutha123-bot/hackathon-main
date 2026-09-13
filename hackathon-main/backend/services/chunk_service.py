#raw - text converted into chunk 
#the pdf_service .py module is gonna return the list of documents
#we are gonna return the chunks in the form of list of docs
#split and then return the list of docs contiaining the chunks so both the input and the output are list of docs

#so larget docs into small and meaningful chunks
#why do we need to use it because to get a ans related to one specific part we are not sending the gemini the whole doc but only the part related to that part
#more pages - more chunks - but we are gonna send only relevant 3 to 5 chunks - so high improvement

#decide the type of splitting - 1000 chars or each sentence or recursiveTextSplitter 

#recursiveTextSplitter - smart way - priority- nextline, . , , we use langchain to do that
import logging

from langchain_text_splitters import RecursiveCharacterTextSplitter
from config.settings import CHUNK_SIZE, CHUNK_OVERLAP

logger = logging.getLogger(__name__)


class ChunkService:

    def __init__(self):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP
        )

    def split_documents(self, documents):

        if not documents:
            logger.warning("No documents to split.")
            return []

        chunks = self.splitter.split_documents(documents)

        counters = {}

        for chunk in chunks:

            source = chunk.metadata.get("source")

            if source not in counters:
                counters[source] = 0

            chunk.metadata["chunk_index"] = counters[source]

            counters[source] += 1

        logger.info(
            "Created %d chunks from documents.",
            len(chunks)
        )

        return chunks