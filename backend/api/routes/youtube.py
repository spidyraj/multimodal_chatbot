from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import get_db
from api.dependencies import get_current_user
from services.youtube_service import search_videos
from services.youtube_rag_service import process_youtube_video_rag, query_youtube_knowledge
from services.youtube_rag_demo import demo_youtube_rag
from schemas.youtube_schema import YouTubeRequest, YouTubeResponse
from pydantic import BaseModel
from typing import List, Optional
from core.logger import logger
from db.models import User

class YouTubeSearchRequest(BaseModel):
    query: str
    max_results: int = 5

class YouTubeVideoInfo(BaseModel):
    video_id: str
    title: str
    description: str
    channel_title: str
    thumbnail_url: Optional[str] = None

class YouTubeSearchResponse(BaseModel):
    videos: List[YouTubeVideoInfo]
    total_results: int

router = APIRouter(prefix="/youtube", tags=["youtube"])

@router.post("/summarize", response_model=YouTubeResponse)
async def summarize_video(
    youtube_request: YouTubeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Summarize YouTube video using enhanced RAG approach
    """
    try:
        logger.info(f"Starting YouTube RAG summarization for user {current_user.id}")
        
        # Use enhanced RAG processing
        result = process_youtube_video_rag(youtube_request.url, current_user.id)
        
        if "error" in result:
            logger.warning(f"YouTube RAG error for user {current_user.id}: {result['error']}")
            return YouTubeResponse(
                response="",
                error=result["error"]
            )
        
        logger.info(f"YouTube RAG video summarized for user {current_user.id}: {result.get('video_id')}")
        
        return YouTubeResponse(
            response=result["response"],
            video_id=result.get("video_id"),
            video_title=result.get("video_title")
        )
        
    except Exception as e:
        logger.error(f"YouTube RAG summarization error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to summarize YouTube video using RAG"
        )

@router.post("/search", response_model=YouTubeSearchResponse)
async def search_videos(
    search_request: YouTubeSearchRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Search for YouTube videos
    """
    try:
        videos = search_videos(search_request.query, search_request.max_results)
        
        video_infos = []
        for video in videos:
            video_infos.append(YouTubeVideoInfo(
                video_id=video['video_id'],
                title=video['title'],
                description=video['description'][:200] + "..." if len(video['description']) > 200 else video['description'],
                channel_title=video['channel_title'],
                thumbnail_url=video.get('thumbnail_url')
            ))
        
        logger.info(f"YouTube search completed for user {current_user.id}: {search_request.query}")
        
        return YouTubeSearchResponse(
            videos=video_infos,
            total_results=len(video_infos)
        )
        
    except Exception as e:
        logger.error(f"YouTube search error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to search YouTube videos"
        )

@router.post("/query-knowledge")
async def query_youtube_videos_knowledge(
    query_request: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Query knowledge from previously processed YouTube videos using RAG
    """
    try:
        query = query_request.get("query", "")
        top_k = query_request.get("top_k", 5)
        
        if not query:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Query is required"
            )
        
        logger.info(f"Querying YouTube knowledge for user {current_user.id}: {query}")
        
        result = query_youtube_knowledge(query, current_user.id, top_k)
        
        if "error" in result:
            logger.error(f"YouTube knowledge query error: {result['error']}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to query YouTube knowledge"
            )
        
        logger.info(f"YouTube knowledge query completed for user {current_user.id}")
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"YouTube knowledge query error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to query YouTube knowledge"
        )

@router.post("/demo-rag")
async def demo_youtube_rag_endpoint(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Demonstrate YouTube RAG system with mock transcript
    """
    try:
        logger.info(f"Starting YouTube RAG demo for user {current_user.id}")
        
        # Use demo RAG processing with mock transcript
        result = demo_youtube_rag("demo_ml", current_user.id)
        
        if "error" in result:
            logger.error(f"YouTube RAG demo error for user {current_user.id}: {result['error']}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to demonstrate YouTube RAG"
            )
        
        logger.info(f"YouTube RAG demo completed for user {current_user.id}")
        
        return YouTubeResponse(
            response=result["response"],
            video_id=result.get("video_id"),
            video_title=result.get("video_title")
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"YouTube RAG demo error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to demonstrate YouTube RAG"
        )
