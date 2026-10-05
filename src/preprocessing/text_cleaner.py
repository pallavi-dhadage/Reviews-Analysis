import re
import string

def clean_text(text: str) -> str:
    """
    Cleans the input text by performing the following operations:
    - Lowercase
    - Remove HTML tags
    - Remove special characters and punctuation
    - Remove extra whitespace
    """
    if not isinstance(text, str):
        return ""
        
    # Lowercase
    text = text.lower()
    
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', ' ', text)
    
    # Remove URLs
    text = re.sub(r'http\S+|www\.\S+', '', text)
    
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text
