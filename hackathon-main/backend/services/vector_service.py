#responsibility - create, load(existing) and manage the vector database
#retrieve vectors based on the question and the vector stored in the database
#input are the chunked docs and the embedding model
#output is the chroma vector store object
#dependencies - chromaDB, embedding service, settings.py
#public methods - create_vector, load_vector, get_retriver - other services has ntg to do with the chroma 
#vector service is the first service which depends on the other services
#incremental indexing - addition of a new doc to the existing doc instead of rebuilding from the start
