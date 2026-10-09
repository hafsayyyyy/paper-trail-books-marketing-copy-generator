
import pytest
from app import app
from src.generator import generate_marketing_copy


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as test_client:
        yield test_client


def test_missing_api_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    with pytest.raises(ValueError, match="OPENAI_API_KEY is missing"):
        generate_marketing_copy(
            "The Lost World",
            "John Smith",
            "Adventure",
            "A journey into a mysterious world.",
            "Young adults"
        )


def test_generate_requires_json(client):
    response = client.post("/generate", data="not json")
    assert response.status_code == 415


def test_generate_rejects_missing_fields(client):
    response = client.post(
        "/generate",
        json={"title": "The Lost World"}
    )
    assert response.status_code == 400


def test_generate_rejects_invalid_copy_type(client):
    response = client.post(
        "/generate",
        json={
            "title": "The Lost World",
            "author": "John Smith",
            "genre": "Adventure",
            "description": "A journey into a mysterious world.",
            "audience": "Young adults",
            "copy_type": "invalid"
        }
    )
    assert response.status_code == 400
