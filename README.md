# Backend Challenge — Python / FastAPI

REST API for managing users and retrieving their associated Pokémon data from PokéAPI.

Built with **Python 3.13, FastAPI, PostgreSQL 15, SQLAlchemy, Alembic, and HTTPX**. Uses Pydantic for validation, Argon2 for password hashing, and Pytest for automated testing.

[![CircleCI](https://dl.circleci.com/status-badge/img/gh/AmielRostan/Backend-challenge-python/tree/master.svg?style=svg)](https://dl.circleci.com/status-badge/redirect/gh/AmielRostan/Backend-challenge-python/tree/master)

## Getting Started

**Requirements:** Docker Desktop with Docker Compose.

Start the API and database:

```bash
bash ./up_dev.sh
```

The script builds the containers, starts PostgreSQL, and applies Alembic migrations automatically.

- **Swagger UI:** http://localhost:8000/docs
- **Health check:** http://localhost:8000/health

Stop the application:

```bash
docker compose down
```

### Local Development (Optional)

Requires Python 3.13, uv, and Docker for PostgreSQL.

```bash
uv sync
cp .env.example .env
docker compose up -d db
uv run alembic upgrade head
uv run fastapi dev
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Health check |
| POST | `/users` | Create user |
| GET | `/users` | List users |
| GET | `/users/{id}` | Get user with Pokémon data |
| PUT | `/users/{id}` | Update user |
| DELETE | `/users/{id}` | Delete user |

Requests are validated with Pydantic. The API returns `404` for missing users, `409` for duplicate emails, and `422` for validation errors. Passwords are hashed and excluded from API responses.

Full request and response schemas are available in Swagger UI.

## Testing & Code Quality

Run the test suite using Docker:

```bash
bash ./up_test.sh
```

Or run locally with PostgreSQL available:

```bash
uv run pytest -v
```

Run tests with coverage:

```bash
uv run pytest --cov=backend_challenge_python --cov-report=term-missing
```

Run linting and formatting checks:

```bash
uv run ruff check .
uv run ruff format --check .
```

**Current results:** 10 passing tests and 91% statement coverage.

## Architecture & Technical Decisions

- **Layered structure:** API routes, services, repositories, and external clients have separate responsibilities.
- **Database:** PostgreSQL with SQLAlchemy and versioned Alembic migrations.
- **Testing:** A separate PostgreSQL test database exercises real database operations; PokéAPI responses are mocked to avoid network dependencies.
- **Security:** Passwords are hashed using Argon2 and are never returned in API responses.
- **Docker:** Provides a reproducible setup for running the API and tests.

## Future Improvements

- Add GitHub Actions for automated linting and testing.
- Expand tests for external API failures and other edge cases.
- Improve external API resilience and add authentication if required for production use.
