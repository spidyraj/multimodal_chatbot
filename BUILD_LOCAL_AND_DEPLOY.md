# 🐳 Build Locally & Deploy to Railway

## 🎯 Why Build Locally?
- ✅ Avoid Railway's 4GB image size limit
- ✅ Test everything before deployment
- ✅ Faster deployment (just pull image)
- ✅ Better debugging and control

## 📋 Step-by-Step Process

### Step 1: Build Docker Image Locally
```bash
# Navigate to backend directory
cd backend

# Build using simple Dockerfile
docker build -f Dockerfile.simple -t multimodal-backend .

# Check image size
docker images multimodal-backend
```

### Step 2: Test Locally
```bash
# Run container locally
docker run -p 8080:8080 \
  -e DATABASE_URL="postgresql://test:test@localhost:5432/test" \
  -e SECRET_KEY="test-secret-key-32-chars-long" \
  -e GROQ_API_KEY="your-groq-key" \
  -e PINECONE_API_KEY="your-pinecone-key" \
  -e PINECONE_ENVIRONMENT="us-west1-gcp-free" \
  -e PINECONE_INDEX_NAME="multimodal-ai" \
  -e USE_LIGHTWEIGHT_EMBEDDINGS=true \
  multimodal-backend

# Test health endpoint
curl http://localhost:8080/health
```

### Step 3: Push to Registry

#### Option A: Docker Hub (Free)
```bash
# Tag for Docker Hub
docker tag multimodal-backend yourusername/multimodal-backend:latest

# Push to Docker Hub
docker push yourusername/multimodal-backend:latest
```

#### Option B: Railway Registry (Recommended)
```bash
# Login to Railway registry
docker login production-us-west2.railway-registry.com

# Tag for Railway
docker tag multimodal-backend production-us-west2.railway-registry.com/your-project/backend:latest

# Push to Railway
docker push production-us-west2.railway-registry.com/your-project/backend:latest
```

### Step 4: Deploy on Railway

#### Method A: Use Railway Image (Recommended)
1. In Railway project settings
2. Set "Image" instead of "GitHub"
3. Enter: `yourusername/multimodal-backend:latest`
4. Set environment variables
5. Deploy

#### Method B: Update Railway.toml
```toml
[build]
# Remove build section, use image instead

[[services]]
image = "yourusername/multimodal-backend:latest"
```

## 🔧 Alternative: Use Railway's Dockerfile

If you prefer Railway to build, use this optimized approach:

### Railway-Optimized Dockerfile
```dockerfile
# Ultra-compact for Railway
FROM python:3.10-slim

WORKDIR /app

# Minimal system deps
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy and install
COPY requirements-minimal.txt .
RUN pip install --no-cache-dir -r requirements-minimal.txt

# Copy app
COPY . .

# Environment
ENV USE_LIGHTWEIGHT_EMBEDDINGS=true

# User and run
RUN useradd app && chown -R app:app /app
USER app
EXPOSE 8080

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```

## 📊 Size Comparison

| Method | Image Size | Build Time | Railway Limits |
|--------|------------|------------|---------------|
| Local Build | ~1.5GB | 2-3 min | No limits ✅ |
| Railway Build | ~1.5GB | 2-3 min | 4GB limit ⚠️ |
| Original Build | 8.1GB | 10-15 min | Exceeds limit ❌ |

## 🎯 Recommended Approach

### For Development:
```bash
# Build and test locally
docker build -f Dockerfile.simple -t multimodal-backend .
docker run -p 8080:8080 multimodal-backend
```

### For Production:
```bash
# Build, test, then push
docker build -f Dockerfile.simple -t multimodal-backend .
# Test locally...
docker push yourusername/multimodal-backend:latest
```

### Railway Deployment:
- Use pre-built image from registry
- Set environment variables
- Deploy (no build needed)

## 🚀 Quick Start Commands

```bash
# 1. Build locally
cd backend
docker build -f Dockerfile.simple -t multimodal-backend .

# 2. Test locally
docker run -p 8080:8080 -e USE_LIGHTWEIGHT_EMBEDDINGS=true multimodal-backend

# 3. Push to registry
docker tag multimodal-backend yourusername/multimodal-backend:latest
docker push yourusername/multimodal-backend:latest

# 4. Deploy on Railway using image
# Set environment variables and deploy!
```

## ✅ Benefits of This Approach

- **No size limits** (Railway's 4GB limit bypassed)
- **Faster deployment** (no build time)
- **Local testing** (catch issues early)
- **Consistent environment** (same image everywhere)
- **Better debugging** (full control over build)

## 🔄 If You Still Want Railway Build

Use the `Dockerfile.simple` with these settings:
- Railway Dockerfile path: `Dockerfile.simple`
- Environment: `USE_LIGHTWEIGHT_EMBEDDINGS=true`
- Should build successfully under 4GB

---

**Recommendation**: Build locally first, test, then push to registry for Railway deployment! 🚀
