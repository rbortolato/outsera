# Implement — Golden Raspberry Awards API

You are the implementation agent for this project.

Your task is to implement the complete Golden Raspberry Awards REST API according to:

* `.github/prompts/spec.prompt.md`
* The assignment requirements
* The CSV dataset available in the project

The final project must use:

* Python 3.9
* FastAPI
* SQLAlchemy
* SQLite in-memory
* Docker
* Docker Compose
* pytest
* Integration tests

Do not use technologies that conflict with these requirements.

---

# 1. Before Implementing

Do NOT immediately start writing code.

First inspect the repository and understand:

1. Existing files.
2. Existing project structure.
3. The CSV dataset.
4. The CSV header and actual column names.
5. The format of the producer field.
6. The format used to identify winners.
7. Existing configuration files.
8. Existing Docker files, if any.
9. Existing tests, if any.

Read `.github/prompts/spec.prompt.md` completely before implementation.

Do not assume the CSV structure from the specification.

Use the actual CSV file as the source of truth for CSV parsing.

If the repository is empty, create the project structure described in the specification.

---

# 2. Implementation Principles

Implement the solution incrementally.

Prioritize:

1. Correctness
2. Simplicity
3. Maintainability
4. Testability
5. Performance

Do not over-engineer the solution.

Do not introduce unnecessary design patterns, frameworks, libraries, abstractions, or infrastructure.

Do not modify unrelated files.

Do not hardcode the expected answer from the supplied dataset.

The evaluator will use different datasets.

---

# 3. Project Structure

Use the following structure unless the existing repository provides a strong reason to use an equivalent structure:

```text
.
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes/
│   │       ├── __init__.py
│   │       └── producers.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py
│   ├── db/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   └── models.py
│   ├── loaders/
│   │   ├── __init__.py
│   │   └── csv_loader.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── movie_repository.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── producer.py
│   └── services/
│       ├── __init__.py
│       └── producer_interval_service.py
│
├── tests/
│   └── integration/
│       └── test_producers.py
│
├── data/
│   └── Movielist.csv
│
├── docs/
│   └── ai-interactions.md
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .dockerignore
├── .gitignore
└── README.md
```

Use appropriate `__init__.py` files.

---

# 4. Python Version

The entire project MUST be compatible with Python 3.9.

Do not use Python features introduced after Python 3.9.

Examples:

Do NOT use:

```python
list[str]
```

if compatibility with Python 3.9 is not guaranteed by the chosen implementation.

Prefer:

```python
from typing import List

List[str]
```

Likewise, avoid syntax that requires Python 3.10+.

Docker must explicitly use Python 3.9.

---

# 5. Dependencies

Create a minimal `requirements.txt`.

Use only dependencies necessary for:

* FastAPI
* ASGI server
* SQLAlchemy
* Pydantic/FastAPI schemas
* pytest
* HTTP integration testing

Pin versions that are compatible with Python 3.9.

Avoid adding libraries simply for convenience.

---

# 6. Database

Implement SQLite using SQLAlchemy.

The database MUST be in-memory.

Do not create a persistent SQLite file.

Do not create a PostgreSQL, MySQL, MongoDB, Redis, or other external database.

The application must work without any external database service.

Pay special attention to SQLite in-memory connection behavior.

The same in-memory database must remain available throughout the application lifecycle.

Configure the SQLAlchemy engine appropriately for this requirement.

---

# 7. Database Model

Create a SQLAlchemy model representing the movie data required by the application.

At minimum, preserve:

* year
* title
* winner
* producers

Use appropriate types.

Do not store unnecessary information unless it simplifies the implementation.

Create database tables during application startup.

---

# 8. CSV Loader

Implement:

```text
app/loaders/csv_loader.py
```

The loader must:

1. Read the CSV file.
2. Read the actual CSV header.
3. Parse rows according to the actual dataset.
4. Identify winning movies.
5. Parse the year.
6. Parse producers.
7. Normalize unnecessary whitespace.
8. Persist the records into the database.

Do not assume column order.

Use column names.

Do not answer API requests by reading the CSV.

The CSV must only be used during data initialization.

---

# 9. Producer Parsing

The producer column may contain multiple producers.

Implement producer parsing according to the actual dataset format.

For example, if the dataset represents:

```text
Producer A and Producer B
```

as two producers, they must become two logical producers.

Do not treat the entire producer string as a single producer.

Handle whitespace consistently.

Avoid making assumptions about producer separators without inspecting the actual dataset.

If multiple separator formats are present, support the formats actually found in the CSV.

---

# 10. Winner Filtering

Only movies that are winners of the target category must participate in the calculation.

The implementation must correctly identify winner rows according to the actual CSV representation.

Do not hardcode movie titles.

Do not hardcode producer names.

Do not hardcode winning years.

---

# 11. Repository

Implement database access in:

```text
app/repositories/movie_repository.py
```

The repository should expose the data required by the service.

Keep SQLAlchemy/database-specific logic inside the repository.

Do not put database queries directly inside FastAPI route handlers.

Avoid N+1 queries.

Prefer a small number of efficient database queries.

---

# 12. Business Logic

Implement the interval calculation in:

```text
app/services/producer_interval_service.py
```

The service must:

1. Obtain winning movie data from the repository.
2. Group winning years by individual producer.
3. Ignore producers with fewer than two wins.
4. Sort each producer's winning years.
5. Compare only consecutive wins.
6. Calculate:

```text
interval = followingWin - previousWin
```

7. Identify the minimum interval.
8. Identify the maximum interval.
9. Return ALL producers tied for the minimum.
10. Return ALL producers tied for the maximum.

Do not compare every possible pair of years.

Example:

```text
Producer A:
2000
2005
2010
```

Valid intervals:

```text
2005 - 2000 = 5
2010 - 2005 = 5
```

Invalid comparison:

```text
2010 - 2000 = 10
```

The invalid comparison must not participate in the result.

---

# 13. Deterministic Results

When multiple producers have the same interval, sort the results deterministically.

Prefer:

```text
producer ASC
```

This ensures stable API responses and reliable integration tests.

---

# 14. API Route

Implement:

```text
GET /api/v1/producers/intervals
```

The route should:

1. Obtain the required dependencies.
2. Call the service.
3. Return the result using Pydantic response schemas.

The route must NOT:

* Read the CSV.
* Execute raw business logic.
* Directly manipulate SQLAlchemy queries.
* Calculate intervals.

---

# 15. Response Schema

Create Pydantic models for the API response.

The response must have exactly this conceptual structure:

```json
{
  "min": [
    {
      "producer": "Producer 1",
      "interval": 1,
      "previousWin": 2008,
      "followingWin": 2009
    }
  ],
  "max": [
    {
      "producer": "Producer 2",
      "interval": 99,
      "previousWin": 1900,
      "followingWin": 1999
    }
  ]
}
```

Use explicit response models.

Do not expose SQLAlchemy models directly.

Keep the API field names exactly as specified:

```text
min
max
producer
interval
previousWin
followingWin
```

---

# 16. FastAPI Application

Implement:

```text
app/main.py
```

The application must:

1. Create the database.
2. Create database tables.
3. Load the CSV.
4. Register API routes.
5. Start serving requests only after initialization succeeds.

Use FastAPI's modern lifespan mechanism where appropriate.

Do not silently ignore initialization errors.

If the CSV cannot be loaded, fail clearly.

---

# 17. Dependency Injection

Use FastAPI dependency injection where appropriate.

Database sessions should not be managed as global mutable state.

Ensure sessions are properly created and closed.

The architecture should make the API straightforward to test.

---

# 18. Integration Tests

Create:

```text
tests/integration/test_producers.py
```

Tests MUST be integration tests.

They must exercise the API through HTTP requests.

Do not test the service by directly calling:

```python
producer_interval_service(...)
```

as the primary testing approach.

The tests should exercise:

```text
HTTP
→ FastAPI
→ route
→ service
→ repository
→ SQLite
```

---

# 19. Integration Test Scenarios

Implement tests for at least:

### Minimum interval

Verify that the API returns the correct producer(s) with the shortest interval.

### Maximum interval

Verify that the API returns the correct producer(s) with the longest interval.

### Minimum tie

Create test data where multiple producers have the same minimum interval.

Verify that ALL of them are returned.

### Maximum tie

Create test data where multiple producers have the same maximum interval.

Verify that ALL of them are returned.

### Single win

A producer with only one win must not appear in either result.

### Consecutive wins

Verify that only consecutive winning years are considered.

### Multiple producers

Verify that movies with multiple producers are correctly associated with each individual producer.

### Response structure

Verify that the API returns:

```text
min
max
producer
interval
previousWin
followingWin
```

### Empty/insufficient dataset

If practical, verify that the application handles a dataset where no producer has at least two wins.

Follow the behavior defined by the implementation/specification rather than inventing a new API contract.

---

# 20. Test Isolation

Tests must not depend on the production CSV result.

Create controlled test data for edge cases.

The implementation must be designed so the database can be initialized with test data.

Avoid tests that modify the actual production dataset permanently.

Tests must be repeatable.

Tests must not depend on execution order.

---

# 21. Docker

Create a `Dockerfile` using Python 3.9.

The container must:

1. Install dependencies.
2. Copy the application.
3. Copy the CSV dataset.
4. Expose the API port.
5. Start the FastAPI application.

Use a production-appropriate ASGI command.

Example concept:

```text
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Do not hardcode a host such as `localhost` inside the container.

---

# 22. Docker Compose

Create:

```text
docker-compose.yml
```

The application must be runnable with:

```bash
docker compose up --build
```

No external database service is required.

The application must be completely self-contained.

Provide a straightforward way to execute integration tests inside Docker.

For example:

```bash
docker compose run --rm app pytest
```

Use the actual service name defined in the compose file.

---

# 23. Configuration

Create a small configuration layer.

At minimum support:

```text
CSV_FILE_PATH
```

with a sensible default such as:

```text
/app/data/Movielist.csv
```

Do not hardcode the CSV path in multiple files.

---

# 24. README

Create a complete `README.md`.

Include:

## Project description

Briefly explain what the API does.

## Technology stack

Document:

* Python 3.9
* FastAPI
* SQLAlchemy
* SQLite
* Docker
* pytest

## Project structure

Briefly explain the important directories.

## Running with Docker

Document:

```bash
docker compose up --build
```

## API

Document:

```text
GET /api/v1/producers/intervals
```

Include example response.

## Running tests

Document the Docker command used to execute integration tests.

## Architecture

Briefly explain:

```text
CSV
 ↓
Loader
 ↓
SQLite
 ↓
Repository
 ↓
Service
 ↓
FastAPI
 ↓
HTTP Response
```

---

# 25. AI Interaction Log

Create:

```text
docs/ai-interactions.md
```

Record the actual AI interactions used during implementation.

Do not fabricate conversations.

Include relevant prompts and a concise description of what the agent implemented or changed.

Update this file as the implementation progresses.

---

# 26. Error Handling

Implement sensible error handling.

Do not expose stack traces to API consumers.

Do not use:

```python
except Exception:
    pass
```

Do not silently ignore malformed CSV data.

Initialization errors should be visible and cause startup failure when appropriate.

---

# 27. Code Quality

Follow these rules:

* PEP 8.
* Type hints.
* Small and focused functions.
* Descriptive names.
* No duplicated business logic.
* No unnecessary abstractions.
* No unnecessary dependencies.
* No global mutable state unless justified.
* No hardcoded dataset results.
* No hardcoded producer names.
* No hardcoded years.
* No hardcoded intervals.
* No direct CSV access from API routes.
* No database access from API routes.
* No business logic in API routes.

---

# 28. Performance

Avoid unnecessary queries.

The preferred flow is:

```text
one efficient query
        ↓
winning records
        ↓
producer grouping
        ↓
sorted years
        ↓
interval calculation
        ↓
min/max
```

Avoid N+1 database queries.

The interval calculation should be efficient for reasonably large datasets.

---

# 29. Validation Before Completion

Before considering the implementation complete, perform all of the following:

### Python

Verify that the project is compatible with Python 3.9.

### Dependencies

Verify that all dependencies install successfully.

### Application

Start the application using Docker.

### API

Call:

```text
GET /api/v1/producers/intervals
```

Verify the response.

### Tests

Run all integration tests.

All tests must pass.

### Docker

Verify that a clean environment can run:

```bash
docker compose up --build
```

without requiring local Python, SQLite, or other services.

### Code

Review the implementation for:

* hardcoded results
* duplicated logic
* incorrect producer parsing
* incorrect winner filtering
* non-consecutive interval calculations
* missing ties
* N+1 queries
* Python >3.9 syntax
* unnecessary dependencies

---

# 30. Final Review Against Specification

Before finishing, compare the implementation against every requirement in:

```text
.github/prompts/spec.prompt.md
```

Create a checklist internally and ensure every acceptance criterion is satisfied.

Do not claim the implementation is complete if any requirement remains unresolved.

---

# 31. Final Output

After implementation, provide a concise summary containing:

1. What was implemented.
2. Main files created/changed.
3. Architecture used.
4. How to run the application.
5. How to run integration tests.
6. Test result.
7. Any remaining limitations or assumptions.

Do not include large code blocks in the final summary.

The source code must remain in the repository.

# Important Constraints

The evaluator will use different datasets.

Therefore:

NEVER hardcode the expected answer from the supplied CSV.

NEVER assume the supplied dataset is the only possible dataset.

NEVER calculate results directly from CSV on every API request.

NEVER compare non-consecutive winning years.

NEVER return only one producer when multiple producers have the same minimum or maximum interval.

NEVER introduce an external database.

NEVER require anything to be installed outside Docker to run the application.

The final implementation must be a complete, executable project.
