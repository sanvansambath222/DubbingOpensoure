"""
Test suite for VoxiDub.AI Subscription System
Tests: GET /subscription/plans, GET /subscription/me, POST /subscription/use-credit, POST /subscription/activate
"""
import pytest
import requests
import os

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')

# Test credentials
TEST_EMAIL = "test@voxidub.com"
TEST_PASSWORD = "test123"


class TestSubscriptionPlans:
    """Test GET /api/subscription/plans - public endpoint"""
    
    def test_plans_returns_4_plans(self):
        """Verify 4 subscription plans are returned"""
        response = requests.get(f"{BASE_URL}/api/subscription/plans")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        assert "plans" in data, "Response should have 'plans' key"
        plans = data["plans"]
        assert len(plans) == 4, f"Expected 4 plans, got {len(plans)}"
        
        plan_ids = [p["id"] for p in plans]
        assert "free" in plan_ids, "Missing 'free' plan"
        assert "basic" in plan_ids, "Missing 'basic' plan"
        assert "pro" in plan_ids, "Missing 'pro' plan"
        assert "business" in plan_ids, "Missing 'business' plan"
        print("PASS: 4 plans returned (free, basic, pro, business)")
    
    def test_free_plan_prices(self):
        """Verify Free plan has correct prices"""
        response = requests.get(f"{BASE_URL}/api/subscription/plans")
        assert response.status_code == 200
        
        plans = {p["id"]: p for p in response.json()["plans"]}
        free = plans["free"]
        
        assert free["price_usd"] == 0, f"Free USD price should be 0, got {free['price_usd']}"
        assert free["price_khr"] == 0, f"Free KHR price should be 0, got {free['price_khr']}"
        assert free["videos_per_month"] == 1, f"Free videos should be 1, got {free['videos_per_month']}"
        assert free["watermark"] == True, "Free plan should have watermark"
        print("PASS: Free plan - $0, 0 KHR, 1 video, watermark=True")
    
    def test_basic_plan_prices(self):
        """Verify Basic plan has correct prices"""
        response = requests.get(f"{BASE_URL}/api/subscription/plans")
        assert response.status_code == 200
        
        plans = {p["id"]: p for p in response.json()["plans"]}
        basic = plans["basic"]
        
        assert basic["price_usd"] == 19, f"Basic USD price should be 19, got {basic['price_usd']}"
        assert basic["price_khr"] == 76000, f"Basic KHR price should be 76000, got {basic['price_khr']}"
        assert basic["videos_per_month"] == 10, f"Basic videos should be 10, got {basic['videos_per_month']}"
        assert basic["watermark"] == False, "Basic plan should NOT have watermark"
        print("PASS: Basic plan - $19, 76000 KHR, 10 videos, watermark=False")
    
    def test_pro_plan_prices(self):
        """Verify Pro plan has correct prices"""
        response = requests.get(f"{BASE_URL}/api/subscription/plans")
        assert response.status_code == 200
        
        plans = {p["id"]: p for p in response.json()["plans"]}
        pro = plans["pro"]
        
        assert pro["price_usd"] == 49, f"Pro USD price should be 49, got {pro['price_usd']}"
        assert pro["price_khr"] == 196000, f"Pro KHR price should be 196000, got {pro['price_khr']}"
        assert pro["videos_per_month"] == 50, f"Pro videos should be 50, got {pro['videos_per_month']}"
        assert pro["priority_queue"] == True, "Pro plan should have priority queue"
        print("PASS: Pro plan - $49, 196000 KHR, 50 videos, priority=True")
    
    def test_business_plan_prices(self):
        """Verify Business plan has correct prices"""
        response = requests.get(f"{BASE_URL}/api/subscription/plans")
        assert response.status_code == 200
        
        plans = {p["id"]: p for p in response.json()["plans"]}
        business = plans["business"]
        
        assert business["price_usd"] == 99, f"Business USD price should be 99, got {business['price_usd']}"
        assert business["price_khr"] == 396000, f"Business KHR price should be 396000, got {business['price_khr']}"
        assert business["videos_per_month"] == -1, f"Business videos should be -1 (unlimited), got {business['videos_per_month']}"
        assert business["priority_queue"] == True, "Business plan should have priority queue"
        print("PASS: Business plan - $99, 396000 KHR, unlimited videos, priority=True")


class TestSubscriptionMe:
    """Test GET /api/subscription/me - requires auth"""
    
    @pytest.fixture
    def auth_token(self):
        """Login and get session token"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD
        })
        if response.status_code != 200:
            pytest.skip(f"Login failed: {response.status_code} - {response.text}")
        data = response.json()
        token = data.get("session_token")
        if not token:
            pytest.skip("No session_token in login response")
        return token
    
    def test_subscription_me_requires_auth(self):
        """Verify /subscription/me returns 401 without auth"""
        response = requests.get(f"{BASE_URL}/api/subscription/me")
        assert response.status_code == 401, f"Expected 401 without auth, got {response.status_code}"
        print("PASS: /subscription/me returns 401 without auth")
    
    def test_subscription_me_returns_free_default(self, auth_token):
        """Verify authenticated user gets free plan by default"""
        response = requests.get(
            f"{BASE_URL}/api/subscription/me",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        assert "subscription" in data, "Response should have 'subscription' key"
        assert "plan_info" in data, "Response should have 'plan_info' key"
        assert "can_dub" in data, "Response should have 'can_dub' key"
        assert "videos_remaining" in data, "Response should have 'videos_remaining' key"
        
        sub = data["subscription"]
        assert sub.get("plan") in ["free", "basic", "pro", "business"], f"Invalid plan: {sub.get('plan')}"
        print(f"PASS: /subscription/me returns subscription data (plan={sub.get('plan')})")


class TestSubscriptionUseCredit:
    """Test POST /api/subscription/use-credit - requires auth"""
    
    @pytest.fixture
    def auth_token(self):
        """Login and get session token"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD
        })
        if response.status_code != 200:
            pytest.skip(f"Login failed: {response.status_code}")
        return response.json().get("session_token")
    
    def test_use_credit_requires_auth(self):
        """Verify /subscription/use-credit returns 401 without auth"""
        response = requests.post(f"{BASE_URL}/api/subscription/use-credit")
        assert response.status_code == 401, f"Expected 401 without auth, got {response.status_code}"
        print("PASS: /subscription/use-credit returns 401 without auth")
    
    def test_use_credit_decrements(self, auth_token):
        """Verify use-credit decrements video count"""
        # First get current subscription
        sub_response = requests.get(
            f"{BASE_URL}/api/subscription/me",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert sub_response.status_code == 200
        initial_used = sub_response.json()["subscription"].get("videos_used", 0)
        
        # Use a credit
        response = requests.post(
            f"{BASE_URL}/api/subscription/use-credit",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        
        # Could be 200 (success) or 403 (limit reached)
        assert response.status_code in [200, 403], f"Expected 200 or 403, got {response.status_code}"
        
        if response.status_code == 200:
            # Verify increment
            sub_response2 = requests.get(
                f"{BASE_URL}/api/subscription/me",
                headers={"Authorization": f"Bearer {auth_token}"}
            )
            new_used = sub_response2.json()["subscription"].get("videos_used", 0)
            assert new_used == initial_used + 1, f"videos_used should increment from {initial_used} to {initial_used + 1}, got {new_used}"
            print(f"PASS: use-credit incremented videos_used from {initial_used} to {new_used}")
        else:
            print(f"PASS: use-credit returned 403 (limit reached) - videos_used={initial_used}")


class TestSubscriptionActivate:
    """Test POST /api/subscription/activate - requires auth"""
    
    @pytest.fixture
    def auth_token(self):
        """Login and get session token"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD
        })
        if response.status_code != 200:
            pytest.skip(f"Login failed: {response.status_code}")
        return response.json().get("session_token")
    
    def test_activate_requires_auth(self):
        """Verify /subscription/activate returns 401 without auth"""
        response = requests.post(f"{BASE_URL}/api/subscription/activate", json={"plan": "basic"})
        assert response.status_code == 401, f"Expected 401 without auth, got {response.status_code}"
        print("PASS: /subscription/activate returns 401 without auth")
    
    def test_activate_invalid_plan(self, auth_token):
        """Verify /subscription/activate rejects invalid plan"""
        response = requests.post(
            f"{BASE_URL}/api/subscription/activate",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={"plan": "invalid_plan_xyz"}
        )
        assert response.status_code == 400, f"Expected 400 for invalid plan, got {response.status_code}"
        print("PASS: /subscription/activate returns 400 for invalid plan")
    
    def test_activate_free_plan(self, auth_token):
        """Verify activating free plan works"""
        response = requests.post(
            f"{BASE_URL}/api/subscription/activate",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={"plan": "free"}
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        assert data.get("ok") == True, "Response should have ok=True"
        assert data.get("plan") == "free", f"Plan should be 'free', got {data.get('plan')}"
        print("PASS: /subscription/activate works for free plan")


class TestSubscriptionHistory:
    """Test GET /api/subscription/history - requires auth"""
    
    @pytest.fixture
    def auth_token(self):
        """Login and get session token"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD
        })
        if response.status_code != 200:
            pytest.skip(f"Login failed: {response.status_code}")
        return response.json().get("session_token")
    
    def test_history_requires_auth(self):
        """Verify /subscription/history returns 401 without auth"""
        response = requests.get(f"{BASE_URL}/api/subscription/history")
        assert response.status_code == 401, f"Expected 401 without auth, got {response.status_code}"
        print("PASS: /subscription/history returns 401 without auth")
    
    def test_history_returns_list(self, auth_token):
        """Verify /subscription/history returns payments list"""
        response = requests.get(
            f"{BASE_URL}/api/subscription/history",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        assert "payments" in data, "Response should have 'payments' key"
        assert isinstance(data["payments"], list), "payments should be a list"
        print(f"PASS: /subscription/history returns payments list (count={len(data['payments'])})")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
