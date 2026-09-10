# Specification — Golden Raspberry Awards API

## 1. Objective

Develop a RESTful API to identify the producers with:

1. The shortest interval between two consecutive Golden Raspberry Awards wins.
2. The longest interval between two consecutive Golden Raspberry Awards wins.

The API must process the provided CSV dataset and persist its data in an in-memory database when the application starts.

The implementation must be robust enough to work correctly with different datasets, not only with the provided dataset.

---

# 2. Mandatory Technology Stack

The project MUST use:

* Python 3.9
* FastAPI
* SQLAlchemy
* SQLite in-memory database
* Docker
* Docker Compose
* pytest
* Integration tests only

Do not introduce unnecessary dependencies.

The application must run entirely inside Docker.

No external database installation must be required.

---

# 3. Functional Requirements

## 3.1 CSV Import

When the application starts:

1. Read the provided CSV file.
2. Parse all movie records.
3. Insert the records into the SQLite in-memory database.
4. Avoid importing the same data multiple times during application startup.
5. The API must only become available after the initial dataset has been loaded successfully.

The CSV must not be used directly to answer API requests.

The database must be the source of truth for API queries.

---

# 4. Producer Award Logic

Only movies that won the "Pior Filme" category must be considered.

For each producer:

1. Find all winning movies associated with that producer.
2. Obtain the respective winning years.
3. Sort the years in ascending order.
4. Compare consecutive winning years.
5. Calculate:

   interval = followingWin - previousWin

For each producer, only consecutive wins must be compared.

Do NOT compare every possible pair of wins.

Example:

Producer A won in:

2000
2005
2010

The intervals are:

2005 - 2000 = 5
2010 - 2005 = 5

The interval between 2000 and 2010 must NOT be considered.

---

# 5. Producer Parsing

A movie may have more than one producer.

The implementation must correctly identify individual producers before calculating intervals.

Example:

"Producer A and Producer B"

must be treated as:

* Producer A
* Producer B

Do not treat the entire string as a single producer.

The implementation must support the producer separator format present in the dataset and should be resilient to common variations in whitespace.

---

# 6. API

Implement a RESTful endpoint using FastAPI.

Recommended endpoint:

GET /api/v1/producers/intervals

The endpoint must return HTTP 200 when the calculation succeeds.

Response format:

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

The response property names MUST be:

* min
* max
* producer
* interval
* previousWin
* followingWin

Use Pydantic response models.

---

# 7. Minimum and Maximum Rules

The API must return ALL producers that have the minimum interval.

The API must return ALL producers that have the maximum interval.

Example:

Producer A -> interval 1
Producer B -> interval 1
Producer C -> interval 5

The `min` array must contain both Producer A and Producer B.

Similarly, if:

Producer A -> interval 10
Producer B -> interval 10
Producer C -> interval 5

The `max` array must contain both Producer A and Producer B.

Do not return only the first producer found.

---

# 8. Producers With Insufficient Wins

A producer with fewer than two winning movies cannot have an interval.

Such producers must not appear in either `min` or `max`.

The implementation must handle this case without errors.

---

# 9. REST Maturity

The API must comply with Richardson Maturity Model Level 2.

Therefore:

* Use HTTP methods correctly.
* Use resource-oriented URLs.
* Return appropriate HTTP status codes.
* Return JSON representations.
* Do not implement RPC-style endpoints.

---

# 10. Architecture

Use a clean and maintainable architecture.

Suggested structure:

app/
├── main.py
├── api/
│   └── routes/
│       └── producers.py
├── core/
│   └── config.py
├── db/
│   ├── database.py
│   └── models.py
├── schemas/
│   └── producer.py
├── repositories/
│   └── movie_repository.py
├── services/
│   └── producer_interval_service.py
└── loaders/
└── csv_loader.py

tests/
└── integration/
└── test_producers.py

data/
└── Movielist.csv

Dockerfile
docker-compose.yml
requirements.txt
README.md

```

The exact structure may be adjusted if there is a strong technical reason, but responsibilities must remain separated.

---

# 11. Layer Responsibilities

## API Layer

Responsible only for:

- HTTP requests
- HTTP responses
- dependency injection
- response serialization

Do not implement business logic in the router.

## Service Layer

Responsible for:

- Producer interval calculation
- Minimum interval
- Maximum interval
- Handling ties
- Business rules

## Repository Layer

Responsible for:

- Database queries
- Retrieving movie/winner data

The service layer must not contain raw SQL/database-specific access logic unless strictly necessary.

## Loader

Responsible for:

- Reading CSV
- Parsing CSV records
- Persisting records into the database

---

# 12. Database

Use SQLite in-memory.

The database must not require an external service.

Use SQLAlchemy with an appropriate configuration for SQLite in-memory usage.

Important:

The application may use multiple connections during its lifecycle. Ensure that the in-memory database remains available to the application and tests throughout the process.

The database schema should contain at least the information required to determine:

- movie title
- winning year
- winner status
- producers

Do not store unnecessary information unless useful for the solution.

---

# 13. Application Startup

The CSV import must happen automatically during application startup.

Use FastAPI lifespan/startup mechanisms.

Startup flow:

1. Create database schema.
2. Read CSV.
3. Validate/parse rows.
4. Insert records.
5. Start serving API requests.

If the CSV cannot be loaded, the application should fail clearly rather than silently starting with incomplete data.

---

# 14. Testing

Only integration tests are required.

Do NOT create unit-test-only suites for the business logic.

Integration tests must exercise the application through the API.

Tests should verify at least:

### Test 1 — Minimum interval

Verify that the endpoint correctly identifies the producer(s) with the shortest interval.

### Test 2 — Maximum interval

Verify that the endpoint correctly identifies the producer(s) with the longest interval.

### Test 3 — Multiple producers with the same minimum interval

Verify that all producers tied for the minimum interval are returned.

### Test 4 — Multiple producers with the same maximum interval

Verify that all producers tied for the maximum interval are returned.

### Test 5 — Producer with only one win

Verify that producers with only one winning movie are excluded.

### Test 6 — Consecutive wins

Verify that only consecutive winning years are used to calculate intervals.

### Test 7 — API response schema

Verify that the response contains exactly the expected structure and fields.

Tests must make HTTP requests against the FastAPI application rather than directly calling service functions.

---

# 15. Test Data

Do not make the implementation dependent on the specific values in the supplied dataset.

The evaluation will use other datasets and different scenarios.

Therefore, tests should include controlled datasets that cover edge cases.

The algorithm must work for arbitrary valid input data.

---

# 16. Docker

The complete application must run with Docker.

Provide:

### Dockerfile

The Docker image must:

- Use a Python 3.9 base image.
- Install dependencies.
- Copy the application.
- Expose the API port.
- Start the FastAPI application.

### Docker Compose

Provide a `docker-compose.yml` that allows the application to be started with:

docker compose up

No external database container is required because SQLite must run in memory.

---

# 17. Configuration

Avoid hardcoding configuration throughout the code.

At minimum, make the CSV path configurable.

Use environment variables where appropriate.

Example:

CSV_FILE_PATH=/app/data/Movielist.csv

---

# 18. Code Quality

Follow these rules:

- Python 3.9 compatible syntax only.
- Use type hints.
- Follow PEP 8.
- Use descriptive names.
- Keep functions focused.
- Avoid duplicated code.
- Avoid unnecessary abstractions.
- Use dependency injection where appropriate.
- Do not use global mutable state unnecessarily.
- Do not introduce unnecessary dependencies.
- Handle errors explicitly.
- Do not silently ignore malformed input.
- Do not expose internal errors or stack traces through the API.

---

# 19. CSV Handling

The CSV loader must:

- Correctly handle the CSV header.
- Correctly parse years.
- Correctly identify winners.
- Correctly parse producers.
- Ignore movies that are not winners.
- Handle empty producer values safely.
- Normalize unnecessary whitespace.

Do not assume that the rows are already ordered.

The calculation must explicitly sort winning years.

---

# 20. Performance

The solution should avoid unnecessary database queries.

Prefer retrieving the relevant winning records in an efficient query and performing the interval calculation in memory.

Avoid an N+1 query pattern.

The algorithm should have approximately:

O(N log N)

complexity or better for N winning records.

---

# 21. Determinism

The API response should be deterministic.

When multiple producers have the same interval, sort the results consistently, preferably alphabetically by producer name.

This prevents tests from depending on database iteration order.

---

# 22. README

Create a README.md containing:

## Requirements

Explain that Docker is required.

## Running the application

Example:

docker compose up --build

## API

Document:

GET /api/v1/producers/intervals

Include an example request and response.

## Running integration tests

Document the exact command required to run the tests.

Example:

docker compose run --rm app pytest

or another appropriate Docker-based command.

## Project structure

Briefly explain the main directories.

---

# 23. AI Interaction Record

The assignment explicitly requires a record of interactions with the AI agent.

Create:

docs/
└── ai-interactions.md

This file must document the prompts/interactions used during development.

Do not fabricate interactions.

As development progresses, append the actual relevant prompts and summaries of the agent responses.

The document should make it clear that AI was used during development.

---

# 24. Acceptance Criteria

The implementation is considered complete only when:

- [ ] Python 3.9 is used.
- [ ] FastAPI is used.
- [ ] SQLAlchemy is used.
- [ ] SQLite in-memory is used.
- [ ] CSV is automatically imported during application startup.
- [ ] API does not directly read the CSV on every request.
- [ ] Only "Pior Filme" winners are considered.
- [ ] Producers are correctly separated.
- [ ] Winning years are sorted before calculating intervals.
- [ ] Only consecutive wins are compared.
- [ ] Producers with fewer than two wins are ignored.
- [ ] Minimum interval is correctly calculated.
- [ ] Maximum interval is correctly calculated.
- [ ] All producers tied for minimum are returned.
- [ ] All producers tied for maximum are returned.
- [ ] API follows Richardson Level 2.
- [ ] API returns the required JSON format.
- [ ] Integration tests cover the required scenarios.
- [ ] Tests interact with the API.
- [ ] Application runs entirely through Docker.
- [ ] No external database installation is required.
- [ ] README contains setup and execution instructions.
- [ ] AI interaction records are included in the repository.
- [ ] Code is compatible with Python 3.9.
- [ ] The solution works with datasets other than the supplied dataset.

---

# 25. Implementation Strategy

Before writing code:

1. Inspect the CSV structure.
2. Inspect the repository structure if an existing project is present.
3. Identify the exact CSV columns required.
4. Define the database model.
5. Define the API response schemas.
6. Define the repository interface.
7. Define the producer interval calculation.
8. Define the application startup lifecycle.
9. Define the integration-test strategy.
10. Define Docker configuration.

After the specification is understood, implement incrementally.

Do not rewrite unrelated files.

Do not add functionality outside the requirements.

Before finishing, run the integration tests and verify the Docker setup.

# Important

The evaluator will use different datasets.

Do not hardcode expected producers, years, intervals, or results from the supplied CSV.

The algorithm must derive the results dynamically from the database.

```
