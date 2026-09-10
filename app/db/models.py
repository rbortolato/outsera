"""SQLAlchemy models."""

from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Movie(Base):
    """A movie entry imported from the awards CSV."""

    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)
    year = Column(Integer, nullable=False)
    title = Column(String(500), nullable=False)
    studios = Column(String(1000), nullable=False, default="")
    producers = Column(String(2000), nullable=False, default="")
    winner = Column(Boolean, nullable=False, default=False)
