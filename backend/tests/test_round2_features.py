"""
Round 2 Features Test Suite for Khmer Dubbing App
Tests: Duplicate project, Merge segments, Split segment, Rename project (PATCH title)
"""
import pytest
import requests
import os
from datetime import datetime, timezone, timedelta

# Get backend URL from environment
BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')
if not BASE_URL:
    # Fallback for local testing
    BASE_URL = "https://khmer-dubbing-hub.preview.emergentagent.com"

API_URL = f"{BASE_URL}/api"
TEST_SESSION_TOKEN = "test_session_001"
TEST_USER_ID = "test-user-001"


@pytest.fixture(scope="module")
def auth_headers():
    """Auth headers for API requests"""
    return {"Authorization": f"Bearer {TEST_SESSION_TOKEN}"}


@pytest.fixture(scope="module")
def api_client():
    """Shared requests session"""
    session = requests.Session()
    session.headers.update({
        "Content-Type": "application/json",
        "Authorization": f"Bearer {TEST_SESSION_TOKEN}"
    })
    return session


@pytest.fixture(scope="module")
def test_project_with_segments(api_client):
    """Create a test project with segments for merge/split testing"""
    # Create project
    response = api_client.post(f"{API_URL}/projects", json={"title": "TEST_Round2_MergeSplit"})
    assert response.status_code == 200, f"Failed to create project: {response.text}"
    project = response.json()
    project_id = project["project_id"]
    
    # Add segments directly via PATCH
    segments = [
        {"id": 0, "start": 0.0, "end": 2.5, "original": "你好世界", "translated": "សួស្តីពិភពលោក", "speaker": "SPEAKER_00", "gender": "female", "voice": "sophea"},
        {"id": 1, "start": 2.5, "end": 5.0, "original": "我是测试", "translated": "ខ្ញុំជាការសាកល្បង", "speaker": "SPEAKER_00", "gender": "female", "voice": "sophea"},
        {"id": 2, "start": 5.0, "end": 8.0, "original": "这是第三段", "translated": "នេះជាផ្នែកទីបី", "speaker": "SPEAKER_01", "gender": "male", "voice": "dara"},
        {"id": 3, "start": 8.0, "end": 11.0, "original": "最后一段", "translated": "ផ្នែកចុងក្រោយ", "speaker": "SPEAKER_01", "gender": "male", "voice": "dara"},
    ]
    
    response = api_client.patch(f"{API_URL}/projects/{project_id}", json={"segments": segments})
    assert response.status_code == 200, f"Failed to add segments: {response.text}"
    
    yield project_id
    
    # Cleanup
    api_client.delete(f"{API_URL}/projects/{project_id}")


class TestDuplicateProject:
    """Tests for POST /api/projects/{id}/duplicate endpoint"""
    
    def test_duplicate_project_creates_copy(self, api_client):
        """POST /api/projects/{id}/duplicate creates a copy with '(Copy)' in title"""
        # Create original project
        response = api_client.post(f"{API_URL}/projects", json={"title": "TEST_Original_Project"})
        assert response.status_code == 200
        original = response.json()
        original_id = original["project_id"]
        
        # Duplicate it
        response = api_client.post(f"{API_URL}/projects/{original_id}/duplicate")
        assert response.status_code == 200, f"Duplicate failed: {response.text}"
        
        duplicate = response.json()
        
        # Verify title has (Copy)
        assert "(Copy)" in duplicate["title"], f"Expected '(Copy)' in title, got: {duplicate['title']}"
        assert duplicate["title"] == "TEST_Original_Project (Copy)"
        
        # Verify it's a different project
        assert duplicate["project_id"] != original_id
        
        # Cleanup
        api_client.delete(f"{API_URL}/projects/{original_id}")
        api_client.delete(f"{API_URL}/projects/{duplicate['project_id']}")
        
        print("✓ Duplicate project creates copy with '(Copy)' in title")
    
    def test_duplicate_resets_share_token_and_dubbed_paths(self, api_client):
        """POST /api/projects/{id}/duplicate resets share_token, dubbed paths"""
        # Create project with share token
        response = api_client.post(f"{API_URL}/projects", json={"title": "TEST_Duplicate_Reset"})
        assert response.status_code == 200
        original = response.json()
        original_id = original["project_id"]
        
        # Create share token
        response = api_client.post(f"{API_URL}/projects/{original_id}/share")
        assert response.status_code == 200
        share_token = response.json()["share_token"]
        
        # Verify original has share token
        response = api_client.get(f"{API_URL}/projects/{original_id}")
        assert response.status_code == 200
        original_updated = response.json()
        assert original_updated["share_token"] == share_token
        
        # Duplicate
        response = api_client.post(f"{API_URL}/projects/{original_id}/duplicate")
        assert response.status_code == 200
        duplicate = response.json()
        
        # Verify duplicate has reset values
        assert duplicate["share_token"] is None, "share_token should be reset to None"
        assert duplicate["dubbed_audio_path"] is None, "dubbed_audio_path should be reset"
        assert duplicate["dubbed_video_path"] is None, "dubbed_video_path should be reset"
        
        # Cleanup
        api_client.delete(f"{API_URL}/projects/{original_id}")
        api_client.delete(f"{API_URL}/projects/{duplicate['project_id']}")
        
        print("✓ Duplicate resets share_token, dubbed_audio_path, dubbed_video_path")
    
    def test_duplicate_updates_status_correctly(self, api_client, test_project_with_segments):
        """POST /api/projects/{id}/duplicate updates status based on segments"""
        project_id = test_project_with_segments
        
        # Duplicate project with segments
        response = api_client.post(f"{API_URL}/projects/{project_id}/duplicate")
        assert response.status_code == 200
        duplicate = response.json()
        
        # Status should be 'translated' since segments have translations
        assert duplicate["status"] in ["translated", "transcribed"], f"Expected translated/transcribed status, got: {duplicate['status']}"
        
        # Cleanup
        api_client.delete(f"{API_URL}/projects/{duplicate['project_id']}")
        
        print("✓ Duplicate updates status correctly based on segments")
    
    def test_duplicate_nonexistent_project_returns_404(self, api_client):
        """POST /api/projects/{id}/duplicate returns 404 for non-existent project"""
        response = api_client.post(f"{API_URL}/projects/nonexistent_project_id/duplicate")
        assert response.status_code == 404
        print("✓ Duplicate non-existent project returns 404")


class TestMergeSegments:
    """Tests for POST /api/projects/{id}/merge-segments endpoint"""
    
    def test_merge_two_segments(self, api_client):
        """POST /api/projects/{id}/merge-segments merges 2 segments correctly"""
        # Create project with segments
        response = api_client.post(f"{API_URL}/projects", json={"title": "TEST_Merge_Two"})
        assert response.status_code == 200
        project_id = response.json()["project_id"]
        
        segments = [
            {"id": 0, "start": 0.0, "end": 2.0, "original": "Hello", "translated": "សួស្តី", "speaker": "SPEAKER_00", "gender": "female"},
            {"id": 1, "start": 2.0, "end": 4.0, "original": "World", "translated": "ពិភពលោក", "speaker": "SPEAKER_00", "gender": "female"},
            {"id": 2, "start": 4.0, "end": 6.0, "original": "Test", "translated": "សាកល្បង", "speaker": "SPEAKER_01", "gender": "male"},
        ]
        api_client.patch(f"{API_URL}/projects/{project_id}", json={"segments": segments})
        
        # Merge segments 0 and 1
        response = api_client.post(f"{API_URL}/projects/{project_id}/merge-segments", json={"segment_ids": [0, 1]})
        assert response.status_code == 200, f"Merge failed: {response.text}"
        
        result = response.json()
        merged_segments = result["segments"]
        
        # Should now have 2 segments (merged + remaining)
        assert len(merged_segments) == 2, f"Expected 2 segments after merge, got {len(merged_segments)}"
        
        # First segment should be merged
        merged = merged_segments[0]
        assert merged["start"] == 0.0, "Merged segment should have first segment's start time"
        assert merged["end"] == 4.0, "Merged segment should have last segment's end time"
        assert "Hello" in merged["original"] and "World" in merged["original"], "Merged original text should contain both"
        assert "សួស្តី" in merged["translated"] and "ពិភពលោក" in merged["translated"], "Merged translated text should contain both"
        
        # Cleanup
        api_client.delete(f"{API_URL}/projects/{project_id}")
        
        print("✓ Merge 2 segments concatenates text and uses first start/last end")
    
    def test_merge_three_segments(self, api_client):
        """POST /api/projects/{id}/merge-segments merges 3+ segments"""
        response = api_client.post(f"{API_URL}/projects", json={"title": "TEST_Merge_Three"})
        assert response.status_code == 200
        project_id = response.json()["project_id"]
        
        segments = [
            {"id": 0, "start": 0.0, "end": 2.0, "original": "One", "translated": "មួយ", "speaker": "SPEAKER_00"},
            {"id": 1, "start": 2.0, "end": 4.0, "original": "Two", "translated": "ពីរ", "speaker": "SPEAKER_00"},
            {"id": 2, "start": 4.0, "end": 6.0, "original": "Three", "translated": "បី", "speaker": "SPEAKER_00"},
            {"id": 3, "start": 6.0, "end": 8.0, "original": "Four", "translated": "បួន", "speaker": "SPEAKER_01"},
        ]
        api_client.patch(f"{API_URL}/projects/{project_id}", json={"segments": segments})
        
        # Merge segments 0, 1, 2
        response = api_client.post(f"{API_URL}/projects/{project_id}/merge-segments", json={"segment_ids": [0, 1, 2]})
        assert response.status_code == 200
        
        result = response.json()
        merged_segments = result["segments"]
        
        # Should now have 2 segments
        assert len(merged_segments) == 2
        
        # First segment should be merged
        merged = merged_segments[0]
        assert merged["start"] == 0.0
        assert merged["end"] == 6.0
        
        # Cleanup
        api_client.delete(f"{API_URL}/projects/{project_id}")
        
        print("✓ Merge 3+ segments works correctly")
    
    def test_merge_invalid_segment_ids_returns_400(self, api_client, test_project_with_segments):
        """POST /api/projects/{id}/merge-segments returns 400 for invalid segment IDs"""
        project_id = test_project_with_segments
        
        # Try to merge with invalid segment ID (out of range)
        response = api_client.post(f"{API_URL}/projects/{project_id}/merge-segments", json={"segment_ids": [0, 100]})
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
        
        print("✓ Merge with invalid segment IDs returns 400")
    
    def test_merge_less_than_two_segments_returns_400(self, api_client, test_project_with_segments):
        """POST /api/projects/{id}/merge-segments returns 400 for less than 2 segments"""
        project_id = test_project_with_segments
        
        # Try to merge with only 1 segment
        response = api_client.post(f"{API_URL}/projects/{project_id}/merge-segments", json={"segment_ids": [0]})
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
        
        # Try to merge with empty list
        response = api_client.post(f"{API_URL}/projects/{project_id}/merge-segments", json={"segment_ids": []})
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
        
        print("✓ Merge with less than 2 segments returns 400")


class TestSplitSegment:
    """Tests for POST /api/projects/{id}/split-segment endpoint"""
    
    def test_split_segment_at_midpoint(self, api_client):
        """POST /api/projects/{id}/split-segment splits a segment into 2 at midpoint"""
        response = api_client.post(f"{API_URL}/projects", json={"title": "TEST_Split_Segment"})
        assert response.status_code == 200
        project_id = response.json()["project_id"]
        
        segments = [
            {"id": 0, "start": 0.0, "end": 4.0, "original": "Hello World", "translated": "សួស្តី ពិភពលោក", "speaker": "SPEAKER_00"},
            {"id": 1, "start": 4.0, "end": 6.0, "original": "Test", "translated": "សាកល្បង", "speaker": "SPEAKER_01"},
        ]
        api_client.patch(f"{API_URL}/projects/{project_id}", json={"segments": segments})
        
        # Split segment 0
        response = api_client.post(f"{API_URL}/projects/{project_id}/split-segment", json={"segment_id": 0})
        assert response.status_code == 200, f"Split failed: {response.text}"
        
        result = response.json()
        split_segments = result["segments"]
        
        # Should now have 3 segments
        assert len(split_segments) == 3, f"Expected 3 segments after split, got {len(split_segments)}"
        
        # First two segments should be the split result
        seg1 = split_segments[0]
        seg2 = split_segments[1]
        
        # Check time split at midpoint (0 + 4) / 2 = 2.0
        assert seg1["start"] == 0.0
        assert seg1["end"] == 2.0
        assert seg2["start"] == 2.0
        assert seg2["end"] == 4.0
        
        # Check text is split
        assert seg1["original"] != seg2["original"], "Split segments should have different text"
        
        # Cleanup
        api_client.delete(f"{API_URL}/projects/{project_id}")
        
        print("✓ Split segment creates 2 segments at midpoint")
    
    def test_split_invalid_segment_id_returns_400(self, api_client, test_project_with_segments):
        """POST /api/projects/{id}/split-segment returns 400 for invalid segment ID"""
        project_id = test_project_with_segments
        
        # Try to split with invalid segment ID
        response = api_client.post(f"{API_URL}/projects/{project_id}/split-segment", json={"segment_id": 100})
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
        
        # Try with negative ID
        response = api_client.post(f"{API_URL}/projects/{project_id}/split-segment", json={"segment_id": -1})
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
        
        print("✓ Split with invalid segment ID returns 400")


class TestRenameProject:
    """Tests for PATCH /api/projects/{id} title update (rename)"""
    
    def test_patch_project_title(self, api_client):
        """PATCH /api/projects/{id} can update title"""
        response = api_client.post(f"{API_URL}/projects", json={"title": "TEST_Original_Title"})
        assert response.status_code == 200
        project_id = response.json()["project_id"]
        
        # Rename via PATCH
        response = api_client.patch(f"{API_URL}/projects/{project_id}", json={"title": "TEST_New_Title"})
        assert response.status_code == 200, f"Rename failed: {response.text}"
        
        updated = response.json()
        assert updated["title"] == "TEST_New_Title", f"Expected 'TEST_New_Title', got: {updated['title']}"
        
        # Verify persistence
        response = api_client.get(f"{API_URL}/projects/{project_id}")
        assert response.status_code == 200
        assert response.json()["title"] == "TEST_New_Title"
        
        # Cleanup
        api_client.delete(f"{API_URL}/projects/{project_id}")
        
        print("✓ PATCH /api/projects/{id} can update title")
    
    def test_patch_updates_updated_at(self, api_client):
        """PATCH /api/projects/{id} updates the updated_at timestamp"""
        response = api_client.post(f"{API_URL}/projects", json={"title": "TEST_Timestamp_Check"})
        assert response.status_code == 200
        project = response.json()
        project_id = project["project_id"]
        original_updated_at = project["updated_at"]
        
        # Wait a moment and update
        import time
        time.sleep(0.1)
        
        response = api_client.patch(f"{API_URL}/projects/{project_id}", json={"title": "TEST_Updated_Title"})
        assert response.status_code == 200
        
        updated = response.json()
        assert updated["updated_at"] != original_updated_at, "updated_at should change after PATCH"
        
        # Cleanup
        api_client.delete(f"{API_URL}/projects/{project_id}")
        
        print("✓ PATCH updates updated_at timestamp")


class TestAuthRequired:
    """Tests that all new endpoints require authentication"""
    
    def test_duplicate_requires_auth(self):
        """POST /api/projects/{id}/duplicate requires authentication"""
        response = requests.post(f"{API_URL}/projects/test/duplicate")
        assert response.status_code == 401
        print("✓ Duplicate endpoint requires auth")
    
    def test_merge_requires_auth(self):
        """POST /api/projects/{id}/merge-segments requires authentication"""
        response = requests.post(f"{API_URL}/projects/test/merge-segments", json={"segment_ids": [0, 1]})
        assert response.status_code == 401
        print("✓ Merge segments endpoint requires auth")
    
    def test_split_requires_auth(self):
        """POST /api/projects/{id}/split-segment requires authentication"""
        response = requests.post(f"{API_URL}/projects/test/split-segment", json={"segment_id": 0})
        assert response.status_code == 401
        print("✓ Split segment endpoint requires auth")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
