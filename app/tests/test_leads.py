import pytest
from fastapi.testclient import TestClient
from app.main import app
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

client = TestClient(app)


def test_list_leads():
    response = client.get("/leads")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_show_add_lead_form():
    response = client.get("/leads/add")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_add_lead():
    response = client.post(
        "/leads/add",
        data={"name": "John Doe", "email": "john@example.com", "phone": "1234567890"},
    )
    assert response.status_code == 200
    assert "Lead added successfully!" in response.text


def test_404_on_invalid_lead():
    response = client.get("/leads/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Lead not found"
