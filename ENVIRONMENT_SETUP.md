# 🚀 Environment Variables Setup Guide

## 📋 Required Environment Variables

### Backend (.env)

#### **🔴 CRITICAL - Must Set These**
```env
# Database (from Railway PostgreSQL)
DATABASE_URL=postgresql://username:password@host:port/database

# JWT Security (generate random 32+ character string)
SECRET_KEY=your-super-secret-key-min-32-characters-long-random-string

# Groq API Key (from https://groq.com/)
GROQ_API_KEY=gsk_your-groq-api-key-here

# Pinecone (from https://app.pinecone.io/)
PINECONE_API_KEY=your-pinecone-api-key
PINECONE_ENVIRONMENT=us-west1-gcp-free  # or your environment
PINECONE_INDEX_NAME=multimodal-ai
```

#### **🟡 Optional - Use Defaults**
```env
# JWT Settings (can use defaults)
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Frontend URL (update after deployment)
FRONTEND_URL=https://your-frontend.railway.app

# Performance (Railway optimization)
USE_HEAVY_EMBEDDINGS=false
EMBEDDING_MODEL=all-MiniLM-L6-v2
```

### Frontend (.env)

```env
# Backend URL (update after backend deployment)
VITE_API_URL=https://your-backend.railway.app
```

## 🔑 How to Get API Keys

### 1. Groq API Key
1. Go to [https://groq.com/](https://groq.com/)
2. Sign up / Login
3. Navigate to API Keys section
4. Click "Create API Key"
5. Copy the key (starts with `gsk_`)

### 2. Pinecone API Key
1. Go to [https://app.pinecone.io/](https://app.pinecone.io/)
2. Create account / Login
3. Create new project
4. Create index with settings:
   - **Name**: `multimodal-ai`
   - **Dimension**: `384`
   - **Metric**: `cosine`
   - **Pod Type**: `p1.x1` (free tier)
5. Copy API Key from project settings

### 3. Railway Database URL
1. In Railway dashboard, create PostgreSQL service
2. Click on the database service
3. Copy the "DATABASE_URL" from connection variables

### 4. Generate SECRET_KEY
```bash
# Method 1: Python
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Method 2: OpenSSL
openssl rand -base64 32

# Method 3: Online generator
# https://randomkeygen.com/
```

## 🚢 Railway Deployment Setup

### Step 1: Create PostgreSQL Database
```bash
# On Railway dashboard
New Project → Database → PostgreSQL
# Copy DATABASE_URL
```

### Step 2: Deploy Backend
```bash
# On Railway dashboard
New Project → Connect GitHub
Root directory: backend
Set environment variables:
- DATABASE_URL (from PostgreSQL)
- SECRET_KEY (generated)
- GROQ_API_KEY (from Groq)
- PINECONE_API_KEY (from Pinecone)
- PINECONE_ENVIRONMENT
- PINECONE_INDEX_NAME=multimodal-ai
Deploy
```

### Step 3: Deploy Frontend
```bash
# On Railway dashboard
New Project → Connect GitHub
Root directory: frontend
Set environment variables:
- VITE_API_URL=https://your-backend-url.railway.app
Deploy
```

### Step 4: Update CORS
```bash
# In backend Railway variables
FRONTEND_URL=https://your-frontend-url.railway.app
Redeploy backend
```

## ⚠️ Common Issues & Fixes

### Issue 1: Database Connection Error
```env
# Railway gives postgres:// but SQLAlchemy needs postgresql://
DATABASE_URL=postgresql://user:pass@host:port/db  # NOT postgres://
```

### Issue 2: Pinecone Index Not Found
```bash
# Create index in Pinecone dashboard first
# Name must match PINECONE_INDEX_NAME exactly
# Dimension must be 384 (for MiniLM)
```

### Issue 3: CORS Error
```env
# Make sure FRONTEND_URL matches deployed frontend URL exactly
FRONTEND_URL=https://your-app.railway.app
```

### Issue 4: Memory Issues on Railway
```env
# Use lightweight embeddings
USE_HEAVY_EMBEDDINGS=false
# This uses hash-based embeddings instead of sentence-transformers
```

## 🧪 Testing Configuration

### Test Backend Health
```bash
curl https://your-backend.railway.app/health
```

Expected response:
```json
{
  "status": "healthy",
  "database": "connected",
  "embedding_model": {
    "model_loaded": false,
    "model_type": "hash-fallback"
  }
}
```

### Test Frontend
```bash
curl https://your-frontend.railway.app/health
```

Expected response:
```
healthy
```

## 🔍 Environment Variable Validation

### Backend Required Variables Check
```python
# In Python shell
import os
required_vars = [
    'DATABASE_URL',
    'SECRET_KEY', 
    'GROQ_API_KEY',
    'PINECONE_API_KEY',
    'PINECONE_ENVIRONMENT',
    'PINECONE_INDEX_NAME'
]

missing = [var for var in required_vars if not os.getenv(var)]
if missing:
    print(f"Missing: {missing}")
else:
    print("All required variables set!")
```

## 📊 Railway Resource Requirements

### Backend (Free Tier)
- **Memory**: 512MB ✅ (with lightweight embeddings)
- **CPU**: Shared ✅
- **Storage**: 1GB ✅
- **Build Time**: ~3-5 minutes ✅

### Frontend (Free Tier)
- **Memory**: 512MB ✅
- **CPU**: Shared ✅
- **Storage**: 1GB ✅
- **Build Time**: ~30 seconds ✅

## 🎯 Production Checklist

- [ ] DATABASE_URL set correctly
- [ ] SECRET_KEY is random and secure
- [ ] GROQ_API_KEY is valid
- [ ] Pinecone index exists
- [ ] PINECONE_API_KEY works
- [ ] FRONTEND_URL matches deployed frontend
- [ ] Backend health check passes
- [ ] Frontend health check passes
- [ ] CORS is configured
- [ ] All API keys are working

---

**Ready for Production! 🚀**
