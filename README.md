# Golden Raspberry Awards API

REST API that calculates the shortest and longest intervals between consecutive
Golden Raspberry Award wins for each producer. The CSV is loaded once during
startup into an in-memory SQLite database; requests never read the CSV directly.

## Requirements

Docker and Docker Compose are required to run the application. No external
database is needed.

## Running the application

```sh
docker compose up --build
```

The API is available at `http://localhost:8000`.

The input file can be changed with `CSV_FILE_PATH`, for example:

```sh
CSV_FILE_PATH=/app/data/Movielist.csv docker compose up --build
```

## API

### `GET /api/v1/producers/intervals`

Example request:

```sh
curl http://localhost:8000/api/v1/producers/intervals
```

Example response:

```json
{
  "min": [
    {
      "producer": "Producer A",
      "interval": 1,
      "previousWin": 2008,
      "followingWin": 2009
    }
  ],
  "max": [
    {
      "producer": "Producer B",
      "interval": 99,
      "previousWin": 1900,
      "followingWin": 1999
    }
  ]
}
```

All producers tied for either extreme are returned in alphabetical order.
Producers with fewer than two winning movies are excluded.

## Running integration tests

Run the tests in Docker:

```sh
docker compose run --rm app pytest
```

For local development, install `requirements.txt` in Python 3.9 and run
`pytest`.
