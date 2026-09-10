"""Movie data access."""

from typing import List

from sqlalchemy.orm import Session

from app.db.models import Movie


class MovieRepository:
    """Queries for movie records used by the interval service."""

    def __init__(self, session: Session):
        self.session = session

    def winning_movies(self) -> List[Movie]:
        """Return all winning movies in one database query."""
        return (
            self.session.query(Movie)
            .filter(Movie.winner.is_(True))
            .order_by(Movie.year.asc(), Movie.id.asc())
            .all()
        )
