from pydantic import BaseModel
from typing import Optional

class YouTubeRequest(BaseModel):
    url: str

class YouTubeResponse(BaseModel):
    response: str
    video_title: Optional[str] = None
    error: Optional[str] = None
