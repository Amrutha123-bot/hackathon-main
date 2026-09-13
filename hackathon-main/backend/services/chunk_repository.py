import logging
from typing import Optional

from supabase import Client

logger = logging.getLogger(__name__)


class ChunkRepository:

    def __init__(self, supabase: Client):
        self.supabase = supabase
        self.table_name = "document_chunks"

    def add_chunks(self, chunks: list[dict]):
        if not chunks:
            return []

        response = (
            self.supabase
            .table(self.table_name)
            .insert(chunks)
            .execute()
        )

        if not response.data:
            raise RuntimeError("Failed to save document chunks.")

        logger.info(
            "Saved %d document chunks.",
            len(response.data)
        )

        return response.data

    def delete_chunks_by_document_id(self, document_id: str):
        response = (
            self.supabase
            .table(self.table_name)
            .delete()
            .eq("document_id", document_id)
            .execute()
        )

        logger.info(
            "Deleted chunks for document: %s",
            document_id
        )

        return response.data

    def search_similar_chunks(
        self,
        query_embedding: list[float],
        match_count: int,
        document_ids: Optional[list[str]] = None
    ):
        params = {
            "query_embedding": query_embedding,
            "match_count": match_count,
            "filter_document_ids": document_ids
        }

        response = self.supabase.rpc(
            "match_document_chunks",
            params
        ).execute()
        logger.info(
        "First retrieved chunk: %s",
        response.data[0] if response.data else "NO RESULTS"
    )

        if response.data is None:
            return []

        logger.info(
            "Retrieved %d similar chunks.",
            len(response.data)
        )

        return response.data