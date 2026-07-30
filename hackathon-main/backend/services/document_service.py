#main work is to save documents metadata - get documents - delete documents

import logging
import json #read and write the json files
import os #check if the file exists and manage paths
from datetime import datetime #store upload timestamps
import uuid #generate unique ids for documents

logger = logging.getLogger(__name__)

class DocumentService:

    def __init__(self):
        self.metadata_file="documents.json"

    def load_documents(self):
        pass

    def save_documents(self):
        pass

    def add_documents(self):
        pass

    def get_all_documents(self):
        pass

    def delete_documents(self):
        pass