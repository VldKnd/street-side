import contextlib
import logging
from typing import AsyncGenerator, Union

import asyncpg
from street_side.v1.data_models.configuration import StreetSideConfiguration

logger = logging.getLogger(__name__)

class PGPool:
    """Postgresql connection pool convenience class."""

    _pool: Union[asyncpg.Pool, None] = None

    @classmethod
    async def get_pool(cls) -> Union[asyncpg.Pool, None]:
        """Get a postgres connection pool."""
        if cls._pool is None:
            cls._pool = await asyncpg.create_pool(
                dsn=StreetSideConfiguration.postgres_dsn,
                min_size=1,
                max_size=StreetSideConfiguration.database_pool_size,
                max_cached_statement_lifetime=0,
                max_inactive_connection_lifetime=15,
                max_cacheable_statement_size=0,
                command_timeout=30,
            )

        return cls._pool

    @classmethod
    @contextlib.asynccontextmanager
    async def get_connection(cls) -> AsyncGenerator[asyncpg.Connection, None]:
        """Get a connection from the connection pool."""
        pool = await cls.get_pool()
        if pool is not None:
            async with pool.acquire() as conn:
                yield conn

    @classmethod
    async def close_connection(cls) -> None:
        """Close the connection pool."""
        if cls._pool is not None:
            logger.info("Closing connection pool")
            await cls._pool.close()
        else:
            logger.info("Connection pool already closed")