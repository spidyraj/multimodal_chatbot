"""
YouTube RAG Service - Enhanced YouTube Summarization using RAG Pattern
Following the pattern: Retrieve → Store in Vector DB → LLM → Output
"""

import re
from typing import List, Dict, Optional
from services.youtube_service import get_transcript, extract_video_id
from services.rag_service import process_document_chunks, retrieve_context
from services.llm_service import ask_llm_smart
from core.logger import logger

def chunk_transcript(transcript: str, chunk_size: int = 1000, overlap: int = 100) -> List[str]:
    """
    Split transcript into chunks with overlap for better context
    """
    if not transcript:
        return []
    
    chunks = []
    start = 0
    
    while start < len(transcript):
        end = start + chunk_size
        
        # Don't create tiny chunks at the end
        if end >= len(transcript):
            chunks.append(transcript[start:])
            break
        
        # Try to break at sentence boundaries
        chunk_text = transcript[start:end]
        
        # Look for sentence ending near the chunk boundary
        for i in range(min(200, len(chunk_text))):
            if chunk_text[-i-1] in '.!?':
                # CRITICAL FIX: Handle i=0 case properly
                actual_chunk = chunk_text if i == 0 else chunk_text[:-i]
                chunks.append(actual_chunk)
                start = end - i
                break
        else:
            # No sentence boundary found, just split at chunk_size
            chunks.append(chunk_text)
            start = end - overlap
        
        # Move start with overlap
        start = max(0, start - overlap)
    
    return chunks

def process_youtube_video_rag(url: str, user_id: int) -> Dict[str, str]:
    """
    Enhanced YouTube processing using RAG pattern:
    1. Retrieve transcript from YouTube
    2. Store transcript chunks in vector database
    3. Use RAG for intelligent summarization
    4. Generate enhanced output
    """
    try:
        logger.info(f"Starting YouTube RAG processing for URL: {url}")
        
        # Step 1: Retrieve transcript from YouTube
        video_id = extract_video_id(url)
        if not video_id:
            return {"error": "Invalid YouTube URL"}
        
        transcript = get_transcript(video_id)
        if not transcript:
            return {"error": "No transcript available for this video"}
        
        logger.info(f"Retrieved transcript: {len(transcript)} characters")
        
        # Step 2: Store transcript chunks in vector database
        chunks = chunk_transcript(transcript, chunk_size=800, overlap=100)
        logger.info(f"Created {len(chunks)} transcript chunks")
        
        document_id = f"youtube_{video_id}"
        storage_success = process_document_chunks(chunks, document_id, user_id)
        
        if not storage_success:
            logger.warning("Failed to store transcript chunks, continuing with direct processing")
        
        # Step 3: Use RAG for intelligent summarization
        rag_summary = generate_rag_summary(video_id, transcript, user_id)
        
        # Step 4: Generate enhanced output
        enhanced_summary = generate_enhanced_summary(video_id, rag_summary, user_id)
        
        logger.info(f"YouTube RAG processing completed for video {video_id}")
        
        return {
            "response": enhanced_summary,
            "video_id": video_id,
            "video_title": f"YouTube Video ({video_id})",
            "processing_method": "RAG",
            "chunks_processed": len(chunks),
            "transcript_length": len(transcript)
        }
        
    except Exception as e:
        logger.error(f"YouTube RAG processing error: {str(e)}")
        return {"error": f"Failed to process video using RAG: {str(e)}"}

def generate_rag_summary(video_id: str, transcript: str, user_id: int) -> str:
    """
    Generate summary using improved RAG pattern with map-reduce approach
    """
    try:
        # First, try to use stored chunks with document-specific filtering
        document_id = f"youtube_{video_id}"
        
        # Wait a moment for Pinecone indexing (reduces timing issues)
        import time
        time.sleep(2)
        
        # Try RAG with document-specific filtering
        rag_queries = [
            "What are the main topics and key points discussed?",
            "What are the most important takeaways or conclusions?",
            "What examples or demonstrations are provided?",
            "What background context or explanations are given?"
        ]
        
        rag_responses = []
        
        for query in rag_queries:
            # Retrieve context with document-specific filtering (prevents data leakage)
            context = retrieve_context(query, user_id=user_id, top_k=3, document_id=document_id)
            
            if context:
                prompt = f"""
                Based on the following transcript context from a YouTube video, please answer: {query}
                
                Context:
                {context}
                
                Please provide a concise and informative answer based on the context.
                """
                
                response = ask_llm_smart(prompt)
                rag_responses.append(f"Q: {query}\nA: {response}")
            else:
                logger.info(f"No context found for query: {query}, will use map-reduce approach")
                break
        
        # If we got good RAG results, use them
        if len(rag_responses) == len(rag_queries):
            rag_summary = "\n\n".join(rag_responses)
            logger.info(f"Generated RAG summary for video {video_id}")
            return rag_summary
        
        # FALLBACK: Use map-reduce approach with chunks directly
        logger.info(f"Using map-reduce approach for video {video_id}")
        return generate_map_reduce_summary(transcript, user_id)
        
    except Exception as e:
        logger.error(f"RAG summary generation error: {str(e)}")
        # Final fallback: simple summary
        return generate_simple_summary(transcript, user_id)

def generate_map_reduce_summary(transcript: str, user_id: int) -> str:
    """
    Generate summary using map-reduce approach (summarize chunks, then combine)
    """
    try:
        # Split transcript into manageable chunks
        chunks = chunk_transcript(transcript, chunk_size=1500, overlap=200)
        
        # Step 1: Map - Summarize each chunk
        chunk_summaries = []
        for i, chunk in enumerate(chunks):
            prompt = f"""
            Please provide a concise summary of the following transcript chunk ({i+1}/{len(chunks)}):
            
            Transcript:
            {chunk}
            
            Focus on the main points, key information, and important details in this chunk.
            Keep the summary under 200 words.
            """
            
            chunk_summary = ask_llm_smart(prompt)
            if chunk_summary and len(chunk_summary) > 50:
                chunk_summaries.append(f"Chunk {i+1} Summary:\n{chunk_summary}")
        
        if not chunk_summaries:
            return "Failed to generate chunk summaries"
        
        # Step 2: Reduce - Combine all chunk summaries
        combined_summaries = "\n\n".join(chunk_summaries)
        
        final_prompt = f"""
        Please create a comprehensive summary of a YouTube video based on these chunk summaries:
        
        {combined_summaries}
        
        Create a well-structured summary that includes:
        1. Main Overview
        2. Key Points
        3. Important Takeaways
        4. Notable Examples or Demonstrations
        
        Format with clear headings and bullet points.
        """
        
        final_summary = ask_llm_smart(final_prompt)
        
        if final_summary and len(final_summary) > 100:
            logger.info(f"Generated map-reduce summary: {len(final_summary)} characters")
            return final_summary
        else:
            return "Failed to generate comprehensive summary"
            
    except Exception as e:
        logger.error(f"Map-reduce summary error: {str(e)}")
        return generate_simple_summary(transcript, user_id)

def generate_simple_summary(transcript: str, user_id: int) -> str:
    """
    Generate simple summary as final fallback
    """
    try:
        # Use a reasonable portion of the transcript
        max_length = 4000
        transcript_snippet = transcript[:max_length] if len(transcript) > max_length else transcript
        
        prompt = f"""
        Please provide a comprehensive summary of the following YouTube video transcript:
        
        Transcript:
        {transcript_snippet}
        
        Include:
        1. Main topics discussed
        2. Key points and insights
        3. Important conclusions or takeaways
        4. Notable examples or demonstrations
        
        Format with clear headings and bullet points for readability.
        """
        
        summary = ask_llm_smart(prompt)
        
        if summary and len(summary) > 100:
            logger.info(f"Generated simple summary: {len(summary)} characters")
            return summary
        else:
            return "Failed to generate summary"
            
    except Exception as e:
        logger.error(f"Simple summary error: {str(e)}")
        return "Error generating summary"

def generate_enhanced_summary(video_id: str, rag_summary: str, user_id: int) -> str:
    """
    Generate enhanced final summary using RAG insights
    """
    try:
        prompt = f"""
        Please create a comprehensive and well-structured summary of a YouTube video based on the following RAG analysis:
        
        Video ID: {video_id}
        
        RAG Analysis Results:
        {rag_summary}
        
        Please create a summary that includes:
        1. **Main Overview**: A concise summary of the video's main topic and purpose
        2. **Key Points**: The most important points and insights discussed
        3. **Takeaways**: Actionable conclusions or lessons learned
        4. **Notable Content**: Any interesting examples, demonstrations, or explanations
        5. **Target Audience**: Who would benefit most from this content
        
        Format the summary with clear headings and bullet points for easy reading.
        Make it comprehensive yet concise and engaging.
        """
        
        enhanced_summary = ask_llm_smart(prompt)
        
        if not enhanced_summary or len(enhanced_summary) < 100:
            logger.warning(f"Enhanced summary too short for video {video_id}")
            return "Failed to generate comprehensive summary"
        
        logger.info(f"Generated enhanced summary for video {video_id}")
        return enhanced_summary
        
    except Exception as e:
        logger.error(f"Enhanced summary generation error: {str(e)}")
        return "Failed to generate enhanced summary"

def query_youtube_knowledge(query: str, user_id: int, top_k: int = 5) -> Dict[str, str]:
    """
    Query stored YouTube video knowledge using RAG
    """
    try:
        logger.info(f"Querying YouTube knowledge: {query}")
        
        # Retrieve relevant context from stored YouTube videos (no document_id filter for cross-video search)
        context = retrieve_context(query, user_id=user_id, top_k=top_k)
        
        if not context:
            return {"response": "I don't have information from previously processed YouTube videos that matches your query.", "context_found": False}
        
        # Generate response based on retrieved context
        prompt = f"""
        Based on the following information from previously processed YouTube videos, please answer the user's question:
        
        User Question: {query}
        
        Context from YouTube videos:
        {context}
        
        Please provide a helpful and informative answer based on the video content. If multiple videos are referenced, indicate which video(s) contain the relevant information.
        """
        
        response = ask_llm_smart(prompt)
        
        return {
            "response": response,
            "context_found": True,
            "context_length": len(context)
        }
        
    except Exception as e:
        logger.error(f"YouTube knowledge query error: {str(e)}")
        return {"error": f"Failed to query YouTube knowledge: {str(e)}"}
