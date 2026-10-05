import main
from main import app
import pytest
@pytest.fixture
def client(tmp_path):
    original_database = main.DATABASE

    test_database = tmp_path / "test_urls.db"

    main.DATABASE = str(test_database)

    main.init_db()

    yield app.test_client()

    main.DATABASE = original_database
def test_home(client):

    response = client.get("/")

    assert response.status_code == 200
    assert response.json["message"] == "your url shortner is running"
def test_shorten_valid_url(client):
    

    response = client.post(
        "/shorten",
        json={
            "url": "https://www.google.com"
        }
    )

    assert response.status_code == 201
    assert response.json["message"] == "URL shortened successfully"
    assert "short_code" in response.json
    assert "short_url" in response.json
def test_shorten_missing_url(client):

    response = client.post(
        "/shorten",
        json={}
    )

    assert response.status_code == 400
    assert response.json["message"] == "JSON body missing"
def test_shorten_url_field_missing(client):
    

    response = client.post(
        "/shorten",
        json={
            "name": "Muhesh"
        }
    )

    assert response.status_code == 400
    assert response.json["error"] == "URL is required"
def test_shorten_invalid_url(client):


    response = client.post(
        "/shorten",
        json={
            "url": "hello"
        }
    )

    assert response.status_code == 400
    assert response.json["message"] == "url is invalid"
def test_redirect_existing_url(client):
 

    create_response = client.post(
        "/shorten",
        json={
            "url": "https://www.google.com"
        }
    )

    assert create_response.status_code == 201

    short_code = create_response.json["short_code"]

    response = client.get(
        f"/{short_code}",
        follow_redirects=False
    )

    assert response.status_code == 302
    assert response.location == "https://www.google.com"
def test_redirect_unknown_code(client):


    response = client.get("/doesnotexist")

    assert response.status_code == 404
    assert response.json["error"] == "short url is not found"