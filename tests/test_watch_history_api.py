import requests

BASE_URL = "http://127.0.0.1:8001"

def test_watch_movie_success():
    payload = {
        "user_id": 101,
        "movie_id": 201
    }

    response = requests.post(f"{BASE_URL}/watch", json=payload)

    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "success"
    assert data["user_id"] == 101
    assert data["movie_id"] == 201


def test_get_watch_history_success():
    response = requests.get(
        f"{BASE_URL}/watch_history",
        params={"user_id": 101}
    )

    assert response.status_code == 200
    data = response.json()

    assert data["user_id"] == 101
    assert isinstance(data["movies"], list)
    assert 201 in data["movies"]

def test_watch_invalid_user():
    payload = {
        "user_id": 999,  # invalid
        "movie_id": 201
    }

    response = requests.post(f"{BASE_URL}/watch", json=payload)

    assert response.status_code == 400
    assert "Invalid user_id" in response.text

def test_watch_invalid_movie():
    payload = {
        "user_id": 101,
        "movie_id": 999  # invalid
    }

    response = requests.post(f"{BASE_URL}/watch", json=payload)

    assert response.status_code == 400
    assert "Invalid movie_id" in response.text

def test_watch_missing_field():
    payload = {
        "user_id": 101
    }

    response = requests.post(f"{BASE_URL}/watch", json=payload)

    assert response.status_code == 422  # FastAPI validation error

def test_watch_wrong_type():
    payload = {
        "user_id": "abc",  # wrong type
        "movie_id": 201
    }

    response = requests.post(f"{BASE_URL}/watch", json=payload)

    assert response.status_code == 422

def test_watch_extra_field():
    payload = {
        "user_id": 101,
        "movie_id": 201,
        "extra": "not_allowed"
    }

    response = requests.post(f"{BASE_URL}/watch", json=payload)

    # FastAPI allows extra fields by default unless restricted
    assert response.status_code == 200

