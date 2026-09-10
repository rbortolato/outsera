"""FastAPI application factory and startup lifecycle."""

from contextlib import asynccontextmanager
from typing import AsyncIterator, Optional

from fastapi import FastAPI

from app.api.routes.producers import router as producers_router
from app.core.config import Settings
from app.db.database import create_database
from app.db.models import Base
from app.loaders.csv_loader import load_movies


def create_app(csv_file_path: Optional[str] = None) -> FastAPI:
    """Build an isolated application and its in-memory database."""
    settings = Settings.from_environment(csv_file_path)
    engine, session_factory = create_database()

    @asynccontextmanager
    async def lifespan(application: FastAPI) -> AsyncIterator[None]:
        Base.metadata.create_all(bind=engine)
        session = session_factory()
        try:
            load_movies(session, settings.csv_file_path)
        finally:
            session.close()
        yield

    application = FastAPI(
        title="Golden Raspberry Awards API",
        version="1.0.0",
        lifespan=lifespan,
    )
    application.state.engine = engine
    application.state.session_factory = session_factory
    application.state.settings = settings
    application.include_router(producers_router)
    return application


app = create_app()
