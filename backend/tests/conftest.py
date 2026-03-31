"""Test configuration and shared fixtures for Khmer Dubbing App tests."""
import os
import pytest

# All test config from environment variables
TEST_BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')
TEST_AUTH_TOKEN = os.environ.get('TEST_SESSION_TOKEN', '')
TEST_USER_ID = os.environ.get('TEST_USER_ID', '')

if not TEST_BASE_URL:
    raise RuntimeError("REACT_APP_BACKEND_URL environment variable is required for tests")
if not TEST_AUTH_TOKEN:
    raise RuntimeError("TEST_SESSION_TOKEN environment variable is required for tests")

API_URL = f"{TEST_BASE_URL}/api"


@pytest.fixture(scope="session")
def base_url():
    return TEST_BASE_URL


@pytest.fixture(scope="session")
def api_url():
    return API_URL


@pytest.fixture(scope="session")
def auth_token():
    return TEST_AUTH_TOKEN


@pytest.fixture(scope="session")
def auth_headers():
    return {"Authorization": f"Bearer {TEST_AUTH_TOKEN}"}
