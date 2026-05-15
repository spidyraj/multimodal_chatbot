from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import get_db
from api.dependencies import get_current_user
from services.youtube_service import summarize_youtube_video
from schemas.youtube_schema import YouTubeRequest, YouTubeResponse
from core.logger import logger
from db.models import User

router = APIRouter(prefix="/youtube", tags=["youtube"])

@router.post("/summarize", response_model=YouTubeResponse)
async def summarize_video(
    youtube_request: YouTubeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Summarize YouTube video
    """
    try:
        result = summarize_youtube_video(youtube_request.url)
        
        if "error" in result:
            logger.warning(f"YouTube error for user {current_user.id}: {result['error']}")
            return YouTubeResponse(
                response="",
                error=result["error"]
            )
        
        logger.info(f"YouTube video summarized for user {current_user.id}: {result.get('video_id')}")
        
        return YouTubeResponse(
            response=result["response"],
            video_id=result.get("video_id"),
            video_title=result.get("video_title")
        )
        
    except Exception as e:
        logger.error(f"YouTube summarization error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to summarize YouTube video"
        )
