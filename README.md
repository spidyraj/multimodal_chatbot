# Multimodal AI System

A production-ready multimodal AI system with RAG (Retrieval-Augmented Generation), YouTube summarization, and chat capabilities.

## Features

- 🔐 **Authentication**: JWT-based user authentication with registration and login
- 💬 **AI Chat**: Conversational AI with context from uploaded documents
- 📄 **Document Upload**: PDF processing with vector storage for RAG
- 🎥 **YouTube Summarization**: AI-powered video transcript summarization
- 🗄️ **Persistent Storage**: PostgreSQL for users, chat history, and usage tracking
- 🔍 **Vector Search**: Pinecone integration for semantic document retrieval
- 🚀 **Production Ready**: Dockerized deployment with Railway support

## Architecture

### Backend (FastAPI)
- **Framework**: FastAPI with async support
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Vector DB**: Pinecone for document embeddings
- **LLM**: Groq API (Llama3-8b-8192)
- **Authentication**: JWT tokens with bcrypt password hashing
- **Embeddings**: SentenceTransformer (all-MiniLM-L6-v2)

### Frontend (React)
- **Framework**: React 18 with Vite
- **Routing**: React Router v6
- **Styling**: Tailwind CSS
- **Icons**: Heroicons
- **HTTP Client**: Axios with interceptors

## Quick Start

### Prerequisites
- Node.js 18+
- Python 3.10+
- PostgreSQL database
- Pinecone account
- Groq API key

### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your actual values
   ```

5. **Run the server**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your backend URL
   ```

4. **Run the development server**
   ```bash
   npm run dev
   ```

## Environment Variables

### Backend (.env)
```env
DATABASE_URL=postgresql://user:password@host:port/dbname
SECRET_KEY=your-secret-key-here
GROQ_API_KEY=your-groq-api-key
PINECONE_API_KEY=your-pinecone-api-key
PINECONE_ENVIRONMENT=your-pinecone-environment
PINECONE_INDEX_NAME=multimodal-ai
FRONTEND_URL=http://localhost:3000
```

### Frontend (.env)
```env
VITE_API_URL=http://localhost:8000
```

## Railway Deployment

### Backend Deployment

1. **Create new Railway project**
2. **Connect GitHub repository**
3. **Set environment variables in Railway dashboard**
4. **Add PostgreSQL database**
5. **Deploy**

### Frontend Deployment

1. **Create new Railway project for frontend**
2. **Connect same repository**
3. **Set root directory to `frontend`**
4. **Set build command: `npm run build`**
5. **Set start command: `npm run preview`**
6. **Set environment variables**
7. **Deploy**

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - User login
- `GET /auth/me` - Get current user info

### Chat
- `POST /chat/` - Send message to AI
- `GET /chat/history` - Get chat history

### Upload
- `POST /upload/pdf` - Upload PDF document
- `DELETE /upload/{document_id}` - Delete document

### YouTube
- `POST /youtube/summarize` - Summarize YouTube video

### Health
- `GET /health` - Health check endpoint

## Usage

1. **Register an account** or login with existing credentials
2. **Upload PDF documents** to enhance chat with context
3. **Chat with AI** using your uploaded documents as knowledge base
4. **Summarize YouTube videos** by pasting video URLs
5. **View chat history** and manage your documents

## Development

### Adding New Features

1. **Backend**: Add new routes in `api/routes/`
2. **Services**: Implement business logic in `services/`
3. **Frontend**: Create components in `src/components/`
4. **Pages**: Add new pages in `src/pages/`

### Database Migrations

For production deployments, consider adding Alembic for database migrations:

```bash
pip install alembic
alembic init alembic
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

## Security Considerations

- JWT tokens expire after 24 hours
- Passwords are hashed with bcrypt
- CORS is configured for specific origins
- Input validation with Pydantic schemas
- SQL injection prevention with SQLAlchemy ORM

## Performance Optimizations

- Connection pooling for database
- Lightweight embedding model for Railway compatibility
- Async FastAPI endpoints
- Request/response caching (can be added)

## Monitoring

- Health check endpoint for monitoring
- Structured logging with timestamps
- Error tracking and reporting
- Usage metrics tracking

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.
