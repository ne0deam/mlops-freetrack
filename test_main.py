
from unittest.mock import patch
from fastapi.testclient import TestClient
import main

client = TestClient(main.app)


def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "🎶 Spotify Recommender is running!"}

def test_recommend_success():
    fake_recs = [{"track_name": "Lucky Star", "artists": "Madonna", "album_name": "Like a Virgin"}]
    with patch("main.recommend_songs", return_value=fake_recs):
        response = client.get("/api/recommend/", params={"track_title": "Lucky", "n": 5})
    assert response.status_code == 200
    data = response.json()
    assert data["requested_track"] == "Lucky"
    assert data["recommendations"] == fake_recs

def test_recommend_not_found():
    with patch("main.recommend_songs", return_value=[]):
        response = client.get("/api/recommend/", params={"track_title": "NoSuchTrack", "n": 5})
    assert response.status_code == 404

def test_recommend_missing_track_title():
    response = client.get("/api/recommend/")
    assert response.status_code == 422

def test_recommend_n_out_of_range():
    with patch("main.recommend_songs", return_value=[{"track_title": "x", "artist": "y", "album_name": "z"}]):
        response = client.get("/api/recommend/", params={"track_title": "Lucky", "n": 100})
    assert response.status_code == 422