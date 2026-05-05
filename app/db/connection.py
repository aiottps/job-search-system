from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.config import config
import urllib
from contextlib import contextmanager

_engine = None
_SessionLocal = None

def get_engine():
    global _engine
    if _engine is None:
        params = urllib.parse.quote_plus(config.db_connection_string)
        _engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")
    return _engine

def get_sessionmaker():
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=get_engine())
    return _SessionLocal

@contextmanager
def db_session():
    """Context manager for database sessions to ensure closure."""
    SessionLocal = get_sessionmaker()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_db():
    """Generator for dependency injection (e.g. FastAPI) or manual use."""
    with db_session() as db:
        yield db
