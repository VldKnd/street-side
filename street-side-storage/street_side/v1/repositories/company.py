from typing import Dict, List

import asyncpg
from street_side.v1.data_models.company import Company


class CompanyRepository():
    def __init__(self, connection: asyncpg.Connection):
        if connection is None:
            raise ValueError(
                "Connection pool cannot be None. "
                "Make sure to initialize the connection pool first."
            )
        self._connection = connection

    async def insert(self, companies: Dict[str, Company]) -> List[str]:
        hash_ids = list(companies.keys())

        existing_hash_ids_records = await self._connection.fetch(
            """
            SELECT
                hash_id
            FROM
                "v1"."companies"
            WHERE
                hash_id = ANY($1)
            """,
            hash_ids,
        )
        existing_hash_ids = {row["hash_id"] for row in existing_hash_ids_records}

        filtered_objects_to_insert = {
            hash_id: _object for hash_id, _object in companies.items()
            if hash_id not in existing_hash_ids
        }

        if len(filtered_objects_to_insert) < 1:
            return hash_ids

        tuples_to_insert = [
            (
                hash_id,
                _object.short_name,
                _object.full_name,
                _object.home_url,
                _object.created_at,
            )
            for hash_id, _object in companies.items()
        ]

        await self._connection.execute(
            """
            INSERT INTO "v1"."companies" (
                "short_name",
                "full_name",
                "home_url",
                "hash_id"
            )
            (
                SELECT
                    record.short_name,
                    record.full_name,
                    record.home_url,
                    record.hash_id
                FROM
                    unnest($1::"v1"."companies"[]) as record
            )
            ON CONFLICT DO NOTHING
            """,
            tuples_to_insert,
        )

        return list(hash_ids)
    
    async def fetch(self, hash_ids: List[str]) -> Dict[str, Company]:
        records = await self._connection.fetch(
            """
            SELECT
                short_name,
                full_name,
                home_url,
                hash_id,
                created_at
            FROM
                "v1"."companies"
            WHERE
                hash_id = ANY($1)
            """,
            list(set(hash_ids)),
        )
        return {
            row["hash_id"]: Company(
                short_name=row["short_name"],
                full_name=row["full_name"],
                home_url=row["home_url"],
                created_at=row["created_at"],
            ) for row in records
        }
   
    async def fetch_by_short_names(self, short_names: List[str]) -> Dict[str, Company]:
        records = await self._connection.fetch(
            """
            SELECT
                short_name,
                full_name,
                home_url,
                hash_id,
                created_at
            FROM
                "v1"."companies"
            WHERE
                short_name = ANY($1)
            """,
            list(set(short_names)),
        )
        return {
            row["short_name"]: Company(
                short_name=row["short_name"],
                full_name=row["full_name"],
                home_url=row["home_url"],
                created_at=row["created_at"],
            ) for row in records
        }