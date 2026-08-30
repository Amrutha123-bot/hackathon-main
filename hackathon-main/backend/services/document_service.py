#main work is to save documents metadata - get documents - delete documents

import logging
import json #read and write the json files
import os #check if the file exists and manage paths
from datetime import datetime #store upload timestamps
import uuid #generate unique ids for documents
from services.supabase_service import SupabaseService
from supabase import Client

logger = logging.getLogger(__name__)

class DocumentService:

    def __init__(self, supabase: Client):
        self.supabase = supabase
        self.table_name="documents" #this is for documents.json
        
    def add_document(
    self,
    user_id: str,
    filename: str,
    filepath: str,
    collection_name: str
    ):
        document = {
            "user_id": user_id,
            "filename": filename,
            "storage_path": filepath,
            "collection_name": collection_name,
        }

        response = (
            self.supabase
            .table(self.table_name)
            .insert(document)
            .execute()
        )

        if not response.data:
            raise RuntimeError("Failed to save document metadata.")

        document = response.data[0]

        logger.info(
            f"Document metadata saved: "
            f"{filename} ({document['id']})"
        )

        return document

    def get_documents_by_collection(self, collection_name: str):
        # documents = self.load_documents()

        response = (self.supabase.table(self.table_name).select("*").eq("collection_name", collection_name).execute())
        return response.data

    def get_document_by_id(self, document_id: str):
        response = (
            self.supabase
            .table(self.table_name)
            .select("*")
            .eq("id", document_id)
            .single()
            .execute()
        )

        return response.data
    
    def get_all_documents(self):
        
        response = (self.supabase.table(self.table_name).select("*").execute())
        return response.data

    def delete_document(self, collection_name: str):
        
        response=self.supabase.table(self.table_name).delete().eq("collection_name", collection_name).execute()
        # filtered_documents = [
        #     document
        #     for document in documents
        #     if document["collection_name"] != collection_name
        # ]

        # if len(filtered_documents) == len(documents):
        #     return False

        # self.save_documents(filtered_documents) as we have been shifted from document.json to supabase
        logger.info(f"Deleted document metadata for collection: " f"{collection_name}")
        return response.data
    def delete_document_by_id(self, document_id: str):
        response = (
            self.supabase
            .table(self.table_name)
            .delete()
            .eq("id", document_id)
            .execute()
        )

        logger.info(
            f"Deleted document metadata: {document_id}"
        )

        return response.data
    
    def delete_uploaded_file(self, document_id: str):
        document = self.get_document_by_id(document_id)

        if not document:
            return False

        filepath = document["storage_path"]

        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                logger.info(
                    f"Deleted file: {filepath}"
                )
            else:
                logger.warning(
                    f"File not found: {filepath}"
                )

        except Exception:
            logger.exception(
                f"Failed to delete file: {filepath}"
            )
            raise

        return True
    def get_document_by_filename(self, user_id: str, filename: str):
        response = (
            self.supabase
            .table(self.table_name)
            .select("*")
            .eq("user_id", user_id)
            .eq("filename", filename)
            .execute()
        )

        return response.data
    
#service has no idea where the client came from 