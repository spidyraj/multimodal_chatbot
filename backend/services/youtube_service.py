import re
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from typing import Optional, Dict
from services.llm_service import ask_llm
from core.logger import logger

def extract_video_id(url: str) -> Optional[str]:
    """
    Extract YouTube video ID from URL
    """
    patterns = [
        r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([a-zA-Z0-9_-]{11})',
        r'youtube\.com/watch\?.*v=([a-zA-Z0-9_-]{11})'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None

def get_transcript(video_id: str) -> Optional[str]:
    """
    Get transcript for YouTube video
    """
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        
        # Combine transcript text
        transcript_text = " ".join([item["text"] for item in transcript_list])
        
        # Clean up the text
        transcript_text = re.sub(r'\[.*?\]', '', transcript_text)  # Remove [Music] etc.
        transcript_text = re.sub(r'\s+', ' ', transcript_text).strip()
        
        return transcript_text
        
    except TranscriptsDisabled:
        logger.warning(f"Transcripts disabled for video {video_id}")
        return None
    except NoTranscriptFound:
        logger.warning(f"No transcript found for video {video_id}")
        return None
    except Exception as e:
        logger.error(f"Error getting transcript for {video_id}: {str(e)}")
        return None

def summarize_youtube_video(url: str) -> Dict[str, str]:
    """
    Summarize YouTube video
    """
    try:
        # Extract video ID
        video_id = extract_video_id(url)
        if not video_id:
            return {"error": "Invalid YouTube URL"}
        
        # Get transcript
        transcript = get_transcript(video_id)
        if not transcript:
            return {"error": "Transcript not available for this video"}
        
        # Limit transcript length for API
        if len(transcript) > 4000:
            transcript = transcript[:4000] + "..."
        
        # Generate summary
        prompt = f"""
        Please provide a comprehensive summary of the following YouTube video transcript:
        
        {transcript}
        
        Focus on the main points, key insights, and any actionable information.
        """
        
        summary = ask_llm(prompt, max_tokens=1500)
        
        return {
            "response": summary,
            "video_id": video_id
        }
        
    except Exception as e:
        logger.error(f"YouTube summarization error: {str(e)}")
        return {"error": "Failed to summarize video. Please try again."}
