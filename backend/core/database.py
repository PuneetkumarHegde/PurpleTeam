"""
Database configuration and session management using SQLAlchemy.
"""

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from config import settings

# Normalize database URL (Render provides postgres:// which SQLAlchemy 2.0 requires as postgresql://)
db_url = settings.DATABASE_URL
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

connect_args = {}
if db_url.startswith("sqlite"):
    connect_args["check_same_thread"] = False

# Database engine
engine = create_engine(
    db_url,
    pool_pre_ping = True,
    echo = settings.DEBUG,
    connect_args = connect_args,
)

# Session factory
SessionLocal = sessionmaker(
    autocommit = False,
    autoflush = False,
    bind = engine
)

# Base class
Base = declarative_base()


def get_db() -> Generator[Session]:
    """
    FastAPI dependency for database sessions
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
