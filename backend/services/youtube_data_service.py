import re
import requests
from typing import Optional, Dict, List
from services.llm_service import ask_llm_smart
from core.logger import logger
from core.config import settings

class YouTubeDataService:
    def __init__(self):
        self.api_key = getattr(settings, 'YOUTUBE_API_KEY', None)
        self.base_url = "https://www.googleapis.com/youtube/v3"
        
    def extract_video_id(self, url: str) -> Optional[str]:
        """Extract YouTube video ID from URL"""
        patterns = [
            r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([a-zA-Z0-9_-]{11})',
            r'youtube\.com/watch\?.*v=([a-zA-Z0-9_-]{11})'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        return None
    
    def get_video_details(self, video_id: str) -> Optional[Dict]:
        """Get video details using YouTube Data API v3"""
        if not self.api_key:
            logger.error("YouTube API key not configured")
            return None
        
        try:
            url = f"{self.base_url}/videos"
            params = {
                'part': 'snippet,contentDetails,statistics',
                'id': video_id,
                'key': self.api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if not data.get('items'):
                logger.error(f"No video found for ID: {video_id}")
                return None
            
            video = data['items'][0]
            snippet = video['snippet']
            
            return {
                'video_id': video_id,
                'title': snippet.get('title', 'Unknown Title'),
                'description': snippet.get('description', ''),
                'channel_title': snippet.get('channelTitle', ''),
                'published_at': snippet.get('publishedAt', ''),
                'duration': video.get('contentDetails', {}).get('duration', ''),
                'view_count': video.get('statistics', {}).get('viewCount', '0'),
                'like_count': video.get('statistics', {}).get('likeCount', '0'),
                'tags': snippet.get('tags', [])
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"YouTube API request failed: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Error getting video details: {str(e)}")
            return None
    
    def get_video_captions(self, video_id: str, language: str = 'en') -> Optional[str]:
        """Get video captions using YouTube Data API v3"""
        if not self.api_key:
            logger.error("YouTube API key not configured")
            return None
        
        try:
            # First, get available caption tracks
            url = f"{self.base_url}/captions"
            params = {
                'part': 'snippet',
                'videoId': video_id,
                'key': self.api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if not data.get('items'):
                logger.info(f"No captions available for video: {video_id}")
                return None
            
            # Find the best caption track
            caption_track = None
            for item in data['items']:
                snippet = item['snippet']
                track_language = snippet.get('language', '')
                
                # Prefer exact language match
                if track_language == language:
                    caption_track = item
                    break
                # Fall back to auto-generated captions
                elif snippet.get('trackKind') == 'asr' and not caption_track:
                    caption_track = item
            
            if not caption_track:
                logger.info(f"No suitable caption track found for video: {video_id}")
                return None
            
            # Download the caption content
            caption_id = caption_track['id']
            download_url = f"{self.base_url}/captions/{caption_id}"
            params = {
                'tfmt': 'srt',  # Get captions in SRT format
                'key': self.api_key
            }
            
            response = requests.get(download_url, params=params, timeout=10)
            response.raise_for_status()
            
            # Parse SRT format and extract text
            srt_content = response.text
            caption_text = self._parse_srt_captions(srt_content)
            
            return caption_text
            
        except requests.exceptions.RequestException as e:
            logger.error(f"YouTube captions API request failed: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Error getting video captions: {str(e)}")
            return None
    
    def _parse_srt_captions(self, srt_content: str) -> str:
        """Parse SRT caption format and extract clean text"""
        try:
            lines = srt_content.split('\n')
            caption_lines = []
            
            for line in lines:
                # Skip timestamp lines and empty lines
                if ' --> ' in line or line.strip().isdigit() or not line.strip():
                    continue
                
                # Remove HTML tags and clean up text
                clean_line = re.sub(r'<[^>]+>', '', line)
                clean_line = re.sub(r'\{[^}]+\}', '', clean_line)  # Remove {formatting}
                clean_line = clean_line.strip()
                
                if clean_line:
                    caption_lines.append(clean_line)
            
            return ' '.join(caption_lines)
            
        except Exception as e:
            logger.error(f"Error parsing SRT captions: {str(e)}")
            return ""
    
    def search_videos(self, query: str, max_results: int = 5) -> List[Dict]:
        """Search for videos using YouTube Data API v3"""
        if not self.api_key:
            logger.error("YouTube API key not configured")
            return []
        
        try:
            url = f"{self.base_url}/search"
            params = {
                'part': 'snippet',
                'q': query,
                'type': 'video',
                'maxResults': max_results,
                'key': self.api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            videos = []
            for item in data.get('items', []):
                snippet = item['snippet']
                videos.append({
                    'video_id': item['id']['videoId'],
                    'title': snippet.get('title', ''),
                    'description': snippet.get('description', ''),
                    'channel_title': snippet.get('channelTitle', ''),
                    'published_at': snippet.get('publishedAt', ''),
                    'thumbnail_url': snippet.get('thumbnails', {}).get('medium', {}).get('url', '')
                })
            
            return videos
            
        except requests.exceptions.RequestException as e:
            logger.error(f"YouTube search API request failed: {str(e)}")
            return []
        except Exception as e:
            logger.error(f"Error searching videos: {str(e)}")
            return []

# Global instance
youtube_service = YouTubeDataService()

def extract_video_id(url: str) -> Optional[str]:
    """Extract YouTube video ID from URL (backward compatibility)"""
    return youtube_service.extract_video_id(url)

def get_video_title(video_id: str) -> Optional[str]:
    """Get video title using YouTube Data API v3"""
    try:
        details = youtube_service.get_video_details(video_id)
        return details['title'] if details else None
    except Exception as e:
        logger.error(f"Error getting video title: {str(e)}")
        return None

def get_transcript(video_id: str) -> Optional[str]:
    """Get transcript for YouTube video using YouTube Data API v3"""
    return youtube_service.get_video_captions(video_id)

def summarize_youtube_video(url: str, user_id: int = None) -> Dict:
    """
    Summarize YouTube video using YouTube Data API v3
    """
    try:
        video_id = extract_video_id(url)
        if not video_id:
            return {
                "response": "",
                "video_id": None,
                "video_title": None,
                "error": "Invalid YouTube URL. Could not extract video ID."
            }
        
        # Get video details
        video_details = youtube_service.get_video_details(video_id)
        if not video_details:
            return {
                "response": "",
                "video_id": video_id,
                "video_title": None,
                "error": "Could not retrieve video details. The video may not exist or is private."
            }
        
        video_title = video_details['title']
        
        # Get captions
        transcript = get_transcript(video_id)
        
        if not transcript:
            # Try to create a summary based on video metadata
            summary_prompt = f"""
            Based on the following YouTube video metadata, please provide a brief summary:
            
            Title: {video_title}
            Description: {video_details.get('description', 'No description available')}
            Channel: {video_details.get('channel_title', 'Unknown')}
            Tags: {', '.join(video_details.get('tags', []))}
            
            Please provide a concise summary of what this video might be about based on the metadata.
            """
            
            try:
                summary_response = ask_llm_smart(summary_prompt)
                return {
                    "response": summary_response,
                    "video_id": video_id,
                    "video_title": video_title,
                    "note": "Summary generated from video metadata (no captions available)"
                }
            except Exception as e:
                logger.error(f"Error generating metadata summary: {str(e)}")
                return {
                    "response": "",
                    "video_id": video_id,
                    "video_title": video_title,
                    "error": "No captions available and could not generate summary from metadata."
                }
        
        # Create summary from transcript
        summary_prompt = f"""
        Please provide a comprehensive summary of the following YouTube video transcript:
        
        Video Title: {video_title}
        Channel: {video_details.get('channel_title', 'Unknown')}
        
        Transcript:
        {transcript[:8000]}  # Limit to first 8000 characters to avoid token limits
        
        Please provide:
        1. A concise summary of the main points
        2. Key takeaways or insights
        3. Overall topic and theme
        """
        
        try:
            summary_response = ask_llm_smart(summary_prompt)
            return {
                "response": summary_response,
                "video_id": video_id,
                "video_title": video_title,
                "transcript_length": len(transcript)
            }
        except Exception as e:
            logger.error(f"Error generating summary: {str(e)}")
            return {
                "response": "",
                "video_id": video_id,
                "video_title": video_title,
                "error": f"Retrieved transcript but failed to generate summary: {str(e)}"
            }
            
    except Exception as e:
        logger.error(f"Error in YouTube video summarization: {str(e)}")
        return {
            "response": "",
            "video_id": None,
            "video_title": None,
            "error": f"An unexpected error occurred: {str(e)}"
        }
