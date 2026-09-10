"""Producer interval HTTP routes."""

from typing import Generator

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.repositories.movie_repository import MovieRepository
from app.schemas.producer import ProducerIntervalsResponse
from app.services.producer_interval_service import ProducerIntervalService

router = APIRouter(prefix="/api/v1/producers", tags=["producers"])


def get_db(request: Request) -> Generator[Session, None, None]:
    """Provide a request-scoped SQLAlchemy session."""
    session_factory = request.app.state.session_factory
    session = session_factory()
    try:
        yield session
    finally:
        session.close()


@router.get("/intervals", response_model=ProducerIntervalsResponse)
def producer_intervals(db: Session = Depends(get_db)) -> ProducerIntervalsResponse:
    service = ProducerIntervalService(MovieRepository(db))
    return ProducerIntervalsResponse(**service.calculate())
