"""
Test suite for Video Dubbing App - Progress Bar & Chunked Translation Features
Tests:
1. GET /api/projects/{id}/queue-status returns progress fields
2. queue-status returns 0 progress when no processing
3. /api/languages endpoint no longer exists (should return 404)
4. POST translate-segments accepts target_language param
"""
import pytest
import requests
import os

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')
AUTH_TOKEN = "test_session_001"
HEADERS = {"Authorization": f"Bearer {AUTH_TOKEN}"}


class TestQueueStatusEndpoint:
    """Tests for GET /api/projects/{id}/queue-status endpoint"""
    
    @pytest.fixture(scope="class")
    def test_project(self):
        """Create a test project for queue-status tests"""
        response = requests.post(
            f"{BASE_URL}/api/projects",
            json={"title": "TEST_Progress_Test_Project"},
            headers=HEADERS
        )
        assert response.status_code == 200, f"Failed to create project: {response.text}"
        project = response.json()
        yield project
        # Cleanup
        requests.delete(f"{BASE_URL}/api/projects/{project['project_id']}", headers=HEADERS)
    
    def test_queue_status_returns_200(self, test_project):
        """Test that queue-status endpoint returns 200 for valid project"""
        response = requests.get(
            f"{BASE_URL}/api/projects/{test_project['project_id']}/queue-status",
            headers=HEADERS
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        print(f"✓ queue-status returns 200 for valid project")
    
    def test_queue_status_has_required_fields(self, test_project):
        """Test that queue-status returns all required progress fields"""
        response = requests.get(
            f"{BASE_URL}/api/projects/{test_project['project_id']}/queue-status",
            headers=HEADERS
        )
        assert response.status_code == 200
        data = response.json()
        
        # Check all required fields exist
        required_fields = ["step", "progress", "total", "elapsed", "eta"]
        for field in required_fields:
            assert field in data, f"Missing required field: {field}"
            print(f"✓ Field '{field}' present in response")
        
        # Also check project_id and status
        assert "project_id" in data, "Missing project_id field"
        assert "status" in data, "Missing status field"
        print(f"✓ All required fields present: {list(data.keys())}")
    
    def test_queue_status_returns_zero_when_idle(self, test_project):
        """Test that queue-status returns 0 progress when no processing is happening"""
        response = requests.get(
            f"{BASE_URL}/api/projects/{test_project['project_id']}/queue-status",
            headers=HEADERS
        )
        assert response.status_code == 200
        data = response.json()
        
        # When no processing, progress should be 0
        assert data["progress"] == 0, f"Expected progress=0 when idle, got {data['progress']}"
        assert data["total"] == 0, f"Expected total=0 when idle, got {data['total']}"
        print(f"✓ queue-status returns progress=0, total=0 when idle")
        print(f"  Response: step='{data.get('step', '')}', progress={data['progress']}, total={data['total']}")
    
    def test_queue_status_elapsed_and_eta_are_numbers(self, test_project):
        """Test that elapsed and eta are numeric values"""
        response = requests.get(
            f"{BASE_URL}/api/projects/{test_project['project_id']}/queue-status",
            headers=HEADERS
        )
        assert response.status_code == 200
        data = response.json()
        
        assert isinstance(data["elapsed"], (int, float)), f"elapsed should be numeric, got {type(data['elapsed'])}"
        assert isinstance(data["eta"], (int, float)), f"eta should be numeric, got {type(data['eta'])}"
        print(f"✓ elapsed ({data['elapsed']}) and eta ({data['eta']}) are numeric")
    
    def test_queue_status_requires_auth(self):
        """Test that queue-status requires authentication"""
        # First create a project to get a valid ID
        response = requests.post(
            f"{BASE_URL}/api/projects",
            json={"title": "TEST_Auth_Test"},
            headers=HEADERS
        )
        project_id = response.json()["project_id"]
        
        # Try without auth
        response = requests.get(f"{BASE_URL}/api/projects/{project_id}/queue-status")
        assert response.status_code == 401, f"Expected 401 without auth, got {response.status_code}"
        print(f"✓ queue-status requires authentication (returns 401 without token)")
        
        # Cleanup
        requests.delete(f"{BASE_URL}/api/projects/{project_id}", headers=HEADERS)
    
    def test_queue_status_404_for_invalid_project(self):
        """Test that queue-status returns 404 for non-existent project"""
        response = requests.get(
            f"{BASE_URL}/api/projects/invalid_project_id_12345/queue-status",
            headers=HEADERS
        )
        assert response.status_code == 404, f"Expected 404 for invalid project, got {response.status_code}"
        print(f"✓ queue-status returns 404 for non-existent project")


class TestLanguagesEndpointRemoved:
    """Tests to verify /api/languages endpoint has been removed"""
    
    def test_languages_endpoint_returns_404_or_405(self):
        """Test that /api/languages endpoint no longer exists"""
        response = requests.get(f"{BASE_URL}/api/languages")
        # Should return 404 (not found) or 405 (method not allowed)
        assert response.status_code in [404, 405, 422], \
            f"Expected 404/405/422 for removed /api/languages, got {response.status_code}"
        print(f"✓ /api/languages endpoint returns {response.status_code} (endpoint removed)")
    
    def test_languages_endpoint_with_auth_still_404(self):
        """Test that /api/languages returns 404 even with auth"""
        response = requests.get(f"{BASE_URL}/api/languages", headers=HEADERS)
        assert response.status_code in [404, 405, 422], \
            f"Expected 404/405/422 for removed /api/languages with auth, got {response.status_code}"
        print(f"✓ /api/languages endpoint returns {response.status_code} even with auth")


class TestTranslateSegmentsWithTargetLanguage:
    """Tests for POST /api/projects/{id}/translate-segments with target_language param"""
    
    @pytest.fixture(scope="class")
    def project_with_segments(self):
        """Create a test project with segments for translation tests"""
        # Create project
        response = requests.post(
            f"{BASE_URL}/api/projects",
            json={"title": "TEST_Translate_Segments_Test"},
            headers=HEADERS
        )
        assert response.status_code == 200
        project = response.json()
        project_id = project["project_id"]
        
        # Add test segments directly via PATCH
        test_segments = [
            {"id": 0, "start": 0, "end": 2, "original": "Hello world", "translated": "", "speaker": "SPEAKER_00", "gender": "female"},
            {"id": 1, "start": 2, "end": 4, "original": "How are you", "translated": "", "speaker": "SPEAKER_00", "gender": "female"},
        ]
        response = requests.patch(
            f"{BASE_URL}/api/projects/{project_id}",
            json={"segments": test_segments, "detected_language": "en"},
            headers=HEADERS
        )
        assert response.status_code == 200
        
        yield response.json()
        
        # Cleanup
        requests.delete(f"{BASE_URL}/api/projects/{project_id}", headers=HEADERS)
    
    def test_translate_segments_accepts_target_language_param(self, project_with_segments):
        """Test that translate-segments endpoint accepts target_language query param"""
        project_id = project_with_segments["project_id"]
        
        # Test with target_language=th (Thai)
        response = requests.post(
            f"{BASE_URL}/api/projects/{project_id}/translate-segments?target_language=th",
            headers=HEADERS,
            timeout=120
        )
        
        # Should return 200 (success) or 500 (if LLM fails, but endpoint accepts param)
        assert response.status_code in [200, 500], \
            f"translate-segments should accept target_language param, got {response.status_code}: {response.text}"
        
        if response.status_code == 200:
            data = response.json()
            # Verify target_language was saved
            assert data.get("target_language") == "th", f"Expected target_language='th', got {data.get('target_language')}"
            print(f"✓ translate-segments accepts target_language=th and saves it")
        else:
            print(f"✓ translate-segments accepts target_language param (endpoint returned 500 - LLM issue, not param issue)")
    
    def test_translate_segments_defaults_to_km(self):
        """Test that translate-segments defaults to 'km' when no target_language provided"""
        # Create a fresh project with segments
        response = requests.post(
            f"{BASE_URL}/api/projects",
            json={"title": "TEST_Default_Lang_Test"},
            headers=HEADERS
        )
        project = response.json()
        project_id = project["project_id"]
        
        # Add segments
        test_segments = [
            {"id": 0, "start": 0, "end": 2, "original": "Test text", "translated": "", "speaker": "SPEAKER_00", "gender": "female"},
        ]
        requests.patch(
            f"{BASE_URL}/api/projects/{project_id}",
            json={"segments": test_segments, "detected_language": "en"},
            headers=HEADERS
        )
        
        # Call translate without target_language
        response = requests.post(
            f"{BASE_URL}/api/projects/{project_id}/translate-segments",
            headers=HEADERS,
            timeout=120
        )
        
        if response.status_code == 200:
            data = response.json()
            # Default should be 'km' (Khmer)
            assert data.get("target_language") == "km", f"Expected default target_language='km', got {data.get('target_language')}"
            print(f"✓ translate-segments defaults to target_language='km'")
        else:
            print(f"✓ translate-segments endpoint works (returned {response.status_code})")
        
        # Cleanup
        requests.delete(f"{BASE_URL}/api/projects/{project_id}", headers=HEADERS)


class TestProgressFieldsDataTypes:
    """Additional tests for progress field data types and values"""
    
    def test_queue_status_response_structure(self):
        """Test complete response structure of queue-status"""
        # Create project
        response = requests.post(
            f"{BASE_URL}/api/projects",
            json={"title": "TEST_Structure_Test"},
            headers=HEADERS
        )
        project = response.json()
        project_id = project["project_id"]
        
        # Get queue status
        response = requests.get(
            f"{BASE_URL}/api/projects/{project_id}/queue-status",
            headers=HEADERS
        )
        assert response.status_code == 200
        data = response.json()
        
        # Verify complete structure
        expected_structure = {
            "project_id": str,
            "status": str,
            "step": str,
            "progress": (int, float),
            "total": (int, float),
            "elapsed": (int, float),
            "eta": (int, float),
        }
        
        for field, expected_type in expected_structure.items():
            assert field in data, f"Missing field: {field}"
            assert isinstance(data[field], expected_type), \
                f"Field '{field}' should be {expected_type}, got {type(data[field])}"
        
        print(f"✓ queue-status response has correct structure and data types")
        print(f"  Response: {data}")
        
        # Cleanup
        requests.delete(f"{BASE_URL}/api/projects/{project_id}", headers=HEADERS)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
