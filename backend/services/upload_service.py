import os
from typing import Optional
from PyPDF2 import PdfReader
from PIL import Image
import pytesseract
from core.logger import logger

def process_uploaded_file(file_path: str, filename: str, user_id: int) -> str:
    """
    Process uploaded file and extract text content
    """
    try:
        file_extension = os.path.splitext(filename)[1].lower()
        
        if file_extension == '.pdf':
            return extract_text_from_pdf(file_path)
        elif file_extension in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
            return extract_text_from_image(file_path)
        elif file_extension in ['.txt', '.md']:
            return extract_text_from_text_file(file_path)
        else:
            logger.warning(f"Unsupported file type: {file_extension}")
            return ""
            
    except Exception as e:
        logger.error(f"File processing error: {str(e)}")
        return ""

def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text from PDF file
    """
    try:
        with open(file_path, 'rb') as file:
            reader = PdfReader(file)
            text = ""
            
            for page in reader.pages:
                text += page.extract_text() + "\n"
            
            return text.strip()
            
    except Exception as e:
        logger.error(f"PDF text extraction error: {str(e)}")
        return ""

def extract_text_from_image(file_path: str) -> str:
    """
    Extract text from image file using OCR
    """
    try:
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image)
        return text.strip()
        
    except Exception as e:
        logger.error(f"Image OCR error: {str(e)}")
        return ""

def extract_text_from_text_file(file_path: str) -> str:
    """
    Extract text from plain text file
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read().strip()
            
    except Exception as e:
        logger.error(f"Text file extraction error: {str(e)}")
        return ""
