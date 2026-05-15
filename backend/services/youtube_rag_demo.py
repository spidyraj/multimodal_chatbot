"""
YouTube RAG Demo - Mock transcript to demonstrate RAG architecture
"""

from typing import Dict
from services.youtube_rag_service import process_document_chunks, retrieve_context, generate_enhanced_summary
from services.llm_service import ask_llm_smart
from core.logger import logger

def create_mock_transcript(video_id: str) -> str:
    """
    Create a mock transcript for demonstration
    """
    mock_transcripts = {
        "demo_ml": """
        Welcome to this comprehensive introduction to Machine Learning. 
        
        In this video, we'll explore the fundamental concepts of machine learning and how it's transforming our world. 
        Machine learning is a subset of artificial intelligence that enables computers to learn and improve from experience without being explicitly programmed.
        
        The three main types of machine learning are:
        1. Supervised learning - where we train models on labeled data
        2. Unsupervised learning - where we find patterns in unlabeled data  
        3. Reinforcement learning - where agents learn through trial and error
        
        Let's dive deeper into supervised learning first. In supervised learning, we have input features and output labels, and the goal is to learn a mapping function that can predict outputs for new inputs.
        
        Common supervised learning algorithms include linear regression, decision trees, random forests, and neural networks. Each has its strengths and weaknesses depending on the problem.
        
        For unsupervised learning, we work with clustering algorithms like K-means, hierarchical clustering, and dimensionality reduction techniques like PCA.
        
        Reinforcement learning has gained popularity through applications like game playing (AlphaGo), robotics, and recommendation systems.
        
        The machine learning workflow typically involves:
        - Data collection and preprocessing
        - Feature engineering and selection
        - Model training and validation
        - Model deployment and monitoring
        
        Key challenges in machine learning include overfitting, underfitting, data quality issues, and computational resource requirements.
        
        To get started with machine learning, I recommend learning Python, understanding basic statistics, and practicing with datasets from platforms like Kaggle.
        
        Remember that machine learning is not magic - it requires careful thought, experimentation, and domain knowledge to be effective.
        
        Thank you for watching this introduction to machine learning. I hope you found it helpful and are excited to learn more about this fascinating field.
        """,
        "demo_ai": """
        Artificial Intelligence is one of the most transformative technologies of our time. 
        
        AI refers to the simulation of human intelligence in machines that are programmed to think and learn like humans.
        
        The field of AI includes several subfields:
        - Machine Learning
        - Deep Learning
        - Natural Language Processing
        - Computer Vision
        - Robotics
        
        Deep learning, which uses neural networks with multiple layers, has revolutionized AI in recent years. It powers applications like image recognition, language translation, and autonomous driving.
        
        Natural Language Processing enables machines to understand and generate human language. This technology powers chatbots, translation services, and sentiment analysis.
        
        Computer Vision allows machines to interpret and understand visual information from the world. Applications include facial recognition, object detection, and medical image analysis.
        
        The future of AI holds tremendous promise, but also raises important questions about ethics, privacy, and the future of work.
        
        As AI continues to advance, we must ensure it's developed responsibly and benefits all of humanity.
        """
    }
    
    return mock_transcripts.get(video_id, mock_transcripts["demo_ml"])

def demo_youtube_rag(video_id: str, user_id: int) -> Dict[str, str]:
    """
    Demonstrate YouTube RAG system with mock transcript
    """
    try:
        logger.info(f"Starting YouTube RAG demo for video: {video_id}")
        
        # Step 1: Get mock transcript
        transcript = create_mock_transcript(video_id)
        logger.info(f"Mock transcript length: {len(transcript)} characters")
        
        # Step 2: Process transcript chunks and store in vector DB
        from services.youtube_rag_service import chunk_transcript
        
        chunks = chunk_transcript(transcript, chunk_size=800, overlap=100)
        logger.info(f"Created {len(chunks)} transcript chunks")
        
        document_id = f"youtube_demo_{video_id}"
        storage_success = process_document_chunks(chunks, document_id, user_id)
        
        if storage_success:
            logger.info("Transcript chunks stored successfully in vector database")
        else:
            logger.warning("Failed to store chunks, continuing with direct processing")
        
        # Step 3: Generate RAG summary
        rag_summary = generate_demo_rag_summary(video_id, transcript, user_id)
        
        # Step 4: Generate enhanced output
        enhanced_summary = generate_enhanced_summary_demo(video_id, rag_summary, user_id)
        
        logger.info(f"YouTube RAG demo completed for video {video_id}")
        
        return {
            "response": enhanced_summary,
            "video_id": video_id,
            "video_title": f"Demo Video: Machine Learning Introduction",
            "processing_method": "RAG_DEMO",
            "chunks_processed": len(chunks),
            "transcript_length": len(transcript),
            "note": "This is a demonstration using mock transcript data"
        }
        
    except Exception as e:
        logger.error(f"YouTube RAG demo error: {str(e)}")
        return {"error": f"Failed to demo RAG processing: {str(e)}"}

def generate_demo_rag_summary(video_id: str, transcript: str, user_id: int) -> str:
    """
    Generate RAG summary using demo approach
    """
    try:
        # Demo RAG queries
        rag_queries = [
            "What are the main topics and key concepts discussed?",
            "What are the most important takeaways or conclusions?",
            "What examples or applications are mentioned?",
            "What background information is provided?"
        ]
        
        rag_responses = []
        
        for query in rag_queries:
            # Try to get context from vector database
            context = retrieve_context(query, user_id=user_id, top_k=3)
            
            if context:
                prompt = f"""
                Based on the following context from a video transcript, please answer: {query}
                
                Context:
                {context}
                
                Please provide a concise and informative answer.
                """
                
                response = ask_llm_smart(prompt)
                rag_responses.append(f"Q: {query}\nA: {response}")
            else:
                # Use direct transcript processing
                context_snippet = transcript[:2000] if len(transcript) > 2000 else transcript
                prompt = f"""
                From this video transcript excerpt, please answer: {query}
                
                Transcript:
                {context_snippet}
                
                Please provide a concise answer based on the content.
                """
                
                response = ask_llm_smart(prompt)
                rag_responses.append(f"Q: {query}\nA: {response}")
        
        return "\n\n".join(rag_responses)
        
    except Exception as e:
        logger.error(f"Demo RAG summary error: {str(e)}")
        return "Failed to generate demo RAG summary"

def generate_enhanced_summary_demo(video_id: str, rag_summary: str, user_id: int) -> str:
    """
    Generate enhanced summary for demo
    """
    try:
        prompt = f"""
        Please create a comprehensive and well-structured summary of a video based on the following RAG analysis:
        
        Video ID: {video_id}
        Video Topic: Machine Learning / Artificial Intelligence
        
        RAG Analysis Results:
        {rag_summary}
        
        Please create a summary that includes:
        1. **Main Overview**: A concise summary of the video's main topic and purpose
        2. **Key Points**: The most important concepts and information discussed
        3. **Takeaways**: Actionable conclusions or lessons learned
        4. **Applications**: Real-world examples and use cases mentioned
        5. **Next Steps**: Recommendations for further learning
        
        Format the summary with clear headings and bullet points for easy reading.
        Make it comprehensive yet concise and engaging.
        """
        
        enhanced_summary = ask_llm_smart(prompt)
        return enhanced_summary
        
    except Exception as e:
        logger.error(f"Demo enhanced summary error: {str(e)}")
        return "Failed to generate demo enhanced summary"
