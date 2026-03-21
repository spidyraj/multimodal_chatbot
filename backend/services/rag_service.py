from typing import List, Optional
from services.embedding_service import embed_single_text
from services.pinecone_service import query_embeddings
from core.logger import logger

def retrieve_context(query: str, user_id: Optional[int] = None, top_k: int = 3) -> str:
    """
    Retrieve relevant context for a query using RAG
    """
    try:
        # Generate embedding for the query
        query_embedding = embed_single_text(query)
        if not query_embedding:
            logger.warning("Failed to generate query embedding")
            return ""
        
        # Build filter for user-specific documents
        filter_dict = None
        if user_id is not None:
            filter_dict = {"user_id": user_id}
        
        # Query Pinecone for relevant documents
        results = query_embeddings(query_embedding, top_k=top_k, filter_dict=filter_dict)
        
        if not results.get("matches"):
            logger.info("No relevant context found")
            return ""
        
        # Extract and format context
        context_parts = []
        for match in results["matches"]:
            if match.get("score", 0) > 0.5:  # Relevance threshold
                metadata = match.get("metadata", {})
                text = metadata.get("text", "")
                if text:
                    # Truncate very long text
                    if len(text) > 500:
                        text = text[:500] + "..."
                    context_parts.append(text)
        
        context = "\n\n".join(context_parts)
        logger.info(f"Retrieved context with {len(context_parts)} parts")
        
        return context
        
    except Exception as e:
        logger.error(f"RAG retrieval error: {str(e)}")
        return ""

def process_document_chunks(chunks: List[str], document_id: str, user_id: int) -> bool:
    """
    Process document chunks and store in vector database
    """
    try:
        from services.embedding_service import embed_texts
        from services.pinecone_service import store_embeddings
        
        # Generate embeddings for all chunks
        embeddings = embed_texts(chunks)
        
        # Prepare vectors for Pinecone
        vectors = []
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            vectors.append({
                "id": f"{document_id}_chunk_{i}",
                "values": embedding,
                "metadata": {
                    "text": chunk,
                    "document_id": document_id,
                    "user_id": user_id,
                    "chunk_index": i
                }
            })
        
        # Store in Pinecone
        success = store_embeddings(vectors)
        return success
        
    except Exception as e:
        logger.error(f"Document processing error: {str(e)}")
        return False
