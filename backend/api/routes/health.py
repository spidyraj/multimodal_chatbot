from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from core.database import get_db
from core.logger import logger
from services.embedding_service import get_model_info

router = APIRouter(tags=["health"])

@router.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """
    Health check endpoint for Railway monitoring
    """
    try:
        # Test database connection
        db.execute(text("SELECT 1"))
        
        # Get embedding model info
        model_info = get_model_info()
        
        return {
            "status": "healthy",
            "database": "connected",
            "embedding_model": model_info,
            "timestamp": "2024-01-01T00:00:00Z"  # Will be updated dynamically
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e),
            "embedding_model": get_model_info()
        }
