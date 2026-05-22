from __future__ import annotations

import pytest
from httpx import AsyncClient, ASGITransport

from stie.api.app import create_app


@pytest.fixture
def app():
    return create_app()


@pytest.fixture
async def client(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.mark.integration
class TestHealthEndpoint:
    async def test_health_check(self, client):
        response = await client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "version" in data
        assert "timestamp" in data

    async def test_health_returns_valid_version(self, client):
        response = await client.get("/api/v1/health")
        data = response.json()
        assert data["version"] == "0.1.0"

    async def test_health_returns_iso_timestamp(self, client):
        response = await client.get("/api/v1/health")
        data = response.json()
        assert "T" in data["timestamp"]

    async def test_auth_endpoint_not_implemented(self, client):
        response = await client.post("/api/v1/auth/login", json={
            "username": "test",
            "password": "test",
        })
        assert response.status_code == 501

    async def test_cors_headers(self, client):
        response = await client.options(
            "/api/v1/health",
            headers={
                "Origin": "http://example.com",
                "Access-Control-Request-Method": "GET",
            },
        )
        assert response.status_code == 200
