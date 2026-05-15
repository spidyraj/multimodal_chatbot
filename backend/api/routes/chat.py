from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from core.database import get_db
from api.dependencies import get_current_user
from services.llm_service import ask_llm
from services.rag_service import retrieve_context
from services.upload_service import process_uploaded_file
from db.crud import create_chat, get_chat_history, increment_usage
from schemas.chat_schema import ChatRequest, ChatResponse, ChatHistoryResponse
from core.logger import logger
from db.models import User
import tempfile
import os

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/", response_model=ChatResponse)
async def chat(
    chat_request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Chat endpoint with RAG support
    """
    try:
        # Retrieve relevant context from documents
        doc_context = retrieve_context(chat_request.message, user_id=current_user.id)
        
        # Combine all context (no file context for regular chat)
        context = ""
        if doc_context:
            context += f"Document Context:\n{doc_context}\n\n"
            
        # Build prompt with context and chat history
        history = get_chat_history(db, current_user.id, limit=3)
        history_text = ""
        
        if history:
            history_text = "\n".join([
                f"Q: {chat.question}\nA: {chat.answer}" 
                for chat in reversed(history)
            ])
            
        prompt = f"""
        You are a helpful AI assistant. Use the provided context and conversation history to answer the user's question.
        
        Previous conversation:
        {history_text}
        
        Context information:
        {context if context else "No specific context available."}
        
        Current question:
        {chat_request.message}
        
        Please provide a helpful and accurate answer based on context and history.
        """
        
        # Get LLM response
        response = ask_llm(prompt)
        
        # Save chat to database
        create_chat(db, current_user.id, chat_request.message, response)
        increment_usage(db, current_user.id)
        
        logger.info(f"Chat response generated for user {current_user.id}")
        
        return ChatResponse(response=response)
        
    except Exception as e:
        logger.error(f"Chat endpoint error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process chat message"
        )

@router.post("/with-file", response_model=ChatResponse)
async def chat_with_file(
    message: str,
    file: UploadFile = File(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Chat endpoint with file upload support
    """
    try:
        # Process uploaded file if provided
        file_context = ""
        if file:
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                content = await file.read()
                tmp_file.write(content)
                tmp_file_path = tmp_file.name
            
            try:
                # Process the file
                file_context = process_uploaded_file(tmp_file_path, file.filename, current_user.id)
                logger.info(f"File processed: {file.filename} for user {current_user.id}")
            finally:
                # Clean up temporary file
                os.unlink(tmp_file_path)
        
        # Retrieve relevant context from documents
        doc_context = retrieve_context(message, user_id=current_user.id)
        
        # Combine all context
        context = ""
        if file_context:
            context += f"Document Context:\n{file_context}\n\n"
        if doc_context:
            context += f"General Context:\n{doc_context}\n\n"
            
        # Build prompt with context and chat history
        history = get_chat_history(db, current_user.id, limit=3)
        history_text = ""
        
        if history:
            history_text = "\n".join([
                f"Q: {chat.question}\nA: {chat.answer}" 
                for chat in reversed(history)
            ])
            
        prompt = f"""
        You are a helpful AI assistant. Use the provided context and conversation history to answer the user's question.
        
        Previous conversation:
        {history_text}
        
        Context information:
        {context if context else "No specific context available."}
        
        Current question:
        {message}
        
        Please provide a helpful and accurate answer based on context and history.
        """
        
        # Get LLM response
        response = ask_llm(prompt)
        
        # Save chat to database
        create_chat(db, current_user.id, message, response)
        increment_usage(db, current_user.id)
        
        logger.info(f"Chat response with file generated for user {current_user.id}")
        
        # Fix context_used to match expected schema if needed. Assuming context_used exists in ChatResponse or not strictly validated.
        return ChatResponse(response=response)
         
    except Exception as e:
        logger.error(f"File chat endpoint error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process chat message with file"
        )

@router.get("/history", response_model=list[ChatHistoryResponse])
async def get_history(
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get chat history for the current user with error handling
    """
    try:
        logger.info(f"Retrieving chat history for user {current_user.id}")
        
        # Use robust chat service
        history = chat_service.get_chat_history_safe(
            user_id=current_user.id,
            db=db,
            limit=limit
        )
        
        logger.info(f"Retrieved {len(history)} chat messages for user {current_user.id}")
        
        return history
        
    except Exception as e:
        logger.error(f"History retrieval error: {str(e)}")
        # Return empty history instead of error
        return []

@router.get("/health")
async def chat_health_check(
    current_user: User = Depends(get_current_user)
):
    """
    Check health of chat services
    """
    try:
        health = chat_service.health_check()
        return {
            "status": "healthy" if health["llm_service"] == "healthy" else "degraded",
            "services": health,
            "user_id": current_user.id
        }
    except Exception as e:
        logger.error(f"Health check error: {str(e)}")
        return {
            "status": "unhealthy",
            "error": str(e)
        }
