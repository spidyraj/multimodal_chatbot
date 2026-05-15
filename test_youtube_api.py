#!/usr/bin/env python3
"""
Test YouTube Transcript API directly
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
import re

def extract_video_id(url: str) -> str:
    """Extract YouTube video ID from URL"""
    patterns = [
        r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([a-zA-Z0-9_-]{11})',
        r'youtube\.com/watch\?.*v=([a-zA-Z0-9_-]{11})'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None

def test_video_transcript(video_url: str):
    """Test transcript retrieval for a video"""
    print(f"\n🎥 Testing video: {video_url}")
    
    video_id = extract_video_id(video_url)
    if not video_id:
        print("❌ Could not extract video ID")
        return
    
    print(f"📹 Video ID: {video_id}")
    
    try:
        # Get available transcript languages
        print("🔍 Getting available transcript languages...")
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        
        print("✅ Available transcripts:")
        for transcript in transcript_list:
            print(f"   - {transcript.language_code} ({transcript.language}) - {'Generated' if transcript.is_generated else 'Manual'}")
        
        # Try to get English transcript
        print("\n📝 Getting English transcript...")
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
            print(f"✅ Got transcript with {len(transcript)} segments")
            
            # Show first few segments
            print("📄 First few transcript segments:")
            for i, segment in enumerate(transcript[:3]):
                print(f"   {i+1}. {segment['text']}")
            
            # Combine full transcript
            full_text = ' '.join([segment['text'] for segment in transcript])
            print(f"\n📊 Full transcript length: {len(full_text)} characters")
            print(f"📊 First 200 chars: {full_text[:200]}...")
            
            return True
            
        except NoTranscriptFound:
            print("❌ No English transcript found")
            
            # Try any available language
            try:
                transcript = YouTubeTranscriptApi.get_transcript(video_id)
                print(f"✅ Got transcript in another language with {len(transcript)} segments")
                return True
            except NoTranscriptFound:
                print("❌ No transcript found in any language")
                return False
                
    except TranscriptsDisabled:
        print("❌ Transcripts are disabled for this video")
        return False
    except Exception as e:
        print(f"❌ Error getting transcript: {str(e)}")
        return False

def main():
    print("🧪 YouTube Transcript API Test")
    print("=" * 50)
    
    # Test videos
    test_videos = [
        "https://www.youtube.com/watch?v=KsX3fRnC_HQ",  # User's video
        "https://www.youtube.com/watch?v=jNQXAC9IVRw",  # First YouTube video
        "https://www.youtube.com/watch?v=afBqo7wCJ9U",  # Educational
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",  # Rick Roll
    ]
    
    success_count = 0
    
    for video_url in test_videos:
        if test_video_transcript(video_url):
            success_count += 1
    
    print(f"\n📈 Results: {success_count}/{len(test_videos)} videos have transcripts available")
    
    if success_count == 0:
        print("\n⚠️  No videos had transcripts available. This could be due to:")
        print("   - YouTube API restrictions")
        print("   - Geographic limitations")
        print("   - Video privacy settings")
        print("   - Rate limiting")
    else:
        print("\n✅ YouTube Transcript API is working!")

if __name__ == "__main__":
    main()
