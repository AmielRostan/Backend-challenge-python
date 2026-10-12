import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from backend_challenge_python.clients.pokemon import PokemonClient
from backend_challenge_python.config import settings
from backend_challenge_python.database import Base, get_db
from backend_challenge_python.main import app
from backend_challenge_python.models.user import User  # noqa: F401
from tests.mocks.pokemon import fake_get_pokemon

test_engine = create_engine(settings.test_database_url)

TestSessionLocal = sessionmaker(bind=test_engine)


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    Base.metadata.create_all(bind=test_engine)

    if test_engine.url.database != "usersdb_test":
        raise RuntimeError("Tests must use the usersdb_test database")

    yield

    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def db_session(setup_test_database):
    with TestSessionLocal() as session:
        session.execute(text("TRUNCATE TABLE users RESTART IDENTITY CASCADE"))
        session.commit()

        yield session


@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()


@pytest.fixture
def mock_pokemon_client(monkeypatch):
    monkeypatch.setattr(
        PokemonClient,
        "get_pokemon",
        fake_get_pokemon,
    )
