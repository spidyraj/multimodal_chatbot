# 🤖 MultiModal AI Chatbot - Multilingual & RAG-Powered

A high-performance, production-ready Multimodal AI system that combines Retrieval-Augmented Generation (RAG), Optical Character Recognition (OCR), and Text-to-Speech (TTS) capabilities. This chatbot can process documents, images, and text while providing a seamless multilingual experience.

🚀 **Live Demo:** [https://multimodal-chatbot-multiluinguial.vercel.app/](https://multimodal-chatbot-multiluinguial.vercel.app/)

---

## ✨ Features

- 🔐 **Secure Authentication**: JWT-based user system with robust registration and login flows.
- 💬 **Intelligent Chat**: Conversational AI powered by Groq's high-speed LLMs.
- 📄 **Advanced Document RAG**: Upload PDFs and documents to create a private knowledge base.
- 🖼️ **Image Recognition (OCR)**: Extract and query information from images using Tesseract OCR.
- 🔊 **Voice Synthesis (TTS)**: Convert AI responses into natural-sounding speech in 10+ languages.
- 🌍 **Multilingual Support**: Communicate and generate audio in English, Hindi, Spanish, French, and more.
- 🔍 **Semantic Search**: Powered by Pinecone vector database for highly relevant context retrieval.
- 🚫 **No YouTube Summarization**: Focuses purely on document, image, and text-based multimodal interactions.

---

## 🛠️ Tech Stack

### Frontend
- **Framework**: [React 18](https://reactjs.org/) with **Vite** for blazing fast development.
- **Styling**: **Tailwind CSS** for a modern, responsive UI.
- **Animations**: **Framer Motion** for smooth, premium transitions.
- **Icons**: **Heroicons** for clean, consistent iconography.
- **State Management**: React Hooks and Context API.
- **API Client**: **Axios** with centralized interceptors for auth management.

### Backend
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) (Python) for high-performance asynchronous API handling.
- **Database**: **PostgreSQL** with **SQLAlchemy ORM** for persistent data (Users, Chats).
- **Vector Store**: **Pinecone** for efficient semantic similarity search.
- **LLM Engine**: **Groq API** (utilizing Llama 3.1 & Gemma 2 models) for near-instant responses.
- **OCR Engine**: **Tesseract OCR** for processing text within images.
- **TTS Engine**: **gTTS (Google Text-to-Speech)** for multilingual audio generation.
- **Document Processing**: **PyPDF2** and **Pillow**.

---

## 🏗️ System Architecture

### 📄 Document & Image Processing (RAG)
The system uses a sophisticated RAG pipeline to allow the LLM to "read" your uploaded files.

```mermaid
graph TD
    subgraph "Ingestion Phase"
    A[User Uploads File] --> B{File Type?}
    B -- PDF --> C[PyPDF2 Extraction]
    B -- Image/OCR --> D[Tesseract OCR]
    B -- Text/MD --> E[Direct Read]
    C --> F[Text Chunking]
    D --> F
    E --> F
    F --> G[Embedding Service]
    G --> H[(Pinecone Vector DB)]
    end

    subgraph "Query Phase"
    I[User Message] --> J[Generate Query Embedding]
    J --> K[Vector Similarity Search]
    K --> L[Retrieve Top-K Context]
    L --> M[Augment Prompt with Context]
    M --> N[Groq LLM Execution]
    N --> O[Final AI Response]
    end
```

### 🔊 Audio Architecture (TTS)
Seamlessly convert text responses into high-quality audio streams.

```mermaid
graph TD
    A[AI Response Text] --> B[Audio Service]
    B --> C{Language Detection}
    C --> D[gTTS Engine]
    D --> E[MP3 Byte Stream Generation]
    E --> F[FastAPI StreamingResponse]
    F --> G[Frontend Audio Component]
    G --> H[User Playback]
```

---

## 🚀 Getting Started

### Prerequisites
- Node.js 18+
- Python 3.10+
- Tesseract OCR installed on your system
- PostgreSQL Database
- API Keys: Groq, Pinecone

### Quick Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/multimodal-chatbot.git
   cd multimodal-chatbot
   ```

2. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env # Add your API keys
   uvicorn main:app --reload
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   cp .env.example .env # Update VITE_API_URL
   npm run dev
   ```

---

## ⚙️ Environment Configuration

### Backend (.env)
Required keys for the backend to function:
```env
DATABASE_URL=postgresql://user:password@host:port/dbname
SECRET_KEY=your-secret-key-here
GROQ_API_KEY=your-groq-api-key
PINECONE_API_KEY=your-pinecone-api-key
PINECONE_ENVIRONMENT=your-pinecone-environment
PINECONE_INDEX_NAME=multimodal-ai
FRONTEND_URL=http://localhost:5173
```

### Frontend (.env)
```env
VITE_API_URL=http://localhost:8000
```

---

## 🧠 AI Models Used
- **Llama 3.1 (Groq)**: Primary model for complex reasoning and context-aware chatting.
- **Gemma 2 (Groq)**: Lightweight model for fast, simple interactions.
- **Tesseract OCR**: Specialized engine for visual text extraction from images.
- **Google TTS**: High-fidelity speech synthesis engine.

---

## 📡 API Reference

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/auth/register` | `POST` | Create a new user account |
| `/auth/login` | `POST` | Authenticate and receive JWT |
| `/chat/` | `POST` | Send a message (with RAG context) |
| `/chat/with-file` | `POST` | Chat while uploading a temporary file |
| `/upload/` | `POST` | Upload document to permanent vector store |
| `/audio/generate` | `POST` | Convert text to speech |
| `/health` | `GET` | System status check |

---

## 🛡️ Security & Performance
- **JWT Protection**: All chat and upload endpoints are protected by secure token-based auth.
- **Environment Isolation**: Secrets are managed via `.env` files and never committed.
- **Asynchronous Processing**: Fast responses even during heavy I/O operations.
- **Connection Pooling**: Optimized database connections for high concurrency.

---

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
