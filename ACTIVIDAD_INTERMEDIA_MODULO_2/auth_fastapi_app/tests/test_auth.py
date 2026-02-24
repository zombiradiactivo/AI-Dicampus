import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import Session
from typing import Generator, AsyncGenerator

from app.main import app
from app.api.auth import get_db
from app.database import Base

# --- Base de Datos de Prueba ---
SQLALCHEMY_DATABASE_URL = "sqlite://"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db() -> Generator[Session, None, None]:
    db = None
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        if db is not None:
            db.close()

app.dependency_overrides[get_db] = override_get_db

# --- FIXTURES ---

@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    """Cliente asíncrono que evita el error de __init__ en Python 3.14"""
    # Usamos ASGITransport para conectar directamente con la app de FastAPI
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# --- CASOS DE PRUEBA (Ahora son asíncronos con 'async def') ---

@pytest.mark.anyio
async def test_register_user_success(client: AsyncClient):
    response = await client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "password123", "full_name": "Test User"}
    )
    assert response.status_code == 200

@pytest.mark.anyio
async def test_register_user_duplicate_email(client: AsyncClient):
    user_data = {"email": "duplicate@example.com", "password": "password123"}
    await client.post("/auth/register", json=user_data)
    response = await client.post("/auth/register", json=user_data)
    assert response.status_code == 400

@pytest.mark.anyio
async def test_login_success(client: AsyncClient):
    await client.post(
        "/auth/register",
        json={"email": "login@example.com", "password": "secretpassword"}
    )
    # Login con form data
    response = await client.post(
        "/auth/login",
        data={"username": "login@example.com", "password": "secretpassword"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

@pytest.mark.anyio
async def test_read_users_me_protected(client: AsyncClient):
    # Sin token
    response = await client.get("/auth/me")
    assert response.status_code == 401

    # Con token
    await client.post("/auth/register", json={"email": "me@example.com", "password": "password"})
    login_res = await client.post("/auth/login", data={"username": "me@example.com", "password": "password"})
    token = login_res.json()["access_token"]
    
    response = await client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200