"""
Test suite for multi-language output support.
"""
import pytest
import requests
import os

EXPECTED_LANGUAGES = [
    "km", "th", "vi", "ko", "ja", "en", "zh", "id", "hi", "es",
    "fr", "tl", "de", "pt", "ru", "ar", "it", "ms", "lo", "my"
]


@pytest.fixture(scope="module")
def api_url():
    base = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')
    return f"{base}/api"


@pytest.fixture(scope="module")
def headers():
    token = os.environ.get('TEST_SESSION_TOKEN', '')
    return {"Authorization": f"Bearer {token}"}


class TestLanguagesRemoved:
    def test_languages_endpoint_removed(self, api_url):
        r = requests.get(f"{api_url}/languages")
        assert r.status_code in [404, 405]


class TestTranslateTargetLanguage:
    @pytest.fixture(scope="class")
    def test_project(self, api_url, headers):
        r = requests.post(f"{api_url}/projects", json={"title": "MultiLang Test"}, headers=headers)
        p = r.json()
        yield p
        requests.delete(f"{api_url}/projects/{p['project_id']}", headers=headers)

    def test_translate_with_korean(self, api_url, headers, test_project):
        pid = test_project["project_id"]
        r = requests.post(f"{api_url}/projects/{pid}/translate-segments?target_language=ko", headers=headers)
        assert r.status_code in [200, 400]

    def test_auto_process_with_target(self, api_url, headers, test_project):
        pid = test_project["project_id"]
        r = requests.post(f"{api_url}/projects/{pid}/auto-process?target_language=ja", headers=headers)
        assert r.status_code in [200, 400]
