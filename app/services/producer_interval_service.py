"""Producer interval business logic."""

from collections import defaultdict
from typing import Any, Dict, List

from app.loaders.csv_loader import parse_producers
from app.repositories.movie_repository import MovieRepository


class ProducerIntervalService:
    """Calculate shortest and longest consecutive winning intervals."""

    def __init__(self, repository: MovieRepository):
        self.repository = repository

    def calculate(self) -> Dict[str, List[Dict[str, Any]]]:
        years_by_producer = defaultdict(list)
        for movie in self.repository.winning_movies():
            for producer in parse_producers(movie.producers):
                years_by_producer[producer].append(movie.year)

        intervals = []
        for producer, years in years_by_producer.items():
            sorted_years = sorted(years)
            for previous, following in zip(sorted_years, sorted_years[1:]):
                intervals.append(
                    {
                        "producer": producer,
                        "interval": following - previous,
                        "previousWin": previous,
                        "followingWin": following,
                    }
                )

        if not intervals:
            return {"min": [], "max": []}

        minimum = min(item["interval"] for item in intervals)
        maximum = max(item["interval"] for item in intervals)
        sort_key = lambda item: (
            item["producer"],
            item["previousWin"],
            item["followingWin"],
        )
        return {
            "min": sorted(
                [item for item in intervals if item["interval"] == minimum],
                key=sort_key,
            ),
            "max": sorted(
                [item for item in intervals if item["interval"] == maximum],
                key=sort_key,
            ),
        }
