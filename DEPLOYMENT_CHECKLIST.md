# 🚀 Railway Deployment Checklist

## ✅ Pre-Deployment Checks

### Backend
- [x] Added PyPDF2 dependency
- [x] Optimized embedding service with fallback
- [x] Added .dockerignore
- [x] Enhanced Dockerfile with health checks
- [x] Created railway.toml config
- [x] Fixed all import issues
- [x] Added memory-efficient batch processing
- [x] Added fallback hash embeddings

### Frontend  
- [x] Fixed CSS parsing issues (removed @apply)
- [x] Replaced custom CSS classes with inline Tailwind
- [x] Fixed useAuth.js parse error
- [x] Added package-lock.json
- [x] Updated Dockerfile for production
- [x] Created railway.toml config

### Environment Variables
- [ ] Set DATABASE_URL (from Railway PostgreSQL)
- [ ] Set SECRET_KEY (generate random 32+ chars)
- [ ] Set GROQ_API_KEY (from groq.com)
- [ ] Set PINECONE_API_KEY (from pinecone.io)
- [ ] Set PINECONE_ENVIRONMENT
- [ ] Set PINECONE_INDEX_NAME = "multimodal-ai"
- [ ] Set FRONTEND_URL (after frontend deployment)

## 🚨 Common Deployment Issues & Fixes

### Backend Issues
1. **Memory Issues**: Sentence-transformers downloads 500MB models
   - ✅ Fixed: Lazy loading + fallback embeddings
   - ✅ Fixed: Batch processing to prevent memory spikes

2. **Build Timeouts**: Large dependencies
   - ✅ Fixed: Optimized Dockerfile with caching
   - ✅ Fixed: .dockerignore to exclude unnecessary files

3. **Missing Dependencies**: PyPDF2 not in requirements
   - ✅ Fixed: Added PyPDF2==3.0.1

### Frontend Issues
1. **CSS Parse Errors**: @apply directives not supported
   - ✅ Fixed: Replaced with inline Tailwind classes

2. **Missing package-lock.json**: npm ci fails
   - ✅ Fixed: Generated and committed package-lock.json

3. **useAuth.js Parse Error**: Hidden characters
   - ✅ Fixed: Recreated file with clean syntax

## 📋 Deployment Steps

### 1. Deploy PostgreSQL
```bash
# On Railway dashboard
New Project → Database → PostgreSQL
# Copy DATABASE_URL
```

### 2. Deploy Backend
```bash
# On Railway dashboard
New Project → Connect GitHub
Root directory: backend
Set environment variables
Deploy
```

### 3. Deploy Frontend
```bash
# On Railway dashboard  
New Project → Connect GitHub
Root directory: frontend
Set VITE_API_URL to backend URL
Deploy
```

### 4. Update CORS
```bash
# In backend Railway variables
FRONTEND_URL=https://your-frontend.railway.app
Redeploy backend
```

## 🔍 Testing Checklist

### Health Checks
- [ ] Backend: `https://backend-url/health`
- [ ] Frontend: `https://frontend-url/`
- [ ] Database: Check connection status
- [ ] Embedding Model: Verify loading

### Functionality Tests
- [ ] User registration
- [ ] User login
- [ ] PDF upload
- [ ] Chat with document context
- [ ] YouTube summarization
- [ ] Error handling

### Performance Tests
- [ ] Cold start time < 30s
- [ ] Memory usage < 512MB
- [ ] Response time < 10s
- [ ] Error rate < 5%

## 🛠️ Troubleshooting

### Backend Fails to Start
1. Check environment variables
2. Verify DATABASE_URL format
3. Check Railway logs for errors
4. Ensure Pinecone index exists

### Frontend Build Fails
1. Check package-lock.json exists
2. Verify no syntax errors in JSX
3. Check Tailwind CSS configuration
4. Ensure all imports are correct

### Memory Issues
1. Monitor Railway resource usage
2. Check embedding model loading
3. Verify batch processing is working
4. Consider upgrading Railway plan if needed

## 📊 Railway Resource Requirements

### Backend (Free Tier)
- Memory: 512MB
- CPU: Shared
- Storage: 1GB
- Build Time: 10 minutes

### Frontend (Free Tier)  
- Memory: 512MB
- CPU: Shared
- Storage: 1GB
- Build Time: 5 minutes

## 🔄 Post-Deployment

1. **Monitor Logs**: Check Railway logs for errors
2. **Test Features**: Verify all functionality works
3. **Set Up Alerts**: Configure Railway alerts
4. **Scale if Needed**: Upgrade plans based on usage
5. **Backup Data**: Export database regularly

## 🎯 Success Metrics

- ✅ Health checks pass
- ✅ All features work
- ✅ No memory errors
- ✅ Fast response times
- ✅ Good user experience

---

**Ready for Production! 🚀**
