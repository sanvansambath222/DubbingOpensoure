#!/usr/bin/env python3
"""
Test file upload functionality for Khmer Dubbing App
"""

import requests
import sys
import json
import tempfile
import os

class FileUploadTester:
    def __init__(self, base_url="https://khmer-dubbing-hub.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.session_token = "test_session_001"
        self.project_id = None

    def create_test_project(self):
        """Create a test project for file upload"""
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.session_token}'
        }
        
        response = requests.post(
            f"{self.api_url}/projects",
            json={"title": "File Upload Test Project"},
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            self.project_id = data['project_id']
            print(f"✅ Created test project: {self.project_id}")
            return True
        else:
            print(f"❌ Failed to create project: {response.status_code}")
            return False

    def test_file_upload(self):
        """Test file upload with a small test file"""
        if not self.project_id:
            print("❌ No project ID available")
            return False

        # Create a small test audio file (MP3 header)
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_file:
            # Write minimal MP3 header
            mp3_header = b'\xff\xfb\x90\x00' + b'\x00' * 100  # Minimal MP3 data
            temp_file.write(mp3_header)
            temp_file_path = temp_file.name

        try:
            headers = {'Authorization': f'Bearer {self.session_token}'}
            
            with open(temp_file_path, 'rb') as f:
                files = {'file': ('test_audio.mp3', f, 'audio/mpeg')}
                
                print(f"🔍 Testing file upload to project {self.project_id}...")
                response = requests.post(
                    f"{self.api_url}/projects/{self.project_id}/upload",
                    files=files,
                    headers=headers,
                    timeout=30
                )
                
                print(f"   Status: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    print("✅ File upload successful!")
                    print(f"   File path: {data.get('original_file_path')}")
                    print(f"   File type: {data.get('file_type')}")
                    return True
                else:
                    print(f"❌ File upload failed: {response.status_code}")
                    try:
                        error_data = response.json()
                        print(f"   Error: {error_data}")
                    except:
                        print(f"   Error: {response.text}")
                    return False
                    
        finally:
            # Clean up temp file
            os.unlink(temp_file_path)

def main():
    print("🚀 Testing File Upload Functionality")
    print("=" * 40)
    
    tester = FileUploadTester()
    
    # Create project and test upload
    if tester.create_test_project():
        success = tester.test_file_upload()
        return 0 if success else 1
    else:
        return 1

if __name__ == "__main__":
    sys.exit(main())