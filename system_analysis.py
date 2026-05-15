#!/usr/bin/env python3
"""
Comprehensive System Analysis for Multimodal AI
"""
import os
import json
from pathlib import Path

def analyze_backend():
    print("=" * 60)
    print("BACKEND ANALYSIS")
    print("=" * 60)
    
    backend_dir = Path("backend")
    
    # 1. Core Files Analysis
    print("\n1. CORE FILES:")
    core_files = {
        "main.py": "FastAPI application entry point",
        "requirements.txt": "Python dependencies",
        ".env.example": "Environment variables template",
        "Dockerfile": "Container configuration"
    }
    
    for file, desc in core_files.items():
        file_path = backend_dir / file
        status = "OK" if file_path.exists() else "MISSING"
        print(f"   {status} {file} - {desc}")
    
    # 2. API Routes Analysis
    print("\n2. API ROUTES:")
    routes_dir = backend_dir / "api/routes"
    if routes_dir.exists():
        routes = [f for f in os.listdir(routes_dir) if f.endswith('.py')]
        for route in routes:
            print(f"   OK {route}")
    else:
        print("   ERROR Routes directory missing")
    
    # 3. Services Analysis
    print("\n3. SERVICES:")
    services_dir = backend_dir / "services"
    if services_dir.exists():
        services = [f for f in os.listdir(services_dir) if f.endswith('.py')]
        for service in services:
            print(f"   OK {service}")
    else:
        print("   ERROR Services directory missing")
    
    # 4. Database Analysis
    print("\n4. DATABASE:")
    db_dir = backend_dir / "db"
    if db_dir.exists():
        db_files = [f for f in os.listdir(db_dir) if f.endswith('.py')]
        for db_file in db_files:
            print(f"   OK {db_file}")
    else:
        print("   ERROR Database directory missing")

def analyze_frontend():
    print("\n" + "=" * 60)
    print("FRONTEND ANALYSIS")
    print("=" * 60)
    
    frontend_dir = Path("frontend")
    
    # 1. Core Files Analysis
    print("\n1. CORE FILES:")
    core_files = {
        "package.json": "Node.js dependencies",
        "src/App.jsx": "React application entry",
        "src/services/api.js": "API service layer",
        "src/hooks/useAuth.jsx": "Authentication hook",
        "src/hooks/useDarkMode.jsx": "Dark mode hook"
    }
    
    for file, desc in core_files.items():
        file_path = frontend_dir / file
        status = "OK" if file_path.exists() else "MISSING"
        print(f"   {status} {file} - {desc}")
    
    # 2. Pages Analysis
    print("\n2. PAGES:")
    pages_dir = frontend_dir / "src/pages"
    if pages_dir.exists():
        pages = [f for f in os.listdir(pages_dir) if f.endswith('.jsx')]
        for page in pages:
            print(f"   OK {page}")
    else:
        print("   ERROR Pages directory missing")
    
    # 3. Components Analysis
    print("\n3. COMPONENTS:")
    components_dir = frontend_dir / "src/components"
    if components_dir.exists():
        components = [f for f in os.listdir(components_dir) if f.endswith('.jsx')]
        for component in components:
            print(f"   OK {component}")
    else:
        print("   ERROR Components directory missing")

def identify_potential_issues():
    print("\n" + "=" * 60)
    print("POTENTIAL ISSUES ANALYSIS")
    print("=" * 60)
    
    issues = []
    
    # Check backend .env
    backend_env = Path("backend/.env")
    if backend_env.exists():
        if backend_env.stat().st_size == 0:
            issues.append("ERROR Backend .env file is empty")
    else:
        issues.append("ERROR Backend .env file missing")
    
    # Check frontend API configuration
    api_file = Path("frontend/src/services/api.js")
    if api_file.exists():
        with open(api_file, 'r') as f:
            content = f.read()
            if 'chatAPI.sendMessage' in content and 'chatAPI.sendWithFile' not in content:
                issues.append("WARNING Chat file upload API missing")
    
    # Check chat component for file upload
    chat_file = Path("frontend/src/pages/Chat.jsx")
    if chat_file.exists():
        with open(chat_file, 'r') as f:
            content = f.read()
            if 'Upload file (coming soon)' in content:
                issues.append("WARNING File upload not implemented in chat")
    
    # Check backend services
    upload_service = Path("backend/services/upload_service.py")
    if upload_service.exists():
        with open(upload_service, 'r') as f:
            content = f.read()
            if 'process_uploaded_file' in content:
                print("OK Upload service exists")
            else:
                issues.append("ERROR Upload service incomplete")
    
    print("\nIDENTIFIED ISSUES:")
    for issue in issues:
        print(f"   {issue}")
    
    return issues

def analyze_dependencies():
    print("\n" + "=" * 60)
    print("DEPENDENCIES ANALYSIS")
    print("=" * 60)
    
    # Backend dependencies
    print("\n1. BACKEND DEPENDENCIES:")
    backend_req = Path("backend/requirements.txt")
    if backend_req.exists():
        with open(backend_req, 'r') as f:
            deps = f.read().split('\n')
            critical_deps = ['fastapi', 'uvicorn', 'sqlalchemy', 'pydantic', 'requests']
            for dep in critical_deps:
                if any(dep in d for d in deps):
                    print(f"   OK {dep}")
                else:
                    print(f"   ERROR {dep} missing")
    
    # Frontend dependencies
    print("\n2. FRONTEND DEPENDENCIES:")
    frontend_pkg = Path("frontend/package.json")
    if frontend_pkg.exists():
        with open(frontend_pkg, 'r') as f:
            try:
                pkg_data = json.load(f)
                deps = pkg_data.get('dependencies', {})
                critical_deps = ['react', 'axios', 'react-router-dom']
                for dep in critical_deps:
                    if dep in deps:
                        print(f"   OK {dep}")
                    else:
                        print(f"   ERROR {dep} missing")
            except:
                print("   ERROR Invalid package.json")

def main():
    print("COMPREHENSIVE SYSTEM ANALYSIS")
    print("Multimodal AI Application")
    
    analyze_backend()
    analyze_frontend()
    analyze_dependencies()
    issues = identify_potential_issues()
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    if not issues:
        print("OK No critical issues found!")
    else:
        print(f"WARNING Found {len(issues)} potential issues")
    
    print("\nRECOMMENDATIONS:")
    print("1. Configure backend .env file with API keys")
    print("2. Implement file upload in chat interface")
    print("3. Add chat with file API endpoint")
    print("4. Test all API endpoints")
    print("5. Verify database connectivity")

if __name__ == "__main__":
    main()
