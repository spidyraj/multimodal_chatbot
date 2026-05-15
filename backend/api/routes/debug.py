from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import get_db
from api.dependencies import get_current_user
from services.youtube_service import extract_video_id, get_transcript, get_video_title
from core.logger import logger
import traceback

router = APIRouter(prefix="/debug", tags=["debug"])

@router.get("/youtube-test")
async def test_youtube_api(
    video_url: str = "https://www.youtube.com/watch?v=KsX3fRnC_HQ",
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Test YouTube API functionality
    """
    try:
        result = {
            "video_url": video_url,
            "video_id": None,
            "transcript_available": False,
            "transcript_length": 0,
            "video_title": None,
            "error": None,
            "debug_info": {}
        }
        
        # Extract video ID
        video_id = extract_video_id(video_url)
        result["video_id"] = video_id
        result["debug_info"]["video_id_extraction"] = "success" if video_id else "failed"
        
        if not video_id:
            result["error"] = "Could not extract video ID from URL"
            return result
        
        # Get video title
        try:
            title = get_video_title(video_id)
            result["video_title"] = title
            result["debug_info"]["title_extraction"] = "success"
        except Exception as e:
            result["debug_info"]["title_extraction"] = f"failed: {str(e)}"
        
        # Get transcript
        try:
            transcript = get_transcript(video_id)
            if transcript:
                result["transcript_available"] = True
                result["transcript_length"] = len(transcript)
                result["debug_info"]["transcript_extraction"] = "success"
                result["debug_info"]["transcript_preview"] = transcript[:200] + "..." if len(transcript) > 200 else transcript
            else:
                result["debug_info"]["transcript_extraction"] = "no transcript found"
        except Exception as e:
            result["error"] = str(e)
            result["debug_info"]["transcript_extraction"] = f"failed: {str(e)}"
            result["debug_info"]["traceback"] = traceback.format_exc()
        
        return result
        
    except Exception as e:
        logger.error(f"Debug endpoint error: {str(e)}")
        return {
            "error": str(e),
            "traceback": traceback.format_exc()
        }

@router.get("/youtube-list-transcripts")
async def list_transcripts(
    video_url: str = "https://www.youtube.com/watch?v=KsX3fRnC_HQ",
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    List all available transcripts for a video
    """
    try:
        from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
        
        video_id = extract_video_id(video_url)
        if not video_id:
            return {"error": "Could not extract video ID"}
        
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            
            transcripts = []
            for transcript in transcript_list:
                transcripts.append({
                    "language_code": transcript.language_code,
                    "language": transcript.language,
                    "is_generated": transcript.is_generated,
                    "is_translatable": transcript.is_translatable,
                    "translation_languages": [
                        {"code": lang["language_code"], "name": lang["language"]}
                        for lang in transcript.translation_languages
                    ] if transcript.is_translatable else []
                })
            
            return {
                "video_id": video_id,
                "transcripts": transcripts,
                "total_transcripts": len(transcripts)
            }
            
        except TranscriptsDisabled:
            return {"error": "Transcripts are disabled for this video"}
        except NoTranscriptFound:
            return {"error": "No transcripts found for this video"}
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}
            
    except Exception as e:
        return {"error": str(e), "traceback": traceback.format_exc()}
