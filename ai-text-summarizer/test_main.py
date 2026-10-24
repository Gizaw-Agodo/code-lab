from fastapi.testclient import TestClient
from httpx import Response

from main import app

client: TestClient = TestClient(app)


def test_health_check() -> None:
    response: Response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_summarize_text() -> None:
    response: Response = client.post(
        "/summarize",
        json={
            "text": (
                "Python is useful. "
                "FastAPI builds APIs. "
                "Testing improves quality."
            ),
            "max_sentences": 2,
        },
    )

    assert response.status_code == 200
    assert response.json()["summary"] == (
        "Python is useful. FastAPI builds APIs."
    )
    assert response.json()["summary_length"] > 0


def test_reject_short_text() -> None:
    response: Response = client.post(
        "/summarize",
        json={"text": "Too short"},
    )

    assert response.status_code == 422