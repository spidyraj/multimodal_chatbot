#!/usr/bin/env python3
"""
Chat functionality test script
"""
import subprocess
import json
from pathlib import Path

def test_api_endpoints():
    print("Testing API Endpoints...")
    
    # Test backend health
    try:
        result = subprocess.run(['curl', '-s', '-w', '%{http_code}', 
                               'https://multimodal-backend-production.up.railway.app/health'], 
                              capture_output=True, text=True, timeout=10)
        print(f"Backend Health: {result.stdout.strip()}")
    except:
        print("Backend Health: FAILED")
    
    # Test frontend
    try:
        result = subprocess.run(['curl', '-s', '-w', '%{http_code}', 
                               'https://multimodal-frontend-production.up.railway.app'], 
                              capture_output=True, text=True, timeout=10)
        print(f"Frontend: {result.stdout.strip()}")
    except:
        print("Frontend: FAILED")

def check_backend_files():
    print("\nChecking Backend Chat Files...")
    
    backend_dir = Path("backend")
    
    # Check chat route
    chat_route = backend_dir / "api/routes/chat.py"
    if chat_route.exists():
        print("OK: chat.py exists")
        
        # Check content
        with open(chat_route, 'r') as f:
            content = f.read()
            
        if '@router.post("/")' in content:
            print("OK: Chat endpoint found")
        else:
            print("ERROR: Chat endpoint missing")
            
        if 'retrieve_context' in content:
            print("OK: RAG context retrieval found")
        else:
            print("WARNING: RAG context missing")
    else:
        print("ERROR: chat.py missing")

def check_frontend_files():
    print("\nChecking Frontend Chat Files...")
    
    frontend_dir = Path("frontend")
    
    # Check chat component
    chat_component = frontend_dir / "src/pages/Chat.jsx"
    if chat_component.exists():
        print("OK: Chat.jsx exists")
        
        with open(chat_component, 'r') as f:
            content = f.read()
            
        if 'loadChatHistory' in content:
            print("OK: Chat history loading found")
        else:
            print("ERROR: Chat history loading missing")
            
        if 'chatAPI.getHistory()' in content:
            print("OK: API call found")
        else:
            print("ERROR: API call missing")
    else:
        print("ERROR: Chat.jsx missing")

def check_api_service():
    print("\nChecking API Service...")
    
    api_service = Path("frontend/src/services/api.js")
    if api_service.exists():
        print("OK: api.js exists")
        
        with open(api_service, 'r') as f:
            content = f.read()
            
        if 'chatAPI' in content:
            print("OK: Chat API found")
        else:
            print("ERROR: Chat API missing")
            
        if 'getHistory' in content:
            print("OK: getHistory method found")
        else:
            print("ERROR: getHistory method missing")
            
        if 'VITE_API_URL' in content:
            print("OK: API URL configuration found")
        else:
            print("ERROR: API URL configuration missing")
    else:
        print("ERROR: api.js missing")

def main():
    print("Chat Functionality Diagnostic")
    print("=" * 40)
    
    test_api_endpoints()
    check_backend_files()
    check_frontend_files()
    check_api_service()
    
    print("\n" + "=" * 40)
    print("Diagnostic Complete!")
    print("\nCommon Issues:")
    print("1. Backend not running or deployed")
    print("2. Frontend API URL misconfigured")
    print("3. Authentication issues")
    print("4. CORS problems")
    print("5. Database connection issues")

if __name__ == "__main__":
    main()
