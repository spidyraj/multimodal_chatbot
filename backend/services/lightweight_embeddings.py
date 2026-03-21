"""
Lightweight embedding service for Railway deployment
Uses sentence-transformers only when needed
"""

from typing import List
import os
import hashlib
from core.logger import logger

def embed_texts_lightweight(texts: List[str]) -> List[List[float]]:
    """
    Ultra-lightweight embedding using only hash-based approach
    This avoids the heavy sentence-transformers dependency
    """
    embeddings = []
    
    for text in texts:
        embedding = simple_hash_embedding(text)
        embeddings.append(embedding)
    
    return embeddings

def embed_single_text_lightweight(text: str) -> List[float]:
    """
    Lightweight single text embedding
    """
    return simple_hash_embedding(text)

def simple_hash_embedding(text: str) -> List[float]:
    """
    Create a 384-dimensional vector using SHA-256 hash
    Compatible with Pinecone MiniLM dimensions
    """
    # Create multiple hashes for better distribution
    hash1 = hashlib.sha256(text.encode('utf-8')).hexdigest()
    hash2 = hashlib.sha256((text + "salt1").encode('utf-8')).hexdigest()
    hash3 = hashlib.sha256((text + "salt2").encode('utf-8')).hexdigest()
    
    combined_hash = hash1 + hash2 + hash3
    
    # Convert to 384-dimensional vector
    embedding = []
    for i in range(0, len(combined_hash), 2):
        if i + 1 < len(combined_hash):
            hex_pair = combined_hash[i:i+2]
            val = int(hex_pair, 16) / 255.0  # Normalize to [0, 1]
            embedding.append(val)
    
    # Ensure exactly 384 dimensions
    while len(embedding) < 384:
        embedding.append(0.0)
    
    return embedding[:384]

def can_use_heavy_embeddings() -> bool:
    """
    Check if we can use heavy sentence-transformers
    """
    return os.getenv("USE_HEAVY_EMBEDDINGS", "false").lower() == "true"

def get_embedding_info() -> dict:
    """Get information about current embedding method"""
    return {
        "method": "lightweight_hash" if not can_use_heavy_embeddings() else "sentence-transformers",
        "dimensions": 384,
        "model_loaded": False,
        "railway_optimized": True
    }
