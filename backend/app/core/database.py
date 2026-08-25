"""
Database engine, session factory, and declarative base.
Uses async SQLAlchemy with asyncpg for non-blocking DB access.
"""

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

# SQLite doesn't support pool_size/max_overflow — detect and configure accordingly
_is_sqlite = settings.DATABASE_URL.startswith("sqlite")
_engine_kwargs = {} if _is_sqlite else {"pool_size": 10, "max_overflow": 20}

# Async engine for FastAPI
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    **_engine_kwargs,
)

# Session factory
async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """SQLAlchemy declarative base for all models."""
    pass


async def get_db() -> AsyncSession:
    """FastAPI dependency — yields an async DB session per request."""
    async with async_session_factory() as session:
        try:
            yield session
            # Note: Explicit session.commit() should be called in endpoints
            # to prevent race conditions during request teardown.
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
