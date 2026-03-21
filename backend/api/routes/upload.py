import os
import uuid
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from core.database import get_db
from api.dependencies import get_current_user
from db.crud import create_document
from services.rag_service import process_document_chunks
from services.pinecone_service import delete_embeddings
from PyPDF2 import PdfReader
from core.logger import logger
from db.models import User
import tempfile

router = APIRouter(prefix="/upload", tags=["upload"])

def extract_text_from_pdf(file_path: str) -> list[str]:
    """
    Extract text chunks from PDF file
    """
    try:
        with open(file_path, 'rb') as file:
            reader = PdfReader(file)
            text = ""
            
            for page in reader.pages:
                text += page.extract_text() + "\n"
            
            # Split text into chunks
            chunks = []
            chunk_size = 1000  # characters per chunk
            overlap = 200     # characters overlap
            
            for i in range(0, len(text), chunk_size - overlap):
                chunk = text[i:i + chunk_size]
                if chunk.strip():
                    chunks.append(chunk.strip())
            
            return chunks
            
    except Exception as e:
        logger.error(f"PDF processing error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to process PDF file"
        )

@router.post("/pdf")
async def upload_pdf(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Upload and process PDF file
    """
    try:
        # Validate file type
        if not file.filename.endswith('.pdf'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only PDF files are allowed"
            )
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_file_path = tmp_file.name
        
        try:
            # Extract text chunks
            chunks = extract_text_from_pdf(tmp_file_path)
            
            if not chunks:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No text could be extracted from the PDF"
                )
            
            # Generate document ID
            document_id = str(uuid.uuid4())
            
            # Process chunks and store in vector database
            success = process_document_chunks(chunks, document_id, current_user.id)
            
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to process document"
                )
            
            # Save document record
            document = create_document(db, current_user.id, file.filename, document_id)
            
            logger.info(f"PDF uploaded successfully: {file.filename} for user {current_user.id}")
            
            return {
                "message": "PDF uploaded and processed successfully",
                "document_id": document_id,
                "filename": file.filename,
                "chunks_processed": len(chunks)
            }
            
        finally:
            # Clean up temporary file
            os.unlink(tmp_file_path)
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"PDF upload error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upload PDF"
        )

@router.delete("/{document_id}")
async def delete_document(
    document_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete document and its embeddings
    """
    try:
        from db.crud import delete_document, get_user_documents
        
        # Get user documents
        documents = get_user_documents(db, current_user.id)
        target_doc = None
        
        for doc in documents:
            if doc.pinecone_id == document_id:
                target_doc = doc
                break
        
        if not target_doc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found"
            )
        
        # Delete embeddings from Pinecone
        chunk_ids = [f"{document_id}_chunk_{i}" for i in range(1000)]  # Estimate
        delete_embeddings(chunk_ids)
        
        # Delete document record
        success = delete_document(db, target_doc.id, current_user.id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete document"
            )
        
        logger.info(f"Document deleted: {document_id} by user {current_user.id}")
        
        return {"message": "Document deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Document deletion error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete document"
        )
