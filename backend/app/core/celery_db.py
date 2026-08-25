from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

_engine = None
_SessionLocal = None

def get_sync_engine():
    global _engine
    if _engine is None:
        logger.info("Initializing shared Celery database engine")
        _is_sqlite = settings.DATABASE_URL_SYNC.startswith("sqlite")
        _kwargs = {} if _is_sqlite else {"pool_size": 5, "max_overflow": 10, "pool_pre_ping": True}
        _engine = create_engine(settings.DATABASE_URL_SYNC, **_kwargs)
    return _engine

def get_sync_session() -> Session:
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=get_sync_engine())
    return _SessionLocal()
