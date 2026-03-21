from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np
from core.logger import logger

# Initialize model (lightweight for Railway compatibility)
model = None

def get_embedding_model():
    global model
    if model is None:
        try:
            model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")
            logger.info("Embedding model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load embedding model: {str(e)}")
            raise
    return model

def embed_texts(texts: List[str]) -> List[List[float]]:
    """
    Convert texts to embeddings
    """
    try:
        model = get_embedding_model()
        embeddings = model.encode(texts, convert_to_tensor=False)
        return embeddings.tolist()
    except Exception as e:
        logger.error(f"Embedding error: {str(e)}")
        raise

def embed_single_text(text: str) -> List[float]:
    """
    Convert single text to embedding
    """
    try:
        embeddings = embed_texts([text])
        return embeddings[0] if embeddings else []
    except Exception as e:
        logger.error(f"Single text embedding error: {str(e)}")
        return []
