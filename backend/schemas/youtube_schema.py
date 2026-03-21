from pydantic import BaseModel

class YouTubeRequest(BaseModel):
    url: str

class YouTubeResponse(BaseModel):
    response: str
    video_title: Optional[str] = None
    error: Optional[str] = None
