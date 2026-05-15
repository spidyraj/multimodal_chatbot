import io
import tempfile
import os
from typing import Optional
from fastapi.responses import StreamingResponse
from gtts import gTTS
from core.logger import logger

def generate_audio_from_text(text: str, language: str = "en", slow: bool = False) -> bytes:
    """
    Generate audio from text using Google Text-to-Speech
    """
    try:
        # Create gTTS object
        tts = gTTS(text=text, lang=language, slow=slow)
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
            tts.save(tmp_file.name)
            tmp_file_path = tmp_file.name
        
        try:
            # Read the audio file
            with open(tmp_file_path, 'rb') as audio_file:
                audio_data = audio_file.read()
            
            return audio_data
            
        finally:
            # Clean up temporary file
            os.unlink(tmp_file_path)
            
    except Exception as e:
        logger.error(f"Audio generation error: {str(e)}")
        return b""

def get_supported_languages() -> dict:
    """
    Get list of supported languages for text-to-speech
    """
    return {
        "en": "English",
        "es": "Spanish", 
        "fr": "French",
        "de": "German",
        "it": "Italian",
        "pt": "Portuguese",
        "ru": "Russian",
        "ja": "Japanese",
        "ko": "Korean",
        "zh": "Chinese",
        "ar": "Arabic",
        "hi": "Hindi"
    }

def validate_audio_request(text: str, language: str = "en") -> tuple[bool, str]:
    """
    Validate audio generation request
    """
    # Check text length
    if not text or len(text.strip()) == 0:
        return False, "Text cannot be empty"
    
    if len(text) > 5000:  # Limit text length
        return False, "Text is too long (max 5000 characters)"
    
    # Check language support
    supported_languages = get_supported_languages()
    if language not in supported_languages:
        return False, f"Language '{language}' is not supported"
    
    return True, "Valid request"
