#main work is to save documents metadata - get documents - delete documents

import logging
import json #read and write the json files
import os #check if the file exists and manage paths
from datetime import datetime #store upload timestamps
import uuid #generate unique ids for documents


logger = logging.getLogger(__name__)

class DocumentService:

    def __init__(self):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.metadata_file = os.path.join(BASE_DIR, "documents.json")

    def load_documents(self):
        if not os.path.exists(self.metadata_file):
            return []
        try:
            with open(self.metadata_file, "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
        
    def save_documents(self, documents):
        with open(self.metadata_file, 'w') as file:
            json.dump(documents, file, indent=4)

    def add_document(self, filename, filepath, collection_name):
        documents=self.load_documents()

        new_document = {
            "id": str(uuid.uuid4()),
            "filename": filename,
            "filepath": filepath,
            "collection_name": collection_name,
            "uploaded_at": datetime.now().isoformat()
        }

        documents.append(new_document)
        self.save_documents(documents)
        return new_document

    def get_documents_by_collection(self, collection_name):
        documents = self.load_documents()

        return [
            document
            for document in documents
            if document["collection_name"] == collection_name
        ]
        

    def get_all_documents(self):
        return self.load_documents()

    def delete_document(self, collection_name):
        documents = self.load_documents()

        filtered_documents = [
            document
            for document in documents
            if document["collection_name"] != collection_name
        ]

        if len(filtered_documents) == len(documents):
            return False

        self.save_documents(filtered_documents)
        return True

    def delete_uploaded_files(self, collection_name):
        documents = self.get_documents_by_collection(collection_name)

        for document in documents:
            filepath = document["filepath"]

            try:
                if os.path.exists(filepath):
                    os.remove(filepath)
                    logger.info(f"Deleted file: {filepath}")
            except Exception:
                logger.exception(f"Failed to delete file: {filepath}")