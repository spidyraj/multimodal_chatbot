# YouTube Data API v3 Setup Guide

## 🚀 **OVERVIEW**

The YouTube summarizer now uses **YouTube Data API v3** for reliable video processing instead of transcript scraping.

## 📋 **SETUP STEPS**

### **1. Get YouTube Data API Key**

1. **Go to Google Cloud Console**: https://console.cloud.google.com/
2. **Create a new project** or select existing one
3. **Enable YouTube Data API v3**:
   - Go to "APIs & Services" → "Library"
   - Search for "YouTube Data API v3"
   - Click "Enable"
4. **Create API Key**:
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "API Key"
   - Copy the API key

### **2. Configure Railway Environment Variables**

Add the following environment variable to your Railway backend service:

```
YOUTUBE_API_KEY=your_youtube_api_key_here
```

### **3. Test the API**

After deployment, test the new endpoints:

#### **YouTube Summarize (Enhanced)**
```bash
POST /youtube/summarize
{
    "url": "https://www.youtube.com/watch?v=KsX3fRnC_HQ"
}
```

#### **YouTube Search (New Feature)**
```bash
POST /youtube/search
{
    "query": "machine learning tutorial",
    "max_results": 5
}
```

## ✨ **NEW FEATURES**

### **🎯 Enhanced Summarization**
- **Video metadata** - Title, description, channel info
- **Caption retrieval** - Using official YouTube API
- **Fallback summaries** - From metadata when captions unavailable
- **Better error handling** - Detailed error messages

### **🔍 Video Search**
- **Search YouTube** - Find videos by query
- **Video details** - Title, description, thumbnails
- **Channel info** - Channel names and metadata
- **Thumbnail URLs** - For preview images

## 📊 **API QUOTA & LIMITS**

### **YouTube Data API v3 Quota:**
- **Daily quota**: 10,000 units (free tier)
- **Video details**: 1 unit per request
- **Caption retrieval**: 100 units per request
- **Search**: 100 units per request
- **Recommended usage**: ~100 videos per day

### **Cost Management:**
- **Monitor quota** in Google Cloud Console
- **Enable billing alerts** if needed
- **Use caching** to reduce API calls
- **Implement rate limiting** for high usage

## 🛠️ **TECHNICAL DETAILS**

### **API Endpoints:**

#### **POST /youtube/summarize**
```json
{
    "url": "https://www.youtube.com/watch?v=VIDEO_ID"
}
```

**Response:**
```json
{
    "response": "Video summary here...",
    "video_id": "VIDEO_ID",
    "video_title": "Video Title",
    "transcript_length": 5000,
    "note": "Summary generated from video metadata (no captions available)"
}
```

#### **POST /youtube/search**
```json
{
    "query": "machine learning",
    "max_results": 5
}
```

**Response:**
```json
{
    "videos": [
        {
            "video_id": "VIDEO_ID",
            "title": "Video Title",
            "description": "Video description...",
            "channel_title": "Channel Name",
            "thumbnail_url": "https://img.youtube.com/vi/VIDEO_ID/mqdefault.jpg"
        }
    ],
    "total_results": 5
}
```

### **Error Handling:**
- **Invalid URLs** - Clear error messages
- **Private videos** - Appropriate responses
- **No captions** - Metadata-based summaries
- **API quota exceeded** - User-friendly messages

## 🔄 **MIGRATION FROM OLD SYSTEM**

### **What Changed:**
- **Old**: YouTube Transcript API (scraping)
- **New**: YouTube Data API v3 (official)

### **Benefits:**
- ✅ **More reliable** - Official API
- ✅ **Better metadata** - Rich video information
- ✅ **Search capability** - Find videos
- ✅ **Proper rate limits** - No more 403 errors
- ✅ **Fallback options** - Metadata summaries

### **Migration Steps:**
1. **Get API key** (steps above)
2. **Add environment variable** to Railway
3. **Deploy updated backend**
4. **Test functionality**

## 🚨 **IMPORTANT NOTES**

### **API Key Security:**
- **Never expose** API key in frontend code
- **Use environment variables** only
- **Regenerate key** if compromised

### **Rate Limiting:**
- **Implement caching** for popular videos
- **Monitor usage** in Google Cloud Console
- **Handle quota exceeded** gracefully

### **Video Availability:**
- **Public videos only** - Private videos won't work
- **Caption availability** - Not all videos have captions
- **Geographic restrictions** - Some videos may be region-locked

## 🎯 **NEXT STEPS**

1. **Get YouTube API Key** from Google Cloud Console
2. **Add YOUTUBE_API_KEY** to Railway environment
3. **Deploy updated backend** with new service
4. **Test YouTube summarization** with your video
5. **Test video search** functionality

## 📞 **SUPPORT**

If you encounter issues:
1. **Check API key** is correctly set
2. **Verify API quota** in Google Cloud Console
3. **Check video availability** (public, not private)
4. **Review Railway logs** for detailed errors

**The YouTube Data API v3 integration provides much more reliable and feature-rich YouTube video processing! 🚀**
