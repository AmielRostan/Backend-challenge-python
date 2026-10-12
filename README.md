# Cursor Backend Challenge Python / FastAPI

A RESTful API for managing users and retrieving their associated Pokemon information from the PokeAPI.

Built with Python and FastAPI, using PostreSQL for data persistance, SQLAlchemy for database access, and Alembic for schema migrations

### Tech Stack

- Python 3.13 - Programming language
- FastAPI - REST API framework and automatic OpenAPI documentation
- Pydantic - Request validation, response serialization, and application settings
- PostgreSQL 15 - Relational database
- SQLAlchemy - ORM and database access
- Alembic - Database schema migrations
- HTTPX - HTTP client for PokeAPI integration
- Pytest - Automated testing
- Docker & Docker Compose - Containerized application and database
- uv - Python dependency and environment management

### Features

- Create, retrieve, update, and delete users.
- Validate incoming requests using Pydantic schemas.
- Store user information in PostgreSQL.
- Hash passwords before storing them.
- Prevent duplicate user email addresses.
- Retrieve Pokemon information from the external PokeAPI.
- Provide interactive API documentation through Swagger UI.
- Apply database migrations automatically when starting the Dockerized application.
- Run automated tests against a separate test database, using mocked external API responses.

### Prerequisites

To run the application and its automated tests using Docker, you only need:

- Git - to clone the repository.
- Docker Desktop - With Docker Compose available and the Docker engine running.

Python and PostgreSQL do not need to be installed locally when using Docker.

For development without Docker containers for the API, you will also need Python 3.13 and uv.

### How to Run the App

#### Using Docker (Recommended)

1. Clone the repository and navigate to the project directory.
2. Start the application:
```bash
bash ./up_dev.sh
```
The script builds and starts the FastAPI application and PostgreSQL database in the background.
Database migrations are applied automatically using Alembic.
3. Access the application:
- Swagger UI: http://localhost:8000/docs
- Health check: http://localhost:8000/health
- OpenAPI schema: http://localhost:8000/openapi.json

To view the application logs:
```bash
docker compose logs -f api
```
To stop the application:
```bash
docker compose down
```
The PostgreSQL data is persisted in a Docker volume, so stopping and recreating containers does not delete existing records.

#### Local Development
1. Install the project dependencies:
```bash
uv sync
```
2. Create a local environment file:
```bash
cp .env.example .env
```
3. Start the PostgreSQL service:
```bash
docker compose up -d db
```
4. Applu database migrations:
```bash
uv run alembic upgrade head
```
5. Start the development server:
```bash
uv run fastapi dev
```
The application will be available at http://localhost:8000

*Note:* The local environment uses localhost:5433 to connect to PostgreSQL, while Docker containers communicate through the internal hostname db:5432.

## How to Run the Tests

The project includes automated tests using **Pytest**, covering the API endpoints, request validation, error handling, and Pokémon integration.

### Using Docker (Recommended)

Run the entire test suite with:

```bash
bash ./up_test.sh
```

The script builds the testing container, starts PostgreSQL if necessary, and executes the tests.

No local Python installation is required.

### Running Tests Locally

Start PostgreSQL:

```bash
docker compose up -d db
```

Install dependencies and execute the test suite:

```bash
uv sync
uv run pytest -v
```

To run a specific test:

```bash
uv run pytest tests/test_users.py::test_create_user -v
```

### Test Isolation

Tests use a dedicated PostgreSQL database (`usersdb_test`), separate from the development database (`usersdb`).

The test configuration creates the required tables before running the suite and removes them afterward.

External PokéAPI responses are mocked, making the tests independent of network availability and the external service.

The suite currently contains **10 automated tests**.

## API Endpoints

The API provides RESTful endpoints for user management and Pokémon data retrieval.

Interactive API documentation is available through **Swagger UI** at:

http://localhost:8000/docs

### Available Endpoints

| Method | Endpoint | Description | Success Status |
|---|---|---|---|
| GET | `/health` | Check API health | `200 OK` |
| POST | `/users` | Create a new user | `201 Created` |
| GET | `/users` | Retrieve all users | `200 OK` |
| GET | `/users/{id}` | Retrieve a user with associated Pokémon information | `200 OK` |
| PUT | `/users/{id}` | Update an existing user | `200 OK` |
| DELETE | `/users/{id}` | Delete a user | `204 No Content` |

### Example: Create a User

**Request**

`POST /users`

```json
{
  "username": "ash",
  "email": "ash@example.com",
  "password": "password123",
  "pokemon_ids": [25, 6]
}
```

The password is securely hashed before being stored in the database and is not included in API responses.

### Error Handling

The API uses standard HTTP status codes:

| Status | Description |
|---|---|
| `404 Not Found` | The requested user does not exist |
| `409 Conflict` | A user with the provided email already exists |
| `422 Unprocessable Entity` | Request validation failed |

FastAPI automatically generates an OpenAPI specification at `/openapi.json`, which can also be used to inspect request and response schemas.

## Project Structure

The application follows a layered architecture, separating HTTP handling, business logic, database access, and external integrations.

```text
backend-challenge-python/
├── alembic/                  # Database migrations
├── docker/
│   └── init/                 # PostgreSQL initialization scripts
├── src/
│   └── backend_challenge_python/
│       ├── api/              # FastAPI routes and HTTP handlers
│       ├── clients/          # External API integrations
│       ├── models/           # SQLAlchemy database models
│       ├── repositories/     # Database access and queries
│       ├── schemas/          # Pydantic request/response models
│       ├── services/         # Business logic
│       ├── config.py         # Application settings
│       ├── database.py       # Database connection and sessions
│       └── main.py           # FastAPI application entry point
├── tests/
│   ├── mocks/                # Mocked external API responses
│   ├── conftest.py           # Shared fixtures and test setup
│   ├── test_health.py
│   └── test_users.py
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
├── uv.lock
├── up_dev.sh
└── up_test.sh
```

### Architecture Overview

- **API:** Defines HTTP endpoints, handles incoming requests, and returns responses.
- **Services:** Implements application business logic and coordinates dependencies.
- **Repositories:** Encapsulates database operations using SQLAlchemy.
- **Clients:** Handles communication with external services, such as PokéAPI.
- **Models:** Defines the database entities and their relationships.
- **Schemas:** Validates incoming data and defines API response structures.

This separation improves maintainability, testability, and readability by keeping each component focused on a specific responsibility.

## Technical Decisions

### Layered Architecture

The application separates HTTP handling, business logic, database access, and external API integrations into dedicated layers.

This keeps route handlers focused on HTTP concerns while allowing business logic and persistence operations to evolve independently.

For a small application, this introduces some additional structure, but improves separation of concerns and maintainability.

### PostgreSQL and SQLAlchemy

PostgreSQL was chosen as the relational database, with SQLAlchemy providing ORM-based database access.

Using PostgreSQL in both development and testing helps ensure that tests exercise the same database behavior as the application.

### Database Migrations with Alembic

Database schema changes are managed through versioned Alembic migrations instead of automatically creating tables at application startup.

When running with Docker, pending migrations are applied before the API starts. This provides a reproducible database setup for reviewers.

### Password Hashing

User passwords are hashed using Argon2 before being stored in PostgreSQL.

Password hashes are excluded from API responses to avoid exposing sensitive information.

### External API Integration

Pokémon information is retrieved from PokéAPI through a dedicated HTTP client using HTTPX.

Keeping this integration separate from the business logic makes it easier to maintain and mock during testing.

### Testing Strategy

The project uses Pytest with a dedicated PostgreSQL test database.

Database operations are tested against a real PostgreSQL instance, while external PokéAPI responses are mocked.

This approach provides confidence in database interactions without making the test suite dependent on external network availability.

### Dockerized Development and Testing

Docker Compose provides a reproducible environment for running the API, PostgreSQL, and automated tests.

Separate scripts simplify the setup process and allow reviewers to start the application or run the test suite with a single command.

## Areas to Improve

The current implementation covers the core challenge requirements. Given additional development time, the following improvements would be prioritized:

### Continuous Integration

Set up a GitHub Actions workflow to automatically run linting and automated tests on every pull request.

This would help detect regressions before changes are merged.

### Test Coverage

Introduce coverage reporting with `pytest-cov` and expand the test suite to cover additional edge cases, including external API failures and database errors.

### External API Resilience

Improve the PokéAPI integration with explicit request timeouts, structured error handling, and appropriate responses when the external service is unavailable.

Caching frequently requested Pokémon data could also reduce unnecessary external API calls.

### Authentication and Authorization

Introduce JWT-based authentication and authorization to protect user management endpoints.

The current implementation focuses on the CRUD operations required by the challenge and does not implement authenticated access.

### Production Deployment

For a production environment, move database migrations into a dedicated deployment step rather than running them on every API container startup.

Additionally, use managed secrets, production-specific database credentials, and more comprehensive application monitoring.

### Code Quality Automation

Integrate Ruff for Python linting and formatting, and enforce consistent code quality checks through CI.