"""HTTP integration tests for the producer intervals endpoint."""

import csv

import pytest
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.fixture
def client(tmp_path):
    csv_path = tmp_path / "movies.csv"
    rows = [
        [2000, "A1", "Studio", "Alpha", "yes"],
        [2005, "A2", "Studio", "Alpha", "yes"],
        [2015, "A3", "Studio", "Alpha", "yes"],
        [2004, "B1", "Studio", "Beta and Gamma", "yes"],
        [2007, "B2", "Studio", "Beta and Gamma", "yes"],
        [2012, "B3", "Studio", "Beta", "yes"],
        [1990, "D1", "Studio", "Delta, Epsilon", "yes"],
        [2000, "D2", "Studio", "Delta, Epsilon", "yes"],
        [2020, "Single", "Studio", "Only Once", "yes"],
        [1990, "Ignored", "Studio", "Alpha", ""],
    ]
    with csv_path.open("w", encoding="utf-8", newline="") as output:
        writer = csv.writer(output, delimiter=";")
        writer.writerow(["year", "title", "studios", "producers", "winner"])
        writer.writerows(rows)

    with TestClient(create_app(str(csv_path))) as test_client:
        yield test_client


def test_intervals_include_minimum_maximum_ties_and_multiple_producers(client):
    response = client.get("/api/v1/producers/intervals")

    assert response.status_code == 200
    assert response.json() == {
        "min": [
            {
                "producer": "Beta",
                "interval": 3,
                "previousWin": 2004,
                "followingWin": 2007,
            },
            {
                "producer": "Gamma",
                "interval": 3,
                "previousWin": 2004,
                "followingWin": 2007,
            },
        ],
        "max": [
            {
                "producer": "Alpha",
                "interval": 10,
                "previousWin": 2005,
                "followingWin": 2015,
            },
            {
                "producer": "Delta",
                "interval": 10,
                "previousWin": 1990,
                "followingWin": 2000,
            },
            {
                "producer": "Epsilon",
                "interval": 10,
                "previousWin": 1990,
                "followingWin": 2000,
            },
        ],
    }


def test_response_contains_only_expected_fields(client):
    response = client.get("/api/v1/producers/intervals")

    assert set(response.json()) == {"min", "max"}
    assert set(response.json()["min"][0]) == {
        "producer",
        "interval",
        "previousWin",
        "followingWin",
    }


def test_single_win_is_excluded(client):
    response = client.get("/api/v1/producers/intervals")
    values = response.json()

    assert "Only Once" not in {item["producer"] for item in values["min"] + values["max"]}


def test_consecutive_wins_are_used(client):
    response = client.get("/api/v1/producers/intervals")
    alpha_intervals = [
        item for item in response.json()["max"] + response.json()["min"]
        if item["producer"] == "Alpha"
    ]

    assert all(item["followingWin"] - item["previousWin"] != 15 for item in alpha_intervals)


def test_multiple_producer_separators_are_supported(client):
    response = client.get("/api/v1/producers/intervals")
    max_producers = [item["producer"] for item in response.json()["max"]]

    assert max_producers == ["Alpha", "Delta", "Epsilon"]


def test_empty_interval_result_is_returned_for_insufficient_dataset(tmp_path):
    csv_path = tmp_path / "single.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as output:
        writer = csv.writer(output, delimiter=";")
        writer.writerow(["year", "title", "studios", "producers", "winner"])
        writer.writerow([2000, "One", "Studio", "Only Once", "yes"])

    with TestClient(create_app(str(csv_path))) as test_client:
        response = test_client.get("/api/v1/producers/intervals")

    assert response.status_code == 200
    assert response.json() == {"min": [], "max": []}
