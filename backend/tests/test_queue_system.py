"""
Test Queue System and Updated Subscription Features for VoxiDub.AI
Tests:
- GET /api/queue/status - returns is_busy, waiting_count, queue_ids
- GET /api/subscription/plans - free plan has videos_per_month=2
- GET /api/subscription/me - creates new user with videos_limit=2
- POST /api/subscription/buy-credits - validates pack IDs
"""
import pytest
import requests
import os

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')

# Test credentials
TEST_EMAIL = "test@voxidub.com"
TEST_PASSWORD = "test123"


class TestQueueStatus:
    """Test GET /api/queue/status endpoint"""
    
    def test_queue_status_returns_200(self):
        """Queue status endpoint should return 200"""
        response = requests.get(f"{BASE_URL}/api/queue/status")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        print("PASS: GET /api/queue/status returns 200")
    
    def test_queue_status_has_is_busy(self):
        """Queue status should have is_busy field"""
        response = requests.get(f"{BASE_URL}/api/queue/status")
        data = response.json()
        assert "is_busy" in data, f"Missing 'is_busy' field in response: {data}"
        assert isinstance(data["is_busy"], bool), f"is_busy should be boolean, got {type(data['is_busy'])}"
        print(f"PASS: is_busy field present and is boolean: {data['is_busy']}")
    
    def test_queue_status_has_waiting_count(self):
        """Queue status should have waiting_count field"""
        response = requests.get(f"{BASE_URL}/api/queue/status")
        data = response.json()
        assert "waiting_count" in data, f"Missing 'waiting_count' field in response: {data}"
        assert isinstance(data["waiting_count"], int), f"waiting_count should be int, got {type(data['waiting_count'])}"
        print(f"PASS: waiting_count field present and is int: {data['waiting_count']}")
    
    def test_queue_status_has_queue_ids(self):
        """Queue status should have queue_ids field"""
        response = requests.get(f"{BASE_URL}/api/queue/status")
        data = response.json()
        assert "queue_ids" in data, f"Missing 'queue_ids' field in response: {data}"
        assert isinstance(data["queue_ids"], list), f"queue_ids should be list, got {type(data['queue_ids'])}"
        print(f"PASS: queue_ids field present and is list: {data['queue_ids']}")


class TestSubscriptionPlans:
    """Test GET /api/subscription/plans - free plan has videos_per_month=2"""
    
    def test_plans_endpoint_returns_200(self):
        """Plans endpoint should return 200"""
        response = requests.get(f"{BASE_URL}/api/subscription/plans")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        print("PASS: GET /api/subscription/plans returns 200")
    
    def test_plans_has_plans_array(self):
        """Response should have plans array"""
        response = requests.get(f"{BASE_URL}/api/subscription/plans")
        data = response.json()
        assert "plans" in data, f"Missing 'plans' field: {data}"
        assert isinstance(data["plans"], list), f"plans should be list"
        print(f"PASS: plans array present with {len(data['plans'])} plans")
    
    def test_free_plan_has_2_videos_per_month(self):
        """Free plan should have videos_per_month=2 (changed from 1)"""
        response = requests.get(f"{BASE_URL}/api/subscription/plans")
        data = response.json()
        plans = data.get("plans", [])
        
        free_plan = None
        for plan in plans:
            if plan.get("id") == "free":
                free_plan = plan
                break
        
        assert free_plan is not None, f"Free plan not found in plans: {[p.get('id') for p in plans]}"
        assert free_plan.get("videos_per_month") == 2, f"Free plan videos_per_month should be 2, got {free_plan.get('videos_per_month')}"
        print(f"PASS: Free plan has videos_per_month=2")
    
    def test_plans_has_credit_packs_array(self):
        """Response should have credit_packs array with 4 packs"""
        response = requests.get(f"{BASE_URL}/api/subscription/plans")
        data = response.json()
        assert "credit_packs" in data, f"Missing 'credit_packs' field: {data}"
        assert isinstance(data["credit_packs"], list), f"credit_packs should be list"
        assert len(data["credit_packs"]) == 4, f"Expected 4 credit packs, got {len(data['credit_packs'])}"
        print(f"PASS: credit_packs array present with {len(data['credit_packs'])} packs")


class TestSubscriptionMe:
    """Test GET /api/subscription/me - creates new user with videos_limit=2"""
    
    @pytest.fixture
    def auth_token(self):
        """Get auth token by logging in"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD
        })
        if response.status_code != 200:
            pytest.skip(f"Login failed: {response.status_code} - {response.text}")
        data = response.json()
        return data.get("session_token")
    
    def test_subscription_me_requires_auth(self):
        """Subscription me endpoint should require auth"""
        response = requests.get(f"{BASE_URL}/api/subscription/me")
        assert response.status_code == 401, f"Expected 401 without auth, got {response.status_code}"
        print("PASS: GET /api/subscription/me returns 401 without auth")
    
    def test_subscription_me_returns_subscription(self, auth_token):
        """Subscription me should return subscription object"""
        response = requests.get(
            f"{BASE_URL}/api/subscription/me",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        data = response.json()
        assert "subscription" in data, f"Missing 'subscription' field: {data}"
        print(f"PASS: GET /api/subscription/me returns subscription object")
    
    def test_subscription_me_has_videos_limit(self, auth_token):
        """Subscription should have videos_limit field"""
        response = requests.get(
            f"{BASE_URL}/api/subscription/me",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        data = response.json()
        sub = data.get("subscription", {})
        assert "videos_limit" in sub, f"Missing 'videos_limit' in subscription: {sub}"
        print(f"PASS: subscription has videos_limit={sub.get('videos_limit')}")
    
    def test_subscription_me_has_videos_remaining(self, auth_token):
        """Response should have videos_remaining field"""
        response = requests.get(
            f"{BASE_URL}/api/subscription/me",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        data = response.json()
        assert "videos_remaining" in data, f"Missing 'videos_remaining' field: {data}"
        print(f"PASS: response has videos_remaining={data.get('videos_remaining')}")


class TestBuyCredits:
    """Test POST /api/subscription/buy-credits - validates pack IDs"""
    
    @pytest.fixture
    def auth_token(self):
        """Get auth token by logging in"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD
        })
        if response.status_code != 200:
            pytest.skip(f"Login failed: {response.status_code} - {response.text}")
        data = response.json()
        return data.get("session_token")
    
    def test_buy_credits_requires_auth(self):
        """Buy credits endpoint should require auth"""
        response = requests.post(f"{BASE_URL}/api/subscription/buy-credits", json={"pack": "pack_5"})
        assert response.status_code == 401, f"Expected 401 without auth, got {response.status_code}"
        print("PASS: POST /api/subscription/buy-credits returns 401 without auth")
    
    def test_buy_credits_rejects_invalid_pack(self, auth_token):
        """Buy credits should reject invalid pack ID"""
        response = requests.post(
            f"{BASE_URL}/api/subscription/buy-credits",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={"pack": "invalid_pack_xyz"}
        )
        assert response.status_code == 400, f"Expected 400 for invalid pack, got {response.status_code}: {response.text}"
        print("PASS: POST /api/subscription/buy-credits returns 400 for invalid pack ID")
    
    def test_buy_credits_accepts_valid_pack_5(self, auth_token):
        """Buy credits should accept pack_5"""
        response = requests.post(
            f"{BASE_URL}/api/subscription/buy-credits",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={"pack": "pack_5"}
        )
        # Should return 200 (payment is mocked, so it succeeds)
        assert response.status_code == 200, f"Expected 200 for pack_5, got {response.status_code}: {response.text}"
        data = response.json()
        assert data.get("ok") == True, f"Expected ok=True, got {data}"
        print(f"PASS: POST /api/subscription/buy-credits accepts pack_5, credits_added={data.get('credits_added')}")
    
    def test_buy_credits_accepts_valid_pack_20(self, auth_token):
        """Buy credits should accept pack_20"""
        response = requests.post(
            f"{BASE_URL}/api/subscription/buy-credits",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={"pack": "pack_20"}
        )
        assert response.status_code == 200, f"Expected 200 for pack_20, got {response.status_code}: {response.text}"
        print("PASS: POST /api/subscription/buy-credits accepts pack_20")
    
    def test_buy_credits_accepts_valid_pack_50(self, auth_token):
        """Buy credits should accept pack_50"""
        response = requests.post(
            f"{BASE_URL}/api/subscription/buy-credits",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={"pack": "pack_50"}
        )
        assert response.status_code == 200, f"Expected 200 for pack_50, got {response.status_code}: {response.text}"
        print("PASS: POST /api/subscription/buy-credits accepts pack_50")
    
    def test_buy_credits_accepts_valid_pack_100(self, auth_token):
        """Buy credits should accept pack_100"""
        response = requests.post(
            f"{BASE_URL}/api/subscription/buy-credits",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={"pack": "pack_100"}
        )
        assert response.status_code == 200, f"Expected 200 for pack_100, got {response.status_code}: {response.text}"
        print("PASS: POST /api/subscription/buy-credits accepts pack_100")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
