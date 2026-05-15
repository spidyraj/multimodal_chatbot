#!/usr/bin/env python3
"""
Backend Services Diagnostic Tool
"""
import os
from pathlib import Path

def check_backend_services():
    """Check all backend services for potential issues"""
    print("=" * 60)
    print("BACKEND SERVICES DIAGNOSTIC")
    print("=" * 60)
    
    backend_dir = Path("backend")
    services_dir = backend_dir / "services"
    
    if not services_dir.exists():
        print("❌ Services directory not found")
        return
    
    services = [f for f in os.listdir(services_dir) if f.endswith('.py')]
    
    for service_file in services:
        print(f"\n📁 Checking {service_file}:")
        service_path = services_dir / service_file
        
        try:
            with open(service_path, 'r') as f:
                content = f.read()
            
            # Check for common issues
            issues = []
            
            # Check imports
            if 'import' in content:
                if 'from services.' in content:
                    print("  ✅ Has service imports")
                else:
                    issues.append("Missing service imports")
            
            # Check error handling
            if 'try:' in content and 'except' in content:
                print("  ✅ Has error handling")
            else:
                issues.append("Missing error handling")
            
            # Check logging
            if 'logger.' in content:
                print("  ✅ Has logging")
            else:
                issues.append("Missing logging")
            
            # Check functions
            if 'def ' in content:
                functions = content.count('def ')
                print(f"  ✅ Has {functions} function(s)")
            else:
                issues.append("No functions defined")
            
            # Report issues
            if issues:
                for issue in issues:
                    print(f"  ⚠️  {issue}")
            else:
                print("  ✅ No issues found")
                
        except Exception as e:
            print(f"  ❌ Error reading file: {str(e)}")

def check_youtube_service():
    """Check YouTube service specifically"""
    print("\n" + "=" * 60)
    print("YOUTUBE SERVICE SPECIFIC CHECK")
    print("=" * 60)
    
    youtube_service_path = Path("backend/services/youtube_service.py")
    
    if not youtube_service_path.exists():
        print("❌ YouTube service not found")
        return
    
    try:
        with open(youtube_service_path, 'r') as f:
            content = f.read()
        
        # Check key components
        checks = {
            'URL extraction': 'extract_video_id',
            'Transcript retrieval': 'get_transcript',
            'Video title': 'get_video_title',
            'Summarization': 'summarize_youtube_video',
            'YouTube API import': 'YouTubeTranscriptApi',
            'Error handling': 'TranscriptsDisabled',
            'LLM integration': 'ask_llm_smart',
            'Logging': 'logger.',
        }
        
        print("\n📋 Component Check:")
        for check, pattern in checks.items():
            if pattern in content:
                print(f"  ✅ {check}")
            else:
                print(f"  ❌ {check}")
        
        # Check URL patterns
        print("\n🔗 URL Pattern Check:")
        if 'youtube\.com/watch\?v=' in content:
            print("  ✅ Standard YouTube URL pattern")
        else:
            print("  ❌ Missing standard YouTube URL pattern")
        
        if 'youtu\.be/' in content:
            print("  ✅ Short YouTube URL pattern")
        else:
            print("  ❌ Missing short YouTube URL pattern")
        
        # Check transcript processing
        print("\n📝 Transcript Processing Check:")
        if 'transcript_list' in content:
            print("  ✅ Processes transcript list")
        else:
            print("  ❌ Missing transcript list processing")
        
        if 'join' in content and 'item["text"]' in content:
            print("  ✅ Combines transcript text")
        else:
            print("  ❌ Missing transcript text combination")
        
        # Check error messages
        print("\n⚠️  Error Messages Check:")
        error_messages = [
            "Invalid YouTube URL",
            "Transcript not available",
            "Failed to summarize"
        ]
        
        for msg in error_messages:
            if msg in content:
                print(f"  ✅ Has '{msg}' error")
            else:
                print(f"  ❌ Missing '{msg}' error")
                
    except Exception as e:
        print(f"❌ Error reading YouTube service: {str(e)}")

def check_dependencies():
    """Check backend dependencies"""
    print("\n" + "=" * 60)
    print("DEPENDENCIES CHECK")
    print("=" * 60)
    
    requirements_path = Path("backend/requirements.txt")
    
    if not requirements_path.exists():
        print("❌ Requirements.txt not found")
        return
    
    try:
        with open(requirements_path, 'r') as f:
            requirements = f.read()
        
        # Critical dependencies for YouTube functionality
        critical_deps = {
            'youtube-transcript-api': 'YouTube transcript retrieval',
            'requests': 'HTTP requests',
            'fastapi': 'Web framework',
            'pydantic': 'Data validation',
            'python-jose': 'JWT handling',
            'PyPDF2': 'PDF processing',
            'Pillow': 'Image processing',
            'pytesseract': 'OCR for images',
        }
        
        print("\n📦 Critical Dependencies:")
        for dep, description in critical_deps.items():
            if dep in requirements:
                print(f"  ✅ {dep} - {description}")
            else:
                print(f"  ❌ {dep} - {description} (MISSING)")
        
        # Optional dependencies
        optional_deps = {
            'sentence-transformers': 'Text embeddings (heavy)',
            'pinecone-client': 'Vector database',
        }
        
        print("\n📦 Optional Dependencies:")
        for dep, description in optional_deps.items():
            if dep in requirements:
                print(f"  ✅ {dep} - {description}")
            else:
                print(f"  ⚠️  {dep} - {description} (OPTIONAL)")
                
    except Exception as e:
        print(f"❌ Error reading requirements: {str(e)}")

def check_api_routes():
    """Check API routes"""
    print("\n" + "=" * 60)
    print("API ROUTES CHECK")
    print("=" * 60)
    
    routes_dir = Path("backend/api/routes")
    
    if not routes_dir.exists():
        print("❌ Routes directory not found")
        return
    
    routes = [f for f in os.listdir(routes_dir) if f.endswith('.py')]
    
    for route_file in routes:
        print(f"\n🛣️  Checking {route_file}:")
        route_path = routes_dir / route_file
        
        try:
            with open(route_path, 'r') as f:
                content = f.read()
            
            # Check for router setup
            if 'APIRouter' in content:
                print("  ✅ Has router setup")
            else:
                print("  ❌ Missing router setup")
            
            # Check for endpoints
            endpoint_count = content.count('@router.')
            print(f"  ✅ Has {endpoint_count} endpoint(s)")
            
            # Check for authentication
            if 'get_current_user' in content:
                print("  ✅ Uses authentication")
            else:
                print("  ⚠️  No authentication")
            
            # Check for error handling
            if 'HTTPException' in content:
                print("  ✅ Has HTTP error handling")
            else:
                print("  ⚠️  Missing HTTP error handling")
                
        except Exception as e:
            print(f"  ❌ Error reading route file: {str(e)}")

def identify_common_issues():
    """Identify common backend issues"""
    print("\n" + "=" * 60)
    print("COMMON ISSUES IDENTIFICATION")
    print("=" * 60)
    
    issues = []
    
    # Check 1: Environment variables
    env_example_path = Path("backend/.env.example")
    env_path = Path("backend/.env")
    
    if env_example_path.exists():
        with open(env_example_path, 'r') as f:
            env_example = f.read()
        
        required_vars = ['DATABASE_URL', 'GROQ_API_KEY', 'SECRET_KEY']
        
        for var in required_vars:
            if var in env_example:
                print(f"  ✅ {var} documented in .env.example")
            else:
                print(f"  ❌ {var} missing from .env.example")
                issues.append(f"Missing {var} in .env.example")
    
    # Check 2: Schema consistency
    try:
        schemas_dir = Path("backend/schemas")
        if schemas_dir.exists():
            schema_files = [f for f in os.listdir(schemas_dir) if f.endswith('.py')]
            
            for schema_file in schema_files:
                schema_path = schemas_dir / schema_file
                with open(schema_path, 'r') as f:
                    schema_content = f.read()
                
                # Check for response models
                if 'Response' in schema_content and 'BaseModel' in schema_content:
                    print(f"  ✅ {schema_file} has response models")
                else:
                    print(f"  ⚠️  {schema_file} may need response models")
                    
    except Exception as e:
        print(f"  ❌ Error checking schemas: {str(e)}")
    
    # Check 3: Service integration
    services_dir = Path("backend/services")
    if services_dir.exists():
        service_files = [f for f in os.listdir(services_dir) if f.endswith('.py')]
        
        for service_file in service_files:
            service_path = services_dir / service_file
            with open(service_path, 'r') as f:
                service_content = f.read()
            
            # Check if services are used in routes
            routes_dir = Path("backend/api/routes")
            if routes_dir.exists():
                route_files = [f for f in os.listdir(routes_dir) if f.endswith('.py')]
                
                service_used = False
                for route_file in route_files:
                    route_path = routes_dir / route_file
                    with open(route_path, 'r') as f:
                        route_content = f.read()
                    
                    service_name = service_file.replace('.py', '')
                    if service_name.replace('_service', '') in route_content:
                        service_used = True
                        break
                
                if service_used:
                    print(f"  ✅ {service_file} is integrated")
                else:
                    print(f"  ⚠️  {service_file} may not be used")
    
    return issues

def main():
    print("BACKEND COMPREHENSIVE DIAGNOSTIC")
    print("Multimodal AI Application")
    
    check_backend_services()
    check_youtube_service()
    check_dependencies()
    check_api_routes()
    issues = identify_common_issues()
    
    print("\n" + "=" * 60)
    print("DIAGNOSTIC SUMMARY")
    print("=" * 60)
    
    if not issues:
        print("✅ No critical issues found!")
        print("\nBackend services appear to be properly configured.")
    else:
        print(f"⚠️  Found {len(issues)} potential issues")
    
    print("\nRECOMMENDATIONS:")
    print("1. Ensure all environment variables are set in Railway")
    print("2. Verify YouTube transcript API is working")
    print("3. Test Groq API connectivity")
    print("4. Check Pinecone integration for RAG")
    print("5. Test file upload functionality")

if __name__ == "__main__":
    main()
