import re
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from typing import Optional, Dict
from services.llm_service import ask_llm_smart
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

def get_video_title(video_id: str) -> Optional[str]:
    """
    Get video title using YouTube API fallback
    Note: This is a simplified version. In production, you might want to use YouTube Data API
    """
    try:
        # Try to get transcript info which sometimes includes metadata
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        
        # For now, return a generic title with video ID
        # In production, you'd use YouTube Data API v3 to get the actual title
        return f"YouTube Video ({video_id})"
        
    except Exception as e:
        logger.warning(f"Could not get video title for {video_id}: {str(e)}")
        return f"YouTube Video ({video_id})"

def get_transcript(video_id: str) -> Optional[str]:
    """
    Get transcript for YouTube video
    """
    try:
        # Try to get transcript in multiple languages
        transcript_list = None
        
        # Try English first
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        except:
            # If English fails, try any available language
            try:
                transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            except:
                pass
        
        if not transcript_list:
            return None
        
        # Combine transcript text
        transcript_text = " ".join([item["text"] for item in transcript_list])
        
        # Clean up the text
        transcript_text = re.sub(r'\[.*?\]', '', transcript_text)  # Remove [Music] etc.
        transcript_text = re.sub(r'\s+', ' ', transcript_text).strip()
        
        # Log transcript info
        logger.info(f"Retrieved transcript for {video_id}: {len(transcript_text)} characters")
        
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
        logger.info(f"Starting YouTube summarization for URL: {url}")
        
        # Extract video ID
        video_id = extract_video_id(url)
        if not video_id:
            logger.error(f"Could not extract video ID from URL: {url}")
            return {"error": "Invalid YouTube URL. Please check the URL and try again."}
        
        logger.info(f"Extracted video ID: {video_id}")
        
        # Get video title
        video_title = get_video_title(video_id)
        
        # Get transcript
        transcript = get_transcript(video_id)
        if not transcript:
            logger.warning(f"No transcript available for video {video_id}")
            return {"error": "Transcript not available for this video. The video may not have subtitles or captions enabled."}
        
        # Check transcript length
        if len(transcript) < 50:
            logger.warning(f"Transcript too short for video {video_id}: {len(transcript)} characters")
            return {"error": "Transcript is too short to generate a meaningful summary."}
        
        # Limit transcript length for API (keep important parts)
        max_length = 8000  # Increased for better summaries
        if len(transcript) > max_length:
            # Take first part and last part to maintain context
            first_part = transcript[:max_length//2]
            last_part = transcript[-max_length//2:]
            transcript = first_part + "\n...\n" + last_part
            logger.info(f"Transcript truncated for video {video_id}: {len(transcript)} characters")
        
        # Generate summary
        prompt = f"""
        Please provide a comprehensive summary of the following YouTube video transcript:
        
        Video Title: {video_title}
        Video ID: {video_id}
        
        Transcript:
        {transcript}
        
        Please provide:
        1. A concise overview of the main topic
        2. Key points and insights discussed
        3. Any important conclusions or takeaways
        4. Notable examples or demonstrations (if any)
        
        Format the summary in a clear, readable way with bullet points for key information.
        """
        
        logger.info(f"Sending transcript to LLM for summarization...")
        summary = ask_llm_smart(prompt)
        
        if not summary or len(summary) < 50:
            logger.error(f"LLM returned empty or very short summary for video {video_id}")
            return {"error": "Failed to generate summary. Please try again."}
        
        logger.info(f"Successfully generated summary for video {video_id}")
        
        return {
            "response": summary,
            "video_id": video_id,
            "video_title": video_title
        }
        
    except Exception as e:
        logger.error(f"YouTube summarization error: {str(e)}")
        return {"error": "Failed to summarize video. Please try again later."}
