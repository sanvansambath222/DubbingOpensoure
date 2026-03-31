"""
Backend API Tests - Actor Features
Tests: upload-actor-voice, PATCH projects with actors
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


class TestActorEndpoints:
    @pytest.fixture(scope="class")
    def test_project(self, api_url, headers):
        r = requests.post(f"{api_url}/projects", json={"title": "Actor API Test"}, headers=headers)
        p = r.json()
        yield p
        requests.delete(f"{api_url}/projects/{p['project_id']}", headers=headers)

    def test_upload_actor_voice_no_file(self, api_url, headers, test_project):
        pid = test_project["project_id"]
        r = requests.post(f"{api_url}/projects/{pid}/upload-actor-voice",
                          data={"actor_id": "SPEAKER_00"}, headers=headers)
        assert r.status_code in [400, 422]

    def test_patch_actors(self, api_url, headers, test_project):
        pid = test_project["project_id"]
        actors = [{"id": "SPEAKER_00", "label": "Girl", "gender": "female", "voice": "sophea"}]
        r = requests.patch(f"{api_url}/projects/{pid}", json={"actors": actors}, headers=headers)
        assert r.status_code == 200
        assert len(r.json()["actors"]) == 1
