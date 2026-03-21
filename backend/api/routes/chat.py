from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import get_db
from api.dependencies import get_current_user
from db.crud import create_chat, get_chat_history, increment_usage
from services.llm_service import ask_llm
from services.rag_service import retrieve_context
from schemas.chat_schema import ChatRequest, ChatResponse, ChatHistoryResponse
from core.logger import logger
from db.models import User

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
        # Retrieve relevant context
        context = retrieve_context(chat_request.message, user_id=current_user.id)
        
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
        
        Provide a helpful and accurate response based on the available information.
        """
        
        # Get response from LLM
        response = ask_llm(prompt)
        
        # Save chat to database
        create_chat(db, current_user.id, chat_request.message, response)
        
        # Increment usage
        increment_usage(db, current_user.id)
        
        logger.info(f"Chat completed for user {current_user.id}")
        
        return ChatResponse(
            response=response,
            context_used=bool(context)
        )
        
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process chat request"
        )

@router.get("/history", response_model=list[ChatHistoryResponse])
async def get_history(
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get chat history for the current user
    """
    try:
        history = get_chat_history(db, current_user.id, limit)
        return history
    except Exception as e:
        logger.error(f"History retrieval error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve chat history"
        )
