"""
Round 2 Features Test Suite for Khmer Dubbing App
Tests: Duplicate project, Merge segments, Split segment, Rename project
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


@pytest.fixture(scope="module")
def test_project(api_url, headers):
    """Create a test project for round 2 tests."""
    r = requests.post(f"{api_url}/projects", json={"title": "Round2 Test"}, headers=headers)
    assert r.status_code == 200
    project = r.json()
    yield project
    requests.delete(f"{api_url}/projects/{project['project_id']}", headers=headers)


class TestDuplicateProject:
    def test_duplicate_creates_copy(self, api_url, headers, test_project):
        pid = test_project["project_id"]
        r = requests.post(f"{api_url}/projects/{pid}/duplicate", headers=headers)
        assert r.status_code == 200
        dup = r.json()
        assert dup["project_id"] != pid
        assert "Copy" in dup["title"]
        requests.delete(f"{api_url}/projects/{dup['project_id']}", headers=headers)


class TestMergeSegments:
    def test_merge_requires_indices(self, api_url, headers, test_project):
        pid = test_project["project_id"]
        r = requests.post(f"{api_url}/projects/{pid}/merge-segments",
                          json={"indices": []}, headers=headers)
        assert r.status_code in [400, 422]


class TestSplitSegment:
    def test_split_requires_valid_index(self, api_url, headers, test_project):
        pid = test_project["project_id"]
        r = requests.post(f"{api_url}/projects/{pid}/split-segment",
                          json={"index": 999}, headers=headers)
        assert r.status_code in [400, 404, 422]


class TestRenameProject:
    def test_rename_updates_title(self, api_url, headers, test_project):
        pid = test_project["project_id"]
        r = requests.patch(f"{api_url}/projects/{pid}",
                           json={"title": "Renamed Test"}, headers=headers)
        assert r.status_code == 200
        assert r.json()["title"] == "Renamed Test"
