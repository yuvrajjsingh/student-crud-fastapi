"""API tests use a temporary SQLite database and never touch real student data."""
import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.database import get_db, initialize_database
from app.main import app
import sqlite3


@pytest.fixture()
def client(tmp_path: Path):
    test_db = tmp_path / "test_students.db"
    os.environ["STUDENT_DB_PATH"] = str(test_db)
    initialize_database(test_db)

    def override_get_db():
        conn = sqlite3.connect(test_db, timeout=10)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    os.environ.pop("STUDENT_DB_PATH", None)


sample = {
    "name": "Aarav Sharma",
    "date_of_birth": "2005-08-17",
    "email": "aarav@example.com",
    "phone": "9876543210",
    "course": "B.Tech CSE",
    "address": "Lucknow",
    "enrollment_date": "2024-08-01",
}


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_and_read_student(client):
    created = client.post("/students", json=sample)
    assert created.status_code == 201
    student = created.json()
    assert student["id"] == 1
    assert student["name"] == "Aarav Sharma"
    assert client.get("/students/1").json()["email"] == "aarav@example.com"


def test_list_filters_by_name_and_course(client):
    client.post("/students", json=sample)
    other = {**sample, "name": "Diya Verma", "email": "diya@example.com", "course": "BCA"}
    client.post("/students", json=other)
    assert len(client.get("/students?name=aarav").json()) == 1
    assert len(client.get("/students?course=bca").json()) == 1


def test_patch_student(client):
    client.post("/students", json=sample)
    response = client.patch("/students/1", json={"course": "M.Tech CSE"})
    assert response.status_code == 200
    assert response.json()["course"] == "M.Tech CSE"
    assert response.json()["name"] == "Aarav Sharma"


def test_put_replaces_student_fields(client):
    client.post("/students", json=sample)
    replacement = {**sample, "name": "Aarav Updated", "course": "BCA"}
    response = client.put("/students/1", json=replacement)
    assert response.status_code == 200
    assert response.json()["name"] == "Aarav Updated"


def test_delete_student(client):
    client.post("/students", json=sample)
    assert client.delete("/students/1").status_code == 204
    assert client.get("/students/1").status_code == 404


def test_missing_record_returns_404(client):
    assert client.get("/students/999").status_code == 404
    assert client.delete("/students/999").status_code == 404


def test_contact_is_required(client):
    invalid = {**sample, "email": None, "phone": None}
    response = client.post("/students", json=invalid)
    assert response.status_code == 422


def test_birth_date_cannot_be_in_future(client):
    invalid = {**sample, "date_of_birth": "2099-01-01"}
    assert client.post("/students", json=invalid).status_code == 422


def test_count_question_uses_database(client):
    client.post("/students", json=sample)
    response = client.post("/ai/ask", json={"question": "How many students are there?"})
    assert response.status_code == 200
    assert "1 student" in response.json()["answer"]
