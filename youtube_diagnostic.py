#!/usr/bin/env python3
"""
YouTube Service Diagnostic Tool
"""
import re
import requests
from urllib.parse import urlparse

def test_youtube_url_extraction():
    """Test YouTube URL extraction patterns"""
    print("=" * 60)
    print("YOUTUBE URL EXTRACTION TEST")
    print("=" * 60)
    
    test_urls = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://youtu.be/dQw4w9WgXcQ",
        "https://youtube.com/embed/dQw4w9WgXcQ",
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=30s",
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=Test",
    ]
    
    patterns = [
        r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([a-zA-Z0-9_-]{11})',
        r'youtube\.com/watch\?.*v=([a-zA-Z0-9_-]{11})'
    ]
    
    for url in test_urls:
        print(f"\nTesting URL: {url}")
        for i, pattern in enumerate(patterns):
            match = re.search(pattern, url)
            if match:
                print(f"  Pattern {i+1}: ✅ Extracted ID: {match.group(1)}")
                break
        else:
            print(f"  ❌ No pattern matched")

def test_youtube_transcript_api():
    """Test YouTube transcript API functionality"""
    print("\n" + "=" * 60)
    print("YOUTUBE TRANSCRIPT API TEST")
    print("=" * 60)
    
    try:
        from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
        print("✅ youtube_transcript_api imported successfully")
        
        # Test with a known video ID (Rick Astley - Never Gonna Give You Up)
        test_video_id = "dQw4w9WgXcQ"
        
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(test_video_id)
            print(f"✅ Transcript retrieved for {test_video_id}")
            print(f"   - Number of segments: {len(transcript_list)}")
            
            if transcript_list:
                first_segment = transcript_list[0]
                print(f"   - First segment: '{first_segment['text'][:50]}...'")
                print(f"   - Duration: {first_segment['duration']}s")
            
        except TranscriptsDisabled:
            print(f"⚠️  Transcripts disabled for {test_video_id}")
        except NoTranscriptFound:
            print(f"⚠️  No transcript found for {test_video_id}")
        except Exception as e:
            print(f"❌ Error getting transcript: {str(e)}")
            
    except ImportError:
        print("❌ youtube_transcript_api not installed")

def test_groq_api():
    """Test Groq API connectivity"""
    print("\n" + "=" * 60)
    print("GROQ API TEST")
    print("=" * 60)
    
    # This would require API key, so we'll just test the endpoint
    try:
        response = requests.get("https://api.groq.com/openai/v1/models", timeout=5)
        if response.status_code == 401:
            print("✅ Groq API endpoint accessible (401 = needs auth)")
        elif response.status_code == 200:
            print("✅ Groq API working")
        else:
            print(f"⚠️  Groq API returned: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Groq API not accessible: {str(e)}")

def analyze_youtube_service():
    """Analyze the YouTube service code"""
    print("\n" + "=" * 60)
    print("YOUTUBE SERVICE CODE ANALYSIS")
    print("=" * 60)
    
    # Read the YouTube service file
    try:
        with open('backend/services/youtube_service.py', 'r') as f:
            content = f.read()
        
        print("✅ YouTube service file found")
        
        # Check for key components
        checks = {
            'extract_video_id function': 'def extract_video_id',
            'get_transcript function': 'def get_transcript',
            'summarize_youtube_video function': 'def summarize_youtube_video',
            'URL patterns': 'youtube\.com/watch\?v=|youtu\.be/',
            'Transcript API import': 'YouTubeTranscriptApi',
            'Error handling': 'TranscriptsDisabled',
            'LLM service integration': 'ask_llm_smart',
            'Regex patterns': 're\.search',
        }
        
        for check, pattern in checks.items():
            if pattern in content:
                print(f"✅ {check}")
            else:
                print(f"❌ {check}")
                
    except FileNotFoundError:
        print("❌ YouTube service file not found")

def check_backend_routes():
    """Check backend YouTube routes"""
    print("\n" + "=" * 60)
    print("BACKEND YOUTUBE ROUTES CHECK")
    print("=" * 60)
    
    try:
        with open('backend/api/routes/youtube.py', 'r') as f:
            content = f.read()
        
        print("✅ YouTube routes file found")
        
        checks = {
            'Router setup': 'APIRouter',
            'Summarize endpoint': '@router.post("/summarize"',
            'Authentication': 'get_current_user',
            'Service integration': 'summarize_youtube_video',
            'Error handling': 'HTTPException',
            'Response model': 'YouTubeResponse',
        }
        
        for check, pattern in checks.items():
            if pattern in content:
                print(f"✅ {check}")
            else:
                print(f"❌ {check}")
                
    except FileNotFoundError:
        print("❌ YouTube routes file not found")

def identify_potential_issues():
    """Identify potential issues with YouTube functionality"""
    print("\n" + "=" * 60)
    print("POTENTIAL ISSUES ANALYSIS")
    print("=" * 60)
    
    issues = []
    
    # Check 1: Schema mismatch
    try:
        with open('backend/api/routes/youtube.py', 'r') as f:
            routes_content = f.read()
        with open('backend/schemas/youtube_schema.py', 'r') as f:
            schema_content = f.read()
        
        if 'video_id' in routes_content and 'video_id' not in schema_content:
            issues.append("❌ Schema mismatch: route returns video_id but schema doesn't include it")
        
        if 'video_title' in schema_content and 'video_title' not in routes_content:
            issues.append("⚠️  Schema has video_title but route doesn't provide it")
            
    except FileNotFoundError:
        issues.append("❌ YouTube files not found")
    
    # Check 2: Model availability
    try:
        with open('backend/services/llm_service.py', 'r') as f:
            llm_content = f.read()
        
        if 'ask_llm_smart' not in llm_content:
            issues.append("❌ ask_llm_smart function not found in LLM service")
        elif 'def ask_llm_smart' not in llm_content:
            issues.append("❌ ask_llm_smart function defined but not implemented")
            
    except FileNotFoundError:
        issues.append("❌ LLM service file not found")
    
    # Check 3: Transcript API dependency
    try:
        with open('backend/requirements.txt', 'r') as f:
            req_content = f.read()
        
        if 'youtube-transcript-api' not in req_content:
            issues.append("❌ youtube-transcript-api not in requirements")
            
    except FileNotFoundError:
        issues.append("❌ Requirements file not found")
    
    print("IDENTIFIED ISSUES:")
    for issue in issues:
        print(f"   {issue}")
    
    return issues

def main():
    print("YOUTUBE SERVICE COMPREHENSIVE DIAGNOSTIC")
    print("Multimodal AI Application")
    
    test_youtube_url_extraction()
    test_youtube_transcript_api()
    test_groq_api()
    analyze_youtube_service()
    check_backend_routes()
    issues = identify_potential_issues()
    
    print("\n" + "=" * 60)
    print("DIAGNOSTIC SUMMARY")
    print("=" * 60)
    
    if not issues:
        print("✅ No critical issues found!")
        print("\nYouTube service should be working properly.")
    else:
        print(f"⚠️  Found {len(issues)} potential issues")
        print("\nRECOMMENDED FIXES:")
        print("1. Fix schema mismatches")
        print("2. Implement missing LLM functions")
        print("3. Verify dependencies are installed")
        print("4. Test with actual YouTube URLs")

if __name__ == "__main__":
    main()
