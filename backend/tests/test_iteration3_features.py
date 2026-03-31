"""
Backend API Tests - Iteration 3 Features
Tests: Health, project actors, upload-actor-voice, transcribe-segments
"""
import pytest
import requests
import os
import io


@pytest.fixture(scope="module")
def api_url():
    base = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')
    return f"{base}/api"


@pytest.fixture(scope="module")
def headers():
    token = os.environ.get('TEST_SESSION_TOKEN', '')
    return {"Authorization": f"Bearer {token}"}


class TestHealthAndBasicEndpoints:
    def test_health_check(self, api_url):
        r = requests.get(f"{api_url}/")
        assert r.status_code == 200

    def test_create_project_has_actors(self, api_url, headers):
        r = requests.post(f"{api_url}/projects", json={"title": "Actor Test"}, headers=headers)
        assert r.status_code == 200
        p = r.json()
        assert "actors" in p
        requests.delete(f"{api_url}/projects/{p['project_id']}", headers=headers)

    def test_patch_project_actors(self, api_url, headers):
        r = requests.post(f"{api_url}/projects", json={"title": "Patch Actors"}, headers=headers)
        p = r.json()
        actors = [{"id": "SPEAKER_00", "label": "Test Boy", "gender": "male", "voice": "dara"}]
        r2 = requests.patch(f"{api_url}/projects/{p['project_id']}",
                            json={"actors": actors}, headers=headers)
        assert r2.status_code == 200
        assert r2.json()["actors"][0]["gender"] == "male"
        requests.delete(f"{api_url}/projects/{p['project_id']}", headers=headers)
