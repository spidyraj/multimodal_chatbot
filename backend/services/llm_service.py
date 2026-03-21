import requests
from typing import Optional
from core.config import settings
from core.logger import logger

# Model configurations for different use cases
MODELS = {
    "fast": "llama3-8b-8192",      # Fast, good for simple queries
    "balanced": "llama3-70b-8192",  # Balanced performance
    "smart": "mixtral-8x7b-32768",  # Most capable for complex tasks
}

def ask_llm(prompt: str, max_tokens: int = 1000, model_type: str = "balanced") -> str:
    """
    Send a prompt to Groq API and get response
    """
    try:
        model = MODELS.get(model_type, MODELS["balanced"])
        
        url = "https://api.groq.com/openai/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {settings.GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": 0.7
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        if response.status_code != 200:
            logger.error(f"Groq API error: {response.status_code} - {response.text}")
            return "I apologize, but I'm having trouble connecting to my brain right now. Please try again."
        
        result = response.json()
        return result["choices"][0]["message"]["content"]
        
    except requests.exceptions.Timeout:
        logger.error("Groq API timeout")
        return "The request took too long. Please try again."
    except requests.exceptions.RequestException as e:
        logger.error(f"Groq API request error: {str(e)}")
        return "I'm having connection issues. Please try again later."
    except Exception as e:
        logger.error(f"Unexpected error in LLM service: {str(e)}")
        return "Something went wrong. Please try again."

def ask_llm_fast(prompt: str, max_tokens: int = 500) -> str:
    """Fast model for simple queries"""
    return ask_llm(prompt, max_tokens, "fast")

def ask_llm_smart(prompt: str, max_tokens: int = 2000) -> str:
    """Smart model for complex tasks"""
    return ask_llm(prompt, max_tokens, "smart")
