#!/usr/bin/env python3
"""
System diagnostic script for Multimodal AI
"""
import os
import sys
import subprocess
from pathlib import Path

def print_header(title):
    print(f"\n{'='*50}")
    print(f" {title}")
    print(f"{'='*50}")

def check_python():
    print_header("Python Environment")
    print(f"Python version: {sys.version}")
    print(f"Python path: {sys.executable}")

def check_backend():
    print_header("Backend Configuration")
    
    # Check backend directory
    backend_dir = Path("backend")
    if backend_dir.exists():
        print(f"OK: Backend directory exists: {backend_dir.absolute()}")
        
        # Check key files
        key_files = ["main.py", "requirements.txt", ".env.example"]
        for file in key_files:
            file_path = backend_dir / file
            status = "OK" if file_path.exists() else "MISSING"
            print(f"{status}: {file}")
        
        # Check .env file
        env_file = backend_dir / ".env"
        if env_file.exists():
            if env_file.stat().st_size > 0:
                print("OK: .env file exists and is not empty")
            else:
                print("WARNING: .env file exists but is empty")
        else:
            print("MISSING: .env file")
    else:
        print("ERROR: Backend directory not found")

def check_frontend():
    print_header("Frontend Configuration")
    
    # Check frontend directory
    frontend_dir = Path("frontend")
    if frontend_dir.exists():
        print(f"OK: Frontend directory exists: {frontend_dir.absolute()}")
        
        # Check key files
        key_files = ["package.json", "src/App.jsx", ".env.example"]
        for file in key_files:
            file_path = frontend_dir / file
            status = "OK" if file_path.exists() else "MISSING"
            print(f"{status}: {file}")
        
        # Check node_modules
        node_modules = frontend_dir / "node_modules"
        status = "OK" if node_modules.exists() else "MISSING"
        print(f"{status}: node_modules directory")
    else:
        print("ERROR: Frontend directory not found")

def check_docker():
    print_header("Docker Configuration")
    
    # Check Docker files
    docker_files = [
        "backend/Dockerfile",
        "frontend/Dockerfile",
        "docker-compose.yml"
    ]
    
    for docker_file in docker_files:
        file_path = Path(docker_file)
        status = "OK" if file_path.exists() else "MISSING"
        print(f"{status}: {docker_file}")

def check_api_connectivity():
    print_header("API Connectivity Test")
    
    # Test common API endpoints (using curl instead of requests)
    test_urls = [
        "https://multimodal-backend-production.up.railway.app/health",
        "https://multimodal-frontend-production.up.railway.app",
        "http://localhost:8000/health",
        "http://localhost:3000"
    ]
    
    for url in test_urls:
        try:
            result = subprocess.run(['curl', '-s', '-o', '/dev/null', '-w', '%{http_code}', url], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                status_code = result.stdout.strip()
                status = "OK" if status_code == "200" else f"WARNING ({status_code})"
                print(f"{status}: {url}")
            else:
                print(f"ERROR: {url} (Connection failed)")
        except (subprocess.TimeoutExpired, FileNotFoundError):
            print(f"ERROR: {url} (Connection test failed)")

def check_environment():
    print_header("Environment Variables")
    
    # Check important environment variables
    env_vars = [
        "DATABASE_URL",
        "GROQ_API_KEY", 
        "PINECONE_API_KEY",
        "SECRET_KEY"
    ]
    
    for var in env_vars:
        value = os.environ.get(var)
        if value:
            masked = value[:8] + "..." if len(value) > 8 else "***"
            print(f"OK: {var}: {masked}")
        else:
            print(f"MISSING: {var}")

def main():
    print("System Diagnostic for Multimodal AI")
    print(f"Working directory: {Path.cwd()}")
    
    check_python()
    check_backend()
    check_frontend()
    check_docker()
    check_api_connectivity()
    check_environment()
    
    print_header("Summary")
    print("System diagnostic complete!")
    print("Check the output above for any issues")
    print("If everything looks good, your system should be working!")

if __name__ == "__main__":
    main()
