"""
Simple test to check if authentication endpoints work
"""
import requests
import json

BASE_URL = "https://multimodal-backend-production.up.railway.app"

def test_auth():
    """Test authentication endpoints"""
    print("🔐 Testing Authentication Endpoints")
    print("=" * 40)
    
    # Test health first
    try:
        print("🏥 Testing health endpoint...")
        health_response = requests.get(f"{BASE_URL}/health", timeout=10)
        print(f"Health Status: {health_response.status_code}")
        if health_response.status_code == 200:
            print(f"Health Response: {health_response.json()}")
        else:
            print(f"Health Error: {health_response.text}")
            return
    except Exception as e:
        print(f"Health Exception: {e}")
        return
    
    # Test login with existing user
    try:
        print("\n🔑 Testing login...")
        login_data = {
            "email": "test2102226581@example.com",
            "password": "testpassword123"
        }
        
        login_response = requests.post(
            f"{BASE_URL}/auth/login",
            json=login_data,
            timeout=10
        )
        
        print(f"Login Status: {login_response.status_code}")
        print(f"Login Response: {login_response.text}")
        
        if login_response.status_code == 200:
            token = login_response.json().get("access_token")
            print(f"Token: {token[:20]}..." if token else "No token")
            
            # Test chat with token
            print("\n💬 Testing chat...")
            chat_data = {"message": "Hello, test message"}
            chat_response = requests.post(
                f"{BASE_URL}/chat",
                json=chat_data,
                headers={"Authorization": f"Bearer {token}"},
                timeout=10
            )
            
            print(f"Chat Status: {chat_response.status_code}")
            print(f"Chat Response: {chat_response.text[:200]}...")
            
    except Exception as e:
        print(f"Chat Exception: {e}")

if __name__ == "__main__":
    test_auth()
