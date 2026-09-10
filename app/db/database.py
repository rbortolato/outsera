"""SQLAlchemy database setup."""

from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool


def create_database():
    """Create an in-memory SQLite engine and its session factory."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        future=True,
    )
    return engine, sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=False,
        future=True,
    )


def session_scope(session_factory: sessionmaker) -> Generator[Session, None, None]:
    """Yield a session and always close it after use."""
    session = session_factory()
    try:
        yield session
    finally:
        session.close()
