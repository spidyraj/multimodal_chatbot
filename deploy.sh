#!/bin/bash

# Multimodal AI Deployment Script
# This script helps deploy the application to Railway

echo "🚀 Multimodal AI Deployment Script"
echo "=================================="

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI is not installed. Installing..."
    npm install -g @railway/cli
fi

# Login to Railway
echo "🔐 Logging into Railway..."
railway login

# Deploy Backend
echo "📦 Deploying Backend..."
cd backend
railway init
railway up
railway add postgresql
railway variables set DATABASE_URL=$(railway variables get DATABASE_URL)
railway variables set SECRET_KEY="your-secret-key-change-this"
railway variables set GROQ_API_KEY="your-groq-api-key"
railway variables set PINECONE_API_KEY="your-pinecone-api-key"
railway variables set PINECONE_ENVIRONMENT="your-pinecone-environment"
railway variables set PINECONE_INDEX_NAME="multimodal-ai"
railway variables set FRONTEND_URL="https://your-frontend-url.railway.app"
railway deploy
BACKEND_URL=$(railway domain)
cd ..

# Deploy Frontend
echo "🎨 Deploying Frontend..."
cd frontend
railway init
railway up
railway variables set VITE_API_URL=$BACKEND_URL
railway deploy
FRONTEND_URL=$(railway domain)
cd ..

# Update Backend CORS with Frontend URL
echo "🔧 Updating Backend CORS..."
cd backend
railway variables set FRONTEND_URL=$FRONTEND_URL
railway deploy
cd ..

echo "✅ Deployment Complete!"
echo "🌐 Frontend URL: $FRONTEND_URL"
echo "🔌 Backend URL: $BACKEND_URL"
echo ""
echo "📝 Next Steps:"
echo "1. Update your Railway variables with actual API keys"
echo "2. Test the application by visiting the frontend URL"
echo "3. Set up your Pinecone index if not already done"
echo "4. Configure your Groq API key"
echo ""
echo "🎉 Your Multimodal AI system is now live!"
