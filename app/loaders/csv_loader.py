"""CSV import functionality."""

import csv
import re
from pathlib import Path
from typing import List

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.models import Movie


REQUIRED_COLUMNS = {"year", "title", "studios", "producers", "winner"}
PRODUCER_SEPARATOR = re.compile(r"\s*,\s*|\s+\band\b\s+|\s*&\s*", re.IGNORECASE)


def parse_producers(value: str) -> List[str]:
    """Return individual producer names from the dataset representation."""
    if not value:
        return []
    return [producer.strip() for producer in PRODUCER_SEPARATOR.split(value) if producer.strip()]


def _is_winner(value: str) -> bool:
    return value.strip().lower() == "yes"


def load_movies(session: Session, csv_file_path: str) -> int:
    """Load the CSV into the database, returning the number of inserted rows."""
    if session.query(Movie.id).first() is not None:
        return 0

    path = Path(csv_file_path)
    if not path.is_file():
        raise FileNotFoundError("CSV file does not exist: {}".format(path))

    movies = []
    with path.open("r", encoding="utf-8", newline="") as csv_file:
        reader = csv.DictReader(csv_file, delimiter=";")
        fieldnames = set(reader.fieldnames or [])
        missing = REQUIRED_COLUMNS - fieldnames
        if missing:
            raise ValueError("CSV is missing required columns: {}".format(", ".join(sorted(missing))))

        for line_number, row in enumerate(reader, start=2):
            try:
                year = int((row.get("year") or "").strip())
            except ValueError as exc:
                raise ValueError("Invalid year on CSV line {}".format(line_number)) from exc

            movies.append(
                Movie(
                    year=year,
                    title=(row.get("title") or "").strip(),
                    studios=(row.get("studios") or "").strip(),
                    producers=(row.get("producers") or "").strip(),
                    winner=_is_winner(row.get("winner") or ""),
                )
            )

    try:
        session.add_all(movies)
        session.commit()
    except SQLAlchemyError:
        session.rollback()
        raise
    return len(movies)
