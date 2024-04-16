from typing import Dict, List

import asyncpg
from street_side.v1.data_models.document import Document


class DocumentRepository():
    def __init__(self, connection: asyncpg.Connection):
        if connection is None:
            raise ValueError(
                "Connection pool cannot be None. "
                "Make sure to initialize the connection pool first."
            )
        self._connection = connection

    async def insert(self, documents: Dict[str, Document]) -> List[str]:
        hash_ids = list(documents.keys())

        existing_hash_ids_records = await self._connection.fetch(
            """
            SELECT
                hash_id
            FROM
                "v1"."documents"
            WHERE
                hash_id = ANY($1)
            """,
            hash_ids,
        )
        existing_hash_ids = {row["hash_id"] for row in existing_hash_ids_records}

        filtered_objects_to_insert = {
            hash_id: _object for hash_id, _object in documents.items()
            if hash_id not in existing_hash_ids
        }

        if len(filtered_objects_to_insert) < 1:
            return hash_ids

        tuples_to_insert = [
            (
                _object.document_type_id,
                _object.date_published,
                _object.quater,
                _object.year,
                _object.file_name,
                _object.remote_url,
                _object.extension,
                hash_id,
            )
            for hash_id, _object in documents.items()
        ]
        
        await self._connection.execute(
            """
            INSERT INTO "v1"."documents" (
                "document_type_id",
                "date_published",
                "quater",
                "year",
                "file_name",
                "remote_url",
                "extension",
                "hash_id",
            )
            (
                SELECT
                    record.document_type_id,
                    record.date_published,
                    record.quater,
                    record.year,
                    record.file_name,
                    record.remote_url,
                    record.extension,
                    record.hash_id,
                FROM
                    unnest($1::"v1"."documents"[]) as record
            )
            ON CONFLICT DO NOTHING
            """,
            tuples_to_insert,
        )

        return list(hash_ids)
    
    async def fetch(self, hash_ids: List[str]) -> Dict[str, Document]:
        records = await self._connection.fetch(
            """
            SELECT
                document_type_id,
                date_published,
                quater,
                year,
                file_name,
                remote_url,
                extension,
                hash_id,
            FROM
                "v1"."documents"
            WHERE
                hash_id = ANY($1)
            """,
            list(set(hash_ids)),
        )
        return {
            row["hash_id"]: Document(
                document_type_id=row["document_type_id"],
                date_published=row["date_published"],
                quater=row["quater"],
                year=row["year"],
                remote_url=row["remote_url"],
                extension=row["extension"],
            ) for row in records
        }