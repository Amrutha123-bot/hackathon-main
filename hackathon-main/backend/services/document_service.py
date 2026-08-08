#main work is to save documents metadata - get documents - delete documents

import logging
import json #read and write the json files
import os #check if the file exists and manage paths
from datetime import datetime #store upload timestamps
import uuid #generate unique ids for documents
from services.supabase_service import SupabaseService

logger = logging.getLogger(__name__)

class DocumentService:

    def __init__(self):
        self.supabase = SupabaseService().get_client()
        self.table_name='documents'
    def add_document(self, filename: str, filepath: str, collection_name: str):
        documents=self.load_documents()
        self.table_name="documents"

        document = {
            "filename": filename,
            "user_id": None,
            "storage_path": filepath,
            "collection_name": collection_name,
        }

        response = (self.supabase.table(self.table_name).insert(document).execute())
        if not response.data:
            raise RuntimeError("Failed to save document metadata.")
        logger.info(f"Document metadata saved: {filename}")
        return response.data[0]

    def get_documents_by_collection(self, collection_name: str):
        # documents = self.load_documents()

        response = (self.supabase.table(self.table_name).select("*").eq("collection_name", collection_name).execute())
        return response.data


    def get_all_documents(self):
        
        response = (self.supabase.table(self.table_name).select("*").execute())
        return response.data

    def delete_document(self, collection_name: str):
        # documents = self.load_documents()
        documents=self.get_doucments_by_collection(collection_name)

        if not documents:
            return False
        (self.supabase.table(self.table_name).delete().eq("collection_name", collection_name).execute())
        # filtered_documents = [
        #     document
        #     for document in documents
        #     if document["collection_name"] != collection_name
        # ]

        # if len(filtered_documents) == len(documents):
        #     return False

        # self.save_documents(filtered_documents) as we have been shifted from document.json to supabase
        logger.info(f"Deleted document metadata for collection: " f"{collection_name}")
        return True

    def delete_uploaded_files(self, collection_name: str):
        documents = self.get_documents_by_collection(collection_name)

        for document in documents:
            filepath = document["storage_path"]

            try:
                if os.path.exists(filepath):
                    os.remove(filepath)
                    logger.info(f"Deleted file: {filepath}")
            except Exception:
                logger.exception(f"Failed to delete file: {filepath}")