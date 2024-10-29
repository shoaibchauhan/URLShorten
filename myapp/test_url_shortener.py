import pytest # type: ignore
from fastapi.testclient import TestClient
from myapp.main import app
from myapp.models import URLMapping
from django.urls import reverse
from django.db import connection

# Initialize the FastAPI test client
client = TestClient(app)

@pytest.fixture(scope="function", autouse=True)
def setup_database():
    # Clear the database before each test
    with connection.cursor() as cursor:
        cursor.execute("TRUNCATE TABLE myapp_urlmapping CASCADE;")  # Ensure this matches your table name
    yield
    # Clean up after tests
    with connection.cursor() as cursor:
        cursor.execute("TRUNCATE TABLE myapp_urlmapping CASCADE;")

def test_shorten_url():
    # Test URL shortening
    response = client.post("/url/shorten", json={"url": "http://example.com"})
    assert response.status_code == 200
    data = response.json()
    assert "short_url" in data
    assert data["short_url"].startswith("http://localhost:8000/r/")

    # Verify the entry in the database
    url_mapping = URLMapping.objects.get(short_url=data["short_url"].split("/")[-1])
    assert url_mapping.original_url == "http://example.com/"  # Include the trailing slash here

def test_shorten_custom_url():
    # Test URL shortening with a custom slug
    response = client.post("/url/shorten/custom", json={
        "url": "http://example.com",
        "custom_slug": "exmpl",
        "expiration_days": 7
    })
    assert response.status_code == 200
    data = response.json()
    assert data["short_url"] == "http://localhost:8000/r/exmpl"
    assert data["custom_slug"] == "exmpl"

    # Verify the entry in the database
    url_mapping = URLMapping.objects.get(short_url="exmpl")
    assert url_mapping.original_url == "http://example.com/"  




def test_short_url_not_found():
    # Test retrieving a non-existent short URL
    response = client.get("/r/nonexistent")
    assert response.status_code == 404
    assert response.json() == {"detail": "HTTP 404: Short URL not found."}  

