from typing import List
import numpy as np
from core.logger import logger
import os
import time
from services.lightweight_embeddings import embed_texts_lightweight, embed_single_text_lightweight

# Initialize model (lightweight for Railway compatibility)
model = None
model_load_time = None

def get_embedding_model():
    """Lazy load embedding model with timeout and retry logic"""
    global model, model_load_time
    
    if model is not None:
        return model
    
    # Check if we should use lightweight embeddings
    if os.getenv("USE_LIGHTWEIGHT_EMBEDDINGS", "true").lower() == "true":
        logger.info("Using lightweight embeddings (hash-based)")
        return None
    
    # Try to import sentence-transformers only when needed
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError:
        logger.warning("sentence-transformers not available, using lightweight embeddings")
        return None
    
    start_time = time.time()
    
    try:
        logger.info("Loading embedding model (this may take a moment on first run)...")
        
        # Use a smaller model for Railway to reduce memory usage
        model_name = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
        
        model = SentenceTransformer(model_name, device="cpu")
        model_load_time = time.time() - start_time
        
        logger.info(f"Embedding model loaded successfully in {model_load_time:.2f}s")
        return model
        
    except Exception as e:
        logger.error(f"Failed to load embedding model: {str(e)}")
        
        # Fallback to a very simple approach if model fails to load
        logger.warning("Using fallback embedding method")
        return None

def embed_texts(texts: List[str]) -> List[List[float]]:
    """
    Convert texts to embeddings with fallback
    """
    # Use lightweight embeddings if enabled or model fails to load
    if os.getenv("USE_LIGHTWEIGHT_EMBEDDINGS", "true").lower() == "true":
        logger.info("Using lightweight hash embeddings")
        return embed_texts_lightweight(texts)
    
    try:
        model = get_embedding_model()
        
        if model is None:
            # Fallback: simple hash-based embeddings
            logger.warning("Using fallback hash-based embeddings")
            return embed_texts_lightweight(texts)
        
        # Process in batches to avoid memory issues
        batch_size = 8
        all_embeddings = []
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            embeddings = model.encode(batch, convert_to_tensor=False)
            all_embeddings.extend(embeddings.tolist())
            
            # Small delay to prevent overwhelming the system
            if i + batch_size < len(texts):
                time.sleep(0.1)
        
        return all_embeddings
        
    except Exception as e:
        logger.error(f"Embedding error: {str(e)}")
        # Return fallback embeddings
        return embed_texts_lightweight(texts)

def embed_single_text(text: str) -> List[float]:
    """
    Convert single text to embedding
    """
    # Use lightweight embeddings if enabled
    if os.getenv("USE_LIGHTWEIGHT_EMBEDDINGS", "true").lower() == "true":
        return embed_single_text_lightweight(text)
    
    try:
        embeddings = embed_texts([text])
        return embeddings[0] if embeddings else embed_single_text_lightweight(text)
    except Exception as e:
        logger.error(f"Single text embedding error: {str(e)}")
        return embed_single_text_lightweight(text)

def simple_hash_embedding(text: str) -> List[float]:
    """
    Fallback embedding using simple hash-based approach
    This creates a 384-dimensional vector (same as MiniLM)
    """
    import hashlib
    
    # Create a deterministic hash-based embedding
    hash_obj = hashlib.sha256(text.encode('utf-8'))
    hash_hex = hash_obj.hexdigest()
    
    # Convert hash to 384-dimensional vector
    embedding = []
    for i in range(0, len(hash_hex), 2):
        hex_pair = hash_hex[i:i+2]
        if len(hex_pair) == 2:
            val = int(hex_pair, 16) / 255.0  # Normalize to [0, 1]
            embedding.append(val)
    
    # Pad or truncate to 384 dimensions
    while len(embedding) < 384:
        embedding.append(0.0)
    
    return embedding[:384]

def get_model_info() -> dict:
    """Get information about the loaded model"""
    use_lightweight = os.getenv("USE_LIGHTWEIGHT_EMBEDDINGS", "true").lower() == "true"
    
    return {
        "model_loaded": model is not None,
        "load_time_seconds": model_load_time,
        "model_type": "sentence-transformers" if model else "hash-fallback",
        "use_lightweight": use_lightweight,
        "railway_optimized": use_lightweight
    }
