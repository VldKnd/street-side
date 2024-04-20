from typing import Dict, List

import asyncpg
from street_side.v1.data_models.document_type import DocumentType


class DocumentTypeRepository():
    def __init__(self, connection: asyncpg.Connection):
        if connection is None:
            raise ValueError(
                "Connection pool cannot be None. "
                "Make sure to initialize the connection pool first."
            )
        self._connection = connection

    async def insert(self, document_types: Dict[str, DocumentType]) -> List[str]:
        hash_ids = list(document_types.keys())

        existing_hash_ids_records = await self._connection.fetch(
            """
            SELECT
                hash_id
            FROM
                "v1"."document_types"
            WHERE
                hash_id = ANY($1)
            """,
            hash_ids,
        )
        existing_hash_ids = {row["hash_id"] for row in existing_hash_ids_records}

        filtered_objects_to_insert = {
            hash_id: _object for hash_id, _object in document_types.items()
            if hash_id not in existing_hash_ids
        }

        if len(filtered_objects_to_insert) < 1:
            return hash_ids

        tuples_to_insert = [
            (
                _object.company_hash_id,
                _object.full_name,
                _object.short_name,
                _object.is_quaterly,
                _object.is_yearly,
                hash_id,
                _object.created_at,
            )
            for hash_id, _object in document_types.items()
        ]
        
        await self._connection.execute(
            """
            INSERT INTO "v1"."document_types" (
                "company_hash_id",
                "full_name",
                "short_name",
                "is_quaterly",
                "is_yearly",
                "hash_id"
            )
            (
                SELECT
                    record.company_hash_id,
                    record.full_name,
                    record.short_name,
                    record.is_quaterly,
                    record.is_yearly,
                    record.hash_id
                FROM
                    unnest($1::"v1"."document_types"[]) as record
            )
            ON CONFLICT DO NOTHING
            """,
            tuples_to_insert,
        )

        return list(hash_ids)
    
    async def fetch(self, hash_ids: List[str]) -> Dict[str, DocumentType]:
        records = await self._connection.fetch(
            """
            SELECT
                company_hash_id,
                full_name,
                short_name,
                is_quaterly,
                is_yearly,
                hash_id,
                created_at
            FROM
                "v1"."document_types"
            WHERE
                hash_id = ANY($1)
            """,
            list(set(hash_ids)),
        )
        return {
            row["hash_id"]: DocumentType(
                company_hash_id=row["company_hash_id"],
                full_name=row["full_name"],
                short_name=row["short_name"],
                is_quaterly=row["is_quaterly"],
                is_yearly=row["is_yearly"],
                created_at=row["created_at"]
            ) for row in records
        }
    
    async def fetch_by_short_names_and_company_hash_id(
            self,
            short_name: str,
            company_hash_id: str
        ) -> Dict[str, DocumentType]:
        records = await self._connection.fetch(
            """
            SELECT
                company_hash_id,
                full_name,
                short_name,
                is_quaterly,
                is_yearly,
                hash_id,
                created_at
            FROM
                "v1"."document_types"
            WHERE
                company_hash_id=$1
                AND
                short_name=$2
            """,
            company_hash_id,
            short_name,
        )

        return {
            row["company_hash_id"] + row["short_name"]:
            DocumentType(
                company_hash_id=row["company_hash_id"],
                full_name=row["full_name"],
                short_name=row["short_name"],
                is_quaterly=row["is_quaterly"],
                is_yearly=row["is_yearly"],
                created_at=row["created_at"]
            ) for row in records
        }