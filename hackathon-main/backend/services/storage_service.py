import logging
from supabase import Client

logger = logging.getLogger(__name__)


class StorageService:

    def __init__(self, supabase: Client):
        self.supabase = supabase
        self.bucket_name = "documents"

    def upload_file(
        self,
        file_path: str,
        storage_path: str,
        content_type: str | None = None
    ):
        with open(file_path, "rb") as file:
            file_bytes = file.read()
        logger.info(
            "LOCAL FILE SIZE before upload: %d bytes",
            len(file_bytes)
        )
        options = {}

        if content_type:
            options["content-type"] = content_type

        response = (
            self.supabase
            .storage
            .from_(self.bucket_name)
            .upload(
                storage_path,
                file_bytes,
                file_options=options
            )
        )

        logger.info(
            "Uploaded file to Supabase Storage: %s",
            storage_path
        )

        return response

    def download_file(self, storage_path: str) -> bytes:

        response = (
            self.supabase
            .storage
            .from_(self.bucket_name)
            .download(storage_path)
        )

        logger.info(
            "Downloaded file from Supabase Storage: %s",
            storage_path
        )

        logger.info(
            "Downloaded file size: %d bytes",
            len(response)
        )

        return response

    def delete_file(self, storage_path: str):

        response = (
            self.supabase
            .storage
            .from_(self.bucket_name)
            .remove([storage_path])
        )

        logger.info(
            "Deleted file from Supabase Storage: %s",
            storage_path
        )

        return response