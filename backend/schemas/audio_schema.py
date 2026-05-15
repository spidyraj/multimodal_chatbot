from pydantic import BaseModel, Field
from typing import Optional

class AudioRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000, description="Text to convert to audio")
    language: str = Field(default="en", description="Language code (en, es, fr, de, it, pt, ru, ja, ko, zh, ar, hi)")
    slow: bool = Field(default=False, description="Speak slowly")

class AudioResponse(BaseModel):
    message: str
    audio_url: Optional[str] = None

class LanguageResponse(BaseModel):
    languages: dict
