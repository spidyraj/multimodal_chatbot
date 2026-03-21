from pinecone import Pinecone, PodSpec
from typing import List, Dict, Any, Optional
from core.config import settings
from core.logger import logger

# Initialize Pinecone
pc = None
index = None

def get_pinecone_index():
    global pc, index
    if pc is None:
        try:
            pc = Pinecone(api_key=settings.PINECONE_API_KEY)
            
            # Check if index exists, create if not
            if settings.PINECONE_INDEX_NAME not in pc.list_indexes().names():
                pc.create_index(
                    name=settings.PINECONE_INDEX_NAME,
                    dimension=384,  # MiniLM dimension
                    metric="cosine",
                    spec=PodSpec(
                        environment=settings.PINECONE_ENVIRONMENT,
                        pod_type="p1.x1"
                    )
                )
                logger.info(f"Created new Pinecone index: {settings.PINECONE_INDEX_NAME}")
            
            index = pc.Index(settings.PINECONE_INDEX_NAME)
            logger.info("Pinecone connection established")
            
        except Exception as e:
            logger.error(f"Pinecone connection error: {str(e)}")
            raise
    
    return index

def store_embeddings(vectors: List[Dict[str, Any]]):
    """
    Store embeddings in Pinecone
    vectors: [{"id": str, "values": List[float], "metadata": dict}]
    """
    try:
        index = get_pinecone_index()
        index.upsert(vectors)
        logger.info(f"Stored {len(vectors)} embeddings in Pinecone")
        return True
    except Exception as e:
        logger.error(f"Pinecone store error: {str(e)}")
        return False

def query_embeddings(query_vector: List[float], top_k: int = 3, filter_dict: Optional[Dict] = None):
    """
    Query embeddings from Pinecone
    """
    try:
        index = get_pinecone_index()
        
        query_params = {
            "vector": query_vector,
            "top_k": top_k,
            "include_metadata": True
        }
        
        if filter_dict:
            query_params["filter"] = filter_dict
        
        result = index.query(**query_params)
        return result
    except Exception as e:
        logger.error(f"Pinecone query error: {str(e)}")
        return {"matches": []}

def delete_embeddings(ids: List[str]):
    """
    Delete embeddings from Pinecone
    """
    try:
        index = get_pinecone_index()
        index.delete(ids=ids)
        logger.info(f"Deleted {len(ids)} embeddings from Pinecone")
        return True
    except Exception as e:
        logger.error(f"Pinecone delete error: {str(e)}")
        return False
