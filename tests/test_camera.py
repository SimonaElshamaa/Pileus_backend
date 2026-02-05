import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.session import SessionLocal
from app.models.camera import Camera

client = TestClient(app)

# Fixture for creating a temporary camera in the DB
@pytest.fixture
def db_camera():
    db = SessionLocal()
    camera = Camera(name="Test Camera")
    db.add(camera)
    db.commit()
    db.refresh(camera)
    yield camera
    db.delete(camera)
    db.commit()
    db.close()


def test_create_camera():
    response = client.post(
        "/api/v1/cameras/",
        json={"name": "Entrance Camera"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["name"] == "Entrance Camera"


def test_get_camera(db_camera):
    response = client.get(f"/api/v1/cameras/{db_camera.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == db_camera.id
    assert data["name"] == db_camera.name


def test_get_camera_not_found():
    response = client.get("/api/v1/cameras/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Camera not found"
