from sqlalchemy.orm import Session
from db.models import User, Chat, Usage, Document
from core.security import get_password_hash, verify_password
from typing import Optional, List

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, email: str, password: str) -> User:
    hashed_password = get_password_hash(password)
    db_user = User(email=email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Create usage record
    usage = Usage(user_id=db_user.id, request_count=0)
    db.add(usage)
    db.commit()
    
    return db_user

def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def create_chat(db: Session, user_id: int, question: str, answer: str) -> Chat:
    db_chat = Chat(user_id=user_id, question=question, answer=answer)
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat

def get_chat_history(db: Session, user_id: int, limit: int = 10) -> List[Chat]:
    return (
        db.query(Chat)
        .filter(Chat.user_id == user_id)
        .order_by(Chat.created_at.desc())
        .limit(limit)
        .all()
    )

def increment_usage(db: Session, user_id: int) -> Usage:
    usage = db.query(Usage).filter(Usage.user_id == user_id).first()
    if usage:
        usage.request_count += 1
        db.commit()
        db.refresh(usage)
    return usage

def get_usage(db: Session, user_id: int) -> Optional[Usage]:
    return db.query(Usage).filter(Usage.user_id == user_id).first()

def create_document(db: Session, user_id: int, filename: str, pinecone_id: str) -> Document:
    db_doc = Document(user_id=user_id, filename=filename, pinecone_id=pinecone_id)
    db.add(db_doc)
    db.commit()
    db.refresh(db_doc)
    return db_doc

def get_user_documents(db: Session, user_id: int) -> List[Document]:
    return db.query(Document).filter(Document.user_id == user_id).all()

def delete_document(db: Session, document_id: int, user_id: int) -> bool:
    doc = db.query(Document).filter(Document.id == document_id, Document.user_id == user_id).first()
    if doc:
        db.delete(doc)
        db.commit()
        return True
    return False
