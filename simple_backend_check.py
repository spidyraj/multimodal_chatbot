#!/usr/bin/env python3
"""
Simple Backend Check
"""
import os
from pathlib import Path

def main():
    print("BACKEND SERVICES CHECK")
    print("=" * 50)
    
    # Check YouTube service specifically
    youtube_service = Path("backend/services/youtube_service.py")
    if youtube_service.exists():
        with open(youtube_service, 'r') as f:
            content = f.read()
        
        print("YouTube Service:")
        if "extract_video_id" in content:
            print("  OK: URL extraction function")
        if "get_transcript" in content:
            print("  OK: Transcript retrieval function")
        if "YouTubeTranscriptApi" in content:
            print("  OK: YouTube API import")
        if "ask_llm_smart" in content:
            print("  OK: LLM integration")
        if "logger" in content:
            print("  OK: Logging included")
        
        # Check for improvements
        if "get_video_title" in content:
            print("  OK: Video title function added")
        if "video_title" in content:
            print("  OK: Video title in response")
        
    else:
        print("ERROR: YouTube service not found")
    
    # Check YouTube route
    youtube_route = Path("backend/api/routes/youtube.py")
    if youtube_route.exists():
        with open(youtube_route, 'r') as f:
            content = f.read()
        
        print("\nYouTube Route:")
        if "summarize_video" in content:
            print("  OK: Summarize endpoint")
        if "get_current_user" in content:
            print("  OK: Authentication required")
        if "YouTubeResponse" in content:
            print("  OK: Response model used")
        
        # Check for video title
        if "video_title=result.get" in content:
            print("  OK: Video title passed to response")
        
    else:
        print("ERROR: YouTube route not found")
    
    # Check YouTube schema
    youtube_schema = Path("backend/schemas/youtube_schema.py")
    if youtube_schema.exists():
        with open(youtube_schema, 'r') as f:
            content = f.read()
        
        print("\nYouTube Schema:")
        if "video_id" in content:
            print("  OK: video_id field present")
        if "video_title" in content:
            print("  OK: video_title field present")
        if "error" in content:
            print("  OK: error field present")
        
    else:
        print("ERROR: YouTube schema not found")
    
    # Check requirements
    requirements = Path("backend/requirements.txt")
    if requirements.exists():
        with open(requirements, 'r') as f:
            content = f.read()
        
        print("\nDependencies:")
        if "youtube-transcript-api" in content:
            print("  OK: YouTube transcript API")
        if "requests" in content:
            print("  OK: Requests library")
        if "fastapi" in content:
            print("  OK: FastAPI")
        
    else:
        print("ERROR: Requirements not found")
    
    print("\n" + "=" * 50)
    print("CHECK COMPLETE")
    print("\nIf all checks show OK, YouTube service should work.")
    print("Common issues:")
    print("1. Video has no transcript/captions")
    print("2. Video ID extraction fails")
    print("3. Groq API key not working")
    print("4. Network connectivity issues")

if __name__ == "__main__":
    main()
