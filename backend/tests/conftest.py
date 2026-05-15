import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
os.environ.setdefault("SECRET_KEY", "test-secret-key-at-least-32-characters-long")
os.environ.setdefault("API_KEY", "change-me-for-local-dev")

from app.database import Base, get_db  # noqa: E402
from app.main import app  # noqa: E402
from app.models import booking, cleaning, guest, room, stay, user  # noqa: F401, E402
from app.seed import seed_database  # noqa: E402

engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def auth_header(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="session", autouse=True)
def create_tables():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    seed_database(session)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture()
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture()
def admin_token(client: TestClient) -> str:
    r = client.post(
        "/api/auth/login",
        data={"username": "admin@hotel.example.com", "password": "admin123"},
    )
    assert r.status_code == 200
    return r.json()["access_token"]


@pytest.fixture()
def staff_token(client: TestClient) -> str:
    r = client.post(
        "/api/auth/login",
        data={"username": "staff@hotel.example.com", "password": "staff123"},
    )
    assert r.status_code == 200
    return r.json()["access_token"]
