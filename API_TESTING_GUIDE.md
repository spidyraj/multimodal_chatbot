# API Testing Guide for Multimodal AI Backend

## Base URL
```
https://multimodal-backend-production.up.railway.app
```

## Authentication Flow

### 1. Register User
**POST** `/auth/register`
```json
{
    "username": "testuser123",
    "email": "test@example.com",
    "password": "testpassword123"
}
```

**Expected Response (200):**
```json
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "token_type": "bearer"
}
```

### 2. Login User
**POST** `/auth/login`
```json
{
    "email": "test@example.com",
    "password": "testpassword123"
}
```

**Expected Response (200):**
```json
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "token_type": "bearer"
}
```

### 3. Get Current User
**GET** `/auth/me`
**Headers:** `Authorization: Bearer <token>`

**Expected Response (200):**
```json
{
    "id": 1,
    "username": "testuser123",
    "email": "test@example.com",
    "created_at": "2026-03-22T20:17:20.000000Z"
}
```

## Main API Endpoints

### 4. Chat History
**GET** `/chat/history?limit=10`
**Headers:** `Authorization: Bearer <token>`

**Expected Response (200):**
```json
[]
```

### 5. Send Chat Message
**POST** `/chat/`
**Headers:** `Authorization: Bearer <token>`
```json
{
    "message": "Hello, how are you?"
}
```

**Expected Response (200):**
```json
{
    "response": "Hello! I'm doing well, thank you for asking. How can I help you today?",
    "message_id": 1
}
```

### 6. Chat with File Upload
**POST** `/chat/with-file`
**Headers:** 
- `Authorization: Bearer <token>`
- `Content-Type: multipart/form-data`

**Form Data:**
- `message`: "Please analyze this document"
- `file`: [PDF file]

**Expected Response (200):**
```json
{
    "response": "I've analyzed the document. Here's what I found...",
    "message_id": 2
}
```

### 7. YouTube Summarizer
**POST** `/youtube/summarize`
**Headers:** `Authorization: Bearer <token>`
```json
{
    "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
}
```

**Expected Response (200):**
```json
{
    "summary": "This video is about...",
    "video_title": "Video Title",
    "video_id": "dQw4w9WgXcQ"
}
```

### 8. Upload PDF
**POST** `/upload/pdf`
**Headers:** 
- `Authorization: Bearer <token>`
- `Content-Type: multipart/form-data`

**Form Data:**
- `file`: [PDF file]

**Expected Response (200):**
```json
{
    "id": "doc_123",
    "filename": "document.pdf",
    "uploaded_at": "2026-03-22T20:17:20.000000Z"
}
```

## Health Check

### 9. Health Check
**GET** `/health`

**Expected Response (200):**
```json
{
    "status": "healthy",
    "timestamp": "2026-03-22T20:17:20.000000Z"
}
```

## Error Responses

### 401 Unauthorized
```json
{
    "detail": "Could not validate credentials"
}
```

### 500 Internal Server Error
```json
{
    "detail": "Internal server error occurred"
}
```

## Testing Steps

1. **Test Health Check** - Verify backend is running
2. **Register User** - Create test account
3. **Login** - Get authentication token
4. **Test Auth** - Verify `/auth/me` works
5. **Test Chat** - Send a message
6. **Test File Upload** - Upload a PDF
7. **Test YouTube** - Summarize a video

## Common Issues

- **CORS errors** - Make sure you're hitting the right URL
- **Token expiration** - Tokens last 24 hours
- **File size limits** - Keep test files small
- **YouTube captions** - Only works with videos that have captions

## Postman Collection

You can import these endpoints as a Postman collection for easier testing.
