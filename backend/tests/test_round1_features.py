"""
Backend API Tests - Round 1 Features
Tests: Health check, share, download SRT/MP3, project fields
"""
import pytest
import requests
import os


@pytest.fixture(scope="module")
def api_url():
    base = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')
    return f"{base}/api"


@pytest.fixture(scope="module")
def headers():
    token = os.environ.get('TEST_SESSION_TOKEN', '')
    return {"Authorization": f"Bearer {token}"}


class TestHealthCheck:
    def test_api_root(self, api_url):
        r = requests.get(f"{api_url}/")
        assert r.status_code == 200
        assert "message" in r.json()


class TestSharedProject:
    def test_shared_nonexistent_returns_404(self, api_url):
        r = requests.get(f"{api_url}/shared/nonexistent_token_123")
        assert r.status_code == 404


class TestProjectFields:
    def test_create_project_has_fields(self, api_url, headers):
        r = requests.post(f"{api_url}/projects", json={"title": "R1 Test"}, headers=headers)
        assert r.status_code == 200
        p = r.json()
        assert "project_id" in p
        assert "share_token" in p or p.get("share_token") is None
        requests.delete(f"{api_url}/projects/{p['project_id']}", headers=headers)

    def test_list_projects(self, api_url, headers):
        r = requests.get(f"{api_url}/projects", headers=headers)
        assert r.status_code == 200
        assert isinstance(r.json(), list)


class TestDownloads:
    @pytest.fixture(scope="class")
    def empty_project(self, api_url, headers):
        r = requests.post(f"{api_url}/projects", json={"title": "Download Test"}, headers=headers)
        p = r.json()
        yield p
        requests.delete(f"{api_url}/projects/{p['project_id']}", headers=headers)

    def test_download_srt_no_segments(self, api_url, headers, empty_project):
        r = requests.get(f"{api_url}/projects/{empty_project['project_id']}/download-srt", headers=headers)
        assert r.status_code == 400

    def test_download_mp3_no_audio(self, api_url, headers, empty_project):
        r = requests.get(f"{api_url}/projects/{empty_project['project_id']}/download-mp3", headers=headers)
        assert r.status_code == 400
