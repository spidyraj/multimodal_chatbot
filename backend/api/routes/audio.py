from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from core.database import get_db
from api.dependencies import get_current_user
from services.audio_service import generate_audio_from_text, validate_audio_request, get_supported_languages
from core.logger import logger
from db.models import User
from schemas.audio_schema import AudioRequest, AudioResponse
import io

router = APIRouter(prefix="/audio", tags=["audio"])

@router.post("/generate")
async def generate_audio(
    audio_request: AudioRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generate audio from text
    """
    try:
        # Validate request
        is_valid, message = validate_audio_request(audio_request.text, audio_request.language)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=message
            )
        
        # Generate audio
        audio_data = generate_audio_from_text(
            text=audio_request.text,
            language=audio_request.language,
            slow=audio_request.slow
        )
        
        if not audio_data:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to generate audio"
            )
        
        logger.info(f"Audio generated for user {current_user.id}")
        
        # Return audio as streaming response
        return StreamingResponse(
            io.BytesIO(audio_data),
            media_type="audio/mpeg",
            headers={
                "Content-Disposition": f"attachment; filename=audio_{current_user.id}.mp3"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Audio generation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate audio"
        )

@router.get("/languages")
async def get_languages():
    """
    Get list of supported languages
    """
    try:
        languages = get_supported_languages()
        return {"languages": languages}
        
    except Exception as e:
        logger.error(f"Languages retrieval error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve supported languages"
        )

@router.post("/speak")
async def speak_text(
    text: str = Query(..., description="Text to convert to speech"),
    language: str = Query("en", description="Language code"),
    slow: bool = Query(False, description="Speak slowly"),
    current_user: User = Depends(get_current_user)
):
    """
    Simple text-to-speech endpoint
    """
    try:
        # Validate request
        is_valid, message = validate_audio_request(text, language)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=message
            )
        
        # Generate audio
        audio_data = generate_audio_from_text(text=text, language=language, slow=slow)
        
        if not audio_data:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to generate audio"
            )
        
        logger.info(f"Text-to-speech generated for user {current_user.id}")
        
        # Return audio as streaming response
        return StreamingResponse(
            io.BytesIO(audio_data),
            media_type="audio/mpeg",
            headers={
                "Content-Disposition": "inline; filename=speech.mp3"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Text-to-speech error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate speech"
        )
