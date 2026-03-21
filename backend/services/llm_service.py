import requests
from typing import Optional
from core.config import settings
from core.logger import logger

def ask_llm(prompt: str, max_tokens: int = 1000) -> str:
    """
    Send a prompt to Groq API and get response
    """
    try:
        url = "https://api.groq.com/openai/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {settings.GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "llama3-8b-8192",
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
